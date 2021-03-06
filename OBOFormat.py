"""
Classes and methods for the GeneOntology OBO v1.2 format.

"""

__author__ = 'Daniel'

supported_stanzas = ['Term', 'Instance', 'Typedef']

class Header(object):
    tags = {}
    type = 'Header'
    required_tags = []
    optional_tags = []

    def __init__(self):
        self.set_required_tags()
        self.set_optional_tags()

    def add_tag(self, key, val):
        self.tags[key] = val

    def __repr__(self):
        # TODO: print in the proper order according to OBO standard
        representation = str(self.type) + "\n"
        for key, val in self.tags.items():
            representation += key + ": " + str(val) + "\n"
        return representation

    def set_required_tags(self):
        self.required_tags = ['format-version']


    def set_optional_tags(self):
        self.optional_tags = ['data-version', 'data', 'saved-by', 'auto-generated-by', 'subsetdef', 'import',
                                  'synonymtypedef', 'idspace', 'default-relationship-id-prefix', 'id-mapping',
                                  'remark']

class Stanza(object):

    def __init__(self, type_, key=None, id_value=None):
        self.type = type_
        self.tags = {}
        self.set_required_tags()
        self.set_optional_tags()
        if key == "id" and Stanza.is_valid_id:
            self.tags[key] = id_value

    def add_tag(self, key, val):
        try:
            self.tags[key].append(val)
        except KeyError:
            self.tags[key] = [val]

    def is_valid_id(tag_id):
        invalid_ids = ["OBO:TYPE", "OBO:TERM", "OBO:TERM_OR_TYPE", "OBO:INSTANCE"]
        if tag_id is None:
            return False
        elif tag_id in invalid_ids:
            return False
        else:
            return True

    def __repr__(self):
        # TODO: print in the proper order according to OBO standard
        representation = "[" + str(self.type) + "]" + "\n"
        for key, val in self.tags.items():
            for item in val:
                representation += key + ": " + str(item) + "\n"
        return representation

    def set_required_tags(self):
        if self.type == 'Term':
            self.required_tags = ['id', 'name']
        elif self.type == 'Typedef':
            self.required_tags = ['id', 'name']
        elif self.type == "Instance":
            self.required_tags = ['id', 'name', 'instance_of']
        else:
            self.required_tags = ['id', 'name']

    def set_optional_tags(self):
        if self.type == 'Term':
            self.optional_tags = ['is_anonymous', 'alt_id', 'def', 'comment', 'subset', 'synonym', 'exact_synonym',
                                  'narrow_synonym', 'broad_synonym', 'xref', 'xref_analog', 'xref_unk', 'is_a',
                                  'intersection_of', 'union_of', 'disjoint_from', 'relationship', 'is_obsolete',
                                   'replaced_by', 'consider', 'created_by', 'creation_date']
        elif self.type == 'Typedef':
            self.optional_tags = ['is_anonymous', 'alt_id', 'def', 'comment', 'subset', 'synonym', 'exact_synonym',
                                  'narrow_synonym', 'broad_synonym', 'xref', 'xref_analog', 'xref_unk', 'is_a',
                                  'relationship', 'is_obsolete', 'replaced_by', 'consider', 'created_by',
                                  'creation_date', 'domain', 'range', 'inverse_of', 'transitive_over', 'is_cyclic',
                                  'is_reflexive', 'is_symmetric', 'is_anti_symmetric', 'is_transitive', 'is_metadata_tag',
                                  ]
        elif self.type == "Instance":
            self.optional_tags = ['property_value', 'is_anonymous', 'namespace', 'alt_id', 'comment', 'xref', 'synonym',
                                  'is_obsolete', 'replaced_by', 'consider']
        else:
            self.optional_tags = []

class OBODump(object):
    def __init__(self, header=None):
        self.header = header
        self.supported_stanzas = {}
        self.unsupported_stanzas = []
        for stanza in supported_stanzas:
            self.supported_stanzas[stanza] = []

    def add_header(self, header):
        self.header = header

    def add_stanza(self, stanza):
        if stanza.type in supported_stanzas:
            self.supported_stanzas[stanza.type].append(stanza)
        else:
            self.unsupported_stanzas.append(stanza)


class Validator(object):
    def __init__(self, obo_object):
        self.type = obo_object.type
        self.required_tags = obo_object.required_tags
        self.optional_Tags = obo_object.optional_tags

class ErrorInvalidID(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def return_stanza(stanza):
    new_stanza = stanza
    return stanza