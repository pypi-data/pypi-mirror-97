COPY . /opt
COPY tests/clouds.yml /opt/inventory/group_vars/all/clouds.yml
COPY tests/domain.yml /opt/inventory/group_vars/all/domain.yml
RUN cd /opt && git add . && git config user.email "me@example.com" && git config user.name "Your Name" && git commit -a -m 'for tests'
