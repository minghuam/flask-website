from app import app
from app import db, login_manager, md
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

class Permission:
	VIEW = 0x01
	ADMIN = 0xFF

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	default = db.Column(db.Boolean, default = False, index = True)
	permissions = db.Column(db.Integer)

	@staticmethod
	def insert_roles():
		roles = {
			'User': (Permission.VIEW, True),
			'Admin': (Permission.ADMIN, False)
		}

		for r in roles:
			role = Role.query.filter_by(name = r).first()
			if role is None:
				role = Role(name = r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

	def __repr__(self):
		return '<Role(id: {0}, name: {1})>'.format(self.id, self.name)

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@staticmethod
	def insert_admin():
		admin = User.query.filter_by(username = app.config['ADMIN_NAME']).first()
		if admin is None:
			admin = User(username = app.config['ADMIN_NAME'],
				password = app.config['ADMIN_PASSWORD'])
		role = Role.query.filter_by(permissions = Permission.ADMIN).first()
		admin.role_id = role.id
		db.session.add(admin)
		db.session.commit()

	def __repr__(self):
		return '<User(id: {0}, username: {1}, role_id: {2})>'.format(self.id, self.username, self.role_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(256))
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow())
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)

	@staticmethod
	def insert_fake(count = 100):
		from random import seed, randint
		import forgery_py
		seed()
		user_count = User.query.count()
		for i in range(count):
			user = User.query.offset(randint(0, user_count - 1)).first()
			post = Post(title = forgery_py.lorem_ipsum.title(randint(2, 5)),
				timestamp = forgery_py.date.date(True),
				author_id = user.id,
				body = forgery_py.lorem_ipsum.paragraphs())
			post.body_html = md.render(post.body)
			db.session.add(post)
		db.session.commit()

	def __repr__(self):
		return '<Post(id: {0}, title: {1}, timestamp: {2}, author id: {3}>'.format(self.id, self.title, self.timestamp, self.author_id)

class Project(db.Model):
	__tablename__ = 'projects'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(256))
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow())
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)

	@staticmethod
	def insert_fake(count = 100):
		from random import seed, randint
		import forgery_py
		seed()
		user_count = User.query.count()
		for i in range(count):
			user = User.query.offset(randint(0, user_count - 1)).first()
			proj = Project(title = forgery_py.lorem_ipsum.title(randint(2, 5)),
				timestamp = forgery_py.date.date(True),
				author_id = user.id,
				body = forgery_py.lorem_ipsum.paragraphs())
			proj.body_html = md.render(proj.body)
			db.session.add(proj)
		db.session.commit()

	def __repr__(self):
		return '<Project(id: {0}, title: {1}, timestamp: {2}, author id: {3}>'.format(self.id, self.title, self.timestamp, self.author_id)