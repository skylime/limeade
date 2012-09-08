=========
Benutzung
=========

Sollten Node.js, Python, MySQL, Django und die anderen Abhängigkeiten 
installiert sein lässt sich die Webanwendung mit Django einrichten. Dazu sollte 
jedoch eine lokale Konfigurationsdatei erstellt werden. Eine Beispieldatei ist 
integriert (local_settings.py.example).

Django
------

Minimal sollte eine Datenbank angelegt werden und folgender Schritt durchgeführt 
werden:

.. code:: bash
   
   cd web/limeade
   python2 manage.py syncdb --migrate

Dies erstellt alle Tabellen in der Datenbank und zugleich auch einen Benutzer 
mit vollen Adminrechten. Starten lässt sich die Anwendung anschließend lokal mit

.. code:: bash
   
   python2 manage.py runserver

Die Webanwendung läuft nun unter http://127.0.0.1:8000/system/ und kann im Admin
mit Daten gefüttert werden (http://127.0.0.1:8000/admin/).

__ http://127.0.0.1:8000/system/
__ http://127.0.0.1:8000/admin/

Node.js Proxy
-------------

Der Node.js Proxy wird im *proxy*-Verzeichnis ebenfalls ausgeführt:

.. code:: bash
   
   node index.js

RabbitMQ und Celery
-------------------

Zum Abschluss muss RabbitMQ und der Deamon im *limed*-Verzeichnis gestaret werden:

.. code:: bash
   
   rabbitmq-server
   celeryd

