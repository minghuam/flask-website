import os

basedir = os.path.abspath(os.path.dirname(__file__))

'''
	How to generate secrete keys? >> os.urandom(24)
'''
SECRET_KEY = 'you-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

ADMIN_NAME = 'admin'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

DEBUG = True

INTRODUCTION = """
Self Introduction
"""

ABOUT = """
#About

##About this site
This site is a weekend project built with Flask - an elegant micro framework.
"""