import datetime
import os

import pytest
import requests_mock as requests_mock_module

from tests.modified_environ import modified_environ

from enough import settings
from enough.common import openstack
from enough.common.openstack import Stack, Heat, OpenStack


#
# Stack
#
@pytest.mark.openstack_integration
def test_stack_create_or_update(openstack_name, openstack_variables,
                                dot_openstack):
    name = openstack_name
    network = openstack_name
    class_c = '10.101.30'
    cidr = f'{class_c}.0/24'
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    d.update(
        internal_network=network,
        internal_network_cidr=cidr
    )
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    r = s.create_or_update()
    assert r['port'] == '22'
    ipv4 = r['ipv4']
    o = OpenStack(settings.CONFIG_DIR)
    assert o.server_connected_to_network(name, network)
    assert r == s.create_or_update()
    assert o.server_connected_to_network(name, network)
    assert r['ipv4'] == ipv4
    s.delete()
    assert not o.network_exists(network)


#
# Heat
#
def test_heat_definition():
    h = Heat(settings.CONFIG_DIR)
    definitions = h.get_stack_definitions()
    assert 'bind-host' in definitions
    definition = h.get_stack_definition('bind-host')
    assert definition['name'] == 'bind-host'


def test_host_from_volume():
    h = Heat(settings.CONFIG_DIR)
    assert h.host_from_volume('cloud-volume') == 'cloud-host'
    assert h.host_from_volume('unknown-volume') is None


def test_heat_definition_encrypted():
    d = 'tests/enough/common/test_openstack/config_dir'
    h = Heat(d)
    definitions = h.get_stack_definitions(share_dir=d)
    assert 'my-host' in definitions
    assert definitions['my-host']['myvariable'] == 'myvalue'


def test_create_test_subdomain_no_bind(mocker):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('enough.common.openstack.Stack.list', return_value=[])
    h = Heat(settings.CONFIG_DIR)
    assert h.create_test_subdomain('my.tld') is None


def test_create_test_subdomain_with_bind(tmpdir, mocker, requests_mock):
    mocker.patch('enough.settings.CONFIG_DIR', str(tmpdir))
    d = f'{tmpdir}/inventory/group_vars/all'
    os.makedirs(d)
    assert not os.path.exists(f'{d}/domain.yml')
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('enough.common.openstack.Stack.list', return_value=['bind-host'])
    mocker.patch('enough.common.openstack.Stack.set_public_key')
    mocker.patch('enough.common.openstack.Stack.create_or_update', return_value={
        'ipv4': '1.2.3.4',
    })
    mocker.patch('enough.common.openstack.Heat.get_stack_definition')
    requests_mock.post(requests_mock_module.ANY, status_code=201)
    h = Heat(settings.CONFIG_DIR)
    with modified_environ(ENOUGH_API_TOKEN="TOKEN"):
        fqdn = h.create_test_subdomain('my.tld')
    assert '.test.my.tld' in fqdn
    assert os.path.exists(f'{d}/domain.yml')


#
# OpenStack
#
def test_server_ip_in_network_ok(mocker):
    ip = '1.2.3.4'
    mocker.patch('enough.common.openstack.OpenStack.server_port_list',
                 return_value="[{'ip_address': '" + ip + "'}, {'ip_address': '1:2:3:4:5'}]")
    o = OpenStack(settings.CONFIG_DIR)
    assert o.server_ip_in_network('server', 'network') == ip


def test_server_ip_in_network_none(mocker):
    mocker.patch('enough.common.openstack.OpenStack.server_port_list',
                 return_value='[]')
    o = OpenStack(settings.CONFIG_DIR)
    assert o.server_ip_in_network('server', 'network') is None


@pytest.mark.openstack_integration
def test_network(openstack_name, dot_openstack):
    o = OpenStack(settings.CONFIG_DIR)
    o.network_and_subnet_create(openstack_name, '10.11.12.0/24')
    assert o.network_exists(openstack_name)
    assert o.subnet_exists(openstack_name)

    dns_ip = '1.2.3.4'
    o.subnet_update_dns(openstack_name, dns_ip)
    r = o.o.subnet.show('--format=value', '-c', 'dns_nameservers', openstack_name)
    assert r.strip() == f"['{dns_ip}']"


@pytest.mark.openstack_integration
def test_backup_create_with_name(openstack_name, dot_openstack, caplog):
    o = OpenStack(settings.CONFIG_DIR)
    o.o.volume.create('--size=1', openstack_name)
    assert o.backup_create([openstack_name]) == 1
    assert o.backup_create([openstack_name]) == 0
    available_snapshot = f'AVAILABLE {o.backup_date()}-{openstack_name}'
    assert available_snapshot in caplog.text
    assert o.backup_prune(0) == 1
    assert o.backup_prune(0) == 0


