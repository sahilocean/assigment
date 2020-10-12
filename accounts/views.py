from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ContactForm
from .serializers import UserSerializer

User = get_user_model()


class SignupViews(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password=make_password(request.data.get("password")))
            return Response({"message": "Succesfully creaing a user"}, status=status.HTTP_201_CREATED)
        else:
            for key, value in serializer.errors.items():
                return Response({key: value}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user = authenticate(**request.data)
        if not user:
            return Response({"error": "Invalid Login creadentials"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        login(request, user)
        serializer = UserSerializer(user).data
        serializer.update({"token": token.key})
        return Response({"data": serializer}, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({"message": "User Sucessfully logout"}, status=status.HTTP_200_OK)


class LoginTemplateView(View):
    permissions_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return render(request, 'registrations/login.html')

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get("password"))
        if not user:
            messages.info(request, "Invalid login credential.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        login(request, user)
        return HttpResponseRedirect('/accounts/contact/')


class SignupTemplateView(View):
    permissions_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return render(request, 'registrations/signup.html')

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(password=make_password(request.data.get("password")))
            messages.info(request, "Successfully created a user.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        return HttpResponseRedirect('/login/')


class ContactView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseRedirect('/login/')
        return render(request, 'contact.html', {"form": ContactForm()})

    def post(self, request, *args, **kwargs):
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Sucessfully submitted a from.")
            return HttpResponseRedirect('/accounts/contact/')
        else:
            messages.info(request, "Invalid form data.")
            return render(request, 'contact.html', {"form": ContactForm()})


class LogOutTemplateView(APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/login/')
