from django.conf.urls import url
from .views import ProjectsJoinableViewset
from .models import Project
from djangoldp.models import Model


urlpatterns = [
    url(r'^projects/joinable/', ProjectsJoinableViewset.urls(model_prefix="projects-joinable",
        model=Project,
        lookup_field=Model.get_meta(Project, 'lookup_field', 'pk'),
        permission_classes=Model.get_meta(Project, 'permission_classes', []),
        fields=Model.get_meta(Project, 'serializer_fields', []),
        nested_fields=Model.get_meta(Project, 'nested_fields', [])))
]
