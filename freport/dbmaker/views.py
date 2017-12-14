# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader

from models import Company


def index(request):
    template = loader.get_template('dbmaker/home.html')
    context = {
        'companies': Company.objects.all()
    }
    return HttpResponse(template.render(context, request))
