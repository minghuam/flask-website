###Create app directories.
```
sudo mkdir /var/www
sudo mkdir /var/www/blog
sudo chown -R ubuntu:ubuntu /var/www/blog
```
Clone the project and copy all files into */var/www/blog*.

###Create python virtual environment.
```
cd /var/www/blog
virtualenv env
```
###Install tools and requirements.
```
sudo apt-get install ngninx
sudo pip install uwsgi
. env/bin/activate
pip install -r requirements.txt
```
Check *uwsgi* version.
```
which uwsgi
uwsgi --version
```

Note: On Ubuntu 12.04, `sudo apt-get install uwsgi` will install *uwsgi* 1.03, which does not work. Use `pip install uwsgi` instead.

### Create database and private data.
Generate *SECRET_KEY* and modify *config.py*. An easy way to do is using
```
os.urandom(24)
```
Make sure the admin password is in the environment variable *ADMIN_PASSWORD*. In virtual environment, create a sqlite database and insert roles and at least one *admin* user.
```
. env/bin/activate
python manage.py shell
db.create_all()
Role.insert_roles()
User.insert_admin()
```

###*nginx* configuration
Create *nginx* configuration file: *blog_nginx.conf*.
```
server{
	listen	80;
	
	# static files
	location /static {
		alias /var/www/blog/app/static/;
	}

	# proxying connections to app servers
	location / {
		include	uwsgi_params;
		uwsgi_pass unix:/var/www/blog/tmp/uwsgi.sock;
	}
}
```
Symlink *nginx*'s configuration file.
```
sudo ln -s /var/www/blog/blog_nginx.conf /etc/nginx/conf.d/
```
###*uwsgi* configuration.
Create *uwsgi* configuration file: *blog_uwsgi.ini*.
```
# work with uwsgi 2.0+
[uwsgi]
venv = /var/www/blog/env
chdir = /var/www/blog

#http = 127.0.0.1:5000
socket = /var/www/blog/tmp/uwsgi.sock
chmod-socket = 666

master = true
module = blog
callable = app
#catch-exceptions = true

logto = /var/www/blog/log/uwsgi.log
```
Comment *socket* and uncomment *http* to test *uwsgi* functionality without *nginx*.

Create *uwsgi* upstart file: /etc/init/blog_uwsgi.conf
```
# uWSGI upstart script
# /etc/init/blog_uwsgi.conf
# respawn

description "Blog uWSGI Emperor"
start on runlevel [2345]
stop on runlevel [06]

exec uwsgi --master --die-on-term --emperor --ini /var/www/blog/blog_uwsgi.ini
```

### Start web server and *WSGI* app.
Start *uwsgi*.
```
sudo start blog_uwsgi
```

Restart *nginx*.
```
sudo service nginx restart
```
