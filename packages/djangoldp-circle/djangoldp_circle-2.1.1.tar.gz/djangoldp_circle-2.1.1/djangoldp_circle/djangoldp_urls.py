from django.conf.urls import url
from .views import CirclesJoinableViewset
from .models import Circle
from djangoldp.models import Model


urlpatterns = [
    url(r'^circles/joinable/', CirclesJoinableViewset.urls(model_prefix="circles-joinable",
        model=Circle,
        lookup_field=Model.get_meta(Circle, 'lookup_field', 'pk'),
        permission_classes=Model.get_meta(Circle, 'permission_classes', []),
        fields=Model.get_meta(Circle, 'serializer_fields', []),
        nested_fields=Model.get_meta(Circle, 'nested_fields', [])))
]
