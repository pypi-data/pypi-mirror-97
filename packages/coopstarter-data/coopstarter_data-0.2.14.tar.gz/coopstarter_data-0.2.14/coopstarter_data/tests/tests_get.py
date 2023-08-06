import uuid
import json
from datetime import datetime, timedelta

from djangoldp.permissions import LDPPermissions

from djangoldp.serializers import LDListMixin, LDPSerializer
from rest_framework.test import APITestCase, APIClient

from coopstarter_data.models import Resource, Review, Step
from coopstarter_data.tests.models import User


class GETTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        LDListMixin.to_representation_cache.reset()
        LDPSerializer.to_representation_cache.reset()
        LDPPermissions.invalidate_cache()

    def setUpLoggedInUser(self):
        self.user = User(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                         password='glass onion')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def setUpResource(self):
        self.resource = self._get_resource(name='Test')

    def _get_attached_review(self, resource=None, **extra):
        if resource is None:
            resource = self.resource

        review = Review.objects.create(**extra)
        resource.review = review
        resource.save()
        return review

    def _get_resource(self, **extra):
        return Resource.objects.create(**extra)

    def _get_step(self):
        return Step.objects.create(name='Test')

    def test_list_resources_nested_serializer(self):
        self.setUpLoggedInUser()
        self.resource = self._get_resource(name='Test', submitter=self.user)

        response = self.client.get('/users/1/')
        self.assertIn('resources', response.data)
        self.assertEqual(len(response.data['resources']['ldp:contains']), 1)
        self.assertEqual(response.data['resources']['ldp:contains'][0]['@id'], self.resource.urlid)

    def test_list_resources_nested_viewset(self):
        self.setUpLoggedInUser()
        self.resource = self._get_resource(name='Test', submitter=self.user)

        response = self.client.get('/users/1/resources/')
        self.assertIn('ldp:contains', response.data)
        self.assertEqual(len(response.data['ldp:contains']), 1)
        self.assertEqual(response.data['ldp:contains'][0]['@id'], self.resource.urlid)

    def test_list_pending_resources(self):
        self.setUpLoggedInUser()
        # one local resource which nobody submitted
        self.setUpResource()
        self._get_attached_review(resource=self.resource, status='pending')

        # two external resources (should not be returned)
        external_resource_backlink = self._get_resource(name='Test2', is_backlink=True, urlid='https://external.com/resource/1/')
        self._get_attached_review(resource=external_resource_backlink, status='pending')
        external_resource_non_backlink = self._get_resource(name='Test3', is_backlink=False, urlid='https://external.com/resource/2/')
        self._get_attached_review(resource=external_resource_non_backlink, status='pending')

        # one local resource which I did submit (should not be returned)
        resource = self._get_resource(name='Test4', submitter=self.user)
        self._get_attached_review(resource=resource, status='pending')

        response = self.client.get('/resources/pending/')
        self.assertIn('ldp:contains', response.data)
        self.assertEqual(len(response.data['ldp:contains']), 1)
        self.assertEqual(response.data['ldp:contains'][0]['name'], 'Test')

    def test_list_pending_resources_anonymous(self):
        self.setUpResource()
        self._get_attached_review(resource=self.resource, status='pending')

        response = self.client.get('/resources/pending/')
        self.assertEqual(response.status_code, 403)

    def test_list_pending_resources_options_anonymous(self):
        self.setUpResource()
        self._get_attached_review(resource=self.resource, status='pending')

        response = self.client.options('/resources/pending/')
        self.assertEqual(response.status_code, 200)

    def test_list_validated_resources(self):
        step = self._get_step()
        self.setUpResource()
        self._get_attached_review(resource=self.resource, status='validated')
        self.resource.steps.add(step)

        pending_resource = self._get_resource()
        self._get_attached_review(resource=pending_resource, status='pending')
        pending_resource.steps.add(step)

        external_resource = self._get_resource(urlid='https://external.com/resource/1/')
        self._get_attached_review(resource=external_resource, status='validated')
        external_resource.steps.add(step)

        response = self.client.get('/steps/{}/resources/validated/'.format(step.pk))
        self.assertIn('ldp:contains', response.data)
        self.assertEqual(len(response.data['ldp:contains']), 1)
        self.assertEqual(response.data['ldp:contains'][0]['name'], 'Test')
