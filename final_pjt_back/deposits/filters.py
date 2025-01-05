import django_filters
from .models import DepositOption, SavingOption, Saving, Deposit


class DepositOptionFilter(django_filters.FilterSet):
    class Meta:
        model = DepositOption
        fields = ['save_trm', 'intr_rate_type_nm']

class SavingOptionFilter(django_filters.FilterSet):
    class Meta:
        model = SavingOption
        fields = ['save_trm', 'intr_rate_type_nm']

class DepositFilter(django_filters.FilterSet):

    class Meta:
        model = Deposit
        fields = ('kor_co_nm',)

class SavingFilter(django_filters.FilterSet):

    class Meta:
        model = Saving
        fields = ('kor_co_nm',)