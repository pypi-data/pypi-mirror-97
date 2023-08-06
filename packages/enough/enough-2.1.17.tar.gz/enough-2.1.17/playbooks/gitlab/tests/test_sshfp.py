testinfra_hosts = ['ansible://bind-host']


def test_sshfp(host):
    domain = host.run('hostname -d').stdout.strip()
    #
    # expected side effect of
    #
    #     - role: install_ssh_records
    #       vars:
    #         install_ssh_records_host: lab
    #
    cmd = host.run(f'dig sshfp +noall +answer @ns1.{domain} lab.{domain}')
    assert cmd.rc == 0
    assert 'SSHFP' in cmd.stdout
    assert 'lab.' + domain in cmd.stdout
