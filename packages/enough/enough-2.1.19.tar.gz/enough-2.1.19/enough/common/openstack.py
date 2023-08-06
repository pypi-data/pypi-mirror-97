import ast
import base64
import datetime
import json
import logging
import os
import re
import requests
import sh
import textwrap
import time
import yaml

from enough import settings
from enough.common import ansible_utils
from enough.common.retry import retry
from enough.common.dotenough import Hosts
from enough.common.ssh import SSH

log = logging.getLogger(__name__)


class OpenStackBase(object):

    INTERNAL_NETWORK = 'internal'
    INTERNAL_NETWORK_CIDR = '10.20.30.0/24'

    def __init__(self, config_dir, **kwargs):
        self.args = kwargs
        self.config_dir = config_dir
        self.config_file = f'{self.config_dir}/inventory/group_vars/all/clouds.yml'
        self.o = sh.openstack.bake(
            '--os-cloud', kwargs.get('cloud', 'production'),
            _tee=True,
            _tty_out=False,
            _out=lambda x: log.info(x.strip()),
            _err=lambda x: log.info(x.strip()),
            _env={'OS_CLIENT_CONFIG_FILE': self.config_file},
        )


class Stack(OpenStackBase):

    class IPNotFound(Exception):
        pass

    def __init__(self, config_dir, definition=None, **kwargs):
        super().__init__(config_dir, **kwargs)
        log.info(f'OS_CLIENT_CONFIG_FILE={self.config_file}')
        self.definition = definition

    def get_template(self):
        return f'{settings.SHARE_DIR}/playbooks/infrastructure/template-host.yaml'

    def set_public_key(self, path):
        self.public_key = open(path).read().strip()

    def _create_or_update(self, action):
        d = self.definition
        parameters = [
            f'--parameter=public_key={self.public_key}',
        ]
        if 'flavor' in d:
            parameters.append(f'--parameter=flavor={d["flavor"]}')
        if 'image' in d:
            parameters.append(f'--parameter=image={d["image"]}')
        if 'port' in d:
            parameters.append(f'--parameter=port={d["port"]}')
        if 'volumes' in d and int(d['volumes'][0]['size']) > 0:
            parameters.append(f"--parameter=volume_size={d['volumes'][0]['size']}")
            parameters.append(f"--parameter=volume_name={d['volumes'][0]['name']}")
        if d.get('network'):
            parameters.append(f'--parameter=network={d["network"]}')
            parameters.append(
                f'--parameter=network_interface_unconfigured={d["network_interface_unconfigured"]}')
            parameters.append(
                f'--parameter=network_interface_routed={d["network_interface_routed"]}')
            parameters.append(
                f'--parameter=network_interface_not_routed={d["network_interface_not_routed"]}')
        log.info(f'_create_or_update: {d["name"]} {parameters}')
        self.o.stack(action, d['name'],
                     '--wait', '--timeout=600',
                     '--template', self.get_template(),
                     *parameters)

    def list(self):
        return [
            s.strip() for s in
            self.o.stack.list('--format=value', '-c', 'Stack Name', _iter=True)
        ]

    def create_or_update(self, return_on_create=False):
        if self.definition['name'] not in self.list():
            self.create()
            if return_on_create:
                return None
        else:
            self._create_or_update('update')
        self.create_internal_network()
        self.connect_internal_network()
        info = {
            'ipv4': self.get_ipv4(),
            'port': self.definition['port'],
        }
        if not self.internal_only() or self.args.get('route_to_internal', True):
            SSH.wait_for_ssh(info['ipv4'], info['port'])
        Hosts(self.config_dir).create_or_update(
            self.definition['name'], info['ipv4'], info['port'])
        return info

    @retry((IPNotFound, sh.ErrorReturnCode_1), 5)
    def get_ipv4(self):
        server = self.definition['name']
        o = OpenStack(self.config_dir, **self.args)
        if self.internal_only():
            ipv4 = o.server_ip_in_network(
                server, self.definition.get('internal_network', OpenStackBase.INTERNAL_NETWORK))
        else:
            ipv4 = o.server_ip_in_network(
                server, self.definition.get('network', 'Ext-Net'))
        if ipv4 is None:
            raise Stack.IPNotFound()
        return ipv4

    def create_internal_network(self):
        network = self.definition.get('internal_network', OpenStackBase.INTERNAL_NETWORK)
        cidr = self.definition.get('internal_network_cidr', OpenStackBase.INTERNAL_NETWORK_CIDR)
        o = OpenStack(self.config_dir, **self.args)
        o.network_and_subnet_create(network, cidr)

    def connect_internal_network(self):
        server = self.definition['name']
        network = self.definition.get('internal_network', OpenStackBase.INTERNAL_NETWORK)
        o = OpenStack(self.config_dir, **self.args)
        if o.server_connected_to_network(server, network):
            return
        self.o.server.add.network(server, network)

    def internal_only(self):
        return self.definition.get('network_internal_only', False)

    def create(self):
        try:
            log.info('create or update')
            self._create_or_update('create')
        except sh.ErrorReturnCode_1:
            log.info('retry create or update')
            # retry once because there is no way to increase the timeout and create fails often
            self._create_or_update('update')

    def delete_no_wait(self):
        name = self.definition['name']
        if name not in self.list():
            Hosts(self.config_dir).delete(name)
            return False

        self.o.stack.delete('--yes', name)
        return True

    def delete_wait(self):
        name = self.definition['name']

        @retry(AssertionError, 9)
        def wait_is_deleted():
            assert name not in self.list(), f'{name} deletion in progress'
        wait_is_deleted()

        Hosts(self.config_dir).delete(name)

        network = self.definition.get('internal_network', OpenStackBase.INTERNAL_NETWORK)
        o = OpenStack(self.config_dir, **self.args)
        o.delete_security_group(name)
        o.network_delete_if_not_used(network)

    def delete(self):
        if self.delete_no_wait():
            self.delete_wait()


