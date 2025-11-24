import unittest
from app import app, repository


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        # Clear the repository before each test
        repository.clear()

    def tearDown(self):
        # Clear the repository after each test
        repository.clear()

    def test_index_shows_empty_warehouses(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ohtuvarasto', response.data)
        self.assertIn(b'Ei varastoja', response.data)

    def test_create_warehouse_get(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Luo uusi varasto', response.data)

    def test_create_warehouse_post(self):
        response = self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Testivarasto', response.data)
        self.assertEqual(len(repository.get_all()), 1)

    def test_index_shows_created_warehouse(self):
        self.client.post('/create', data={
            'nimi': 'Olutvarasto',
            'tilavuus': '50',
            'alku_saldo': '10'
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Olutvarasto', response.data)
        self.assertIn(b'50', response.data)
        self.assertIn(b'10', response.data)

    def test_edit_warehouse_get(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '20'
        })
        warehouse_id = list(repository.get_all().keys())[0]
        response = self.client.get(f'/edit/{warehouse_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Muokkaa varastoa', response.data)
        self.assertIn(b'Testivarasto', response.data)

    def test_edit_warehouse_post(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '20'
        })
        warehouse_id = list(repository.get_all().keys())[0]
        response = self.client.post(f'/edit/{warehouse_id}', data={
            'nimi': 'Muokattu varasto',
            'tilavuus': '150',
            'alku_saldo': '30'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Muokattu varasto', response.data)
        warehouse = repository.get_by_id(warehouse_id)
        self.assertEqual(warehouse.nimi, 'Muokattu varasto')
        self.assertEqual(warehouse.varasto.tilavuus, 150)

    def test_add_content_get(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '20'
        })
        warehouse_id = list(repository.get_all().keys())[0]
        response = self.client.get(f'/add/{warehouse_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'varastoon', response.data)

    def test_add_content_post(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '20'
        })
        warehouse_id = list(repository.get_all().keys())[0]
        response = self.client.post(f'/add/{warehouse_id}', data={
            'maara': '10'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        warehouse = repository.get_by_id(warehouse_id)
        self.assertEqual(warehouse.varasto.saldo, 30)

    def test_delete_warehouse(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '20'
        })
        warehouse_id = list(repository.get_all().keys())[0]
        self.assertEqual(len(repository.get_all()), 1)
        
        response = self.client.post(f'/delete/{warehouse_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(repository.get_all()), 0)

    def test_edit_nonexistent_warehouse_redirects(self):
        response = self.client.get('/edit/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ohtuvarasto', response.data)

    def test_add_to_nonexistent_warehouse_redirects(self):
        response = self.client.get('/add/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ohtuvarasto', response.data)

    def test_delete_nonexistent_warehouse_redirects(self):
        response = self.client.post('/delete/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ohtuvarasto', response.data)
