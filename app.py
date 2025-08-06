from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Entry
from forms import LoginForm, EntryForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///debit_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='nihar').first():
        admin_user = User(
            username='nihar',
            password=generate_password_hash('sinu1234'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(
            date=str(form.date.data),
            price=form.price.data,
            payment_method=form.payment_method.data,
            payment_reason=form.payment_reason.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash("Entry added successfully!", "success")
        return redirect(url_for('entries'))
    return render_template('index.html', form=form)

@app.route('/entries')
@login_required
def entries():
    if current_user.role == 'admin':
        entries = Entry.query.all()
    else:
        entries = Entry.query.filter_by(user_id=current_user.id).all()
    return render_template('entries.html', entries=entries)

@app.route('/entry/update/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def update_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if current_user.role != 'admin' and entry.user_id != current_user.id:
        abort(403)
    form = EntryForm(obj=entry)
    if request.method == 'GET':
        try:
            if entry.date:
                form.date.data = datetime.strptime(entry.date, '%Y-%m-%d').date()
        except Exception:
            form.date.data = None
    if form.validate_on_submit():
        entry.date = form.date.data.strftime('%Y-%m-%d')
        entry.price = form.price.data
        entry.payment_method = form.payment_method.data
        entry.payment_reason = form.payment_reason.data
        db.session.commit()
        flash('Entry updated successfully!', 'success')
        return redirect(url_for('entries'))
    return render_template('update_entry.html', form=form, entry=entry)

@app.route('/entry/delete/<int:entry_id>', methods=['POST', 'GET'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if current_user.role != 'admin' and entry.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        db.session.delete(entry)
        db.session.commit()
        flash("Entry deleted successfully!", "success")
        return redirect(url_for('entries'))
    return render_template('confirm_delete.html', entry=entry)

if __name__ == '__main__':
    app.run(debug=True)