class Heat(OpenStackBase):

    def get_stack_definitions(self, share_dir=settings.SHARE_DIR):
        ansible = ansible_utils.Ansible(self.config_dir, share_dir,
                                        self.args.get('inventory'))
        return ansible.get_hostvars(variable=None)

    def get_stack_definition(self, host):
        hostvars = self.get_stack_definitions()[host]
        return Heat.hostvars_to_stack(host, hostvars)

    @staticmethod
    def hostvars_to_stack(host, hv):
        definition = {
            'name': host,
            'port': hv.get('ansible_port', '22'),
            'flavor': hv['openstack_flavor'],
            'image': hv['openstack_image'],
            'network': hv.get('openstack_network'),
            'network_internal_only': hv.get('network_internal_only'),
            'network_interface_unconfigured': hv.get('network_interface_unconfigured'),
            'network_interface_routed': hv.get('network_interface_routed'),
            'network_interface_not_routed': hv.get('network_interface_not_routed'),
            'internal_network': OpenStackBase.INTERNAL_NETWORK,
            'internal_network_cidr': hv.get('openstack_internal_network_cidr',
                                            OpenStackBase.INTERNAL_NETWORK_CIDR),
        }
        if 'openstack_volumes' in hv:
            definition['volumes'] = hv['openstack_volumes']
        return definition

    def host_from_volume(self, name):
        for host, definition in self.get_stack_definitions().items():
            for v in definition.get('openstack_volumes', []):
                if v['name'] == name:
                    return host
        return None

    def is_working(self):
        # retry to verify the API is stable
        for _ in range(5):
            try:
                self.o.stack.list()
            except sh.ErrorReturnCode_1:
                return False
        return True

    def create_missings(self, names, public_key):
        return self.create_or_update(Hosts(self.config_dir).missings(names), public_key)

    def create_or_update(self, names, public_key):
        r = {}
        created = []
        #
        # Launch the creation of all stacks in // and do not wait for them to complete
        #
        for name in names:
            s = Stack(self.config_dir, self.get_stack_definition(name),
                      **self.args)
            s.set_public_key(public_key)
            info = s.create_or_update(return_on_create=True)
            if info:
                r[name] = info
            else:
                created.append(name)
        #
        # Verify all stacks previously launched complete as expected
        #
        for name in created:
            s = Stack(self.config_dir, self.get_stack_definition(name),
                      **self.args)
            s.set_public_key(public_key)
            info = s.create_or_update(return_on_create=True)
            r[name] = s.create_or_update()
        return r

    def create_test_subdomain(self, domain):
        d = f"{self.config_dir}/inventory/group_vars/all"
        assert os.path.exists(d)
        if 'bind-host' not in Stack(self.config_dir, **self.args).list():
            return None
        h = Heat(self.config_dir, **self.args)
        s = Stack(self.config_dir, h.get_stack_definition('bind-host'),
                  **self.args)
        s.set_public_key(f'{self.config_dir}/infrastructure_key.pub')
        bind_host = s.create_or_update()

        # reverse so the leftmost part varies, for human readability
        s = str(int(time.time()))[::-1]
        subdomain = base64.b32encode(s.encode('ascii')).decode('ascii').lower()

        fqdn = f'{subdomain}.test.{domain}'
        log.info(f'creating test subdomain {fqdn}')

        token = os.environ['ENOUGH_API_TOKEN']

        r = requests.post(f'https://api.{domain}/delegate-test-dns/',
                          headers={'Authorization': f'Token {token}'},
                          json={
                              'name': subdomain,
                              'ip': bind_host['ipv4'],
                          })
        r.raise_for_status()
        open(f'{d}/domain.yml', 'w').write(textwrap.dedent(f"""\
        ---
        domain: {fqdn}
        """))
        return fqdn


