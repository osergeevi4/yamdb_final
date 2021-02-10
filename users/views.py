from api_yamdb import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import EmailSerializer, UserSerializer


@api_view(['POST'])
def get_conf_code(request):
    email = request.data.get('email')
    user = get_object_or_404(User, email=email)
    if User.objects.filter(email=email).exists():
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Код подтверждения '
        message = f'Твой код для регистрации: {confirmation_code}'
        from_email = settings.EMAIL_HOST_USER
        to_email = email
        send_mail(
            mail_subject, message,
            from_email,
            [to_email],
        )
        return Response(f'Вам был выслан код для регистрации на {email}', status=200)


@api_view(['POST'])
def get_token(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, code):
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        return Response({'AccessToken': f'{access}', 'RefreshToken': f'{refresh}'}, status=200)
    return Response(status=400)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin, IsAuthenticated,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, methods=['PATCH', 'GET'],
            permission_classes=(IsAuthenticated,))
    def me(self, request, ):
        serializer = UserSerializer(request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
