RUN pip install python-openstackclient python-heatclient # this is not necessary to run tests but to cleanup leftovers when tests fail
RUN pip install tox
# BEGIN dependencies playbooks/infrastructure/test-pipelining.yml
RUN apt-get install -y python
# END dependencies playbooks/infrastructure/test-pipelining.yml
# BEGIN dependencies of test/ssh
RUN apt-get install -y jq
RUN pip install tox yq
RUN apt-get install -y python3-apt python3-libvirt python3-lxml # required because python3 is used not python2
# END dependencies of test/ssh
RUN git init
COPY requirements.txt requirements-dev.txt tox.ini setup.cfg setup.py README.md /opt/
RUN mkdir /opt/docs
COPY docs/requirements.txt /opt/docs/
RUN tox --notest
# BEGIN dependencies enabling .test resolution in the test container
RUN apt-get install -y bind9
COPY tests/named.conf.local /etc/bind
COPY tests/named.conf.options /etc/bind
COPY tests/entrypoint.sh /opt
ENTRYPOINT ["/opt/entrypoint.sh"]
# END dependencies enabling .test resolution in the test container
