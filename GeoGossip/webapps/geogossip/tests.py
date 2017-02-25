from django.test import TestCase
from django.test import Client
from django.contrib.auth import authenticate
from models import User


# Create your tests here.
class EndToEndTest(TestCase):
    def setUp(self):
        super(EndToEndTest, self).setUp()
        self.client = Client()
        self.user = User.objects.create_user(username='stonebai', first_name='Shi', last_name='Bai',
                                             email='shib@andrew.cmu.edu', password='123')
        new_user = authenticate(username=self.user.username, password='123')
        self.assertIsNotNone(new_user)
        self.client.login(username=self.user.username, password='123')
        pass
    #
    # def test_home(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     pass

    def test_profile(self):
        response = self.client.get('/geogossip/profile/' + str(self.user.id))
        self.assertEqual(response.status_code, 200)
        pass

    def test_get_group_with_get_method(self):
        response = self.client.get('/geogossip/get-groups')
        self.assertEqual(response.status_code, 404)
        pass

    def test_get_group_success(self):
        response = self.client.post('/geogossip/get-groups', data={
            'lat': 0.0,
            'lon': 0.0
        })
        self.assertEqual(response.status_code, 200)
        pass

    def test_get_group_with_invalid_lat(self):
        response = self.client.post('/geogossip/get-groups', data={
            'lat': 91.0,
            'lon': 0.0
        })
        self.assertEqual(response.status_code, 400)
        pass

    def test_get_group_with_invalid_lon(self):
        response = self.client.post('/geogossip/get-groups', data={
            'lat': 0.0,
            'lon': 181.0
        })
        self.assertEqual(response.status_code, 400)
        pass

    def test_get_business_with_get_method(self):
        response = self.client.get('/geogossip/get-businesses')
        self.assertEqual(response.status_code, 404)
        pass

    def test_get_business_success(self):
        response = self.client.post('/geogossip/get-businesses', data={
            'lat': 0.0,
            'lon': 0.0
        })
        self.assertEqual(response.status_code, 200)
        pass

    def test_get_business_with_invalid_lat(self):
        response = self.client.post('/geogossip/get-businesses', data={
            'lat': 91.0,
            'lon': 0.0
        })
        self.assertEqual(response.status_code, 400)
        pass

    def test_get_business_with_invalid_lon(self):
        response = self.client.post('/geogossip/get-businesses', data={
            'lat': 0.0,
            'lon': 181.0
        })
        self.assertEqual(response.status_code, 400)
        pass

    def test_non_exists_group_chat(self):
        response = self.client.get('/geogossip/group-chat/1')
        self.assertEqual(response.status_code, 404)
        pass

    def test_non_exists_avatar(self):
        response = self.client.get('/geogossip/avatar/1')
        self.assertEqual(response.status_code, 404)
        pass

    # def test_profile(self):
    #     response = self.client.get('/geogossip/profile/7')
    #     self.assertEqual(response.status_code, 200)
    #     pass

    # test user_id = 30(invalid uid), redirect to home page
    def test_get_profileWithInvalidID_session(self):
        response = self.client.get('/geogossip/profile/30')
        self.assertEqual(response.status_code, 404)
        pass

    #############################################################
    #                   Test @login_required                    #
    #############################################################
    def test_home_session(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)
        pass

    def test_logout_session(self):
        client = Client()
        response = client.get('/geogossip/logout')
        self.assertEqual(response.status_code, 302)
        pass

    def test_get_group_session(self):
        client = Client()
        response = client.get('/geogossip/get-groups')
        self.assertEqual(response.status_code, 302)
        pass

    def test_get_getBusinesses_session(self):
        client = Client()
        response = client.get('/geogossip/get-businesses')
        self.assertEqual(response.status_code, 302)
        pass

    def test_get_createGroup_session(self):
        client = Client()
        response = client.get('/geogossip/create-group')
        self.assertEqual(response.status_code, 302)
        pass

    # test user_id = 7
    def test_get_profile_session(self):
        client = Client()
        response = client.get('/geogossip/profile/7')
        self.assertEqual(response.status_code, 302)
        pass

    def test_get_profileWithoutID_session(self):
        client = Client()
        response = client.get('/geogossip/profile')
        self.assertEqual(response.status_code, 404)
        pass
    pass
