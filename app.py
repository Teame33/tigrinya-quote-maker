from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)
login_manager.login_view = 'login'

# Forms
class QuoteForm(FlaskForm):
    quote_text = TextAreaField('Quote', validators=[DataRequired()])
    author = StringField('Author')
    submit = SubmitField('Create Quote')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    quotes = db.relationship('Quote', backref='author', lazy=True)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    author_text = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    style_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __init__(self, text, author_text, user_id, style_data):
        self.text = text
        self.author_text = author_text
        self.user_id = user_id
        self.style_data = style_data

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        recent_quotes = Quote.query.filter_by(user_id=current_user.id).order_by(Quote.created_at.desc()).limit(3).all()
    else:
        recent_quotes = []
    return render_template('index.html', quotes=recent_quotes)

@app.route('/create_quote', methods=['GET', 'POST'])
@login_required
def create_quote():
    form = QuoteForm()
    if form.validate_on_submit():
        quote = Quote(
            text=form.quote_text.data,
            author_text=form.author.data,
            user_id=current_user.id,
            style_data=request.form.get('style_data')
        )
        db.session.add(quote)
        db.session.commit()
        flash('Quote created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_quote.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/save_quote', methods=['POST'])
def save_quote():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Please login to save quotes'})
    
    try:
        data = request.get_json()
        
        # Create style data dictionary
        style_data = {
            'font_family': data['font_family'],
            'font_size': data['font_size'],
            'text_color': data['text_color'],
            'background_type': data['background_type'],
            'horizontal_offset': data['horizontal_offset'],
            'vertical_offset': data['vertical_offset'],
            'background_image': data.get('background_image')
        }
        
        # Create new quote
        new_quote = Quote(
            text=data['quote_text'],
            author_text=data['author'],
            user_id=current_user.id,
            style_data=style_data
        )
        
        db.session.add(new_quote)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Quote saved successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Error saving quote: {str(e)}")  # Add debugging output
        return jsonify({'success': False, 'message': str(e)})

@app.route('/my_quotes')
@login_required
def my_quotes():
    quotes = Quote.query.filter_by(user_id=current_user.id).order_by(Quote.created_at.desc()).all()
    return render_template('my_quotes.html', quotes=quotes)

@app.route('/delete_quote/<int:quote_id>', methods=['DELETE', 'POST'])
@login_required
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    if quote.user_id != current_user.id:
        if request.method == 'DELETE':
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        else:
            flash('You are not authorized to delete this quote.', 'error')
            return redirect(url_for('index'))
    
    try:
        db.session.delete(quote)
        db.session.commit()
        if request.method == 'DELETE':
            return jsonify({'success': True})
        else:
            flash('Quote deleted successfully!', 'success')
            return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        if request.method == 'DELETE':
            return jsonify({'success': False, 'message': str(e)})
        else:
            flash('Error deleting quote. Please try again.', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("Database tables created successfully!")
    app.run(debug=True)
