from rest_framework import serializers
from .models import User, BaseGames, RecommendResult

class UserSerializer(serializers.ModelSerializer) :
    class Meta:
        model = User
        fields = '__all__'

  
class RecommendResultSerializer(serializers.ModelSerializer) :
    class Meta:
        model = RecommendResult
        fields = '__all__'

class BaseGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseGames
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genres'] = instance.genres.split(',')  # 문자열을 리스트로 변환
        return data

    def to_internal_value(self, data):
        data_copy = data.copy()
        data_copy['genres'] = ','.join(data['genres'])  # 리스트를 문자열로 변환
        return super().to_internal_value(data_copy)
