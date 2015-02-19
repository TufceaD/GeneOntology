"""
Classes and methods for the GeneOntology OBO v1.2 format.

"""

__author__ = 'Daniel'

supported_stanzas = ['[Term]', '[Instance]', '[Typedef]']

class Header:
    tags = {}
    type = 'header'

    def __init__(self):
        pass

    def add_tag(self, key, val):
        self.tags[key] = val

class Stanza:
    tags = {}
    type = None

    def __init__(self, type_, key=None, id_value=None):
        self.type = type_
        if key == "id" and Stanza.is_valid_id:
            self.tags[key] = id_value

    def add_tag(self, key, val):
        if key == "id":
            if Stanza.is_valid_id:
                self.tags[key] = val
        else:
            self.tags[key] = val

    def is_valid_id(tag_id):
        invalid_ids = ["OBO:TYPE", "OBO:TERM", "OBO:TERM_OR_TYPE", "OBO:INSTANCE"]
        if tag_id is None:
            return False
        elif tag_id in invalid_ids:
            return False
        else:
            return True