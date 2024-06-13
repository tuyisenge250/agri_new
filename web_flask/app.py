import sys
sys.path.append('/home/benjamin/agrinew')
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import storage
from models.user import User
from models.blogs import Blog
from models.news_letter import News
from models.product import Product
from models.resource import Resource


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://tuyisenge:tuyisenge2003@localhost/agrinew'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)

# Define routes and views
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = storage.all(User).values()
        user = next((u for u in users if u.username == username and u.password == password), None)

        if user:
            session['user_id'] = user.id
            flash('Login successful')
            return redirect(url_for('profile', user_id=user.id))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
def landing():
    return render_template('landingpage.html')

@app.route('/market')
def market():
    blogs = storage.all(Blog).values()
    blog_list = []
    for blog in blogs:
        blog_dict = blog.to_dict()
        if blog.image:
            blog_dict['image'] = url_for('static', filename=blog.image)

        user = next((u for u in storage.all(User).values() if u.id == blog.user_id), None)
        if user:
            blog_dict['username'] = user.username
            blog_dict['first_name'] = user.first_name
            blog_dict['second_name'] = user.last_name
            blog_dict['image_profile'] = url_for('static', filename=user.image)
        blog_list.append(blog_dict)

    news = storage.all(News).values()
    new_market = []
    for new in news:
        new_dict = new.to_dict()
        print(new_dict)
        new_dict['image'] = url_for('static', filename='images/agri_market_Eac.png')
        if new.status == 'market':
            new_market.append(new_dict)

    products = storage.all(Product).values()
    product_market = []
    for product in products:
        product_dict = product.to_dict()
        if product.image:
            product_dict['image'] = url_for('static', filename=product.image)
        product_market.append(product_dict)

    return render_template('mark.html', blogs=blog_list, new=new_market, product=product_market)

@app.route('/create', methods=('GET', 'POST'))
def createlogin():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        image = request.files['image']
        username = request.form['username']
        description = request.form['description']
        
        my_user = User()
        my_user.first_name = first_name
        my_user.last_name = last_name
        my_user.email = email
        my_user.password = password
        my_user.username = username
        my_user.description = description
        
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            my_user.image = os.path.join('images', filename)
        
        storage.new(my_user)
        storage.save()
        
        return redirect(url_for('login'))
    
    return render_template('create.html')

@app.route('/addnews', methods=('GET', 'POST'))
def addnew():
    my_news = News()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        status = request.form['status']
        image = request.files['image']
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            my_news.image = os.path.join('images', filename)
        my_news.status = status
        my_news.content = content
        my_news.title = title
        storage.new(my_news)
        storage.save()
    return render_template('addnews.html')

@app.route('/fetchat')
def fetching():
    users = storage.all(User).values()
    user_list = []

    for user in users:
        user_dict = user.to_dict()
        if user.image:
            user_dict['image'] = url_for('static', filename=user.image)
        user_list.append(user_dict)
    return render_template('create.html', users=user_list)

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in first")
        return redirect(url_for('login'))
    
    user = storage.get(User, user_id)
    if user.image:
        user.image = url_for('static', filename=user.image) if user.image else None
    
    if request.method == 'POST':
        blog = request.form['blogs']
        image = request.files['image']
        my_blog = Blog()

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            my_blog.image = os.path.join('images', filename)
        
        my_blog.blog = blog
        my_blog.user_id = user_id
        storage.new(my_blog)
        storage.save()
        
        flash("Blog post saved successfully")
        return redirect(url_for('profile', user_id=user_id))

    return render_template('profile.html', user_id=user_id, user=user)

@app.route('/createresource', methods=['GET', 'POST'])
def createresource():
    product = storage.all(Product).values()
    resource = Resource()
    if request.method == 'POST':
        crops = request.form['crops']
        content = request.form['content']
        crop = next((p for p in product if p.name == crops), None)
        if not crop:
            flash('Create this crop first.')
            return redirect(url_for('creatproduct'))
        else:
            resource.crops = crop.id
            resource.content = content
            storage.new(resource)
            storage.save()
            flash('Your crop content has been set successfully.')
            return redirect(url_for('market'))
    return render_template('createresource.html')

@app.route('/createproduct', methods=['POST', 'GET'])
def creatproduct():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        price = request.form['price']
        discription = request.form['discription']
        image = request.files['image']
        product = Product()
        if image and image.filename != "":
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                product.image = os.path.join('images', filename)
        product.name = name
        product.discription = discription
        product.price = price
        product.type = type
        storage.new(product)
        storage.save()
    return render_template('product.html')

@app.route('/resource')
def resource():
    return render_template('resource.html')

@app.route('/adminstration')
def adminstration():
    return render_template('adminstration.html')

@app.route('/news')
def news():
    news = storage.all(News).values()
    news_letter = []
    for new in news:
        news_dict = new.to_dict()
        if new.image:
            news_dict['image'] = url_for('static', filename=new.image)
        news_letter.append(news_dict)
    
    return render_template('news.html', news=news_letter)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
