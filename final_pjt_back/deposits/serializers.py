from rest_framework import serializers
from .models import Deposit, DepositOption, Saving, SavingOption

# 예금 옵션 정보
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit',)

# 예금 정보 전체 생성/조회
class DepositSerializer(serializers.ModelSerializer):
    DepositOption_list = DepositOptionSerializer(many=True, read_only=True)
    class Meta:
        model = Deposit
        fields = '__all__'
        # read_only_fields = ('recomm_user')        


# 적금 옵션 정보 조회
class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields=('saving',)

# 적금 전체 정보 생성/조회
class SavingSerializer(serializers.ModelSerializer):
    # 역참조 
    savingOption_list = SavingOptionSerializer(many=True, read_only=True)
    class Meta:
        model = Saving
        fields = '__all__'

