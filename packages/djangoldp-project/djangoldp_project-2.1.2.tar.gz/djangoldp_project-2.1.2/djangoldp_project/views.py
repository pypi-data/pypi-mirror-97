from djangoldp.filters import LocalObjectFilterBackend
from djangoldp.views import LDPViewSet
from django.http import Http404


class ProjectMembersViewset(LDPViewSet):

    def get_parent(self):
        raise NotImplementedError("get_parent not implemented in ProjectMembersViewset")

    def is_safe_create(self, user, validated_data, *args, **kwargs):
        from djangoldp_project.models import Project

        try:
            if 'project' in validated_data.keys():
                project = Project.objects.get(urlid=validated_data['project']['urlid'])
            else:
                project = self.get_parent()

            # public projects any user can add
            if project.status == 'Public':
                return True

            # other projects any project member can add a user
            if project.members.filter(user=user).exists():
                return True
        except Project.DoesNotExist:
            return True
        except (KeyError, AttributeError):
            raise Http404('project not specified with urlid')

        return False


class ProjectsJoinableViewset(LDPViewSet):

    filter_backends = [LocalObjectFilterBackend]

    def get_queryset(self):
        return super().get_queryset().exclude(members__user=self.request.user.id)\
            .exclude(status="Private")\
            .exclude(status="Archived")
