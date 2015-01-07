from flask import abort
from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user
from datetime import datetime
from app import app
from app import db
from app import md
from models import Post, Project, User
from forms import LoginForm, NewPostForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', 
		content = md.render(app.config['INTRODUCTION']))

@app.route('/about')
def about():
	return render_template('index.html', 
		content = md.render(app.config['ABOUT']))

@app.route('/projects')
def projects():
	projects = Project.query.order_by(Project.timestamp.desc()).all()
	return render_template('projects.html', entries = projects)

@app.route('/blog')
def blog():
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('blog.html', entries = posts)

@app.route('/projects/<int:pid>')
def view_project(pid):
	entry = Project.query.get_or_404(pid)
	return render_template('entry.html', entry = entry)

@app.route('/blog/<int:pid>')
def view_blog(pid):
	entry = Post.query.get_or_404(pid)
	return render_template('entry.html', entry = entry)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('index'))
		else:
			flash("Invalid username or password")

	return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
	form = NewPostForm()
	if form.validate_on_submit():

		title = form.title.data
		body = form.body.data
		user = User.query.get_or_404(current_user.get_id())	
		
		post = Post(title = title,
			timestamp = datetime.utcnow(),
			author_id = user.id,
			body = body)

		post.body_html = md.render(body)

		db.session.add(post)
		db.session.commit()
		return redirect(url_for('blog'))

	return render_template('new_post.html', form = form)

@app.route('/blog/edit/<int:pid>')
@login_required
def edit_post(pid):
	return "<h1>Not Implemented!</h1>"

@app.route('/blog/delete/<int:pid>')
@login_required
def delete_post(pid):
	post = Post.query.get_or_404(pid)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('blog'))

@app.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
	form = NewPostForm()
	if form.validate_on_submit():

		title = form.title.data
		body = form.body.data
		user = User.query.get_or_404(current_user.get_id())	

		project = Project(title = title,
			timestamp = datetime.utcnow(),
			author_id = user.id,
			body = body)

		project.body_html = md.render(body)

		db.session.add(project)
		db.session.commit()
		return redirect(url_for('projects'))

	return render_template('new_post.html', form = form)

@app.route('/projects/edit/<int:pid>')
@login_required
def edit_project(pid):
	return "<h1>Not Implemented!</h1>"

@app.route('/projects/delete/<int:pid>')
@login_required
def delete_project(pid):
	project = Project.query.get_or_404(pid)
	db.session.delete(project)
	db.session.commit()
	return redirect(url_for('projects'))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500