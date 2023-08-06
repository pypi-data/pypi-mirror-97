from django.db import models
from django.core.mail import send_mail
from djangoldp.models import Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from djangoldp_conversation.models import Conversation, Message
from djangoldp_like.models import Like
from django.utils import timezone
from django.template import loader
from djangoldp_i18n.views import I18nLDPViewSet
from django.utils.translation import ugettext_lazy as _

class LearningOutcome (Model) :
    name = models.CharField(max_length=256, verbose_name="Learning outcome", null=True, blank=True)
    
    class Meta:
        rdf_type = 'coopstarter:skills'
        view_set = I18nLDPViewSet
        depth = 1

    def __str__(self):
        return str(self.name)

class InterfaceLanguage (Model):
    code = models.CharField(max_length=2, verbose_name="ISO Code", null=True, blank=True)
    name = models.CharField(max_length=64, verbose_name="Language name", null=True, blank=True)
    
    class Meta:
        rdf_type = 'coopstarter:interfacelanguage'

    def __str__(self):
        return str(self.name) + '(' + str(self.code) + ')'

class Country (Model):
    code = models.CharField(max_length=2, verbose_name="ISO Code", null=True, blank=True)
    name = models.CharField(max_length=64, verbose_name="Country name", null=True, blank=True)
    
    class Meta:
        rdf_type = 'coopstarter:country'

    def __str__(self):
        return str(self.name) + '(' + str(self.code) + ')'

class Language (Model):
    code = models.CharField(max_length=2, verbose_name="ISO Code", null=True, blank=True)
    name = models.CharField(max_length=64, verbose_name="Language name", null=True, blank=True)

    class Meta:
        rdf_type = 'coopstarter:language'

    def __str__(self):
        return str(self.name) + '(' + str(self.code) + ')'

class Organisation (Model):
    name = models.CharField(max_length=128, verbose_name="Name", null=True, blank=True)
    website = models.CharField(max_length=4096, verbose_name="Website", null=True, blank=True)

    class Meta:
        rdf_type = 'coopstarter:organisation'

    def __str__(self):
        if self.name is None or self.name == '':
            return str(self.website)
        return str(self.name)

class Step (Model):
    name = models.CharField(max_length=128, verbose_name="Name", null=True, blank=True)
    order = models.IntegerField(verbose_name="Order", blank=True, null=True, default=0)
    
    class Meta:
        anonymous_perms = ['view']
        serializer_fields=["@id", "resources", "name", "order"]
        nested_fields=["resources"]
        container_path = 'steps/'
        rdf_type = 'coopstarter:step'
        view_set = I18nLDPViewSet
        depth = 1
    
    def __str__(self):
        return str(self.name) + '(' + str(self.order) + ')'

class Format (Model):
    name = models.CharField(max_length=128, verbose_name="Title", blank=True, null=True)

    class Meta:
        rdf_type = 'coopstarter:format'
        view_set = I18nLDPViewSet
        depth = 1

    def __str__(self):
        return str(self.name)

class Field (Model):
    name = models.CharField(max_length=128, verbose_name="Title", null=True, blank=True)

    class Meta:
        rdf_type = 'coopstarter:field'
        view_set = I18nLDPViewSet
        depth = 1

    def __str__(self):
        return str(self.name)

class Type (Model):
    name = models.CharField(max_length=128, verbose_name="Title", null=True, blank=True)

    class Meta:
        rdf_type = 'coopstarter:resourcetype'
        view_set = I18nLDPViewSet
        depth = 1

    def __str__(self):
        return str(self.name)

class Target (Model):
    name = models.CharField(max_length=128, verbose_name="name", blank=True, null=True)
    value = models.CharField(max_length=128, verbose_name="value", blank=True, null=True)

    class Meta:
        rdf_type = 'coopstarter:target'
        view_set = I18nLDPViewSet
        depth = 1

    def __str__(self):
        return str(self.name)

class SharingCriteria (Model):
    name = models.CharField(max_length=128, verbose_name="name", blank=True, null=True)
    value = models.CharField(max_length=128, verbose_name="value", blank=True, null=True)

    class Meta:
        rdf_type = 'coopstarter:sharingcriteria'
        view_set = I18nLDPViewSet
        depth = 1

    def __str__(self):
        return str(self.name)


