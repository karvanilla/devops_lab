import pytest
from app import db
from models import Competition, Jockey, Horse, Owner
from datetime import date, time


class TestRoutes:

    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_jockeys_list_route(self, client):
        response = client.get('/jockeys')
        assert response.status_code == 200

    def test_horses_list_route(self, client):
        response = client.get('/horses')
        assert response.status_code == 200

    def test_login_page(self, client):
        response = client.get('/login')
        assert response.status_code == 200
        assert b'username' in response.data
        assert b'password' in response.data

    def test_protected_routes_redirect(self, client):
        protected_routes = ['/add_competition', '/add_jockey', '/admin']

        for route in protected_routes:
            response = client.get(route)
            assert response.status_code == 302

    def test_competition_results_route(self, client):
        with client.application.app_context():
            Competition.query.delete()
            db.session.commit()

            competition = Competition(
                date=date(2024, 1, 15),
                time=time(14, 30),
                location='Test Location',
                name='Test Competition'
            )
            db.session.add(competition)
            db.session.commit()

            response = client.get(f'/competition/{competition.id}')
            assert response.status_code == 200

    def test_jockey_competitions_route(self, client):
        with client.application.app_context():
            Jockey.query.delete()
            db.session.commit()

            jockey = Jockey(
                name='Test Jockey',
                address='Test Address',
                age=25,
                rating=4.0
            )
            db.session.add(jockey)
            db.session.commit()

            response = client.get(f'/jockey/{jockey.id}')
            assert response.status_code == 200