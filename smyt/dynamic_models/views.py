from cStringIO import StringIO
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.urlresolvers import reverse, clear_url_caches
from django.db.models.loading import get_model, get_models, get_app
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin
from django.db import models

from collections import OrderedDict
from django.utils.crypto import get_random_string
from django.utils.importlib import import_module
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
import xmltodict
import yaml
import glob
import re
import codecs
import json

def format_xml(d):
    result = OrderedDict()
    if 'tables' not in d:
        if 'table' in d:
            d = {'tables': {'table': [d['table']]}}
    for table in d['tables']['table']:
        result[str(table['@title'])] = OrderedDict({'fields': list(OrderedDict((key[1:], value) for key, value in i.iteritems()) for i in table['fields'])})
    return result


def format_yaml(d):
    result = OrderedDict(d)
    return result


class FileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        f = self.cleaned_data['file']
        try:
            data = format_xml(xmltodict.parse(f))
        except Exception as e:
            print e
            f.seek(0)
            try:
                data = format_yaml(yaml.load(f))
            except Exception as e:
                raise ValidationError(e)
        if len(data) == 0:
            raise ValidationError("Can't find any tables in loaded file")
        return data


MODELS_PATH = settings.BASE_DIR + '/dynamic_models/models'
table2model = lambda table_name: table_name.title().replace('_', '').replace(' ', '').replace('-', '')


def index(request):
    stdout = StringIO()
    stderr = StringIO()
    form = FileForm()
    if request.method == 'POST':
        form = FileForm(request.POST.copy(), files=request.FILES.copy())
        if form.is_valid():
            def get_model_content():
                for _table_name, fields in form.cleaned_data['file'].iteritems():
                    table_name = table2model(_table_name)

                    try:
                        if not get_model('dynamic_models', table_name):
                            model = type(table_name, (models.Model,), {'__module__': 'dynamic_models'})
                        else:
                            raise RuntimeError()
                    except LookupError:
                        model = type(table_name, (models.Model,), {'__module__': 'dynamic_models'})
                    except RuntimeError:
                        table_name = "%s_%s" % (table_name, get_random_string(length=4))
                        model = type(str(table_name), (models.Model,), {'__module__': 'dynamic_models'})

                    yield "\nclass %s(models.Model):" % table_name

                    for data_field in fields['fields']:
                        field_title = data_field.get('title', '')
                        field_name = data_field.get('id', '')
                        if data_field['type'] == 'char':
                            field = models.CharField(field_title, max_length=250)
                            field.contribute_to_class(model, field_name)
                            yield "   %s = models.CharField(u'%s', max_length=250)" % (field_name, field_title)
                        elif data_field['type'] == 'int':
                            field = models.IntegerField(field_title)
                            field.contribute_to_class(model, field_name)
                            yield "   %s = models.IntegerField(u'%s')" % (field_name, field_title)
                        elif data_field['type'] == 'date':
                            field = models.DateField(field_title)
                            field.contribute_to_class(model, field_name)
                            yield "   %s = models.DateField(u'%s')" % (field_name, field_title)
                    admin.site.register(model)

            model_content = '\n'.join(get_model_content())

            if model_content:
                current_file_number = max(map(lambda file_path: int(re.search('(?P<number>[0-9]{4}).*\.py$', file_path).groupdict().get('number', 0)),
                                          glob.glob(MODELS_PATH+'/[0-9]*_*.py')) or [-1])
                next_file_number = int(current_file_number) + 1
                next_file_name = "%04d_auto.py" % next_file_number
                next_file_path = MODELS_PATH+'/'+next_file_name

                with codecs.open(next_file_path, 'w', "utf-8") as f:
                    f.write("# -*- coding: utf-8 -*-\n")
                    f.write("from django.db import models\n\n")
                    f.write(model_content)

                call_command('makemigrations', stdout=stdout, stderr=stderr)
                stdout.seek(0)
                stderr.seek(0)
                if not stderr.read():
                    stdout.seek(0)
                    stderr.seek(0)
                    call_command('migrate', stdout=stdout, stderr=stderr)
                    if not stderr.read():
                        reload(import_module(settings.ROOT_URLCONF))
                        clear_url_caches()
                        return HttpResponseRedirect(reverse('index'))

    stderr.seek(0)
    app = get_app('dynamic_models')

    tables = list({'name': model.__name__, 'title': model._meta.verbose_name} for model in get_models(app))

    return render(request, 'index.html', {
        'form': form,
        'error': stderr.read(),
        'tables_json': json.dumps(tables)
    })


@api_view(['POST'])
def table_headers(request):
    name = request.DATA['name']
    model = get_model('dynamic_models', name)
    fields = []
    for field in model._meta.fields:
        fields.append({'name': field.name, 'title': field.verbose_name})
    return Response(fields)


class DynamicModelSet(ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        self.model = get_model('dynamic_models', kwargs['name'])
        return super(DynamicModelSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        class DynamicModelSerializer(ModelSerializer):
            class Meta:
                model = self.model
        return DynamicModelSerializer

