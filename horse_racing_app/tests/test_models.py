import pytest
from app import db
from models import Owner, Horse, Jockey, Competition, Result, User, Role
from datetime import date, time


class TestModels:

    def test_owner_creation(self, client):
        with client.application.app_context():
            Owner.query.delete()
            db.session.commit()

            owner = Owner(
                name='John Doe',
                address='Moscow',
                phone='+79991234567'
            )
            db.session.add(owner)
            db.session.commit()

            saved_owner = Owner.query.filter_by(name='John Doe').first()
            assert saved_owner is not None
            assert saved_owner.name == 'John Doe'
            assert saved_owner.phone == '+79991234567'

    def test_horse_creation(self, client):
        with client.application.app_context():
            Horse.query.delete()
            Owner.query.delete()
            db.session.commit()

            owner = Owner(name='Test Owner', address='Address', phone='123')
            db.session.add(owner)
            db.session.commit()

            horse = Horse(
                name='Bucephalus',
                gender='male',
                age=5,
                owner_id=owner.id
            )
            db.session.add(horse)
            db.session.commit()

            saved_horse = Horse.query.filter_by(name='Bucephalus').first()
            assert saved_horse is not None
            assert saved_horse.name == 'Bucephalus'
            assert saved_horse.gender == 'male'
            assert saved_horse.owner_id == owner.id

    def test_jockey_creation(self, client):
        with client.application.app_context():
            Jockey.query.delete()
            db.session.commit()

            jockey = Jockey(
                name='Peter Smith',
                address='Saint Petersburg',
                age=25,
                rating=4.5
            )
            db.session.add(jockey)
            db.session.commit()

            saved_jockey = Jockey.query.filter_by(name='Peter Smith').first()
            assert saved_jockey is not None
            assert saved_jockey.name == 'Peter Smith'
            assert saved_jockey.rating == 4.5

    def test_user_password(self, client):
        with client.application.app_context():
            user = User(username='testuser')
            user.set_password('correct_password')
            db.session.add(user)
            db.session.commit()

            saved_user = User.query.filter_by(username='testuser').first()
            assert saved_user.check_password('correct_password')
            assert not saved_user.check_password('wrong_password')

    def test_competition_creation(self, client):
        with client.application.app_context():
            Competition.query.delete()
            db.session.commit()

            competition = Competition(
                date=date(2024, 1, 15),
                time=time(14, 30),
                location='Moscow Stadium',
                name='Champions Cup'
            )
            db.session.add(competition)
            db.session.commit()

            saved_competition = Competition.query.filter_by(name='Champions Cup').first()
            assert saved_competition is not None
            assert saved_competition.name == 'Champions Cup'
            assert saved_competition.location == 'Moscow Stadium'