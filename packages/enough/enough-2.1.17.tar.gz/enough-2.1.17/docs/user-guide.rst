Using Enough
============

Requirements
------------

Technical
~~~~~~~~~

* The ``clouds.yml`` credentials for either OVH or Fuga.

* The current code base requires:

  * The `Orchestration API available <https://wiki.openstack.org/wiki/Heat>`__:
    `Heat`, at least ``heat_template_version``: ``2016-10-14``/``newton``.
  * A public IPv4 per virtual machine (not a *floating IP* but a *direct IP*).
    IPv6 isn't supported yet.
  * In order to deploy every available services: 15 virtual machines.
  * The flavors must be provided with an attached root disk by default (not an
    explicit block storage) most of the virtual machines use 2Go RAM, some
    hosts/tests require 4Go or 8Go RAM.
  * A `Debian GNU/Linux <https://www.debian.org/>`_ stable image.

Knowledge
~~~~~~~~~

Enough is based on `Ansible <https://www.ansible.com/>`__, `OpenStack
<https://www.openstack.org/>`__ and `Debian GNU/Linux`_.  Debian GNU/Linux
based virtual machines are created on an OpenStack tenant and provisioned
with Ansible playbooks.

Each service adds more components such as `Let's encrypt
<https://letsencrypt.org/>`__, `Docker <https://www.docker.com/>`__ or
`Snap <https://snapcraft.io/>`__. And they also implement concepts
such as `Virtual Private Network
<https://en.wikipedia.org/wiki/Virtual_private_network>`__, `Reverse
Proxy <https://en.wikipedia.org/wiki/Reverse_proxy>`__ or `Certificate
Authority <https://en.wikipedia.org/wiki/Certificate_authority>`__.

If all goes well, Enough can be used even if the user knows nothing
more than what is in this guide. When something goes wrong, fixing the
problem or understanding the cause will require intimate knowledge
about all of the above. If that happens, it is best to start a
`discussion in the forum
<https://forum.enough.community/c/support/5>`__ and ask for help.

Installation
------------

* `Install Docker <http://docs.docker.com/engine/installation/>`__.

* Copy `clouds.yml` in `~/.enough/example.com/inventory/group_vars/all/clouds.yml` and edit
  to add `password:` next to `auth_url:` under the `production:` name.

* Add the ``enough`` CLI to ``~/.bashrc``:

.. code::

    eval "$(docker run --rm enoughcommunity/enough:latest install)"

* Verify that it works:

.. code::

    enough --version

Upgrade
-------

To upgrade to the latest Enough version:

.. code::

    $ docker pull enoughcommunity/enough:latest
    $ eval "$(docker run --rm enoughcommunity/enough:latest install)"

.. _bind_create:

Create the DNS name server
--------------------------

Assuming the domain name (``example.com`` for example) is registered,
it must be delegated to a dedicated name server before any service can
be created by Enough:

.. code::

     enough --domain example.com service create bind

Upon successfull completion, a machine named ``bind-host`` exists and
its public IP must be used as a `GLUE record
<https://en.wikipedia.org/wiki/Glue_record>`__.

.. code::

     $ enough --domain example.com openstack server list
     +---------------+--------------+--------+-----------------------+-----------+--------+
     | ID            | Name         | Status | Networks              | Image     | Flavor |
     +---------------+--------------+--------+-----------------------+-----------+--------+
     | 2b9a1bda-c2c0 | bind-host    | ACTIVE | Ext-Net=51.178.60.121 | Debian 10 | s1-2   |
     +---------------+--------------+--------+-----------------------+-----------+--------+

To verify the DNS running at bind-host works as expected:

.. code::

     $ dig @ip-of-the-bind-host bind.example.com
     $ enough --domain example.com ssh bind-host


It can then be used to instruct the `registrar
<https://en.wikipedia.org/wiki/Domain_name_registrar>`__ of
``example.com`` to delegate all domain name resolutions to this
IP. The exact method for performing this DNS delegation depends on the
registrar (`Gandi
<https://docs.gandi.net/en/domain_names/advanced_users/glue_records.html>`__
is different from `OVH
<https://docs.ovh.com/gb/en/domains/glue_registry/>`__, etc.). But it needs
to be done only once.

.. note::
   It will take time for the delegation to be effective.
   It can be as quick as one hour but delays from 24h to 72h are not uncommon.

To verify the delegation is effective:

.. code::

     getent hosts bind.example.com


Create or update a service
--------------------------

The following services are available:

