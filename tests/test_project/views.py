from django.http import HttpResponse
from rest_framework.decorators import action
from tests.test_project.models import TestModel

from django_resource_viewset.views import ResourceViewSet


class ReturningResourceViewSet(ResourceViewSet):
    def _return_self(self):
        r = HttpResponse()
        r.view = self
        return r


class TestModelResourceViewSet(ReturningResourceViewSet):
    queryset = TestModel.objects.all()

    def index(self, request, *args, **kwargs):
        return self._return_self()

    def store(self, request, *args, **kwargs):
        return self._return_self()

    def create(self, request, *args, **kwargs):
        return self._return_self()

    def show(self, request, pk, *args, **kwargs):
        return self._return_self()

    def edit(self, request, pk, *args, **kwargs):
        return self._return_self()

    def update(self, request, pk, *args, **kwargs):
        return self._return_self()

    def partial_update(self, request, pk, *args, **kwargs):
        return self._return_self()

    def destroy(self, request, pk, *args, **kwargs):
        return self._return_self()


class FakeResourceViewSet(ReturningResourceViewSet):
    context_object_name = 'fake'

    def index(self, request, *args, **kwargs):
        return self._return_self()

    def store(self, request, *args, **kwargs):
        return self._return_self()

    def create(self, request, *args, **kwargs):
        return self._return_self()

    def show(self, request, pk, *args, **kwargs):
        return self._return_self()

    def update(self, request, pk, *args, **kwargs):
        return self._return_self()

    def partial_update(self, request, pk, *args, **kwargs):
        return self._return_self()

    def destroy(self, request, pk, *args, **kwargs):
        return self._return_self()

    def edit(self, request, pk, *args, **kwargs):
        return self._return_self()

    @action(detail=False, url_path='refresh-list')
    def refresh_list(self, request, *args, **kwargs):
        return self._return_self()

    @action(detail=True, url_path='refresh-single')
    def refresh_single(self, request, *args, **kwargs):
        return self._return_self()
