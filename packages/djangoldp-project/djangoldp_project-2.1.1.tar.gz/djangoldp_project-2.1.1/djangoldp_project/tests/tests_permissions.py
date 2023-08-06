import uuid
import json
from datetime import datetime, timedelta

from djangoldp.serializers import LDListMixin, LDPSerializer
from rest_framework.test import APITestCase, APIClient

from djangoldp_project.models import Project, Member, Customer
from djangoldp_project.tests.models import User


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        LDListMixin.to_representation_cache.reset()
        LDPSerializer.to_representation_cache.reset()

    def setUpLoggedInUser(self):
        self.user = User(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                         password='glass onion')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def _get_random_project(self, status_choice='Public', customer=None):
        return Project.objects.create(name='Test', status=status_choice, customer=customer)

    def _get_random_customer(self, owner=None):
        return Customer.objects.create(owner=owner)

    def setUpProject(self, status_choice='Public'):
        self.project = self._get_random_project(status_choice)

    def _get_request_json(self, **kwargs):
        res = {
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        for kwarg in kwargs:
            if isinstance(kwargs[kwarg], str):
                res.update({kwarg: {'@id': kwargs[kwarg]}})
            else:
                res.update({kwarg: kwargs[kwarg]})

        return res

    def _get_random_user(self):
        return User.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test', last_name='Test',
                                   username=str(uuid.uuid4()))

    # test project permissions
    def test_list_project_anonymous(self):
        self.setUpProject('Public')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 403)

    def test_list_project_authenticated(self):
        self.setUpLoggedInUser()
        # a public project, a private project I'm in and a private project I'm not in
        another_user = self._get_random_user()
        public_project = self._get_random_project('Public')
        my_project = self._get_random_project('Private')
        Member.objects.create(project=my_project, user=self.user)
        private_project = self._get_random_project('Private')

        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['ldp:contains']), 2)

    # test customer permissions
    def test_list_customer_anonymous(self):
        self._get_random_customer()
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 403)
        # self.assertEqual(len(response.data['ldp:contains']), 1)

    def test_list_customer_authenticated(self):
        self.setUpLoggedInUser()
        self._get_random_customer()

        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_get_customer_anonymous(self):
        customer = self._get_random_customer()

        response = self.client.get('/customers/{}/'.format(customer.pk))
        self.assertEqual(response.status_code, 403)

    def test_get_customer_authenticated(self):
        self.setUpLoggedInUser()
        customer = self._get_random_customer()

        response = self.client.get('/customers/{}/'.format(customer.pk))
        self.assertEqual(response.status_code, 404)

    def test_get_customer_owner(self):
        self.setUpLoggedInUser()
        customer = self._get_random_customer(owner=self.user)

        response = self.client.get('/customers/{}/'.format(customer.pk))
        self.assertEqual(response.status_code, 200)

    # members of one of their projects can view the customer
    def test_get_customer_project_member(self):
        self.setUpLoggedInUser()
        customer = self._get_random_customer()

        project = self._get_random_project(status_choice='Private', customer=customer)
        Member.objects.create(project=project, user=self.user)

        response = self.client.get('/customers/{}/'.format(customer.pk))
        self.assertEqual(response.status_code, 200)

    def test_post_customer_anonymous(self):
        response = self.client.post('/customers/', data=json.dumps({}), content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

    def test_post_customer_authenticated(self):
        self.setUpLoggedInUser()
        response = self.client.post('/customers/', data=json.dumps({}), content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)

    # removing a Member - I am an admin
    def test_delete_project_member_admin(self):
        self.setUpLoggedInUser()
        self.setUpProject('Private')

        Member.objects.create(project=self.project, user=self.user, is_admin=True)
        another_user = self._get_random_user()
        Member.objects.create(project=self.project, user=another_user, is_admin=False)

        self.assertEqual(Member.objects.count(), 2)
        response = self.client.delete('/project-members/2/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Member.objects.count(), 1)
