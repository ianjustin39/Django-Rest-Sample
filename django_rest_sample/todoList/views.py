from django.shortcuts import render

# Create your views here.
from .models import TodoList
from .serializers import TodoListSerializer
from .models import fun_raw_sql_query

from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from main.permissions import ShareAppIsAuthenticated
from main.authentication import MyJSONWebTokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.
class TodoListViewSet(viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    # permission_classes = (IsAuthenticated,)
    permission_classes = (ShareAppIsAuthenticated,)
    authentication_classes = [MyJSONWebTokenAuthentication,]  # 就是這裡!

    # /api/music/raw_sql_query/
    @action(methods=['get'], detail=False)
    # @permission_classes((IsAuthenticated, ))
    def raw_sql_query(self, request):
        title = request.query_params.get('title', None)
        todo_list = fun_raw_sql_query(title=title)
        serializer = TodoListSerializer(todo_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
