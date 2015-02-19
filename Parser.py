"""
A parser for the GeneOntology OBO v1.2 format.

"""

import OBOFormat


__author__ = "Daniel Tufcea"


def parse_obo(filename):
    """
    Parses a Gene Ontology dump in OBO v1.2 format.
    returns OBODump object containing header, supported_stanzas and unsupported_stanzas
    Keyword arguments:
        filename: The filename to read
    """
    output = OBOFormat.OBODump()
    current_stanza = None
    current_header = None
    with open(filename, "r") as infile:
        current_header = OBOFormat.Header()  # header is read first
        current_stanza = None  # header is read first

        for line in infile:
            line = line.strip()
            if not line:
                continue  # Skip empty line
            if isinstance(line, basestring) and line[1:-1] in OBOFormat.supported_stanzas:
                if current_header: # add header to output when we meet a stanza
                    output.add_header(current_header)
                    current_header = None
                elif current_stanza: # add previous stanza when we meet a new stanza
                    output.add_stanza(current_stanza)
                    current_stanza = None

                current_stanza = OBOFormat.Stanza(line[1:-1])
            elif isinstance(line, basestring) and line[0] == "[" and line[-1] == "]":
                # is unsupported <stanza>

                if current_header: # add header to output when we meet a stanza
                    output.add_header(current_header)
                    current_header = None
                elif current_stanza: # add previous stanza when we meet a new stanza
                    output.add_stanza(current_stanza)
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
        if current_header: # add header if there were no stanzas
            output.add_header(current_header)
            current_header = None
        elif current_stanza: # add last stanza
            output.add_stanza(current_stanza)
            current_stanza = None
    return output


if __name__ == "__main__":
    """Print out the number of GO objects in the given GO OBO file"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The input file in GO OBO v1.2 format.')
    args = parser.parse_args()
    # Iterate over stanzas
    stanza_counter = 0
    obo_dump = parse_obo(args.filename)
    for stanza_type in OBOFormat.supported_stanzas: #ignore header and count all the stanzas
        print stanza_type, len(obo_dump.supported_stanzas[stanza_type])
        stanza_counter += len(obo_dump.supported_stanzas[stanza_type])
    print 'Unsupported', len(obo_dump.unsupported_stanzas)
    stanza_counter += len(obo_dump.unsupported_stanzas)
    print "Found %d objects" % stanza_counter
