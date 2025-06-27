from rest_framework.reverse import reverse
from django.utils.http import urlencode
from drones import views
from drones.models import DroneCategory, Pilot
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

VERSION = 'v1:'

class DroneCategoryTests(APITestCase):



    def post_drone_category(self, name):
        url = reverse(VERSION + views.DroneCategoryList.name)
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_drone_category(self):
        new_drone_category_name = 'Hexacopter'
        response = self.post_drone_category(new_drone_category_name)
        print('nPK {0}n'.format(DroneCategory.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count() == 1
        assert DroneCategory.objects.get().name == new_drone_category_name

    def test_post_existing_drone_category_name(self):
        # url = reverse(views.DroneCategoryList.name)
        new_drone_category_name = 'Duplicate Copter'
        # data = {'name': new_drone_category_name}
        response1 = self.post_drone_category(new_drone_category_name)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_drone_category_by_name(self):
        drone_category_name1 = 'Hexacopter'
        self.post_drone_category(drone_category_name1)
        drone_category_name2 = 'Octocopter'
        self.post_drone_category(drone_category_name2)
        filter_by_name = {'name': drone_category_name1}
        url = '{0}?{1}'.format(reverse(VERSION + views.DroneCategoryList.name), urlencode(filter_by_name))
        print(url)
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == drone_category_name1

    def test_get_drone_categories_collection(self):
        new_drone_category_name = 'Super Copter'
        self.post_drone_category(new_drone_category_name)
        url = reverse(VERSION + views.DroneCategoryList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == new_drone_category_name

    def test_update_drone_category(self):
        drone_category_name = 'Cat Init Name'
        response = self.post_drone_category(drone_category_name)
        url = reverse(VERSION + views.DroneCategoryDetail.name, {response.data['pk']})
        update_drone_category_name = 'Updated Name'
        data = {'name': update_drone_category_name}
        patch_response = self.client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == update_drone_category_name

    def test_get_drone_category(self):
        drone_category_name = 'Easy to retrieve'
        response = self.post_drone_category(drone_category_name)
        url = reverse(VERSION + views.DroneCategoryDetail.name, {response.data['pk']})
        get_response = self.client.get(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == drone_category_name


class PilotTEsts(APITestCase):
    def post_pilot(self, name, gender, races_count):
        url = reverse(VERSION + views.PilotList.name)
        data = {
            'name': name,
            'gender': gender,
            'races_count': races_count
        }
        response = self.client.post(url, data, forat='json')
        return response

    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD'
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token.key))

    def test_post_and_get_pilot(self):
        self.create_user_and_set_token_credentials()
        new_pilot_name = 'Gaston'
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 5
        response = self.post_pilot(
            new_pilot_name,
            new_pilot_gender,
            new_pilot_races_count
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count() == 1
        saved_pilot = Pilot.objects.get()
        assert saved_pilot.name == new_pilot_name
        assert saved_pilot.gender == new_pilot_gender
        assert saved_pilot.races_count == new_pilot_races_count
        url = reverse(VERSION + views.PilotDetail.name, {saved_pilot.pk})
        authorized_get_response = self.client.get(url, format='json')
        assert authorized_get_response.status_code == status.HTTP_200_OK
        assert authorized_get_response.data['name'] == new_pilot_name
        self.client.credentials()
        unauthorized_get_response = self.client.get(url, format='json')
        assert unauthorized_get_response.status_code == status.HTTP_401_UNAUTHORIZED
