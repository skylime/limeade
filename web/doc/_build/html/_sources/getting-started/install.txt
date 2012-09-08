============
Installation
============

Der Source Code kann von Github geladen werden. Entweder per direkten Download
oder über Git.

.. code:: bash
   
   git clone git@github.com:fatality/limeade.git

Installation der Anforderungen
------------------------------


Die Installation der Anforderungen wird beispielhaft für **Arch Linux**
beschrieben.

**Celery und django-celery:**

.. code:: bash
   
   pip2 install -U Celery
   pip2 install -U django-celery

**pyOpenSSL:**

.. code:: bash
   
   pacman -S python2-pyopenssl

**lxml:**

.. code:: bash
   
   pacman -S python2-lxml

**Ipy:**

.. code:: bash
   
   pacman -S python2-ipy

**libvirt:**

Um libvirt und somit auch KVM benutzen zu können, muss der Computer 
Virtualisierung unterstützen. Dies lässt sich mit folgendem Befehl testen:

.. code:: bash
   
   grep -E "(vmx|svm)" --color=always /proc/cpuinfo

Wenn die Ausgabe korrekt ist und der Computer Virtualisierung unterstützt kann 
libvirt, KVM und QEMU installiert und eingerichtet werden.

.. code:: bash
   
   pacman -S qemu-kvm libvirt dnsmasq virt-manager

Um dnsmasq korrekt einzurichten empfiehlt sich folgende diese Anleitung__. 
Libvirt als Normaluser verwenden zu können ist in dieser Anleitung__ 
beschrieben.

__ https://wiki.archlinux.org/index.php/Dnsmasq
__ https://wiki.archlinux.org/index.php/Libvirt#Configuration

**libvirt und TCP:**

Die Datei */etc/libvirt/libvirtd.conf* öffnen und folgende Stellen ändern:

::
    
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

In den `Arch User Repositories`_ findet sich ein `Paket für RabbitMQ`_ welches 
installiert werden muss.

.. _Arch User Repositories: https://aur.archlinux.org/
.. _Paket für RabbitMQ: http://aur.archlinux.org/packages.php?ID=19090

Anschließend wird der RabbitMQ als root gestartet:

.. code:: bash
   
   rabbitmq-server

Läuft der Server, müssen folgende drei Schritte durchgeführt werden:

.. code:: bash
   
   rabbitmqctl add_user limeade EimequuChuap8aa8ohyo
   rabbitmqctl add_vhost limeade
   rabbitmqctl set_permissions -p limeade limeade ".*" ".*" ".*"

Der Server läuft nun und empfängt Nachrichten, leitet diese aber noch nicht 
weiter. Dazu muss der Deamon limed mittels Celery gestartet werden. In der 
*settings.py* müssen dazu noch die Angaben für MySQL gemacht werden, damit 
völlig automatisch Datenbanken erstellt werden können.

