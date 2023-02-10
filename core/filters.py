import django_filters
from django.db import models as dm
from core.models import Product, Balance



class BalanceFilter(django_filters.rest_framework.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='date_created', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = Balance
        fields = ['start_date', 'end_date']

        # filter_overrides = {
        #     dm.DateTimeField: {
        #         'filter_class': django_filters.DateTimeFilter
        #     },
        # }