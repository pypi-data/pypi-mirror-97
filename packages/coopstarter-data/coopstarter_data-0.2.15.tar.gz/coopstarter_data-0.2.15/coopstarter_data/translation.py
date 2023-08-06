from modeltranslation.translator import register, translator, TranslationOptions
from .models import Resource, Type, Format, LearningOutcome, Step, Field, SharingCriteria, Target

# A translation option is a class that declares which fields of a model to translate
# registering it with the translator creates duplicate columns for each language, in the database
# (https://django-modeltranslation.readthedocs.io/en/latest/registration.html#changes-automatically-applied-to-the-model-class)
@register(Resource)
class ResourceTranslationOptions(TranslationOptions):
    fields = ('description', 'name')

@register(Type)
class TypeTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Field)
class FieldTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(SharingCriteria)
class SharingCriteriaTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Format)
class FormatTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Target)
class TargetTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Step)
class StepTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(LearningOutcome)
class LearningOutcomeTranslationOptions(TranslationOptions):
    fields = ('name',)

