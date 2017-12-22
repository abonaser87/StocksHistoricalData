# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader

from models import Company, StatementRow, StatementFact


def index(request):
    template = loader.get_template('dbmaker/home.html')
    context = {
        'companies': Company.objects.all()
    }
    return HttpResponse(template.render(context, request))


def report(request,statement_id,company_id):
    template = loader.get_template('dbmaker/statement.html')
    dict = {}
    rows = StatementRow.objects.filter(statementId=statement_id)
    dates = StatementFact.objects.filter(companyId=company_id,statementRowId__in=StatementRow.objects.filter(statementId=statement_id))
    temp=[]
    facts=[]
    for date in dates:
        if str(date.entrydate) in temp:
           break
        else:
            temp.append(str(date.entrydate))
    for date in dates:
            facts.append(str(date.amount))
    i=0
    j=0
    for row in rows:
        dict[row] = []
        while i < len(temp):
            dict[row].append(facts[j])
            i = i + 1
            j = j + 1
        i = 0
    context = {
        'rows': rows,
        'facts': dict,
        'dates': temp
    }
    return HttpResponse(template.render(context, request))