* :doc:`bind <services/bind>` for `DNS server <https://www.isc.org/bind/>`__ at ``bind.examples.com``
* :doc:`icinga <services/monitoring>` for `monitoring <https://icinga.com/>`__ at ``icinga.example.com``.
* :doc:`postfix <services/postfix>` for `SMTP server <http://www.postfix.org/>`__ at ``postfix.example.com``.
* :doc:`OpenVPN <services/VPN>`, for `VPN <https://openvpn.net/>`__ at ``openvpn.example.com``
* :doc:`wazuh <services/ids>` for `Intrusion Detection System <https://wazuh.com/>`__ at ``wazuh.example.com``.
* :doc:`chat <services/mattermost>`, for `instant messaging <https://mattermost.com/>`__ at ``chat.example.com``
* :doc:`cloud <services/nextcloud>`, for `file sharing <https://nextcloud.com/>`__ at ``cloud.example.com``
* ``forum``, for `discussions and mailing lists <https://www.discourse.org/>`__ at ``forum.example.com``
* ``packages``, a `static web service <https://www.nginx.com/>`__ at ``packages.example.com``
* ``pad``, for `collaborative note taking <https://etherpad.org/>`__ at ``pad.example.com``
* :doc:`Weblate <services/weblate>`, for `online translations <https://weblate.org/>`__ at ``weblate.example.com``
* :doc:`WordPress <services/wordpress>`, for `CMS <https://wordpress.org/>`__ at ``wordpress.example.com``
* :doc:`openedX <services/openedx>`, for `MOOC platform <https://open.edx.org/>`__ at ``openedx.example.com``
* ``website``, for `static websites <https://gohugo.io/>`__ at ``website.example.com``
* ``wekan``, for `kanban <https://wekan.github.io/>`__ at ``wekan.example.com``
* :doc:`gitlab <services/gitlab>`, for `software development <https://gitlab.com/>`__ at ``lab.example.com``
* ``api``, for :doc:`Enough development <community/contribute>` at ``api.example.com``
* :doc:`Jitsi <services/jitsi>`, for `video conferencing <https://jitsi.org/>`__ at ``jitsi.example.com``
* :doc:`Psono <services/psono>`, for `password management <https://psono.com/>`__ at ``psono.example.com``

As an example, the cloud service can be created as follows:

.. code::

     enough --domain example.com service create cloud

..  note::
    If the command fails, because of a network failure or any other reason,
    it is safe to run it again. It is idempotent.

When it completes successfully, it is possible to login
``https://cloud.example.com`` with user ``admin`` and password
``mynextcloud``.

Restore a service
-----------------

Stateless services such as :doc:`bind <services/bind>` do not need
backup: they can be rebuilt from scratch if the machine hosting them
fails. For instance, if `bind-host` is lost:

.. code::

   $ enough --domain example.com host create bind-host
   $ enough --domain example.com playbook

However, most services such as :doc:`file sharing <services/nextcloud>`
and :doc:`translations <services/weblate>` rely on persistent
information that are located in a encrypted volume attached to the
machine. A daily :doc:`backup <services/backup>` is made in case a
file is inadvertendly lost.

Infrastructure services and access
----------------------------------

Networks
~~~~~~~~

By default all hosts are connected to two networks: one with a public
IP and the other with a private IP. This can be changed by setting the
`network_internal_only` variable in
`~/.enough/example.com/inventory/group_vars/all/network.yml`, using
`this example
<https://lab.enough.community/main/infrastructure/blob/master/inventory/group_vars/all/network.yml>`__.

The default can also be changed for a given host (for instance
`weblate-host`) by setting the desired value in the
`~/.enough/example.com/inventory/host_vars/weblate-host/network.yml` file.

.. _user_guide_vpn:

VPN
~~~

A VPN can optionally be installed for clients to access hosts that do
not have public IPs.

A host with a public IP must be chosen to deploy the VPN. For instance
`bind-host` by adding the following to `~/.enough/example.com/inventory/services.yml`:

.. code::

   openvpn-service-group:
     hosts:
       bind-host:

It can then be created with:

.. code::

     enough --domain example.com service create openvpn

The certificates for clients to connect to the VPN will be created
from the list in the `openvpn_active_clients` variable in
`~/.enough/example.com/inventory/group_vars/all/openvpn.yml`,
using `this example
<https://lab.enough.community/main/infrastructure/blob/master/inventory/group_vars/all/openvpn.yml>`__.

For each name in the `openvpn_active_clients` list, a `.tar.gz` file will be created in the
`~/.enough/example.com/openvpn/` directory. For instance, for

.. code::

   ---
   openvpn_active_clients:
    - loic

The file `~/.enough/example.com/openvpn/loic.tar.gz` will be
created and contains OpenVPN credentials. The specific instructions
to use them depends on the client.

Certificates
~~~~~~~~~~~~

