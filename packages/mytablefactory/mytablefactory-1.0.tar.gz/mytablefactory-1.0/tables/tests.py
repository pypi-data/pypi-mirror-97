from django.test import TestCase
from django.test import Client
from .models import Table, Leg, Foot
import pytest

class TablesTest(TestCase):

    def test_create(self):
        c = Client()
        response = c.post('/api/tables/create/', {"name": "Table One"})
        self.assertEqual(response.status_code, 201)
        response = c.post('/api/tables/create/', {"name": "Table Two"})
        self.assertEqual(response.status_code, 201)
        response = c.post('/api/tables/create/', {"name": "Table One"})
        self.assertEqual(response.status_code, 400)
        pass

    def test_list(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/tables/create/', {"name": "Table Two"})
        response = c.get('/api/tables/')
        response_body = response.json()
        self.assertEqual(response.status_code, 200)
        assert response_body["count"] == 2
        pass

    def test_detail(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        response = c.get('/api/tables/1/')
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        assert response_body["name"] == "Table One"
        pass

    def test_update(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        response = c.patch('/api/tables/1/update/', json={"name": "Updated"})
        self.assertEqual(response.status_code, 200)
        pass

    def test_delete(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        response = c.delete('/api/tables/1/delete/', json={})
        self.assertEqual(response.status_code, 204)
        pass


class LegsTest(TestCase):

    def test_create(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        response = c.post('/api/legs/create/', {"table_id": "1"})
        self.assertEqual(response.status_code, 201)
        pass

    def test_list(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/legs/create/', {"table_id": "1"})
        c.post('/api/legs/create/', {"table_id": "1"})
        c.post('/api/legs/create/', {"table_id": "1"})
        response = c.get('/api/legs/')
        response_body = response.json()
        self.assertEqual(response.status_code, 200)
        assert response_body["count"] == 3
        pass

    def test_detail(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/legs/create/', {"table_id": "1"})
        response = c.get('/api/legs/1/')
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        assert response_body["table_id"] == 1
        pass

    def test_update(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/tables/create/', {"name": "Table Two"})
        c.post('/api/legs/create/', {"table_id": "1"})
        response = c.patch('/api/legs/1/update/', json={"table_id": "2"})
        self.assertEqual(response.status_code, 200)
        pass

    def test_delete(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/legs/create/', {"table_id": "1"})
        response = c.delete('/api/legs/1/delete/', json={})
        self.assertEqual(response.status_code, 204)
        pass


class FeetTest(TestCase):
    
    def test_create(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/tables/create/', {"name": "Table Two"})
        c.post('/api/legs/create/', {"table_id": "1"})
        c.post('/api/legs/create/', {"table_id": "2"})
        c.post('/api/legs/create/', {"table_id": "1"})
        response = c.post('/api/feet/create/', { "radius": 3, "legs": [1]})
        self.assertEqual(response.status_code, 201)
        response = c.post('/api/feet/create/', { "radius": 3, "legs": [1, 2]})
        self.assertEqual(response.status_code, 201)
        pass

    def test_list(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/tables/create/', {"name": "Table Two"})
        c.post('/api/legs/create/', {"table_id": "1"})
        c.post('/api/legs/create/', {"table_id": "2"})
        c.post('/api/feet/create/', { "radius": 1, "legs": [1, 2]})
        c.post('/api/feet/create/', { "radius": 2, "legs": [1]})
        c.post('/api/feet/create/', { "radius": 3, "legs": [2]})
        response = c.get('/api/feet/')
        response_body = response.json()
        self.assertEqual(response.status_code, 200)
        assert response_body["count"] == 3
        pass

    def test_detail(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/tables/create/', {"name": "Table Two"})
        c.post('/api/legs/create/', {"table_id": "1"})
        c.post('/api/legs/create/', {"table_id": "2"})
        c.post('/api/feet/create/', { "radius": 1, "legs": [1, 2]})
        response = c.get('/api/feet/1/')
        response_body = response.json()
        self.assertEqual(response.status_code, 200)
        assert len(response_body["legs"]) == 2
        pass

    def test_update(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/tables/create/', {"name": "Table Two"})
        c.post('/api/legs/create/', {"table_id": "1"})
        c.post('/api/legs/create/', {"table_id": "2"})
        c.post('/api/feet/create/', { "radius": 1, "legs": [1]})
        response = c.patch('/api/feet/1/update/', json={"legs": [1, 2]})
        self.assertEqual(response.status_code, 200)
        pass

    def test_delete(self):
        c = Client()
        c.post('/api/tables/create/', {"name": "Table One"})
        c.post('/api/tables/create/', {"name": "Table Two"})
        c.post('/api/legs/create/', {"table_id": "1"})
        c.post('/api/legs/create/', {"table_id": "2"})
        c.post('/api/feet/create/', { "radius": 1, "legs": [1]})
        response = c.delete('/api/feet/1/delete/', json={})
        self.assertEqual(response.status_code, 204)
        pass

