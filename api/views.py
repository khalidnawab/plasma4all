from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from plasma.models import *
from rest_framework import status, generics
import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_plasma_requests(request):
    requests = Profile.objects.filter(plasma_completed=False, plasma_request=True)
    serializer = ProfileSerializer(requests, many=True)
    return JsonResponse({'all_plasma_requests': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_donation_requests(request):
    requests = Profile.objects.filter(donation_completed=False, donation_request=True)
    serializer = ProfileSerializer(requests, many=True)
    return JsonResponse({'all_donation_requests': serializer.data}, safe=False, status=status.HTTP_200_OK)