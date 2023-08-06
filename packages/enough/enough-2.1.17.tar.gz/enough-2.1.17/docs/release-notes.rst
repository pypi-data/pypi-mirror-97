Release Notes
=============

2.1.17
------

* When using the libvirt infrastructure driver, the name of the host
  running the bind service is `bind-host` by default and can be
  changed. The following should be set in the
  `~/.enough/example.com/inventory/services.yml`::

       bind-service-group:
         hosts:
           bindother-host:

  This is useful when running more than one Enough instance from a single libvirt
  instance. When using the OpenStack infrastructure driver the bind service must
  run from a host named `bind-host`.

2.1.16
------

* Hosts can now be provisionned using libvirt instead of OpenStack. For instance::

    $ enough --domain example.com host create --driver libvirt bind
    bind: building image
    bind: preparing image
    bind: creating host
    bind: waiting for ipv4 to be allocated
    bind: waiting for 10.23.10.164:22 to come up
    Check if SSH is available on 10.23.10.164:22
    bind: host is ready
    +-------+--------------+
    | Field | Value        |
    +-------+--------------+
    | name  | bind         |
    | user  | debian       |
    | port  | 22           |
    | ip    | 10.23.10.164 |


2.1.15
------

website
~~~~~~~

* The ansible variable `website_repository` can be used to specify a repository other than `the default <https://lab.enough.community/main/website>`__.

certificates
~~~~~~~~~~~~

* Retry every minute during two hours if `no HTTPS certificate can be obtained <https://lab.enough.community/main/infrastructure/-/issues/314>`__. It is assumed that the cause for the failure is that DNS propagation can take a few hours.

nextcloud
~~~~~~~~~

* Reduce `memory requirements <https://lab.enough.community/main/infrastructure/-/issues/321>`__ when downloading files from Nextcloud. It can become a problem when the size of the file is large (i.e. greater than 1GB).

forum
~~~~~

* Pin the `discourse version and the plugins <https://lab.enough.community/main/infrastructure/-/issues/303>`__ to the latest stable release.

2.1.14
------

postfix
~~~~~~~

* `Fixes a bug <https://lab.enough.community/main/infrastructure/-/merge_requests/406>`__ blocking all outgoing mails on the relay.

2.1.13
------

gitlab
~~~~~~

* Add missing dependencies (debops.libvirt*) that would fail when trying
  to deploy a CI runner.

2.1.12
------

icinga
~~~~~~

The icinga client address was `hostvars[inventory_hostname]['ansible_host']` prior
to 2.1.12. It now is `icinga_client_address` which defaults to `hostvars[inventory_hostname]['ansible_host']`.
It can be used to resolve the following problem:

* The icinga master has a private IP and no public IP
* The icinga master goes through a router with a public IP
* The icinga client has a public IP which is the default for `icinga_client_address`
* The icinga master tries to ping the icinga client public IP but fails because the firewall of the client does not allow ICMP from the router public IP

The `icinga_client_address` of the client is set to the internal IP
instead of the public IP. The ping will succeed because the firewall
allows ICMP from any host connected to the internal network.

Development
~~~~~~~~~~~

* Added basic `support for running tests with libvirt <https://lab.enough.community/main/infrastructure/-/merge_requests/302>`__
  instead of OpenStack.
