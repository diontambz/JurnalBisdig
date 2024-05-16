from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask_login import UserMixin
from database import db 
from flask import render_template, redirect, url_for, request, flash
from forms import ArticleForm
from flask import session
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
application = app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = b'\x81A\xc3]\xd0yV\r\x988\x1aS\x9a\x84\x8b\xb0\xc2\x9b\x0biAw\xf4>'
db.init_app(app)
login_manager = LoginManager(app)


# Definisikan model User untuk autentikasi
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

# Definisikan model Bookmark untuk menyimpan bookmark artikel
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Bookmark %r>' % self.id

# Fungsi untuk memuat user dari database
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Fungsi preprocessing teks
# Optimisasi Preprocessing dengan spaCy
nlp = spacy.load("en_core_web_sm")
def preprocess_text(text):
    # Kode optimasi preprocessing menggunakan spaCy
    text = str(text).lower()
    doc = nlp(text)
    processed_text = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
    return processed_text

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = ''
    recommended_articles_dicts = []
    search_performed = False

    if request.method == 'POST':
        search_performed = True
        keyword = request.form['keyword']
        data = pd.read_csv("datasetbisdig.csv")
        data.columns = [col.lower() for col in data.columns]

        if 'title' in data.columns and 'source title' in data.columns and 'abstract' in data.columns and 'author keywords' in data.columns:
            data['processed_text'] = (data['title'] + ' ' + data['source title']+ ' ' + data['abstract']+ ' ' + data['author keywords']).apply(preprocess_text)
        else:
            return jsonify({'error': 'Kolom yang diperlukan ("title", "source titile", "abstract", "author keywords") tidak ditemukan dalam data.'}), 400

        #Preproccesing Keyword
        processed_keyword = preprocess_text(keyword)
        #Menggabungkan Data preproccesing keduanya kedalam list 
        all_texts = data['processed_text'].tolist() + [processed_keyword]
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        # Mengambil baris akhir
        keyword_vector = tfidf_matrix[-1]
        # Mengambil semua baris kecuali baris terakhir (keyword)
        article_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(keyword_vector, article_vectors)[0]
        data['similarity'] = similarities

        filtered_data = data[data['similarity'] > 0.1]
        recommended_articles = filtered_data.sort_values(by='similarity', ascending=False).head(15)

        recommended_articles_dicts = []
        for index, row in recommended_articles.iterrows():
            if row['similarity'] < 0.0001:
                recommended_articles_dicts.append({
                    'id': row['title'],  # Menggunakan title sebagai id
                    'title': row['title'],
                    'similarity': f"| Similarity: {row[1]['similarity']:.4f}",
                    'year': row['year']
                })
            else:
                recommended_articles_dicts.append({
                    'id': row['title'],  # Menggunakan title sebagai id
                    'title': row['title'],
                    'year': row['year']
                })

    # Periksa apakah ada parameter article_id dalam URL
    article_id = request.args.get('article_id')
    if article_id:
        article = get_article_by_id(article_id)
        if article:
            return render_template('article_detail.html', article=article)
        else:
            flash('Article not found.', 'danger')

    return render_template('index2.html', keyword=keyword, recommended_articles=recommended_articles_dicts, search_performed=search_performed)

# Rute untuk login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

