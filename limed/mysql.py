from celery.decorators import task
import MySQLdb
import settings
import re

@task(ignore_result=True)
def create_db(user, password, name):
	# validation happens in django, just to be safe
	if not re.match(r'[a-zA-Z0-9-]+$', user): return
	if not re.match(r'[a-zA-Z0-9-]+$', name): return

	db_name = user + "_" + name

	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, 'mysql')
	c = db.cursor()
	c.execute("create database " + db_name)
	# clear possible previous permissions
	c.execute("grant usage on *.* to %s", (db_name))
	c.execute("drop user %s", (db_name, ))

	c.execute("grant all privileges on " + db_name + ".* TO %s IDENTIFIED BY %s", (db_name, password))
	db.commit()

@task()
def list_dbs(user):
	if not re.match(r'[a-zA-Z0-9-]+$', user): return []
	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, 'mysql')
	c = db.cursor()
	c.execute("select Db from db where Db like '" + user + r"\_%';")
	dbs = [(n[0], n[0][len(user + '_'):]) for n in c.fetchall()]
	return dbs


@task()
def delete_db(user, name):
	if not re.match(r'[a-zA-Z0-9-]+$', user): return
	if not re.match(r'[a-zA-Z0-9-]+$', name): return
	
	db_name = user + "_" + name

	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, 'mysql')
	c = db.cursor()
	c.execute("drop user %s", (db_name, ))
	c.execute("drop database " + db_name)
	db.commit()

@task()
def edit_db(user, password, name):
	if not re.match(r'[a-zA-Z0-9-]+$', user): return
	if not re.match(r'[a-zA-Z0-9-]+$', name): return

	db_name = user + "_" + name

	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, 'mysql')
	c = db.cursor()
	c.execute("set password for %s = PASSWORD(%s)", (db_name, password))
	db.commit()	
