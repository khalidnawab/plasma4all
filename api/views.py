from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


from .serializers import ProfileSerializer, UserSerializer
from plasma.models import *
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_list(request, action):
    if action == 1:
        requests = Profile.objects.filter(plasma_completed=False, plasma_request=True)
        serializer = ProfileSerializer(requests, many=True)
        return JsonResponse({'all_plasma_requests': serializer.data}, safe=False, status=status.HTTP_200_OK)
    elif action == 2:
        requests = Profile.objects.filter(donation_completed=False, donation_request=True)
        serializer = ProfileSerializer(requests, many=True)
        return JsonResponse({'all_donation_requests': serializer.data}, safe=False, status=status.HTTP_200_OK)
    elif action == 3:
        requests = Profile.objects.filter(plasma_completed=True, plasma_request=True)
        serializer = ProfileSerializer(requests, many=True)
        return JsonResponse({'all_donation_requests': serializer.data}, safe=False, status=status.HTTP_200_OK)
    elif action == 4:
        requests = Profile.objects.filter(donation_completed=True, donation_request=True)
        serializer = ProfileSerializer(requests, many=True)
        return JsonResponse({'all_donation_requests': serializer.data}, safe=False, status=status.HTTP_200_OK)
    else:
        data = {"Error": "Unknown action"}
        return Response(data=data)



@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def request_plasma(request, pk, action):

    try:
        note_item = Profile.objects.get(pk=pk)
        # returns 1 or 0
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = {}
        if action == 1:
            note_item.plasma_request = True
            note_item.save()
            data["success"] = "Plasma request submitted successfully."
            return Response(data=data)
        elif action == 2:
            note_item.donation_request = True
            note_item.save()
            data["success"] = "Donation request submitted successfully."
            return Response(data=data)
        elif action == 3:
            note_item.plasma_completed = True
            note_item.save()
            data["success"] = "Plasma request marked as complete."
            return Response(data=data)
        elif action == 4:
            note_item.donation_completed = True
            note_item.save()
            data["success"] = "Donation request marked as completed."
            return Response(data=data)
        elif action == 5:
            note_item.plasma_completed = False
            note_item.save()
            data["success"] = "Plasma request marked as incomplete."
            return Response(data=data)
        elif action == 6:
            note_item.donation_completed = False
            note_item.save()
            data["success"] = "Donation request marked as incomplete."
            return Response(data=data)
        else:
            data["Error"] = "Unknown action"
            return Response(data=data)



class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_patient(request):
    data = request.data
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    data["user"] = user.pk
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
       serializer.save(user=user)
       return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)