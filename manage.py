from flask.ext.script import Shell, Manager
from app import app, db
from app.models import User, Role, Permission, Post, Project

def make_context():
	return dict(app=app, db=db, User=User, Role=Role, 
		Permission=Permission, Post=Post, Project=Project)

manager = Manager(app)
manager.add_command("shell", Shell(make_context = make_context))

if __name__ == '__main__':
	manager.run()