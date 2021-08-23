from typing import List
from typing import Union

from django.test import Client, TestCase
from django.urls import reverse
from django_resource_viewset.views import ResourceViewSet


class ResourceRouterTestCase(TestCase):
    def test_model_routes(self):
        self.assertEqual('/testModel/', reverse('testmodel-list'))
        self.assertEqual('/testModel/create/', reverse('testmodel-create'))
        self.assertEqual('/testModel/1/edit/', reverse('testmodel-edit', kwargs={'pk': 1}))
        self.assertEqual('/testModel/1/', reverse('testmodel-detail', kwargs={'pk': 1}))

    def test_basename_routes(self):
        self.assertEqual('/fake/', reverse('fake-list'))
        self.assertEqual('/fake/refresh-list/', reverse('fake-refresh-list'))
        self.assertEqual('/fake/create/', reverse('fake-create'))
        self.assertEqual('/fake/1/refresh-single/', reverse('fake-refresh-single', kwargs={'pk': 1}))
        self.assertEqual('/fake/1/edit/', reverse('fake-edit', kwargs={'pk': 1}))
        self.assertEqual('/fake/1/', reverse('fake-detail', kwargs={'pk': 1}))



class TestModelResourceViewSetTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def assert_template_names(self, expected: Union[str, List[str]], view: ResourceViewSet):
        if isinstance(expected, str):
            expected = [expected]

        self.assertEqual(expected, view.get_template_names())

    def test_model_viewset_template_names(self):
        view = self.client.get(reverse('testmodel-list')).view
        self.assert_template_names('testmodel_index', view)

        view = self.client.post(reverse('testmodel-list')).view
        self.assert_template_names('testmodel_store', view)

        view = self.client.get(reverse('testmodel-create')).view
        self.assert_template_names('testmodel_create', view)

        view = self.client.get(reverse('testmodel-detail', kwargs={'pk': 1})).view
        self.assert_template_names('testmodel_show', view)

        view = self.client.put(reverse('testmodel-detail', kwargs={'pk': 1})).view
        self.assert_template_names('testmodel_update', view)

        view = self.client.patch(reverse('testmodel-detail', kwargs={'pk': 1})).view
        self.assert_template_names('testmodel_partial_update', view)

        view = self.client.delete(reverse('testmodel-detail', kwargs={'pk': 1})).view
        self.assert_template_names('testmodel_destroy', view)

        view = self.client.get(reverse('testmodel-edit', kwargs={'pk': 1})).view
        self.assert_template_names('testmodel_edit', view)

    def test_manual_viewset_template_names(self):
        view = self.client.get(reverse('fake-refresh-single', kwargs={'pk': 1})).view
        self.assert_template_names('fake_refresh_single', view)

        view = self.client.get(reverse('fake-refresh-list')).view
        self.assert_template_names('fake_refresh_list', view)

        view = self.client.get(reverse('fake-list')).view
        self.assert_template_names('fake_index', view)

        view = self.client.post(reverse('fake-list')).view
        self.assert_template_names('fake_store', view)

        view = self.client.get(reverse('fake-refresh-list')).view
        self.assert_template_names('fake_refresh_list', view)

        view = self.client.get(reverse('fake-detail', kwargs={'pk': 1})).view
        self.assert_template_names('fake_show', view)

        view = self.client.put(reverse('fake-detail', kwargs={'pk': 1})).view
        self.assert_template_names('fake_update', view)

        view = self.client.patch(reverse('fake-detail', kwargs={'pk': 1})).view
        self.assert_template_names('fake_partial_update', view)

        view = self.client.get(reverse('fake-edit', kwargs={'pk': 1})).view
        self.assert_template_names('fake_edit', view)

        view = self.client.delete(reverse('fake-detail', kwargs={'pk': 1})).view
        self.assert_template_names('fake_destroy', view)
