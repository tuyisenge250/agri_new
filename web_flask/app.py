
import sys
sys.path.append('/home/benjamin/agrinew')
import os
from werkzeug.utils import secure_filename
from models import storage
from models.base_models import Base_model
from models.user import User
from models.blogs import Blog
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify,session
from flask_login import LoginManager
from models.product import Product

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get('users', user_id)

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


    return render_template('login.html')
@app.route('/')
def hello_world():
    return render_template('index.html')

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
            blog_dict['image_profile'] = url_for('static' , filename=user.image)

        blog_list.append(blog_dict)

    return render_template('mark.html', blogs=blog_list)

@app.route('/create', methods=('GET', 'POST'))
def createlogin():
    if request.method == 'POST':
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            image = request.files['image']
            username = request.form['username']
            my_user = User()
            my_user.first_name = first_name
            my_user.last_name = last_name
            my_user.email = email
            my_user.password = password
            my_user.username = username
            if image and image.filename != "":
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                my_user.image = os.path.join('images', filename)
            my_user.save()
            return redirect('login')
    return render_template('create.html')

@app.route('/fetchat')
def fetching():
    users = storage.all(User).values()
    print(users)
    user_list = []

    for user in users:
        user_dict = user.to_dict()
        if user.image:
            user_dict['image'] = url_for('static', filename=user.image)
        user_list.append(user_dict)
    print(user_list)
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
        my_blog.save()
        flash("Blog post saved successfully")
        return redirect(url_for('profile', user_id=user_id))

    return render_template('profile.html', user_id=user_id)

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
        product.save()
    return render_template('product.html')
@app.route('/resource')
def resource():
    return render_template('resource.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)
