from django.db import models
from picklefield.fields import PickledObjectField
import face_recognition
import cv2
import datetime
from django.contrib.auth.models import User
from django.conf import settings
import os.path
from PIL import Image
import numpy as np
#import time
# from django.db.models.signals import post_migrate


# def insert_initial_data(sender, verbosity, **kwargs): #def insert_initial_data(sender, app, created_models, verbosity, **kwargs):
#     #if Location in created_models:
#     for name in ('ak'):
#          User.objects.get_or_create(username=name, password='ak123', is_superuser=True)
#     for name in ('universal'):
#         Location.objects.get_or_create(loc_name=name, owner=1)
#
# post_migrate.connect(insert_initial_data)

# Create your models here.

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='customers', on_delete=models.CASCADE)
    #additional
    address = models.TextField()
    #profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:

            if self._state.adding:
                Location.objects.get_or_create(loc_name='Universal', owner=self.owner)


        except Exception as e:
            print(e)

        super(Customer, self).save(*args, **kwargs)

class Location(models.Model):
    #created = models.DateTimeField(auto_now_add=True)
    loc_name = models.CharField(max_length=100) #, unique=True) #, default='universal')
    last_updated = models.CharField(max_length=128, default='0002-02-02 00:00:00.000000')# datetime min time is 0001-01-01 00:00:00.000000
    owner = models.ForeignKey('auth.User', related_name='locations', on_delete=models.CASCADE)

    def __str__(self):
        return self.loc_name

def analytics_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    now = datetime.datetime.now()
    return 'user_{0}/{1}/{2}/{3}/{4}/analytics/{5}'.format(instance.owner, instance.sno, now.strftime('%Y'),now.strftime('%m'),now.strftime('%d'),filename)

def images_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    now = datetime.datetime.now()
    return 'user_{0}/{1}/{2}/{3}/{4}/images/{5}'.format(instance.owner, instance.sno, now.strftime('%Y'),now.strftime('%m'),now.strftime('%d'),filename)

def videos_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    now = datetime.datetime.now()
    return 'user_{0}/{1}/{2}/{3}/{4}/videos/{5}'.format(instance.owner, instance.sno, now.strftime('%Y'),now.strftime('%m'),now.strftime('%d'), filename)

def script_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/script/{2}'.format(instance.owner, instance.sno, filename)

class Device(models.Model):
    #created = models.DateTimeField(auto_now_add=True)
    sno = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey('auth.User', related_name='devices', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, default=1, on_delete=models.CASCADE)#models.CharField(max_length=128)#,blank=True, null=True default='Universal'
    analytics_file = models.FileField(upload_to=analytics_directory_path, blank=True)
    image_file = models.ImageField(upload_to=images_directory_path, blank=True)
    video_file = models.FileField(upload_to=videos_directory_path, blank=True)
    script_file = models.FileField(upload_to=script_directory_path, blank=True)

    def __str__(self):
        return self.sno

    def save(self, *args, **kwargs):
        try:

            if self._state.adding:
                #print(self.location.id)
                #print(self.location.owner)
                if self.location.id == 1:
                    if self.location.owner != self.owner:
                        loc = Location.objects.get(loc_name='Universal', owner=self.owner)
                        #print(type(loc))
                        #print(loc.id)
                        self.location = loc


        except Exception as e:
            print(e)

        super(Device, self).save(*args, **kwargs)
def person_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.owner, instance.uid, filename)

def enrolment_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.owner, instance.location, filename)

class Person(models.Model):
    #created = models.DateTimeField(auto_now_add=True)
    uid = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey('auth.User', related_name='persons', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, default=1, on_delete=models.CASCADE) #models.CharField(max_length=128) #blank=True, null=True,
    #none_loc_last_updated = models.CharField(max_length=128, null=True) # models.BooleanField(default=False)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    profile_pic = models.ImageField(upload_to=person_directory_path)
    phone = models.PositiveIntegerField()
    email = models.EmailField(max_length=264,unique=True)
    #enrolment_data = models.FileField(upload_to=enrolment_directory_path, blank=True)
    enrolment_data = PickledObjectField(blank=True, null=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        try:
            if self._state.adding:
                #print(self.location.id)
                #print(self.location.owner)
                if self.location.id == 1:
                    if self.location.owner != self.owner:
                        loc = Location.objects.get(loc_name='Universal', owner=self.owner)
                        #print(type(loc))
                        #print(loc.id)
                        self.location = loc

            #generate the face encoding of the person
            #filepath = 'faceid/media/user_{0}/{1}/{2}'.format(self.owner, self.uid, self.profile_pic)
            #media_path = '/'.join(settings.MEDIA_ROOT.split('\\'))
            filepath = r'{0}\user_{1}\{2}\{3}'.format(settings.MEDIA_ROOT, self.owner, self.uid, self.profile_pic)#'arun.jpeg')#
            #print(filepath)
            #time.sleep(50)
            #print(self.profile_pic.open())
            pil_image = Image.open(self.profile_pic)
            image = np.array(pil_image)
            #print(os.path.isfile(filepath))
            #image = cv2.imread(image)#'F:/Technical/Python/Django/DRF_Projects/samadrishti/faceid/media/user_demo1/emp01/arun.jpeg'#self.profile_pic)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # detect the (x, y)-coordinates of the bounding boxes
	        # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb)
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            #print(len(encodings))
            #print(encodings[0].shape)
            self.enrolment_data = encodings[0]
            #print (self.location.id)

            if self.location is not None:
                loc = Location.objects.get(id=self.location.id)
                loc.last_updated = datetime.datetime.now()
                #print (loc.last_updated)
                loc.save()
            # else:
            #     self.none_loc_last_updated = datetime.datetime.now()
        except Exception as e:
            print(e)

        super(Person, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     """
    #     Use the `face_recognition` library to create a pickel
    #     representation of the face encodings of persons.
    #     """
    #
    #
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = 'table' if self.linenos else False
    #     options = {'title': self.title} if self.title else {}
    #     formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                           full=True, **options)
    #     self.highlighted = highlight(self.code, lexer, formatter)
    #     super().save(*args, **kwargs)
