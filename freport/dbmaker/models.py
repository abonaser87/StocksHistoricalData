from __future__ import unicode_literals

from django.db import models


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        app_label = 'dbmaker'
        db_table = 'company'


class Statement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        app_label = 'dbmaker'
        db_table = 'statement'


class StatementRow(models.Model):
    id = models.AutoField(primary_key=True)
    rowOrder = models.IntegerField(blank=True, null=True)
    rowTitle = models.CharField(max_length=255, blank=True, null=True)
    rowDescription = models.CharField(max_length=255, blank=True, null=True)
    rowProperties = models.CharField(max_length=255, blank=True, null=True)
    statementId = models.ForeignKey(Statement, db_column='statementId')

    def __str__(self):
        return self.rowTitle
    class Meta:
        app_label = 'dbmaker'
        db_table = 'statementRow'
        managed = False


class StatementFact(models.Model):
    companyId = models.ForeignKey(Company, db_column='companyId')
    statementRowId = models.ForeignKey(StatementRow, db_column='statementRowId')
    entrydate = models.DateField(null=False,db_column='entrydate')
    amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return 'Date = {} , Amount = {}'.format(self.entrydate,str(self.amount))
    class Meta:
        managed = False
        db_table = 'statementFact'
        app_label = 'dbmaker'
