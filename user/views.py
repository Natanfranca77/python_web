from django.shortcuts import render
from django.http import Http404
from rest_framework import generics
from .serializers import UserSerializers,UserListSerializer,UserUpdateSerializer, customTokenSerializer
from .models import UserModel
from rest_framework_simplejwt.views import TokenObtainPairView 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .permissions import ValidToken,validAdmin
from .middlewares import Middlewares
from django.contrib.auth.hashers import make_password
class CreateUserView(generics.CreateAPIView):
    model=UserModel
    serializer_class=UserSerializers
class CustomTokenView(TokenObtainPairView):
    serializer_class=customTokenSerializer

class logoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        refresh=request.data.get('refresh_token')
        if refresh:
            try:
                token= RefreshToken(refresh)
                token.blacklist()
                return Response({'detail':'logout realizado com sucesso'},status=200)

            except Exception as e:
                return Response({'detail':'Erro ao realizar o logout'},status=400)
            
        return Response({'detail':'O token não enviado!'},status=400)
class UserViewPrivate(APIView):
    permission_classes=[ValidToken]
    queryset=UserModel.objects.all()

    def get_queryset(self,pk):
        try:
            return self.queryset.get(pk=pk)
        except UserModel.DoesNotExist:
            raise Http404
        
    def put(self,request):
        user_id=Middlewares
        user_id=Middlewares.decode(request.headers)
        tipo= self .get_queryset(user_id)
        #data=UserSerializers(tipo).data
        user= tipo
        data=request.data

        try:
            if(data['password'] and user.check_password(data['password_back'])):
                user.set_password(make_password(data['password']))
                data['password']= make_password(data['password'])

        except:
            data['password']= user.password
        serializer= UserUpdateSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'detail':'Autualizado com sucesso'
            },status=200)
        return Response(serializer.errors,status=400)
class AdminView(APIView):
    permission_classes=[ValidToken,validAdmin]
    queryset=UserModel.objects.all()

    def get_queryset(self,pk,tipo):
        try:
            return self.queryset.get(pk=pk,tipo=tipo)
        except UserModel.DoesNotExist:
            return Http404
    
    def get(self,request,id=None):
        if id is not None:
            user=self.get_queryset(id,tipo="client")
            serializers=UserListSerializer(user)
        else:
            users=self.queryset.filter(tipo="client")
            serializers=UserListSerializer(users,many=True)
        
        return Response(serializers.data,status=200)
    def patch(self,request,id):
        user=self.get_queryset(id,tipo="client")
        serializers=UserSerializers(user,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            serializers=UserSerializers(serializers)
            return Response(serializers.data,status=201)
        return Response(serializers.errors,status=400)
    