import django_filters

from .models import GameJam


class GameJamsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Название джема')

    date_start = django_filters.DateFilter(field_name='date_start', label='Дата начала джема', lookup_expr='gte')
    date_end = django_filters.DateFilter(field_name='date_end', label='Дата окончания джема', lookup_expr='lte')

    status = django_filters.ChoiceFilter(field_name='status', lookup_expr='exact', choices=GameJam.jam_status)

    class Meta:
        model = GameJam
        fields = ['title', 'date_start', 'date_end', 'status']
