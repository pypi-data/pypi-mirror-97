from django.conf import settings

from djangoldp.permissions import LDPPermissions
from djangoldp_project.xmpp import XMPP_SERVERS, get_client_ip
from djangoldp_project.filters import CustomerFilterBackend, ProjectFilterBackend, ProjectMemberFilterBackend


class CustomerPermissions(LDPPermissions):
    filter_backends=[CustomerFilterBackend]

    def get_object_permissions(self, request, view, obj):
        from djangoldp_project.models import Member

        perms = super().get_object_permissions(request, view, obj)

        user = request.user
        if not user.is_anonymous:
            # members of one of their projects can view the customer
            if Member.objects.filter(project__customer=obj, user=user).exists():
                perms.add('view')

        return perms


class ProjectPermissions(LDPPermissions):
    filter_backends=[ProjectFilterBackend]

    def get_object_permissions(self, request, view, obj):
        perms = super().get_object_permissions(request, view, obj)

        user = request.user
        if not user.is_anonymous:
            # permissions gained by being a member, and admin
            if obj.members.filter(user=user).exists():
                perms = perms.union({'view'})

                if obj.members.filter(user=user).get().is_admin:
                    perms = perms.union({'add', 'change', 'delete'})

            # permissions gained by the project being public
            if obj.status == 'Public':
                perms = perms.union({'view', 'add'})

        return perms

    def get_container_permissions(self, request, view, obj=None):
        perms = super().get_container_permissions(request, view, obj)

        if not request.user.is_anonymous:
            default_perms = getattr(settings, 'USER_AUTHENTICATED_PROJECT_PERMISSIONS', ['view', 'add'])
            perms = perms.union(set(default_perms))

            # a superuser can always add new projects
            if request.user.is_superuser:
                perms = perms.union({'add'})

        return perms
    
    def has_permission(self, request, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_object_permission(request, view, obj)


class ProjectMemberPermissions(LDPPermissions):
    filter_backends = [ProjectMemberFilterBackend]

    def get_object_permissions(self, request, view, obj):
        perms = super().get_object_permissions(request, view, obj)

        user = request.user

        if not user.is_anonymous:
            # the operation is on myself
            if obj.user == user:
                perms.add('view')

                if not obj.is_admin or obj.project.members.filter(is_admin=True).count() > 1:
                    perms.add('delete')

                if obj.project.status == 'Public':
                    perms = perms.union({'add', 'delete'})

            # the operation is on another member
            else:
                # permissions gained in public projects
                if obj.project.status == 'Public':
                    perms = perms.union({'view', 'add'})

                # permissions gained for all members
                if obj.project.members.filter(user=user).exists():
                    perms = perms.union({'view', 'add'})

                    # permissions gained for admins (on other users)
                    if obj.project.members.filter(user=user).get().is_admin:
                        perms = perms.union({'view', 'add'})

                        if not obj.is_admin:
                            perms.add('delete')
                    else:
                        perms.add('view')

        return perms
    
    def has_permission(self, request, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_object_permission(request, view, obj)
