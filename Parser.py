"""
A parser for the GeneOntology OBO v1.2 format.

"""

import OBOFormat


__author__ = "Daniel Tufcea"


def parse_obo(filename):
    """
    Parses a Gene Ontology dump in OBO v1.2 format.
    returns unsanitized list [header, [list of first supported stanza], [list of second supported stanza], ...,
        [list of last supported stanza], [list of unsupported stanzas]]
    Keyword arguments:
        filename: The filename to read
    """
    output = [[] for _ in range(len(OBOFormat.supported_stanzas) + 2)]

    with open(filename, "r") as infile:
        current_header = OBOFormat.Header()  # header is read first
        current_stanza = None  # header is read first

        for line in infile:
            line = line.strip()
            if not line:
                continue  # Skip empty line
            if line in OBOFormat.supported_stanzas:
                if current_header:
                    output[0] = current_header
                    current_header = None
                else:
                    output[1 + OBOFormat.supported_stanzas.index(line)].append(current_stanza)
                    current_stanza = None

                current_stanza = OBOFormat.Stanza(line[1:-1])
            elif isinstance(line, basestring) and line[0] == "[" and line[-1] == "]":
                # is unsupported stanza
                if current_header:
                    output[0] = current_header
                    current_header = None
                else:
                    output[1 + len(OBOFormat.supported_stanzas)].append(current_stanza)
                    current_stanza = None

                current_stanza = OBOFormat.Stanza(line[1:-1])
            else:  # Not <stanza>

                if current_header is None and current_stanza is None:
                    continue
                else:
                    key, sep, val = line.partition(":")
                    if current_header:
                        current_header.add_tag(key, val)
                    if current_stanza:
                        current_stanza.add_tag(key, val)

        # Return header or last stanza
        if current_header is not None:
            output[0] = current_header
            current_header = None
        elif current_stanza is not None:
            type_ = "["+current_stanza.type+"]"
            if type_ in OBOFormat.supported_stanzas:
                output[1 + OBOFormat.supported_stanzas.index(type_)].append(current_stanza)
                current_stanza = None
            else:
                output[1 + len(OBOFormat.supported_stanzas)].append(current_stanza)
                current_stanza = None

    return output


if __name__ == "__main__":
    """Print out the number of GO objects in the given GO OBO file"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The input file in GO OBO v1.2 format.')
    args = parser.parse_args()
    # Iterate over GO terms
    stanza_counter = 0
    obo_objects = parse_obo(args.filename)
    for stanza_type in obo_objects[1:-1]: #ignore header
        print len(stanza_type)
        for stanza in stanza_type:
            stanza_counter += 1
    print "Found %d GO terms" % stanza_counter
