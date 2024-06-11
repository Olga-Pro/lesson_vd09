from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcript
from app.forms import RegistrationForm, LoginForm, EditProfileForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcript.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcript.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = EditProfileForm()
    if form.validate_on_submit():
        change_made = False

        if current_user.username != form.username.data:
            current_user.username = form.username.data
            change_made = True
        if current_user.email != form.email.data:
            current_user.email = form.email.data
            change_made = True

        if form.password.data:
            # Проверяем, изменился ли пароль, до хэширования
            if not bcript.check_password_hash(current_user.password, form.password.data):
                hashed_password = bcript.generate_password_hash(form.password.data).decode('utf-8')
                if current_user.password != hashed_password:
                    current_user.password = hashed_password
                    change_made = True

        if change_made:
            db.session.commit()
            flash('Данные аккаунта успешно изменены!', 'success')
        else:
            flash('Данные не изменены!', 'info')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', form=form)



