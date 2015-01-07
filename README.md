##Create app directories.
```
sudo mkdir /var/www
sudo mkdir /var/www/blog
sudo chown -R ubuntu:ubuntu /var/www/blog
```
##Create python virtual environment.
```
cd /var/www/blog
virtualenv env
. env/bin/activate
```
##Install tools and requirements.
```
sudo apt-get install ngninx
sudo pip install uwgsi
pip install -r requirements.txt
```
Check *uwgsi* version
```
which uwgsi
uwgsi --version
```

Note: On Ubuntu 12.04, `sudo apt-get install uwgsi` will install *uwgsi* 1.03, which does not work. Use `pip install uwgsi` instead.

##*nginx* configuration
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
##*uwsgi* configuration.
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

description "uWSGI Emperor"
start on runlevel [2345]
stop on runlevel [06]

exec uwsgi --master --die-on-term --emperor --ini /var/www/blog/blog_uwsgi.ini
```

## Start web server and *WSGI* app.
Start *uwsgi*.
```
sudo start blog_uwsgi
```

Restart *nginx*.
```
sudo service nginx restart
```