class Searcher(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="searcher_profile", on_delete=models.CASCADE,
                                null=True)
    organisation = models.ForeignKey(Organisation, null=True, on_delete=models.CASCADE, related_name="searchers")
    
    class Meta:
        auto_author = 'user'
        owner_field = 'user'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        serializer_fields=["@id", "user", "organisation"]
        nested_fields=["user", "organisation"]
        container_path = 'searchers/'
        rdf_type = 'coopstarter:searcher'
        depth = 1
    
    def __str__(self):
        if self.user is not None:
            return self.user.get_full_name()
        if self.organisation is not None:
            return str(self.organisation)
        return str(None)

class Contributor(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="contributor_profile", on_delete=models.CASCADE,
                                null=True)
    phone = models.CharField(max_length=25, null=True, blank=True, verbose_name='Phone number')
    organisation = models.ForeignKey(Organisation, null=True, on_delete=models.SET_NULL, related_name="contributors")
    country = models.ForeignKey(Country, null=True, related_name="contributors", on_delete=models.SET_NULL)
    languages = models.ManyToManyField(Language, blank=True)

    headline = models.CharField(max_length=256, blank=True, null=True, verbose_name='Headline or current position')
    city = models.CharField(max_length=256, blank=True, null=True, verbose_name='City')

    biography = models.TextField(blank=True, null=True, verbose_name="Tell us more about your activities")
    skills = models.TextField(blank=True, null=True, verbose_name="What skills can you share with our searchers ?")

    fields = models.ManyToManyField(Field, blank=True)
    organisationName = models.CharField(max_length=256, blank=True, null=True, verbose_name='Organisation name, to get info on unexisting ones')
    organisationContact = models.CharField(max_length=256, blank=True, null=True, verbose_name='Organisation contact, to get info on unexisting ones')
    headline = models.CharField(max_length=256, blank=True, null=True, verbose_name='Headline or current position')

    linkedin = models.CharField(max_length=256, null=True, blank=True, verbose_name='Linkedin account')
    twitter = models.CharField(max_length=256, null=True, blank=True, verbose_name='Twitter account')
    registered_on = models.DateTimeField(default=timezone.now)

    class Meta:
        auto_author = 'user'
        serializer_fields=["@id", "phone", "headline", "biography", "city", "skills", "linkedin",\
                           "twitter", "organisation", "fields", "languages", "country", "organisationContact", "organisationName"]
        nested_fields=["user", "organisation", "fields", "languages", "country"]
        container_path = 'contributors/'
        rdf_type = 'coopstarter:contributor'
        owner_field = 'user'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        depth = 1

    def __str__(self):
        if self.user is not None:
            return self.user.get_full_name()
        return str(self.urlid)

class Review (Model):
    comment =  models.TextField(verbose_name="Comment", blank=True, null=True)
    status = models.CharField(max_length=32, choices=(('pending', 'Pending'), ('inappropriate', 'Inappropriate'), ('validated', 'Validated'), ('to_improve', 'Improvement required')), verbose_name="Resource status", blank=True, null=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='reviews')

    class Meta:
        owner_field = 'reviewer'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change']
        serializer_fields=["@id", "reviewer", "comment", "status"]
        nested_fields=["reviewer"]
        owner_perms = ['inherit', 'change', 'control', 'delete']
        container_path = 'reviews/'
        rdf_type = 'coopstarter:review'
        depth = 1

    def __str__(self):
        return '(' + str(self.status) + ')' + str(self.comment)

