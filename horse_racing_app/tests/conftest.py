import pytest
import os
import tempfile
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db
from models import User, Role


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # Очищаем базу
            db.create_all()

            # Создаем тестовые роли
            admin_role = Role(name='admin')
            member_role = Role(name='member')
            db.session.add(admin_role)
            db.session.add(member_role)

            # Создаем тестовых пользователей
            admin_user = User(username='admin')
            admin_user.set_password('admin')
            admin_user.roles.append(admin_role)

            member_user = User(username='member')
            member_user.set_password('member')
            member_user.roles.append(member_role)

            db.session.add(admin_user)
            db.session.add(member_user)
            db.session.commit()

        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def auth_client(client):
    client.post('/login', data={
        'username': 'admin',
        'password': 'admin'
    })
    return client