@pytest.mark.openstack_integration
def test_volume_prune(openstack_name, dot_openstack, caplog):
    o = OpenStack(settings.CONFIG_DIR)

    volume_precious = openstack_name
    o.o.volume.create('--size=1', volume_precious)
    days = 2

    old = days + 1
    old_date = (datetime.datetime.today() - datetime.timedelta(old)).strftime('%Y-%m-%d')

    old_volume_with_snapshot = f'{old_date}-old-with-snapshot-{openstack_name}'
    o.o.volume.create('--size=1', old_volume_with_snapshot)
    old_volume_snapshot = f'snapshot-{openstack_name}'
    o.o.volume.snapshot.create('--volume', old_volume_with_snapshot, old_volume_snapshot)

    old_volume = f'{old_date}-old-{openstack_name}'
    o.o.volume.create('--size=1', old_volume)

    recent = days - 1
    recent_date = (datetime.datetime.today() - datetime.timedelta(recent)).strftime('%Y-%m-%d')

    recent_volume = f'{recent_date}-{openstack_name}'
    o.o.volume.create('--size=1', recent_volume)

    assert o.volume_prune(days) == {'deleted': [old_volume],
                                    'has_snapshots': [old_volume_with_snapshot],
                                    'no_date_prefix': [volume_precious],
                                    'recent': [recent_volume]}


@pytest.mark.openstack_integration
def test_backup_create_no_names(openstack_name, dot_openstack, caplog):
    o = OpenStack(settings.CONFIG_DIR)
    o.o.volume.create('--size=1', openstack_name)
    o.backup_create([])
    available_snapshot = f'AVAILABLE {o.backup_date()}-{openstack_name}'
    assert available_snapshot in caplog.text


@pytest.mark.openstack_integration
def test_openstack_replace_volume(openstack_name, dot_openstack,
                                  openstack_variables):
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    d.update({
        'volumes': [
            {
                'size': '1',
                'name': openstack_name,
            },
        ],
    })
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    s.create_or_update()

    o = OpenStack(settings.CONFIG_DIR)
    assert openstack_name in o.o.volume.list('--name', openstack_name)

    other_volume = f'{openstack_name}_other'
    date = o.backup_date()
    backup_volume = f'{date}-{openstack_name}'

    o.o.volume.create('--size=1', other_volume)
    o.replace_volume(openstack_name, other_volume, delete_volume=True)
    assert o.o.volume.list('--name', other_volume).strip() == ''
    assert o.o.volume.list('--name', backup_volume).strip() == ''
    assert o.o.volume.list(
        '-f=value', '-c=Name', '--name', openstack_name).strip() == openstack_name

    other_volume = f'{openstack_name}_backedup'
    o.o.volume.create('--size=1', other_volume)
    o.replace_volume(openstack_name, other_volume, delete_volume=False)
    assert o.o.volume.list('--name', other_volume).strip() == ''
    assert o.o.volume.list(
        '-f=value', '-c=Name', '--name', backup_volume).strip() == backup_volume
    assert o.o.volume.list(
        '-f=value', '-c=Name', '--name', openstack_name).strip() == openstack_name


@pytest.mark.openstack_integration
def test_openstack_volume_resize_ok(openstack_name, dot_openstack,
                                    openstack_variables):
    size = 1
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    d.update({
        'volumes': [
            {
                'size': str(size),
                'name': openstack_name,
            },
        ],
    })
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    s.create_or_update()

    o = OpenStack(settings.CONFIG_DIR)

    assert size == int(o.o.volume.show(
        '-c', 'size', '--format=value', openstack_name).strip())

    new_size = 2
    assert o.volume_resize(openstack_name, openstack_name, new_size) is True

    assert new_size == int(o.o.volume.show(
        '-c', 'size', '--format=value', openstack_name).strip())

    assert o.volume_resize(openstack_name, openstack_name, new_size) is False

    with pytest.raises(openstack.OpenStackVolumeResizeMismatch):
        o.volume_resize(openstack_name, 'UNKNOWN', new_size)

    with pytest.raises(openstack.OpenStackVolumeResizeShrink):
        o.volume_resize(openstack_name, openstack_name, 1)


@pytest.mark.openstack_integration
def test_openstack_volume_resize_no_volume(openstack_name, dot_openstack, openstack_variables):
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    s.create_or_update()

    o = OpenStack(settings.CONFIG_DIR)

    with pytest.raises(openstack.OpenStackVolumeResizeMissing):
        o.volume_resize(openstack_name, openstack_name, 1)


@pytest.mark.openstack_integration
def test_openstack_security_group(openstack_name, dot_openstack):
    o = OpenStack(settings.CONFIG_DIR)
    o.o.security.group.create(openstack_name)
    assert o.delete_security_group(openstack_name) is True
    assert o.delete_security_group(openstack_name) is False


@pytest.mark.openstack_integration
def test_destroy_volumes_with_same_name(openstack_name, dot_openstack):
    volume_name = f'{openstack_name}-test-destroy-volume'
    o = OpenStack(settings.CONFIG_DIR)
    o.o.volume.create('--size', '1', volume_name)
    o.o.volume.create('--size', '1', volume_name)
    assert 2 == o.o.volume.list().count(volume_name)
    o.destroy_everything(openstack_name)
    assert 0 == o.o.volume.list().count(volume_name)
