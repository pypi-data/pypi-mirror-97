from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

class KnowledgebaseAdmin(TabbedTranslationAdmin):
    group_fieldsets = True
    fieldsets = [
        (u'Type', {'fields': ('name',)}),
        (u'Format', {'fields': ('name',)}),
        (u'Field', {'fields': ('name',)}),
        (u'Step', {'fields': ('name',)}),
        (u'LearningOutcome', {'fields': ('name',)}),
    ]