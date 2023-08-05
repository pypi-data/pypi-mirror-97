import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.module_loading import import_string
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings

from . import signals
from .permissions import IsSuperuser
from .serializers import ExAuthTokenSerializer

L = logging.getLogger(__name__)


class ExObtainAuthToken(ObtainAuthToken):
    """
    To obtain authentication token for users using their ``username`` and ``password``
    Required fields: ``username``, ``password``
    """
    serializer_class = ExAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serializer = get_serializer_class()(user)
        data = serializer.data
        data['token'] = token.key

        signals.post_login.send(None, instance=user, masquerade=False)

        return Response(data)


@api_view(['POST'])
@permission_classes((IsSuperuser,))
def masquerade_login(request, *args, **kwargs):
    user_id = request.data.get('user_id')

    try:
        user = get_user_model().objects.get(id=user_id)
    except (ObjectDoesNotExist, ValueError):
        raise Http404

    token, created = Token.objects.get_or_create(user=user)
    data = get_serializer_class()(user).data
    data['token'] = token.key

    signals.post_login.send(None, instance=user, masquerade=True)

    return Response(data)


def get_serializer_class():
    user_model = get_user_model()

    serializer_str = getattr(settings, 'AUTH_SERIALIZER', None)
    try:
        return import_string(serializer_str)
    except (ImportError, AttributeError):
        class Default(ModelSerializer):
            class Meta:
                model = user_model
                exclude = ('password',)

        return Default


#: To bind CustomObtainAuthToken to system's URL
obtain_auth_token = ExObtainAuthToken.as_view()
