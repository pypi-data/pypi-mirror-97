import logging

log = logging.getLogger(__name__)


class Passwords(object):

    def __init__(self, enough):
        self.enough = enough

    def get_or_create(self, service):
        
