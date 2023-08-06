from django.db.models import Q
from django.conf import settings
from djangoldp.filters import LDPPermissionsFilterBackend
from djangoldp_circle.xmpp import get_client_ip, XMPP_SERVERS
from rest_framework_guardian.filters import ObjectPermissionsFilter
from guardian.utils import get_anonymous_user


class CircleFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return queryset
        elif request.user.is_anonymous or (
                getattr(settings, 'ANONYMOUS_USER_NAME', True) is not None and
                request.user == get_anonymous_user()):
            return queryset.filter(status='Public')
        else:
            objects = super().filter_queryset(request, queryset, view).values_list('pk')
            return queryset.filter(
                Q(members__user=request.user) |
                Q(status='Public') |
                Q(pk__in=objects)
            ).distinct()


class CircleMemberFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return queryset
        elif request.user.is_anonymous or (
                getattr(settings, 'ANONYMOUS_USER_NAME', True) is not None and
                request.user == get_anonymous_user()):
            return view.model.objects.none()
        else:
            objects = super().filter_queryset(request, queryset, view).values_list('pk')
            return queryset.filter(
                Q(user=request.user) |
                Q(circle__status='Public') |
                Q(circle__members__user=request.user) |
                Q(pk__in=objects)
            ).distinct()