class Resource (Model):
    # Mandatory Fields
    name = models.CharField(max_length=256, verbose_name="Title", blank=True, null=True)

    format = models.ForeignKey(Format, null=True, related_name='resources', on_delete=models.SET_NULL)
    publication_year = models.IntegerField(verbose_name="Publication Year", null=True, blank=True)
    languages = models.ManyToManyField(Language, blank=True, verbose_name="Languages", related_name='resources')
    fields = models.ManyToManyField(Field, blank=True, verbose_name="Fields", related_name='resources')
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    uri = models.CharField(max_length=4086, verbose_name="Location/weblink", blank=True, null=True)
    resource_author = models.CharField(max_length=256, verbose_name="Author", blank=True, null=True)
    skills = models.ManyToManyField(LearningOutcome, blank=True, verbose_name="Learning outcomes/skills", related_name='resources')

    # Complementary fields
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    iframe_link = models.TextField(verbose_name="Iframe link", blank=True, null=True)
    preview_image = models.URLField(blank=True, null=True)

    # Classification Fields
    target = models.ForeignKey(Target, verbose_name="Target audience", blank=True, null=True, on_delete=models.SET_NULL)
    type = models.ManyToManyField(Type, blank=True, verbose_name="Type of content", related_name='resources')
    sharing = models.ForeignKey(SharingCriteria, blank=True, null=True, verbose_name="Sharing profile", related_name='resources', on_delete=models.SET_NULL)
    steps = models.ManyToManyField(Step, blank=True, related_name="resources")

    # Relations to other models
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='resources')
    related = models.ManyToManyField("self", blank=True)
    conversations = models.ManyToManyField(Conversation, blank=True, related_name='resources')
    likes = models.ManyToManyField(Like, blank=True, related_name='resources')
    review = models.OneToOneField(Review, blank=True, null=True, verbose_name="Associated review", related_name='resource', on_delete=models.SET_NULL)
 
    class Meta:
        auto_author='submitter'
        owner_field = 'submitter'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        nested_fields=["submitter",\
                       "format", "conversations", "steps", "languages", "fields",\
                       "type", "related", "likes", "review", "country", "skills", "brokenlinks"]
        serializer_fields=["@id", "name", "description", "resource_author", "uri", "publication_year", "submitter",\
                           "format", "target", "skills",\
                           "conversations", "steps", "languages", "fields", "country",\
                           "type", "submitter", "related", "likes", "review", "sharing",\
                           "preview_image", "iframe_link", "brokenlinks"]
        container_path = 'resources/'
        rdf_type = 'coopstarter:resource'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        view_set = I18nLDPViewSet
        depth = 1

    def __str__(self):
        return str(self.name)

class Request (Model):
    # Mandatory Fields
    name = models.CharField(max_length=128, verbose_name="Title", null=True, blank=True)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    status = models.CharField(max_length=32, verbose_name="Status", choices=(('pending', 'Pending'), ('validated', 'Validated')), default="pending")
    
    language = models.ForeignKey(Language, blank=True, verbose_name="Language", on_delete=models.SET_NULL, null=True)
    fields = models.ManyToManyField(Field, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, related_name="requests", null=True)
    skills = models.TextField(verbose_name="Learning outcomes/skills", null=True, blank=True)
    
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='requests')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='reviewed_requests')

    created_on = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        ordering = ['-created_on']
        auto_author='submitter'
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add', 'change']
        owner_field = 'submitter'
        serializer_fields=["@id", "name", "description", "skills", "fields", "language",\
                           "organisation", "submitter", "reviewer", "created_on", "country", "status"]
        owner_perms = ['inherit', 'change', 'control', 'delete']
        nested_fields=["language", "fields", "organisation", "submitter", "country"]
        container_path = 'requests/'
        rdf_type = 'coopstarter:request'
        depth = 1
        
    def __str__(self):
        return str(self.name)

class BrokenLink(Model):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="brokenlinks",
                                  null=True, blank=True)
    resource = models.ForeignKey(Resource, null=True, on_delete=models.SET_NULL, related_name="brokenlinks")
    
    class Meta:
        auto_author = 'submitter'
        owner_field = 'submitter'
        owner_perms = ['inherit', 'change', 'control', 'delete']
        anonymous_perms = ['view']
        authenticated_perms = ['inherit', 'add']
        serializer_fields=["@id", "submitter", "resource"]
        nested_fields=["submitter", "resource"]
        container_path = 'brokenlinks/'
        rdf_type = 'coopstarter:brokenlinks'
        depth = 1
    

