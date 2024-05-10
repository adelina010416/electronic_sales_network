from rest_framework import status
from rest_framework.test import APITestCase

from traders.models import NetworkItem
from users.models import User


class NetworkItemAPITestCase(APITestCase):

    def setUp(self):
        self.factory = NetworkItem.objects.create(
            name='тестовый завод',
            type='factory',
            email='test_factory_@mail.ru',
            country='still_test',
            city='test_again',
            street='some_street',
            house='some_house')
        self.retail_network = NetworkItem.objects.create(
            name='тестовая розничная сеть',
            type='retail network',
            email='test_retail_network_@mail.ru',
            country='still_test',
            city='test_again',
            street='some_street',
            house='some_house',
            supplier=self.factory)
        self.ie = NetworkItem.objects.create(
            name='тестовое ИП',
            type='individual entrepreneur',
            email='test_ie_@mail.ru',
            country='still_test',
            city='test_again',
            street='some_street',
            house='some_house',
            supplier=self.retail_network)
        self.user = User.objects.create(
            email='testuser@mail.ru', is_active=True, is_staff=False)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_items_list(self):
        response = self.client.get('/trades/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_items_detail(self):
        response = self.client.get('/trades/items/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), self.factory.name)

    def test_network_create(self):
        data = {
            "manufacturer": self.factory.name,
            "distributor": self.retail_network.name,
            "consumer": self.ie.name,
            "name": "test"
        }
        response = self.client.post('/trades/networks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del data['distributor']
        response = self.client.post('/trades/networks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': [
                             'Указанный потребитель не является '
                             'потребителем указанного производителя!']})

        data['consumer'] = self.retail_network.name
        response = self.client.post('/trades/networks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['distributor'] = self.retail_network.name
        response = self.client.post('/trades/networks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': [
                             'Указанный потребитель не является '
                             'потребителем указанного распространителя!']})

        data['distributor'] = self.ie.name
        response = self.client.post('/trades/networks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': [
                             'Указанный распространитель не является '
                             'потребителем указанного производителя!']})
