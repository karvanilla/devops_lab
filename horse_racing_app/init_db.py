from config import Config
from models import db, Owner, Horse, Jockey, Competition, Result, Role, User
from datetime import datetime, time
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def init_database():
    with app.app_context():
        # Создание таблиц
        db.create_all()

        # Проверяем, есть ли уже данные в базе
        if Owner.query.count() == 0:
            print("Добавление тестовых данных...")
            
            # Добавление тестовых данных
            # Владельцы
            owner1 = Owner(name="Иван Петров", address="ул. Ленина, 10", phone="+7-123-456-7890")
            owner2 = Owner(name="Мария Сидорова", address="пр. Победы, 25", phone="+7-987-654-3210")
            db.session.add(owner1)
            db.session.add(owner2)
            db.session.commit()

            # Лошади
            horse1 = Horse(name="Буцефал", gender="male", age=5, owner_id=1)
            horse2 = Horse(name="Звезда", gender="female", age=4, owner_id=1)
            horse3 = Horse(name="Ветер", gender="male", age=6, owner_id=2)
            db.session.add(horse1)
            db.session.add(horse2)
            db.session.add(horse3)

            # Жокеи
            jockey1 = Jockey(name="Алексей Иванов", address="ул. Спортивная, 15", age=25, rating=8.5)
            jockey2 = Jockey(name="Екатерина Смирнова", address="пр. Мира, 30", age=28, rating=9.2)
            db.session.add(jockey1)
            db.session.add(jockey2)

            # Состязания
            competition1 = Competition(date=datetime(2023, 10, 15).date(), 
                                      time=time(14, 30), 
                                      location="Центральный ипподром", 
                                      name="Кубок осени")
            competition2 = Competition(date=datetime(2023, 11, 5).date(), 
                                      time=time(13, 0), 
                                      location="Северный ипподром", 
                                      name="Гран-при севера")
            db.session.add(competition1)
            db.session.add(competition2)

            # Результаты
            result1 = Result(competition_id=1, jockey_id=1, horse_id=1, position=1, time="2:15.30")
            result2 = Result(competition_id=1, jockey_id=2, horse_id=2, position=2, time="2:16.45")
            result3 = Result(competition_id=2, jockey_id=1, horse_id=3, position=1, time="2:10.20")
            result4 = Result(competition_id=2, jockey_id=2, horse_id=1, position=3, time="2:12.80")
            db.session.add(result1)
            db.session.add(result2)
            db.session.add(result3)
            db.session.add(result4)

            # Роли и пользователи
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                admin_role = Role(name='admin')
                db.session.add(admin_role)

            member_role = Role.query.filter_by(name='member').first()
            if not member_role:
                member_role = Role(name='member')
                db.session.add(member_role)
            
            db.session.commit()

            # Пользователи
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(username='admin')
                admin_user.set_password('admin')
                admin_user.roles.append(admin_role)
                db.session.add(admin_user)

            member_user = User.query.filter_by(username='member').first()
            if not member_user:
                member_user = User(username='member')
                member_user.set_password('member')
                member_user.roles.append(member_role)
                db.session.add(member_user)

            db.session.commit()
            print("База данных инициализирована с тестовыми данными!")
        else:
            print("В базе данных уже есть данные, инициализация не требуется.")

if __name__ == '__main__':
    init_database()