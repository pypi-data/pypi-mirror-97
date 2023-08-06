import argparse

from enough.common import options


def test_set_options():
    parser = argparse.ArgumentParser()
    assert options.set_options(parser) == parser
    args = parser.parse_args([])
    driver = 'libvirt'
    args = parser.parse_args(['--driver', driver])
    assert args.driver == driver
