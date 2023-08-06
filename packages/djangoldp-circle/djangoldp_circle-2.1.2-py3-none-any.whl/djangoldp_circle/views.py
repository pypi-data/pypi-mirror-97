from djangoldp.filters import LocalObjectFilterBackend
from djangoldp.views import LDPViewSet
from djangoldp.models import Model
from django.http import Http404


class CircleMembersViewset(LDPViewSet):

    def get_parent(self):
        raise NotImplementedError("get_parent not implemented in CircleMembersViewset")

    def is_safe_create(self, user, validated_data, *args, **kwargs):
        from djangoldp_circle.models import Circle, CircleMember

        try:
            if 'circle' in validated_data.keys():
                circle = Circle.objects.get(urlid=validated_data['circle']['urlid'])
            else:
                circle = self.get_parent()

            # public circles any user can add
            if circle.status == 'Public':
                return True

            # other circles any circle member can add a user
            if circle.members.filter(user=user).exists():
                return True
        except Circle.DoesNotExist:
            return True
        except (KeyError, AttributeError):
            raise Http404('circle not specified with urlid')

        return False


class CirclesJoinableViewset(LDPViewSet):

    filter_backends = [LocalObjectFilterBackend]

    def __init__(self, **kwargs):
        from djangoldp_circle.models import Circle

        kwargs['model'] = Circle
        kwargs['nested_fields'] = Circle.nested.fields()
        super().__init__(**kwargs)

    def get_queryset(self):
        return super().get_queryset().exclude(members__user=self.request.user.id)\
            .exclude(status="Private")\
            .exclude(status="Archived")
