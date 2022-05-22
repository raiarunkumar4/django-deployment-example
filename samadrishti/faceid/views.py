from django.shortcuts import render
from faceid.models import Customer, Device, Location, Person
from faceid.serializers import CustomerSerializer, DeviceSerializer, LocationSerializer, PersonSerializer, DeviceSerializer_IsRegistered, PersonSerializer_GetEnrolment
from faceid.permissions import IsOwnerOrReadOnly, IsOwnerOrSuperOrReadOnly
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import renderers
from datetime import datetime
from PIL import Image
import numpy as np
#from picklefield.fields import PickledObjectField
import face_recognition
import cv2
import pickle
import base64
# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    #queryset = Customer.objects.all()

    def get_queryset(self, *args, **kwargs):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        if self.request.user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.all().filter(owner=self.request.user)

    #queryset = get_queryset()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    #def perform_create(self, serializer):
        #serializer.save(owner=self.request.user)
    @action(detail=False)
    def get_template (self, request, pk=None):

        #enrolment_data = PickledObjectField(null=True, blank=True)
        #print(request.data)
        #print(request.query_params)
        #print(request.query_params.get('sno'))
        if "photo" in request.data:
            profile_image = request.data['photo']#request.query_params.get('emp-photo')
        else:
            return Response([{'status': 'Data Missing'}])

        #print(profile_image)
        pil_image = Image.open(profile_image)
        image = np.array(pil_image)
        #print(image)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)
        #print(len(encodings))
        #print(encodings[0].shape)
        enrolment_data = pickle.dumps(encodings[0])
        dev_status = [{'status': 'ok'}]
        return Response(dev_status + [{'template':base64.b64encode(enrolment_data)}])

class LocationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    #queryset = Location.objects.all()
    def get_queryset(self, *args, **kwargs):
        """
        This view should return a list of all the locations
        for the currently authenticated user.
        """
        if self.request.user.is_superuser:
            return Location.objects.all()
        return Location.objects.all().filter(owner=self.request.user)
        #return Location.objects.all().filter(owner=self.request.user)

    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DeviceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    #queryset = Device.objects.all()
    def get_queryset(self, *args, **kwargs):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        if self.request.user.is_superuser:
            return Device.objects.all()
        return Device.objects.all().filter(owner=self.request.user)

    serializer_class = DeviceSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]IsOwnerOrSuperOrReadOnly
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperOrReadOnly] #IsOwnerOrSuperOrReadOnly because you need to upload the analytics, images, videos

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False)
    def is_registered (self, request, pk=None):

        #print(request.query_params.get('sno'))
        device = self.get_queryset().filter(sno=request.query_params.get('sno')) #
        if device.count() == 0:
            return Response([{'status': 'Not Registered'}])
        # else:
        #     #for key, value in device[0].items():
        #     print(device[0].location)
        #     for dev in device:
        #         print(dev.location)
        #serializer = self.get_serializer(device, many=True) DeviceSerializer_IsRegistered
        serializer = DeviceSerializer_IsRegistered(device, many=True)
        dev_status = [{'status': 'Registered'}]
        return Response(dev_status + serializer.data)
        # if serializer.is_valid():
        #     dev_sno = serializer.validated_data['sno']
        #     device = self.get_queryset().filter(sno=dev_sno) #Device.objects.all().filter(sno=dev_sno)
        #     serializer = self.get_serializer(device)
        #     return Response(serializer.data)
        # else:
        #     print("Invalid Serializer")
        #     return Response(serializer.errors,
        #                     status=status.HTTP_400_BAD_REQUEST)

class PersonViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    #queryset = Person.objects.all()

    def get_queryset(self, *args, **kwargs):
        """
        This view should return a list of all the persons
        for the currently authenticated user.
        """
        if self.request.user.is_superuser:
            return Person.objects.all()
        return Person.objects.all().filter(owner=self.request.user)
        #return Person.objects.all().filter(owner=self.request.user)

    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False)
    def get_enrolment (self, request, pk=None):

        loc_id = request.query_params.get('loc_id')#request.data['loc_id']
        #print(loc_id)
        if loc_id == "null":
            return Response([{'status': 'Invalid loc_id'}])
        persons = self.get_queryset().filter(location=loc_id)
        if persons.count() == 0:
            return Response([{'status': 'No Enrolment for the location'}])
        serializer = PersonSerializer_GetEnrolment(persons, many=True)
        return Response([{'status': 'Enrolment available for the location'}] + serializer.data)
    # @action(detail=False)
    # def get_enrolment (self, request, pk=None):
    #
    #     loc = request.data['location']
    #     print(request.data['date_string'])
    #     if request.data['date_string'] == "null":
    #         return Response([{'status': 'Invalid date_string'}])
    #     date_obj = datetime.strptime(request.data['date_string'], '%Y-%m-%d %H:%M:%S.%f')
    #     print (loc)
    #     if loc == "null":
    #         #person = self.get_queryset().filter(location=None).last()
    #         persons = self.get_queryset().filter(location=None)
    #         #print(type(persons))
    #         if persons.count() == 0:
    #             return Response([{'status': 'No Enrolment for the location'}])
    #         person = persons.last()
    #         # print(type(person))
    #         # print(person.id)
    #         # print(person.none_loc_last_updated)
    #         # if person is None:
    #         #      return Response([{'status': 'No Enrolment for the location'}])
    #         loc_last_update = datetime.strptime(person.none_loc_last_updated, '%Y-%m-%d %H:%M:%S.%f')
    #         if  loc_last_update > date_obj:
    #             serializer = self.get_serializer(persons, many=True)
    #             return Response([{'status': 'Update available for the location'}] + serializer.data)
    #         else:
    #             return Response([{'status': 'No update available for the location'}])
    #
    #     else:
    #         locations = Location.objects.all().filter(loc_name=loc)
    #         print(type(locations))
    #         if locations.count() == 0:
    #             return Response([{'status': 'No such location'}])
    #         loc_last_update = datetime.strptime(locations[0].last_updated, '%Y-%m-%d %H:%M:%S.%f')
    #         if  loc_last_update > date_obj:
    #             persons = self.get_queryset().filter(location=locations[0].id)
    #             print(type(persons))
    #             if persons.count() == 0:
    #                 return Response([{'status': 'No Enrolment for the location'}])
    #             serializer = self.get_serializer(persons, many=True)
    #             return Response([{'status': 'Update available for the location'}] + serializer.data)
    #         else:
    #             return Response([{'status': 'No update available for the location'}])

        # device = self.get_queryset().filter(sno=request.data['sno']) #
        # if device.count() is 0:
        #     return Response([{'status': 'Not Registered'}])
        # else:
        #     #for key, value in device[0].items():
        #     print(device[0].location)
        #     for dev in device:
        #         print(dev.location)
        # serializer = self.get_serializer(device, many=True)
        # dev_status = [{'status': 'Registered'}]
        # return Response(dev_status + serializer.data)
