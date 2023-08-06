from enough.common import retry

testinfra_hosts = ['ansible://cloud-host']


def test_nextcloud(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    cmd = host.run("""
    set -xe
    curl --silent https://cloud.$(hostname -d)/login |
       grep --quiet 'This application requires JavaScript'
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc


def test_nextcloud_via_tor(host):
    with host.sudo():
        host.run("apt-get install -y curl")

    @retry.retry(AssertionError, tries=5)
    def run():
        cmd = host.run("""
        set -xe
        hostname=$(sudo cat /var/lib/tor/services/cloud/hostname)
        torsocks curl --silent http://$hostname/login |
           grep --quiet 'This application requires JavaScript'
        """)
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc

    run()
