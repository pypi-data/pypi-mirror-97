from django.apps import AppConfig
from django.contrib import admin
from .admin import KnowledgebaseAdmin
from .models import Resource, LearningOutcome, Type, Format, Field, Step, Target

admin.site.register(Resource, KnowledgebaseAdmin)
admin.site.register(LearningOutcome, KnowledgebaseAdmin)
admin.site.register(Type, KnowledgebaseAdmin)
admin.site.register(Format, KnowledgebaseAdmin)
admin.site.register(Field, KnowledgebaseAdmin)
admin.site.register(Step, KnowledgebaseAdmin)
admin.site.register(Target, KnowledgebaseAdmin)

class CoopstarterConfig(AppConfig):
    name = 'coopstarter'
