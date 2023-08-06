from rest_framework import authentication, permissions, viewsets
from rest_framework.response import Response

try:
    from rest_framework.decorators import action as list_route

    list_route_kwargs = {"detail": False}
except ImportError:
    from rest_framework.decorators import list_route

    list_route_kwargs = {}


from dj_dynamic_settings.models import Setting
from dj_dynamic_settings.registry import registry
from dj_dynamic_settings.serializers import (
    DynamicSettingSerializer,
    RegistryItemSerializer,
)


class DynamicSettingsViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = DynamicSettingSerializer
    permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )

    @list_route(methods=["GET"], url_path="registry", **list_route_kwargs)
    def get_registry(self, *args, **kwargs):
        items = [registry[key] for key in registry.keys()]
        serializer = RegistryItemSerializer(items, many=True)
        return Response(serializer.data)