# Rute Untuk Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Initialize error variables
    username_error = None
    email_error = None

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()

        username_error = False
        email_error = False

        if user_by_username:
            username_error = True
        if user_by_email:
            email_error = True

        if not username_error and not email_error:
            user = User(name=name, username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', username_error=username_error, email_error=email_error)

# Rute untuk logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Rute untuk menambahkan bookmark
@app.route('/bookmark/<path:article_id>', methods=['POST'])
@login_required
def add_bookmark(article_id):
    # Logika untuk menambahkan bookmark dengan menggunakan TITLE sebagai article_id
    bookmark = Bookmark(article_id=article_id, user_id=current_user.id)
    db.session.add(bookmark)
    db.session.commit()
    # Mengembalikan respons JSON daripada melakukan pengalihan
    return jsonify({'message': 'Article bookmarked successfully.', 'status': 'success'})

# Rute untuk melihat daftar bookmark
@app.route('/bookmarks')
@login_required
def view_bookmarks():
    bookmarks = current_user.bookmarks.all()
    article_data = []
    for bookmark in bookmarks:
        article = get_article_by_id(bookmark.article_id)
        if article:
            article_data.append(article)
    return render_template('bookmarks.html', bookmarks=article_data)

# Tambahkan rute untuk menghapus bookmark
@app.route('/bookmark/<path:article_id>/delete', methods=['POST'])
@login_required
def delete_bookmark(article_id):
    # Hapus bookmark berdasarkan article_id dan user_id
    bookmark = Bookmark.query.filter_by(article_id=article_id, user_id=current_user.id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        flash('Bookmark removed successfully.', 'success')
    else:
        flash('Bookmark not found.', 'danger')
    return redirect(url_for('view_bookmarks'))

# Rute untuk melihat detail artikel
@app.route('/article/<path:article_id>')
def article_detail(article_id):
    # Ambil data artikel dari database atau sumber data lainnya berdasarkan article_id
    article = get_article_by_id(article_id)
    
    if article:
        return render_template('article_detail.html', article=article)
    else:
        flash('Article not found.', 'danger')
        return redirect(url_for('index'))
        

# Konfigurasi Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dionsandy404@gmail.com'
app.config['MAIL_PASSWORD'] = 'zbpq fpov hhrm jrha'
mail = Mail(app)

# Inisialisasi URLSafeTimedSerializer
app.config['SECRET_KEY'] = os.urandom(24)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Rute untuk forget_password
@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Membuat token untuk reset password
            token = serializer.dumps(email, salt='reset-password')
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Mengirim email dengan tautan reset password
            msg = Message('Reset Password', sender='dionsandy404@gmail.com', recipients=[email])
            msg.body = f'Untuk mereset password Anda, silakan klik tautan berikut: {reset_url}'
            mail.send(msg)
            
            flash('Tautan reset password telah dikirim ke email Anda.', 'success')
            return redirect(url_for('forget_password'))
        else:
            flash('Email tidak ditemukan.', 'danger')
            return redirect(url_for('forget_password'))
    return render_template('forget_password.html')

# Rute untuk reset_password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='reset-password', max_age=3600)
    except SignatureExpired:
        flash('Tautan reset password telah kedaluwarsa.', 'danger')
        return redirect(url_for('forget_password'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()
            flash('Password Anda telah direset.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Terjadi kesalahan saat mereset password.', 'danger')
            return redirect(url_for('reset_password'))
    
    return render_template('reset_password.html', token=token)

# Rute Saran
@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message('Saran', sender=email, recipients=['dionsandy404@gmail.com'])
        msg.body = f"Nama: {name}\nEmail: {email}\n\nPesan:\n{message}"
        mail.send(msg)
        
        flash('Terima kasih atas saran Anda!', 'success')
        return redirect(url_for('suggestions'))
    return render_template('suggestions.html')

# Rute About Us
@app.route('/about')
def about():
    return render_template('about.html')

# Rute Untuk Informasi User Profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        # Perbarui nama pengguna
        if name != current_user.name:
            current_user.name = name
            db.session.commit()
            flash('Nama berhasil diperbarui.', 'success')

        # Perbarui username pengguna
        if username != current_user.username:
            user_with_username = User.query.filter_by(username=username).first()
            if user_with_username:
                flash('Username sudah digunakan oleh pengguna lain.', 'danger')
            else:
                current_user.username = username
                db.session.commit()
                flash('Username berhasil diperbarui.', 'success')

        # Perbarui email pengguna
        if email != current_user.email:
            user_with_email = User.query.filter_by(email=email).first()
            if user_with_email:
                flash('Email sudah digunakan oleh pengguna lain.', 'danger')
            else:
                current_user.email = email
                db.session.commit()
                flash('Email berhasil diperbarui.', 'success')

        # Perbarui password pengguna
        if password:
            current_user.password = password
            db.session.commit()
            flash('Password berhasil diperbarui.', 'success')

    return render_template('profile.html', editing=False)



data = pd.read_csv("datasetbisdig.csv")    
def get_article_by_id(article_id):
    try:
        article = data[data['Title'] == article_id].to_dict('records')[0]
        return article
    except IndexError:
        return None
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #app.run(debug=True) 