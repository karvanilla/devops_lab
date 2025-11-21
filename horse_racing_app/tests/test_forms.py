import pytest
from app import db
from models import Owner, Horse, Jockey, Competition
from datetime import date, time


class TestForms:

    def test_add_owner_post(self, auth_client):
        with auth_client.application.app_context():
            Owner.query.delete()
            db.session.commit()

        response = auth_client.post('/add_owner', data={
            'name': 'New Owner',
            'address': 'New Address',
            'phone': '+79998887766'
        }, follow_redirects=True)

        assert response.status_code == 200

        with auth_client.application.app_context():
            owner = Owner.query.filter_by(name='New Owner').first()
            assert owner is not None
            assert owner.phone == '+79998887766'

    def test_add_jockey_post(self, auth_client):
        with auth_client.application.app_context():
            Jockey.query.delete()
            db.session.commit()

        response = auth_client.post('/add_jockey', data={
            'name': 'New Jockey',
            'address': 'Jockey Address',
            'age': '28',
            'rating': '4.7'
        }, follow_redirects=True)

        assert response.status_code == 200

        with auth_client.application.app_context():
            jockey = Jockey.query.filter_by(name='New Jockey').first()
            assert jockey is not None
            assert jockey.rating == 4.7

    def test_add_competition_post(self, auth_client):
        with auth_client.application.app_context():
            Competition.query.delete()
            db.session.commit()

        response = auth_client.post('/add_competition', data={
            'name': 'New Competition',
            'location': 'New Stadium',
            'date': '2024-02-01',
            'time': '15:30'
        }, follow_redirects=True)

        assert response.status_code == 200

        with auth_client.application.app_context():
            competition = Competition.query.filter_by(name='New Competition').first()
            assert competition is not None
            assert competition.location == 'New Stadium'