@receiver(post_save, sender=Resource)
def create_review(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if created:
        if not instance.review:
            reviewInstance = Review.objects.create(resource=instance, status="pending")
            instance.review = reviewInstance
            instance.save()
    if not created:
        if instance.review:
            if instance.review.status == 'to_improve':
                review = instance.review
                review.status='pending'
                review.save()
                message_text = loader.render_to_string(
                    'emails/txt/reviewer_modification_notification.txt', 
                    {
                        'review': review,
                        'resource': instance
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/reviewer_modification_notification.html', 
                    {
                        'review': review,
                        'resource': instance
                    }
                )

                send_mail(
                    _('The resource you reviewed has been modified'),
                    message_text,
                    '"Knowledge Base" <kb@starter.coop>',
                    [review.reviewer.email],
                    html_message=message_html
                )

@receiver(post_save, sender=Review)
def update_review(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if not created:
        if getattr(settings, 'UPDATE_REVIEW', True) and instance.resource is not None:
            resource = instance.resource
            if instance.status == 'validated':
                subject = _('The resource you submitted has been validated !')
                message = loader.render_to_string(
                    'emails/txt/resource_validation_notification.txt', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/resource_validation_notification.html', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
            elif instance.status == 'to_improve':
                subject = _('The resource you submitted requires some improvements')
                message = loader.render_to_string(
                    'emails/txt/resource_improvement_notification.txt', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/resource_improvement_notification.html', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
            elif instance.status == 'inappropriate':
                subject = _('The resource you submitted is considered inappropriate')
                message = loader.render_to_string(
                    'emails/txt/resource_refusal_notification.txt', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )
                message_html = loader.render_to_string(
                    'emails/html/resource_refusal_notification.html', 
                    {
                        'review': instance,
                        'resource': resource
                    }
                )

            if instance.status != 'pending':
                send_mail(
                    subject,
                    message,
                    '"Knowledge Base" <kb@starter.coop>',
                    [resource.submitter.email],
                    html_message=message_html
                )


@receiver(post_save, sender=BrokenLink)
def send_mail_to_resource_submitter(sender, instance, created, **kwargs):
    if created:
        message_text = loader.render_to_string(
            'emails/txt/report_broken_link.txt',
            {
                'brokenlink': instance,
            }
        )

        message_html = loader.render_to_string(
            'emails/html/report_broken_link.html',
            {
                'brokenlink': instance,
            }
        )

        send_mail(
            _('The resource you submitted has a brokenlink'),
            message_text,
            '"Knowledge Base" <kb@starter.coop>',
            [instance.resource.submitter.email],
            html_message=message_html
        )

@receiver(post_save, sender=Request)
def send_mail_to_request_submitter(sender, instance, created, **kwargs):
    if not created and instance.status == 'validated':
        message_text = loader.render_to_string(
            'emails/txt/request_managed.txt',
            {
                'request': instance,
            }
        )

        message_html = loader.render_to_string(
            'emails/html/request_managed.html',
            {
                'request': instance,
            }
        )

        send_mail(
            _('The request for a resource you submitted has been managed'),
            message_text,
            '"Knowledge Base" <kb@starter.coop>',
            [instance.submitter.email],
            html_message=message_html
        )

@receiver(post_save, sender=Contributor)
def create_contributor_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if created:
        staff = get_user_model().objects.filter(is_staff=True)
        for user in staff :
            message_text = loader.render_to_string(
                'emails/txt/new_contributor_subscription.txt',
                {
                    'user': user,
                    'contributor': instance,
                }
            )

            message_html = loader.render_to_string(
                'emails/html/new_contributor_subscription.html',
                {
                    'user': user,
                    'contributor': instance,
                }
            )
            send_mail(
                _('New contributor profile completed'),
                message_text,
                '"Knowledge Base" <kb@starter.coop>',
                [user.email],
                html_message=message_html
            )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user(sender, instance, created, **kwargs):
    if kwargs.get('raw', False):
        return False

    if created:
        staff = get_user_model().objects.filter(is_staff=True)
        for user in staff :
            message_text = loader.render_to_string(
                'emails/txt/new_user_subscription.txt',
                {
                    'user': user,
                    'new_user': instance,
                }
            )

            message_html = loader.render_to_string(
                'emails/html/new_user_subscription.html',
                {
                    'user': user,
                    'new_user': instance,
                }
            )
            send_mail(
                _('New user account registration'),
                message_text,
                '"Knowledge Base" <kb@starter.coop>',
                [user.email],
                html_message=message_html
            )