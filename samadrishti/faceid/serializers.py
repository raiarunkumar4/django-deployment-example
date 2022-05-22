from rest_framework import serializers
from faceid.models import Customer, Location, Device, Person
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class LocationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #devicesatlocation = DeviceSerializer(many=True)
    class Meta:
        model = Location
        fields = ['url', 'id', 'loc_name', 'owner', 'last_updated']

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #location = serializers.ReadOnlyField(source='location.loc_name')

    class Meta:
        model = Device
        fields = ['url', 'id', 'sno', 'location', 'owner', 'analytics_file', 'image_file', 'video_file', 'script_file']

class DeviceSerializer_IsRegistered(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    loc_name = serializers.ReadOnlyField(source='location.loc_name')
    loc_id = serializers.ReadOnlyField(source='location.id')
    loc_last_update = serializers.ReadOnlyField(source='location.last_updated')
    # is_registered = serializers.BooleanField(False)
    class Meta:
        model = Device
        fields = ['id','owner','loc_id', 'loc_name', 'loc_last_update' , 'script_file']

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #location = serializers.ReadOnlyField(source='location.loc_name')

    class Meta:
        model = Person
        fields = ['url', 'id', 'uid', 'location', 'owner', 'first_name', 'last_name', 'profile_pic', 'phone', 'email', 'enrolment_data']

class PersonSerializer_GetEnrolment(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    #loc_name = serializers.ReadOnlyField(source='location.loc_name')

    class Meta:
        model = Person
        fields = ['uid', 'first_name', 'last_name', 'phone', 'email', 'enrolment_data']

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    #locations = serializers.HyperlinkedRelatedField(many=True, view_name='location-detail', read_only=True)
    #devices = serializers.HyperlinkedRelatedField(many=True, view_name='device-detail', read_only=True)
    #persons = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail', read_only=True)
    # username = serializers.ReadOnlyField(source='user.username')
    # password = serializers.ReadOnlyField(source='user.password')
    user = UserSerializer(required=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    #locations = LocationSerializer(many=True,required=False)
    class Meta:
        model = Customer
        fields = ['url', 'id','user', 'address', 'owner']#, 'locations', 'devices', 'persons']
    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of customer
        :return: returns a successfully created customer record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        customer, created = Customer.objects.update_or_create(user=user,
                            address=validated_data.pop('address'), owner=user)
        return customer

    def update(self, instance, validated_data):

        if validated_data.get('user') != None:
            user_data = validated_data.pop('user')
            user_ser = UserSerializer(instance=instance.user, data=user_data)
            if user_ser.is_valid():
                user_ser.save()
            #instance.user.email = validated_data.get('email', instance.user)
            instance.user.email = user_data.pop('email')
            #instance.phone = validated_data.get('phone', instance.phone)
        if validated_data.get('address') != None:
            instance.address = validated_data.get('address')
        instance.save()
        return instance
