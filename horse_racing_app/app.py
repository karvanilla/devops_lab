from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Owner, Horse, Jockey, Competition, Result, Role, User
from hooks import register_error_handlers
from datetime import datetime
from config import Config
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from decorators import role_required

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Регистрация обработчиков ошибок
register_error_handlers(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    competitions = Competition.query.all()
    jockeys_count = Jockey.query.count()
    horses_count = Horse.query.count()
    return render_template('index.html',
                          competitions=competitions,
                          jockeys_count=jockeys_count,
                          horses_count=horses_count)

@app.route('/add_competition', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_competition():
    if request.method == 'POST':
        try:
            competition = Competition(
                date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
                time=datetime.strptime(request.form['time'], '%H:%M').time(),
                location=request.form['location'],
                name=request.form['name']
            )
            db.session.add(competition)
            db.session.commit()
            flash('Состязание успешно добавлено', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении состязания: {str(e)}', 'error')
    
    return render_template('add_competition.html')

@app.route('/add_jockey', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_jockey():
    if request.method == 'POST':
        try:
            jockey = Jockey(
                name=request.form['name'],
                address=request.form['address'],
                age=int(request.form['age']),
                rating=float(request.form['rating'])
            )
            db.session.add(jockey)
            db.session.commit()
            flash('Жокей успешно добавлен', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении жокея: {str(e)}', 'error')
    
    return render_template('add_jockey.html')

@app.route('/add_horse', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_horse():
    owners = Owner.query.all()
    
    if request.method == 'POST':
        try:
            horse = Horse(
                name=request.form['name'],
                gender=request.form['gender'],
                age=int(request.form['age']),
                owner_id=int(request.form['owner_id'])
            )
            db.session.add(horse)
            db.session.commit()
            flash('Лошадь успешно добавлена', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении лошади: {str(e)}', 'error')
    
    return render_template('add_horse.html', owners=owners)

@app.route('/add_owner', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_owner():
    if request.method == 'POST':
        try:
            owner = Owner(
                name=request.form['name'],
                address=request.form['address'],
                phone=request.form['phone']
            )
            db.session.add(owner)
            db.session.commit()
            flash('Владелец успешно добавлен', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении владельца: {str(e)}', 'error')
    
    return render_template('add_owner.html')

@app.route('/add_result', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_result():
    competitions = Competition.query.all()
    jockeys = Jockey.query.all()
    horses = Horse.query.all()
    
    if request.method == 'POST':
        try:
            result = Result(
                competition_id=int(request.form['competition_id']),
                jockey_id=int(request.form['jockey_id']),
                horse_id=int(request.form['horse_id']),
                position=int(request.form['position']),
                time=request.form['time']
            )
            db.session.add(result)
            db.session.commit()
            flash('Результат успешно добавлен', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении результата: {str(e)}', 'error')
    
    return render_template('add_result.html', competitions=competitions, jockeys=jockeys, horses=horses)

@app.route('/competition/<int:competition_id>')
def competition_results(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    results = Result.query.filter_by(competition_id=competition_id).all()
    return render_template('competition_results.html', competition=competition, results=results)

@app.route('/jockey/<int:jockey_id>')
def jockey_competitions(jockey_id):
    jockey = Jockey.query.get_or_404(jockey_id)
    results = Result.query.filter_by(jockey_id=jockey_id).all()
    return render_template('jockey_competitions.html', jockey=jockey, results=results)

@app.route('/horse/<int:horse_id>')
def horse_competitions(horse_id):
    horse = Horse.query.get_or_404(horse_id)
    results = Result.query.filter_by(horse_id=horse_id).all()
    return render_template('horse_competitions.html', horse=horse, results=results)

@app.route('/jockeys')
def jockeys_list():
    jockeys = Jockey.query.all()
    return render_template('jockeys_list.html', jockeys=jockeys)

@app.route('/horses')
def horses_list():
    horses = Horse.query.all()
    return render_template('horses_list.html', horses=horses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Успешный вход', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    return 'Панель администратора - доступ разрешён'

def init_database():
    """Инициализация базы данных с созданием ролей и пользователей"""
    with app.app_context():
        db.create_all()

        # Создаем роли если их нет
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)

        member_role = Role.query.filter_by(name='member').first()
        if not member_role:
            member_role = Role(name='member')
            db.session.add(member_role)
        
        db.session.commit()

        # Создаем пользователя admin если его нет
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin')
            admin_user.set_password('admin')
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)

        # Создаем пользователя member если его нет
        member_user = User.query.filter_by(username='member').first()
        if not member_user:
            member_user = User(username='member')
            member_user.set_password('member')
            member_user.roles.append(member_role)
            db.session.add(member_user)
        
        db.session.commit()

if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
