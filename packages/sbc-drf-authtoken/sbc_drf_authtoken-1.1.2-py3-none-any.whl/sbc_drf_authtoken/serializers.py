from rest_framework.authtoken.serializers import AuthTokenSerializer


class ExAuthTokenSerializer(AuthTokenSerializer):
    def validate_username(self, value):
        return value.lower() if value else value
