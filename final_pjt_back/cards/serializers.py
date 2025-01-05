from rest_framework import serializers
from .models import Card


class Cardserializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CardBenefitserializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('card_benefits',)