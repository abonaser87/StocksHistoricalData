# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Company, Statement, StatementRow, StatementFact
# Register your models here.
admin.site.register(Company)
admin.site.register(Statement)
admin.site.register(StatementRow)
admin.site.register(StatementFact)
