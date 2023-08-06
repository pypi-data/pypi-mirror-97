from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tables.models import Table, Leg, Foot


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# class TableSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)

#     def create(self, validated_data):
#         return Table.objects.create(validated_data)

#     #def update(self, validated_data):
#     #    return Table.objects.create(validated_data)

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'name')

class LegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leg
        fields = '__all__'

class FootSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foot
        fields = '__all__'