By default certificates are obtained from `Let's Encrypt
<https://letsencrypt.org>`__. But if a host is not publicly
accessible, it can be configured to obtain a certificate from a
certificate authority dedicated to the Enough instance. The default
for `certificate_authority` should be set in
`~/.enough/example.com/inventory/group_vars/all/certificate.yml`, using `this example <https://lab.enough.community/main/infrastructure/blob/master/inventory/group_vars/all/certificate.yml>`__.

The default can also be changed for a given host (for instance
`weblate-host`) by setting the desired value in the
`~/.enough/example.com/inventory/host_vars/weblate-host/network.yml` file.

.. _attached_volumes:

Attached volumes
~~~~~~~~~~~~~~~~

Provisioning
++++++++++++

A volume can be created and attached to the host. It can be resized at
a later time, when more space is needed. For instance, before creating
`weblate-host`, the desired volume size and name can be set in the
`~/.enough/example.com/inventory/host_vars/weblate-host/provision.yml`
file like so:

.. code::

   ---
   openstack_volumes:
     - name: weblate-volume
       size: 10


Encrypting and Mounting
+++++++++++++++++++++++

The volume can then be encrypted, formatted and mounted by specifying
the mount point in the `encrypted_device_mount_point` variable like so:

.. code::

   ---
   openstack_volumes:
     - name: weblate-volume
       size: 10
   encrypted_device_mount_point: /srv

By default `Docker <https://www.docker.com/>`__ or `Snap
<https://snapcraft.io/>`__ will be set to reside in the
`encrypted_device_mount_point` directory so that the data it contains
is encrypted. It can be disabled with the
`encrypted_volume_for_docker` and `encrypted_volume_for_snap`
variables like so:

.. code::

   ---
   openstack_volumes:
     - name: weblate-volume
       size: 10
   encrypted_device_mount_point: /srv
   encrypted_volume_for_docker: false
   encrypted_volume_for_snap: false

Resizing
++++++++

The size of a volume can be increased (but never decreased) by
modifying the value from (for instance) 10GB

.. code::

   ---
   openstack_volumes:
     - name: weblate-volume
       size: 10

to 20GB

.. code::

   ---
   openstack_volumes:
     - name: weblate-volume
       size: 20

The resize operation is done with the following command (the host will
be rebooted). If the volume already has the desired size, the command
will do nothing.

.. code::

   $ enough --domain example.com volume resize weblate-host weblate-volume

If the volume is mounted as an encrypted partition, it should then be
extended to use the additional disk space. There is no need to unmount
the partition.

.. code::

   $ enough --domain example.com ssh weblate-host -- sudo cryptsetup resize --key-file=/etc/cryptsetup/keyfile spare
   $ enough --domain example.com ssh weblate-host -- sudo resize2fs /dev/mapper/spare

Services
~~~~~~~~

The following services are always available:

* :doc:`bind <services/bind>` for `DNS server <https://www.isc.org/bind/>`__ at ``bind.examples.com``
* `security groups <https://docs.openstack.org/nova/train/admin/security-groups.html>`__ for :ref:`firewall <firewall>`.

Background tasks
~~~~~~~~~~~~~~~~

* :doc:`Volumes and hosts backups <services/backup>`.
* `Unattended upgrades <https://wiki.debian.org/UnattendedUpgrades>`__.
* Tracking changes in `/etc/ for each machine <http://source.etckeeper.branchable.com>`__.

Access
~~~~~~

The `SSH public keys <https://en.wikipedia.org/wiki/Secure_Shell>`__ found in
files matching ``authorized_keys_globs`` are installed on every machine.

.. code::

   ---
   authorized_keys_globs:
     - ssh_keys/dachary.pub
     - ssh_keys/glen.pub

.. _restore_service_from_backup:

Restore a service from a backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To restore the volume attached to a service from a designated backup:

.. code::

   $ enough --domain example.com openstack volume snapshot list
   ...
   | 6b75f34e | 2020-04-12-cloud-volume | None | available | 100 |
   ...
   $ enough --domain example.com backup restore 2020-04-12-cloud-volume

In this example, the restoration is done as follows:

* The :doc:`cloud service <services/nextcloud>` is created, if it does not
  already exist.

* The machine (``cloud-host``) attached to the volume (``cloud-volume``) is
  stopped. The volume is detached and deleted.

* A new volume ``cloud-volume`` is created from the
  ``2020-04-12-cloud-volume`` backup and attached to ``cloud-host``.

* The machine (``cloud-host``) is restarted.

Create a clone of a service from a backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is convenient to create a clone of an existing service based on a
backup for:

* testing and experimenting without disrupting production
* verify an upgrade won't loose any data
* teaching
* etc.

