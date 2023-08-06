Hugo
====

`Hugo <https://gohugo.io/>`__ is available at `www.example.com` and is documented in `this file
<https://lab.enough.community/main/infrastructure/blob/master/playbooks/website/roles/website/defaults/main.yml>`__
and can be modified in the
`~/.enough/example.com/inventory/group_vars/website-service-group.yml`
file.

The service is created on the host specified by the `--host` argument:

.. code::

    $ enough --domain example.com service create --host website-host website
