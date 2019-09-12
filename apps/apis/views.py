import shortuuid
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.mongo import Mongo
from .models import Device
from .serializers import DeviceSerializer
# Create your views here.

client = Mongo(settings.MONGO_URL, settings.MONGO_PORT)

mqtt_db = client.mqtt


class DeviceView(APIView):

    def post(self, request):
        product_name = request.data["product_name"]
        device_name = shortuuid.uuid()
        password = shortuuid.uuid()
        username = "%s/%s" % (product_name, device_name)

        new_device = Device(product_name,
                            device_name,
                            username,
                            password)

        obj = mqtt_db.insert_one(new_device.to_doc())
        serialized = DeviceSerializer(obj)
        return Response(serialized.data)