.. code::

   $ enough --domain example.com openstack volume snapshot list
   ...
   | 6b75f34e | 2020-04-12-cloud-volume | None | available | 100 |
   ...
   $ enough --domain example.com backup restore \
            --target-domain test.d.enough.community \
            2020-04-12-cloud-volume

Once the service is cloned, it will be available at
``https://cloud.test.d.enough.community``. In this example, the
cloning is done as follows:

* A dedicated OpenStack region is used to restore the backup

.. note::

   The OpenStack region where the backup is restored is in the
   `clone` section of the `~/.enough/example.com/inventory/group_vars/all/clouds.yml`
   file and it can be modified if the default is not suitable.

* A volume is created from the ``2020-04-12-cloud-volume`` snapshot

* The :doc:`cloud service <services/nextcloud>` is created (in the
  region dedicated to restoring the backup) as well as all the
  services it depends on, if they do not already exist. Including the
  :doc:`DNS server <services/bind>`.

* The ``test.d.enough.community`` domain is delegated to the
  :doc:`DNS server <services/bind>` located in the
  OpenStack region where the backup was restored
  so that ``https://cloud.test.d.enough.community`` resolves
  to the newly created :doc:`cloud service <services/nextcloud>`.

It is possible restore the service step by step with the following commands:

.. code::

   $ enough --domain example.com backup clone volume \
            --target-domain test.d.enough.community 2020-07-29-cloud-volume
   $ enough --domain test.d.enough.community service create cloud
   $ enough --domain test.d.enough.community backup restore 2020-07-29-cloud-volume

Restoring a service that requires a VPN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the service restored in a clone requires a VPN (that is if it runs
on an private IP), a new VPN must be setup before the user can access
it.

If the service is cloned with:

.. code::

   $ enough --domain example.com backup restore \
            --target-domain test.d.enough.community \
            2020-04-12-cloud-volume

The credentials to connect to the VPN of the clone are found in the
`~/.enough/test.d.enough.community/openvpn` directory (for instance
`~/.enough/test.d.enough.community/openvpn/loic.tar.gz`).

.. note::

   Although the `loic.tar.gz` file has the same name as in the
   original, it will connect to a the VPN server in the clone. Care
   must be taken to **not** override credentials that existed before
   the cloning operation.

The subnet of internal network of the clone is hardcoded in
`.enough/test.d.enough.community/inventory/group_vars/all/internal_network.yml`:

.. code:

   ---
   openstack_internal_network_prefix: "10.11.10.0"
   openstack_internal_network_cidr: "10.11.10.0/24"


Low level commands
------------------

The following are not useful if only relying on the ``service``
command above. They can however be helpful to run Ansible or OpenStack
manually.

Adding hosts
~~~~~~~~~~~~

The hosts (OpenStack virtual machines) are created automatically when
a service is provided. It is however possible to create a new host or
destroy an existing one.

The first step is to edit ``~/.enough/example.com/inventory/all.yml`` and
add the name of the new host:

.. code::

   ---
   all-hosts:
    hosts:
     my-host:
     bind-host:
     forum-host:
     ...

Creating a new host:

.. code::

   enough --domain example.com host create my-host

SSH to a host:

.. code::

   enough --domain example.com ssh my-host

Removing hosts
~~~~~~~~~~~~~~

Every host is known to ``icinga``, ``bind`` and ``wazuh`` and it
should be deleted from these services before being removed.

* Add the host to the ``deleted-hosts`` group in ``~/.enough/example.com/inventory/all.yml``:

.. code::

   ---
   deleted-hosts:
     hosts:
       some-host:

* Run the playbook:

.. code::

   enough --domain example.com playbook

* Physically delete the host

.. code::

   enough --domain example.com host delete my-host

Running openstack
~~~~~~~~~~~~~~~~~

The `openstack <https://docs.openstack.org/python-openstackclient>`__
CLI can be used as follows:

.. code::

   $ enough --domain example.com openstack -- help

Which is exactly equivalent to:

.. code::

   $ OS_CLIENT_CONFIG_FILE=~/.enough/example.com/inventory/group_vars/all/clouds.yml \
     openstack --os-cloud production help


Running ansible-playbook
~~~~~~~~~~~~~~~~~~~~~~~~

The `ansible-playbook <https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html>`__
CLI can be used as follows:

.. code::

   $ enough --domain example.com playbook -- --limit localhost,icinga-host \
     --private-key ~/.enough/example.com/infrastructure_key \
     ~/.enough/example.com/enough-playbook.yml

It implicitly uses the following inventories (via multiple
**--inventory** options), in order (the last inventory listed has
precedence):

* ~/.enough/example.com/inventory
* `built in Enough inventory <https://lab.enough.community/main/infrastructure/tree/master/inventory>`__
