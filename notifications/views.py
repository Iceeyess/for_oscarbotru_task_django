from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response

from notifications.serializers import NotificationSerializer


# Create your views here.
class NotificationAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        """Решил пойти к родительскому классу и верстать в нем, поскольку он без примесей.
        Данный метод проверяет, является ли поле recipient списком или строкой или иным типом данных.
        В зависимости от факта, возвращает список из созданных объектов, один созданный объект(случай с одним адресом)
        или ошибку в валидации данных"""
        data = self.request.data
        recipient = data.get('recipient')
        if isinstance(recipient, list):
            data_response = list()  # Список для созданных объектов
            for rec in recipient:
                serializer = NotificationSerializer(
                    data={'recipient': rec, 'message': data.get('message'), 'delay': data.get('delay')})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data_response.append(serializer.data)
            return JsonResponse(data=data_response, safe=False)
        elif isinstance(recipient, str):
            serializer = NotificationSerializer(data={'recipient': recipient, 'message': data.get('message'), 'delay': data.get('delay')})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'recipient': ['Получатель должен быть валидным адресом электронной почты или номером Телеграм состоящий только из цифр.']}, status=400)





