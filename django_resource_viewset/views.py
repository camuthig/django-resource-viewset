from typing import Optional

from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from rest_framework.viewsets import ViewSetMixin


class ResourceRouter(SimpleRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'index',
                'post': 'store'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/create{trailing_slash}$',
            mapping={
                'get': 'create',
            },
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'show',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/edit{trailing_slash}$',
            mapping={
                'get': 'edit',
            },
            name='{basename}-edit',
            detail=True,
            initkwargs={'suffix': 'Edit'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


class BaseResourceViewSet(SingleObjectMixin, MultipleObjectMixin, ViewSetMixin, View):
    """A ViewSet that defines the underlying functions but does not define any view handling"""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the request, capturing the action name.

        The DRF `initialize_request` function defines the `action` on the view instance,
        making it important to call it. would usually be called as part of the `as_view` from DRF's `APIView`
        but because this class extends Django's `View`, which uses a `setup` function instead, it is missed.
        """
        method = request.method.lower()

        if method in self.http_method_names:
            self.action = self.action_map.get(method)
            handler = getattr(self, method, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_context_object_name(self, obj):
        """Get the name of the item to be used in the context."""
        if self.context_object_name:
            base_context_name = self.context_object_name
            if not self.detail:
                return f'{base_context_name}_list'

            return self.context_object_name

        if not hasattr(obj, 'model'):
            raise ValueError(
                'Either set the context_object_name or the model or ensure ' +
                'the object defines a model to determine the context_name'
            )

        base_context_name = obj.model._meta.model_name

        if not self.detail:
            return f'{base_context_name}_list'

        return base_context_name


class ResourceViewSet(TemplateResponseMixin, BaseResourceViewSet):
    """A ViewSet that defines basic implementations of all view handling."""
    template_base: Optional[str] = None

    def get_template_names(self):
        return [f'{self.get_template_base()}_{self.action}']

    def get_template_base(self):
        if self.template_name:
            return self.template_name

        if self.context_object_name:
            return self.context_object_name

        if self.queryset:
            return self.queryset.model._meta.object_name.lower()

        if self.basename:
            return self.basename

        raise ValueError(
            'One of template_name, context_object_name, queryset, or basename must be ' +
            'set on the viewset to determine the template base name'
        )
