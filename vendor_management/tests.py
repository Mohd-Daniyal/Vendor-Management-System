from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from rest_framework import status
from .models import Vendor, PurchaseOrder
import json


class VendorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='password')
        self.access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        data = {
            'name': 'Gada Electronics',
            'contact_details': '9090456789',
            'address': 'Gokuldham',
            'on_time_delivery_rate': 0.0,
            'quality_rating_avg': 0.0,
            'average_response_time': 0.0,
            'fulfillment_rate': 0.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vendor(self):
        vendor = Vendor.objects.create(name='Gada Electronics', contact_details='9090456789', address='Gokuldham',
                                       on_time_delivery_rate=0.0, quality_rating_avg=0.0, average_response_time=0.0,
                                       fulfillment_rate=0.0)
        url = reverse('vendor-retrieve', kwargs={'vendor_id': vendor.vendor_code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Gada Electronics')

    def test_create_vendor_missing_fields(self):
        url = reverse('vendor-list-create')
        data = {
            'name': 'Bhide Papad',
            'contact_details': '9123456789'
            # Missing 'address' field
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PurchaseOrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_create_purchase_order(self):
        vendor = Vendor.objects.create(name='Gada Electronics', contact_details='9090456789', address='Gokuldham',
                                       on_time_delivery_rate=0.0, quality_rating_avg=0.0, average_response_time=0.0,
                                       fulfillment_rate=0.0)
        url = reverse('purchase-order-list')
        data = {
            'vendor': vendor.vendor_code, 
            'order_date': '2024-04-15T12:00:00Z',
            'actual_delivery_date': '2024-04-23T12:00:00Z',
            'expected_delivery_date': '2024-04-21T12:00:00Z',
            'items': json.dumps([{"item_id": 101, "description": "Mobile Phone", "quantity": 5},
                                 {"item_id": 102, "description": "TV", "quantity": 5}]),
            'quantity': 10,
            'status': 'pending',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_purchase_order(self):
        vendor = Vendor.objects.create(name='Gada Electronics', contact_details='9090456789', address='Gokuldham',
                                       on_time_delivery_rate=0.0, quality_rating_avg=0.0, average_response_time=0.0,
                                       fulfillment_rate=0.0)
        po = PurchaseOrder.objects.create(vendor=vendor, order_date='2024-04-15T12:00:00Z',
                                          actual_delivery_date='2024-04-23T12:00:00Z',
                                          expected_delivery_date='2024-04-21T12:00:00Z', items=[], quantity=10,
                                          status='pending')
        url = reverse('po-retrieve', kwargs={'po_number': po.po_number})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pending')

    def test_create_purchase_order_invalid_data(self):
        vendor = Vendor.objects.create(name='Gada Electronics', contact_details='9090456789', address='Gokuldham',
                                       on_time_delivery_rate=0.0, quality_rating_avg=0.0, average_response_time=0.0,
                                       fulfillment_rate=0.0)
        url = reverse('purchase-order-list')
        data = {
            'vendor': vendor.vendor_code, 
            'order_date': '2024-04-13T12:00:00Z',
            'actual_delivery_date': '2024-04-05T12:00:00Z',
            'expected_delivery_date': '2024-04-15T12:00:00Z',
            'quantity': 10,
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class VendorPerformanceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_get_vendor_performance(self):
        vendor = Vendor.objects.create(name='Gada Electronics', contact_details='9090456789', address='Gokuldham',
                                       on_time_delivery_rate=84.0, quality_rating_avg=3.8, average_response_time=25.0,
                                       fulfillment_rate=88.0)
        url = reverse('vendor-performance', kwargs={'vendor_id': vendor.vendor_code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 84.0)
        self.assertEqual(response.data['quality_rating_avg'], 3.8)
        self.assertEqual(response.data['average_response_time'], 25.0)
        self.assertEqual(response.data['fulfillment_rate'], 88.0)

    def test_get_vendor_performance_invalid_vendor(self):
        url = reverse('vendor-performance', kwargs={'vendor_id': 'invalid_vendor_id'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_vendor_performance_no_data(self):
        vendor = Vendor.objects.create(name='Gada Electronics', contact_details='9090456789', address='Gokuldham',
                                       on_time_delivery_rate=0, quality_rating_avg=0, average_response_time=0,
                                       fulfillment_rate=0)
        url = reverse('vendor-performance', kwargs={'vendor_id': vendor.vendor_code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 0)
        self.assertEqual(response.data['quality_rating_avg'], 0)
        self.assertEqual(response.data['average_response_time'], 0)
        self.assertEqual(response.data['fulfillment_rate'], 0)

