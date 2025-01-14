from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response

from notifications.serializers import NotificationSerializer


# Create your views here.
class NotificationAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        recipient = data.get('recipient')
        if isinstance(recipient, list):
            data_response = list()
            for rec in recipient:
                serializer = NotificationSerializer(
                    data={'recipient': rec, 'message': data.get('message'), 'delay': data.get('delay')})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data_response.append(serializer.data)
            Response(data_response, status=201)
        elif isinstance(recipient, str):
            serializer = NotificationSerializer(data={'recipient': recipient, 'message': data.get('message'), 'delay': data.get('delay')})
            serializer.is_valid(raise_exception=True)
            serializer.save()

        else:
            return Response({'recipient': ['Получатель должен быть валидным адресом электронной почты или номером Телеграм состоящий только из цифр.']}, status=400)
        Response(serializer.data, status=201)




