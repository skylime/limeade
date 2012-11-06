# Einsatz von WebSockets zur Echtzeit-Administration eines Hosting-Clusters

## Features:

Verwaltung und Anlegen von

- VHosts
- FTP
- MySQL Datenbanken
- Backups
- Cloud Instanzen
- Domains
- SSL Zertifikaten
- E-mail Adressen, Weiterleitungen und Mailbboxen

## Requirements:

- [Python](http://www.python.org) == 2.7
- [Django](http://www.djangoproject.com/) >= 1.3
- [Node.js](http://www.nodejs.org) >= 0.6
- [MySQL](http://www.mysql.com) >= 5.0

### more requirements:

- [Celery](http://celeryproject.org/) und [django-celery](http://docs.celeryproject.org/en/latest/django/index.html)
- [pyOpenSSL](http://packages.python.org/pyOpenSSL)
- [lxml](http://lxml.de/)
- [Ipy](http://c0re.23.nu/c0de/IPy/)
- [libvirt](http://libvirt.org/)
- [RabbitMQ](http://www.rabbitmq.com/)

### Integrierte Anwendungen (Django)

- [South](http://south.aeracode.org/)
- [django-uni-form](http://django-uni-form.rtfd.org/)

## Installation der Anforderungen

Die Installation der Anforderungen wird beispielhaft für **Arch Linux**
beschrieben.

**Celery und django-celery:**
    
    $ pip2 install -U Celery
    $ pip2 install -U django-celery

**pyOpenSSL:**
    
    $ pacman -S python2-pyopenssl

**lxml:**
    
    $ pacman -S python2-lxml

**Ipy:**
    
    $ pacman -S python2-ipy

**libvirt:**

Um libvirt und somit auch KVM benutzen zu können, muss der Computer 
Virtualisierung unterstützen. Dies lässt sich mit folgendem Befehl testen:
    
    $ grep -E "(vmx|svm)" --color=always /proc/cpuinfo

Wenn die Ausgabe korrekt ist und der Computer Virtualisierung unterstützt kann 
libvirt, KVM und QEMU installiert und eingerichtet werden.
    
    $ pacman -S qemu-kvm libvirt dnsmasq virt-manager

Um dnsmasq korrekt einzurichten empfiehlt sich folgende diese [Anleitung](https://wiki.archlinux.org/index.php/Dnsmasq).

Libvirt als Normaluser verwenden zu können ist in dieser [Anleitung](https://wiki.archlinux.org/index.php/Libvirt#Configuration) 
beschrieben.

**libvirt und TCP:**

Die Datei */etc/libvirt/libvirtd.conf* öffnen und folgende Stellen ändern:
    
    listen_tls = 0
    listen_tcp = 1
    auth_tcp=none

Die Deamon Datei */etc/conf.d/libvirtd* öffnen und den Eintrag 
*LIBVIRTD_ARGS* in *LIBVIRTD_ARGS="--listen"* ändern.

Als letzter Schritt die QEMU Konfiguration in libvirt (*/etc/libvirt/qemu.conf*) 
öffnen und *vnc_listen = "0.0.0.0"* eintragen bzw. den Kommentar entfernen.

Als nächstes kann mittels virt-manager eine VM angelegt werden. Die Daten der VM
können im Django Admin später eingetragen werden.

**RabbitMQ:**

In den (`Arch User Repositories`](https://aur.archlinux.org/) findet sich ein [`Paket für RabbitMQ`](http://aur.archlinux.org/packages.php?ID=19090) welches 
installiert werden muss.

Anschließend wird der RabbitMQ als root gestartet:
    
    $ rabbitmq-server

Läuft der Server, müssen folgende drei Schritte durchgeführt werden:
    
    $ rabbitmqctl add_user limeade EimequuChuap8aa8ohyo
    $ rabbitmqctl add_vhost limeade
    $ rabbitmqctl set_permissions -p limeade limeade ".*" ".*" ".*"

Der Server läuft nun und empfängt Nachrichten, leitet diese aber noch nicht 
weiter. Dazu muss der Deamon limed mittels Celery gestartet werden. In der 
*settings.py* müssen dazu noch die Angaben für MySQL gemacht werden, damit 
völlig automatisch Datenbanken erstellt werden können.

## Benutzung

Sollten Node.js, Python, MySQL, Django und die anderen Abhängigkeiten 
installiert sein lässt sich die Webanwendung mit Django einrichten. Dazu sollte 
jedoch eine lokale Konfigurationsdatei erstellt werden. Eine Beispieldatei ist 
integriert (local_settings.py.example).

Minimal sollte eine Datenbank angelegt werden und folgender Schritt durchgeführt 
werden:
    
    $ cd web/limeade
    $ python2 manage.py syncdb --migrate

Dies erstellt alle Tabellen in der Datenbank und zugleich auch einen Benutzer 
mit vollen Adminrechten. Starten lässt sich die Anwendung anschließend lokal mit
    
    $ python2 manage.py runserver

Die Webanwendung läuft nun unter http://127.0.0.1:8000/system/ und kann im Admin
mit Daten gefüttert werden (http://127.0.0.1:8000/admin/).

Der Node.js Proxy wird im proxy Verzeichnis ebenfalls ausgeführt:
    
    $ node index.js

Zum Abschluss muss RabbitMQ und der Deamon im limed-Verzeichnis gestaret werden:
    
    $ rabbitmq-server
    $ celeryd