class OpenStackLeftovers(Exception):
    pass


class OpenStackBackupCreate(Exception):
    pass


class OpenStackShutoff(Exception):
    pass


class OpenStackVolumeResizeMissing(Exception):
    pass


class OpenStackVolumeResizeMismatch(Exception):
    pass


class OpenStackVolumeResizeShrink(Exception):
    pass


class OpenStack(OpenStackBase):

    def __init__(self, config_dir, **kwargs):
        super().__init__(config_dir, **kwargs)
        self.config = yaml.safe_load(open(self.config_file))

    @retry(OpenStackLeftovers, tries=8)
    def destroy_everything(self, prefix):
        log.info('destroy_everything acting')
        leftovers = []

        def delete_snapshots():
            snapshots = self.o.volume.snapshot.list('--format=json',
                                                    '-c', 'Name', '-c', 'ID')
            for snapshot in json.loads(snapshots.stdout):
                if prefix is None or prefix in snapshot['Name']:
                    leftovers.append(f'snapshot({snapshot["ID"]})')
                    self.o.volume.snapshot.delete(snapshot['ID'])

        def delete_stacks():
            r = self.o.stack.list('--format=json', '-c', 'Stack Name', '-c', 'Stack Status')
            for name, status in [(x["Stack Name"], x["Stack Status"])
                                 for x in json.loads(r.stdout)]:
                if prefix is None or prefix in name:
                    leftovers.append(f'stack({name})')
                    if status == 'DELETE_FAILED' or not status.startswith('DELETE'):
                        self.o.stack.delete('--yes', '--wait', name)

        def delete_images():
            for image in self.o.image.list('--private', '--format=value', '-c', 'Name', _iter=True):
                image = image.strip()
                if prefix is None or prefix in image:
                    leftovers.append(f'image({image})')
                    self.o.image.delete(image)

        def delete_volumes():
            volumes = self.o.volume.list('--format=json', '-c', 'Name',
                                         '-c', 'ID')

            for volume in json.loads(volumes.stdout):
                if prefix is None or prefix in volume['Name']:
                    leftovers.append(f'volume({volume["ID"]})')
                    self.o.volume.delete(volume['ID'])

        def delete_networks():
            for network in self.o.network.list('--no-share', '--format=value', '-c', 'Name',
                                               _iter=True):
                network = network.strip()
                if prefix is None or prefix in network:
                    leftovers.append(f'network({network})')
                    self.o.network.delete(network)

        #
        # There may be complex interdependencies between resources and
        # no easy way to figure them out. For instance, say there
        # exists a volume created from a snapshot of a volume created
        # by a stack. The stack cannot be deleted befor the volume created
        # from the snapshot is deleted. Because the snapshot cannot be deleted
        # before all volumes created from it are deleted. And the volumes from
        # which the snapshot are created cannot be deleted before all their
        # snapshots are deleted.
        #
        for f in (delete_snapshots, delete_stacks, delete_images, delete_volumes, delete_networks):
            try:
                f()
            except sh.ErrorReturnCode_1:
                pass

        if leftovers:
            raise OpenStackLeftovers('scheduled removal of ' + ' '.join(leftovers))

    def run(self, *args):
        return self.o(*args)

    def delete_security_group(self, name):
        try:
            self.o.security.group.delete(name)
        except sh.ErrorReturnCode_1:
            return False
        return True

    def network_exists(self, name):
        network = self.o.network.list('--format=value', '-c', 'Name', '--name', name)
        return network.strip() == name

    def network_create(self, name):
        if not self.network_exists(name):
            self.o.network.create(name)

    def network_delete_if_not_used(self, name):
        if not self.network_exists(name):
            return

        ports = self.o.port.list('--network', name, '--format=json', '-c',
                                 'ID', '-c', 'device_owner')
        ports = [port for port in json.loads(str(ports))
                 if port['device_owner'].startswith('compute:')]
        if not ports:
            self.o.network.delete(name)

    def subnet_exists(self, name):
        subnet = self.o.subnet.list('--format=value', '-c', 'Name', '--name', name)
        return subnet.strip() == name

    def subnet_create(self, name, cidr):
        if not self.subnet_exists(name):
            self.o.subnet.create('--subnet-range', cidr,
                                 '--dns-nameserver=8.8.8.8',
                                 '--network', name,
                                 name)

    def subnet_update_dns(self, name, *dns):
        args = [f'--dns-nameserver={ip}' for ip in dns]
        args.append(name)
        self.o.subnet.set('--no-dns-nameserver', *args)

    def network_and_subnet_create(self, name, cidr):
        self.network_create(name)
        self.subnet_create(name, cidr)

    def server_connected_to_network(self, server, network):
        return self.server_ip_in_network(server, network)

    def server_port_list(self, server, network):
        return self.o.port.list('--server', server, '--network', network,
                                '--format=value', '-c', 'Fixed IP Addresses')

    def server_ip_in_network(self, server, network):
        info = self.server_port_list(server, network).strip()
        if info == '':
            return None
        pattern = r"^[0-9.]+$"
        found = None
        for subnet in ast.literal_eval(info):
            if re.match(pattern, subnet['ip_address']):
                found = subnet['ip_address']
        return found

    def backup_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')

    def backup_create(self, volumes):
        if len(volumes) == 0:
            volumes = [x.strip() for x in self.o.volume.list('--format=value', '-c', 'Name')]
        date = self.backup_date()
        snapshots = self._backup_map()
        count = 0
        for volume in volumes:
            s = f'{date}-{volume}'
            if s not in snapshots:
                self.o.volume.snapshot.create('--force', '--volume', volume, s)
                count += 1
        self._backup_available(volumes, date)
        return count

    def _backup_map(self):
        return dict(self._backup_list())

    def _backup_list(self):
        r = self.o.volume.snapshot.list('--format=json', '-c', 'Name', '-c', 'Status',
                                        '--limit', '5000')
        return [(x["Name"], x["Status"]) for x in json.loads(r.stdout)]

    @retry(OpenStackBackupCreate, tries=7)
    def _backup_available(self, volumes, date):
        available = []
        waiting = []
        for name, status in self._backup_list():
            if not name.startswith(date):
                continue
            if status == "available":
                available.append(name)
            else:
                waiting.append(f'{status} {name}')
        available = ",".join(available)
        waiting = ",".join(waiting)
        progress = f'WAITING on {waiting}\nAVAILABLE {available}'
        log.debug(progress)
        if len(waiting) > 0:
            raise OpenStackBackupCreate(progress)

    def backup_prune(self, days):
        before = (datetime.datetime.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')
        count = 0
        for name, status in self._backup_list():
            if name[:10] > before:
                continue
            self.o.volume.snapshot.delete(name)
            count += 1
        return count

    def volume_prune(self, days):
        r = self.o.volume.snapshot.list(
            '--format=json', '--long', '-c', 'Volume', '--limit', '5000')
        volumes_with_snapshots = set([x["Volume"] for x in json.loads(r.stdout)])
        r = self.o.volume.list('--format=json', '-c', 'Name', '-c', 'ID', '--limit', '5000')
        before = (datetime.datetime.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')
        info = {
            'no_date_prefix': [],
            'has_snapshots': [],
            'deleted': [],
            'recent': [],
        }
        for volume, volume_id in set([(x["Name"], x["ID"]) for x in json.loads(r.stdout)]):
            if re.match(r'^\d\d\d\d\-\d\d-\d\d-', volume):
                if volume_id in volumes_with_snapshots:
                    info['has_snapshots'].append(volume)
                elif volume[:10] < before:
                    self.o.volume.delete(volume)
                    info['deleted'].append(volume)
                else:
                    info['recent'].append(volume)
            else:
                info['no_date_prefix'].append(volume)
        return info

    @retry(OpenStackShutoff, tries=5)
    def server_wait_shutoff(self, host):
        status = self.o.server.show('--format=value', '-c=status', host)
        status = status.strip()
        if status != 'SHUTOFF':
            raise OpenStackShutoff('Unexpected status: %r' % status)

    def replace_volume(self, host, volume, delete_volume):
        self.o.server.stop(host)
        self.server_wait_shutoff(host)
        attached = self.o.server.show(
            '--format=yaml', '-c', 'volumes_attached', host).stdout.strip()
        current_volume_id = yaml.safe_load(attached)['volumes_attached'][0]['id']
        current_volume = self.o.volume.show(
            '--format=value', '-c', 'name', current_volume_id).strip()
        self.o.server.remove.volume(host, current_volume_id)
        # fetch volume id now because next block might assign an existing volume
        # name to another volume
        volume_id = self.o.volume.show('--format=value', '-c', 'id', volume).stdout.strip()
        if delete_volume:
            # using current_volume_id here is not possible unfortunately
            self.o.volume.delete(current_volume)
        else:
            date = self.backup_date()
            self.o.volume.set('--name', f'{date}-{current_volume}', current_volume_id)
        self.o.volume.set('--name', current_volume, volume_id)
        self.o.server.add.volume(host, volume_id)
        self.o.server.start(host)

    def volume_resize(self, host, volume, size):
        attached = self.o.server.show(
            '--format=yaml', '-c', 'volumes_attached', host).stdout.strip()
        volumes_attached = yaml.safe_load(attached)['volumes_attached']
        if not volumes_attached:
            raise OpenStackVolumeResizeMissing(
                f'{host} is not attached {volume}, it is not attached to any volume')
        current_volume_id = volumes_attached[0]['id']
        current_volume = self.o.volume.show(
            '--format=value', '-c', 'name', current_volume_id).strip()
        if current_volume != volume:
            raise OpenStackVolumeResizeMismatch(
                f'{host} is not attached {volume}, it is attached to {current_volume}')
        current_size = int(self.o.volume.show('-c', 'size', '--format=value', volume).strip())
        if current_size == size:
            log.info(f'resize of {host} volume {volume} is not necessary, it already is {size}GB')
            return False
        if current_size > size:
            raise OpenStackVolumeResizeShrink(
                f'{host} {volume} is {current_size}GB and cannot be shrinked to {size}GB')
        self.o.server.stop(host)
        self.server_wait_shutoff(host)
        self.o.server.remove.volume(host, volume)
        self.o.volume.set('--size', size, volume)
        self.o.server.add.volume(host, volume)
        self.o.server.start(host)
        return True

    def region_empty(self):
        volumes = self.o.volume.list()
        servers = self.o.server.list()
        images = self.o.image.list('--private')
        return volumes.strip() == '' and servers.strip() == '' and images.strip() == ''
