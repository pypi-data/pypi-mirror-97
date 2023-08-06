#!/bin/bash

# ENOUGH_API_TOKEN=abc tests/run-tests.sh tox -e openvpn -- --enough-no-create --enough-no-tests playbooks/openvpn/tests

set -e

function prepare_environment() {
    if test $(id -u) != 0 ; then
        SUDO=sudo
    fi
    if test "$(dpkg-query -W -f='${db:Status-Abbrev}' git)" != "ii " ; then
        $SUDO apt-get update
        $SUDO apt-get install -y git
    fi
    if test -d ~/.ansible && test "$(find ~/.ansible ! -user $(id -u) -print -quit)" ; then
        $SUDO chown -R $(id -u) ~/.ansible
    fi
    local d=/var/lib/libvirt/images/enough
    if test -e /usr/sbin/libvirtd && ! test -d $d ; then
	$SUDO mkdir -p $d
	$SUDO chgrp libvirt $d
	$SUDO chmod 771 $d
    fi
}

function prepare_repository() {
    git submodule --quiet sync
    git submodule --quiet update --init --recursive
}

function prepare_inventory() {
    if test "$GITLAB_CI" ; then
	cat > tests/clouds.yml <<EOF
clouds:
  production:
    auth:
      auth_url: "https://auth.cloud.ovh.net/v3/"
      project_name: "AAAAAAA"
      project_id: "BBBBB"
      user_domain_name: "CCCCCCC"
      username: "DDDDDDD"
      password: "EEEEEEEE"
    region_name: "FFFFFF"
EOF
    fi
    cp -a tests/clouds.yml inventory/group_vars/all/clouds.yml

    if ! test -f inventory/group_vars/all/domain.yml ; then
        cat > tests/domain.yml <<EOF
---
domain: enough.community
EOF
        cp tests/domain.yml inventory/group_vars/all/domain.yml
    else
        cat inventory/group_vars/all/domain.yml > tests/domain.yml
    fi
}

function image_name() {
    if test "$GITLAB_CI" ; then
        echo enough-tox-$(date +%s)
        trap "docker rm -f $name >& /dev/null || true ; docker rmi --no-prune $name >& /dev/null || true"  EXIT
    else
        echo enough-tox-$(pwd | md5sum | cut -f1 -d' ')
    fi
}

function build_image() {
    local name="$1"
    local max_execution_time="$2"

    (
        cat enough/common/data/base.dockerfile
        cat tests/tox.dockerfile
        if test "$GITLAB_CI" ; then
            cat tests/copy-to-opt.dockerfile
        fi
    ) | timeout $max_execution_time docker build \
		--build-arg=USER_ID="$(id -u)" \
		--build-arg=DOCKER_GID="$(getent group docker | cut -d: -f3)" \
		--build-arg=LIBVIRT_GID="$(getent group libvirt | cut -d: -f3)" \
		--build-arg=KVM_GID="$(getent group kvm | cut -d: -f3)" \
		--build-arg=USER_NAME="${USER:-root}" \
		--tag $name -f - .
}

function run_tests() {
    local name="$1"
    shift
    local d="$1"
    shift

    prepare_inventory
    prepare_repository

    find $d \( -name '*.pyc' -o -name '*.pyo' -o -name __pycache__ \) -delete
    if test "$GITLAB_CI" ; then
        args="--workdir /opt"
        : ${PYTEST_ADDOPTS=-m \"not openstack_integration and not libvirt_integration\"}
        PASS_GITLAB_CI="-e GITLAB_CI=${GITLAB_CI}"
    else
        args="--volume ${d}:${d} --workdir ${d} --volume $HOME/.enough:$HOME/.enough --volume $HOME/.ansible:$HOME/.ansible -e HOME=$HOME"
        # handle git worktree
        git_dir="$(git rev-parse --absolute-git-dir)"
        if [ "${git_dir}" != "${d}/.git" ]; then
            git_common_dir="$(git rev-parse --git-common-dir)"
            args="$args --volume ${git_common_dir}:${git_common_dir}"
        fi
        PASS_GITLAB_CI=""
	local interactive=-ti
    fi
    if echo -- $@ | grep -e '--enough-driver.libvirt' ; then
	args="$args --dns 127.0.0.1"
    fi

    if test -e /dev/kvm ; then
	args="$args --device /dev/kvm"
    fi

    container_name="$name-$(date +%s)"
    docker run $interactive --rm \
	   --name $container_name \
	   --user "${USER:-root}" \
	   -e PYTEST_ADDOPTS="${PYTEST_ADDOPTS-}" \
	   -e ENOUGH_API_TOKEN=$ENOUGH_API_TOKEN ${PASS_GITLAB_CI} \
	   --cap-add=NET_ADMIN \
	   --device=/dev/net/tun \
	   $args \
	   --volume /run/libvirt/libvirt-sock:/run/libvirt/libvirt-sock \
	   --volume /var/run/docker.sock:/var/run/docker.sock \
	   --volume /var/lib/libvirt/images/enough:/var/lib/libvirt/images/enough \
	   $name "${@:-tox}"
}

function main() {
    prepare_environment
    prepare_inventory

    local name=$(image_name "$@")
    echo -n Creating or refreshing the docker image to run the tests...
    build_image $name 15 < /dev/null > /dev/null 2>&1 || build_image $name 7200
    echo done!
    local toplevel=$(git rev-parse --show-toplevel)
    run_tests $name $toplevel "$@"
}

main "$@"
