import pytest


class TestAuthentication:

    def test_successful_login(self, client):
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin'
        }, follow_redirects=True)

        assert response.status_code == 200

    def test_failed_login(self, client):
        response = client.post('/login', data={
            'username': 'wrong',
            'password': 'wrong'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'login' in response.data.lower() or b'error' in response.data.lower()