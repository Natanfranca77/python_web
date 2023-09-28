from django.shortcuts import render
from .serializer import tarefaSerializer
from rest_framework.views import APIView
from user.permissions import ValidToken,IsNotSuspended
from .models import TarefaModel
from django.http import Http404
import jwt
from django.conf import settings
from uuid import UUID
from rest_framework.response import Response

class TarefaView(APIView):
    serializer_class= tarefaSerializer
    permission_classes =[ValidToken,IsNotSuspended]
    queryset=TarefaModel.objects.all()
    def get_object(self,pk,user):
        try:
            return self.queryset.get(pk=pk,user=user)
        except TarefaModel.DoesNotExist:
            return Http404
    def post(self,request):
        user_id=jwt.decode(request.headers.get("token"),settings.SECRET_KEY,algorithms=["HS256"])
        request.data["user"]=UUID(user_id["user_id"])

        serializer=tarefaSerializer(data=request.data)
        if(serializer.is_valid()):
            tarefa=serializer.save()
            return Response(tarefaSerializer(tarefa).data,status=201)
        return Response(serializer.errors,status=400)
    
    def get (self,request,id=None):
        user_id=jwt.decode(request.headers.get('token'),settings.SECRET_KEY,algorithms=['HS256'])
        user_id=UUID(user_id['user_id'])

        if id is not None:
            tarefa=self.get_object(id,user=user_id)
            serializer= tarefaSerializer(tarefa)
        else:
            tarefas=self.queryset.filter(user=user_id,delete=False)
            serializer= tarefaSerializer(tarefas,many=True)
        return Response(serializer.data,status=200)
    def patch(self,request,id):

        user_id=jwt.decode(request.headers.get('token'),
            settings.SECRET_KEY,algorithms=["HS256"])

        print(user_id["user_id"])
        user = UUID(user_id["user_id"])
        tarefa= self.queryset.get(id=id,user=user)
        serializer=tarefaSerializer(tarefa,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=202)
        return Response(serializer.errors,status=400)
    def delete(self,request,id):
        user_id = jwt.decode(request.headers.get('token'),settings.SECRET_KEY,algorithms=["HS256"])
        user=UUID(user_id['user_id'])
        tarefa=self.get_object(id,user=user)
        tarefa.delete=True
        tarefa.save()
        serializer=tarefaSerializer(tarefa)
        if serializer.data['delete']:
            return Response({"menssage":"deletado com sucesso!!"},status=200)
        return Response ({"menssage":"algo deu errado ao deletar!!"},status=400)
