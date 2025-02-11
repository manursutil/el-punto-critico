from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from . import db
from .models import Post
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/')
def home():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('home.html', posts=posts)

@views.route('article/<int:id>')
def article(id):
    post = Post.query.get_or_404(id)
    return render_template('article.html', post=post)


UPLOAD_FOLDER = 'website/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')
        
        from .models import Post
        if title and content:
            image_filename = None
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, image_filename))
            
            
            new_post = Post(
                content=content, 
                title=title, 
                image_filename=image_filename, 
                admin_id=current_user.id
                )
            db.session.add(new_post)
            db.session.commit()
            flash('Post added!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Please fill in all fields!', category='error')
            
    return render_template('add.html')

@views.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if post.admin_id != current_user.id:
        flash('You do not have permission to edit this post.', category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        if 'delete' in request.form:
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted!', category='success')
            return redirect(url_for('views.home'))
    
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
            post.image_filename = image_filename
        
        db.session.commit()
        flash('Post updated!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template('edit.html', post=post)