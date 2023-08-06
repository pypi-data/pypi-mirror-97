import random
import string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from djangoldp.models import Model
from .permissions import CustomerPermissions, ProjectPermissions, ProjectMemberPermissions

from .views import ProjectMembersViewset
import logging

logger = logging.getLogger('djangoldp')


class Customer(Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    logo = models.URLField(blank=True, null=True)
    companyRegister = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_customers", on_delete=models.SET_NULL,
                              null=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    class Meta(Model.Meta):
        auto_author = 'owner'
        owner_field = 'owner'
        anonymous_perms = []
        authenticated_perms = ['add']
        owner_perms = ['inherit', 'view', 'change', 'delete']
        permission_classes = [CustomerPermissions]

    def __str__(self):
        return self.name or self.urlid


class BusinessProvider(Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    fee = models.PositiveIntegerField(default='0', null=True, blank=True)

    def __str__(self):
        return self.name or self.urlid


def auto_increment_project_number():
  last_inc = Project.objects.all().order_by('id').last()
  if not last_inc:
    return 1
  return last_inc.number + 1


MODEL_MODIFICATION_USER_FIELD = 'modification_user'
STATUS_CHOICES = [
    ('Public', 'Public'),
    ('Private', 'Private'),
    ('Archived', 'Archived'),
]


class Project(Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Private', null=True, blank=True)
    number = models.PositiveIntegerField(default=auto_increment_project_number, editable=False)
    creationDate = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='+')
    driveID = models.TextField(null=True, blank=True)
    businessProvider = models.ForeignKey(BusinessProvider, blank=True, null=True, on_delete=models.SET_NULL)
    jabberID = models.CharField(max_length=255, blank=True, null=True)
    jabberRoom = models.BooleanField(default=True)

    class Meta(Model.Meta):
        empty_containers = ["captain"]
#        depth = 1 # Disabled due to captain being serialized
        permission_classes = [ProjectPermissions]
        anonymous_perms = []
        authenticated_perms = []
        owner_perms = []
        rdf_type = 'hd:project'

    def __str__(self):
        return self.name or self.urlid

    def get_admins(self):
        return self.members.filter(is_admin=True)


class Member(Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    class Meta(Model.Meta):
        container_path = "project-members/"
        permission_classes = [ProjectMemberPermissions]
        anonymous_perms = []
        authenticated_perms = ['view', 'add']
        owner_perms = ['inherit']
        unique_together = ['user', 'project']
        rdf_type = 'hd:projectmember'
        view_set = ProjectMembersViewset

    def __str__(self):
        return str(self.pk) or self.urlid

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.username == "hubl-workaround-493":
                self.user = None

        # cannot be duplicated Members
        if not self.pk and Member.objects.filter(project=self.project, user=self.user).exists():
            return

        super(Member, self).save(*args, **kwargs)

@receiver(post_save, sender=Member)
def fix_user_hubl_workaround_493(sender, instance, **kwargs):
    if not instance.user:
        try:
            request_user = getattr(instance, MODEL_MODIFICATION_USER_FIELD, None)
            if request_user is None:
                raise Exception('request user was unexpectadly None!')
            user = get_user_model().objects.get(pk=request_user.pk)
            instance.user = user
            instance.save()
        except Exception as e:
            logger.error('error in fix_user_hubl_workaround_493.. ' + str(e))
            if instance.pk is not None:
                instance.delete()


@receiver(pre_save, sender=Project)
def set_jabberid(sender, instance, **kwargs):
    if isinstance(getattr(settings, 'JABBER_DEFAULT_HOST', False), str) and not instance.jabberID:
        instance.jabberID = '{}@conference.{}'.format(
            ''.join(
                [
                    random.choice(string.ascii_letters + string.digits)
                    for n in range(12)
                ]
            ).lower(),
            settings.JABBER_DEFAULT_HOST
        )
        instance.jabberRoom = True


@receiver(post_save, sender=Project)
def set_creator_as_member(instance, created, **kwargs):
    if created:
        request_user = getattr(instance, MODEL_MODIFICATION_USER_FIELD, None)
        if request_user:
            try:
                Member.objects.create(user=request_user, project=instance, is_admin=True)
            except Exception as e:
                logger.error('Unable to set current user as member of the created project ' + str(e))


@receiver(post_save, sender=Project)
def set_captain_as_member(instance, created, **kwargs):
    if instance.captain is not None:
        try:
            captain_member = instance.members.get(user=instance.captain)
            if not captain_member.is_admin:
                captain_member.is_admin = True
                captain_member.save()
        except Member.DoesNotExist:
            Member.objects.create(user=instance.captain, project=instance, is_admin=True)

@receiver(post_delete, sender=Member)
def delete_project_on_last_member_delete(sender, instance, **kwargs):
    # if this was the last member of the project, the project should be deleted too
    if instance.project.pk is not None and instance.project.members.count() == 0:
        instance.project.delete()

@receiver(pre_delete, sender=Member)
def manage_deleted_project_captain(sender, instance, **kwargs):
    # was the captain removed?
    if instance.user is not None and instance.user == instance.project.captain:
        # if there are another admin: pick one, set them as captain
        alt = instance.project.members.filter(is_admin=True).exclude(user=instance.user)[:1]
        if not alt.exists():
            # if there is another member: pick one, set them as captain
            alt = instance.project.members.all().exclude(user=instance.user)[:1]
        if alt.exists():
            instance.project.captain = alt[0].user
            instance.project.save()
