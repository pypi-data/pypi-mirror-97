from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from mayan.apps.rest_api.generics import GenericAPIView

# TODO: Remove after the move to Mayan EDMS 4.0.


class BlankSerializer(serializers.Serializer):
    """Serializer for the object action API view"""


class ObjectActionAPIView(GenericAPIView):
    serializer_class = BlankSerializer

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def object_action(self):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        return self.view_action(request, *args, **kwargs)

    def view_action(self, request, *args, **kwargs):
        self.object = self.get_object()

        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                setattr(self.object, key, value)

        result = self.object_action(request=request)

        if result:
            # If object action returned serializer.data
            headers = self.get_success_headers(data=result)
            return Response(
                data=result, status=status.HTTP_200_OK, headers=headers
            )
        else:
            return Response(status=status.HTTP_200_OK)
