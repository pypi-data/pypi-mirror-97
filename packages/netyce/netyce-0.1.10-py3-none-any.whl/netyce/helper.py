import logging
import pprint
import os
import json
import xmltodict
import pickle
import re
import ipaddress


def beautify(value, indent=0, return_str=False, **kwargs):
    """Using pprint to beautify the output.

    Args:
        value: The input to be beautified
        indent (int): Set the indentation spaces, default = 0
        return_str (bool): Returns a formatted string if True
        **kwargs: Any known key/values for the pprint.PrettyPrinter function

    """
    pp = pprint.PrettyPrinter(indent=indent, **kwargs)
    if return_str:
        return pp.pformat(value)
    pp.pprint(value)


def enable_debug():
    """Enabling debug."""
    logging.basicConfig(level=logging.DEBUG)


def is_int(val):
    """Returns True if it is an Integer or a String containing integers.

    Args:
        val: The input to be validated

    Returns:
        boolean.

    """
    if isinstance(val, (str, int)) and (isinstance(val, int) or val.isdigit()):
        return True
    else:
        return False


def is_ip(ipaddr):
    try:
        ipaddress.ip_address(ipaddr)
    except ValueError or TypeError:
        return False
    return True


def is_ipv4(ipaddr):
    try:
        ipaddress.IPv4Address(ipaddr)
    except ValueError or TypeError:
        return False
    return True


def is_ipv6(ipaddr):
    try:
        ipaddress.IPv6Address(ipaddr)
    except ValueError or TypeError:
        return False
    return True


def save_file(data, filename):
    """Save data to a file
    filename is expected to be a string.
    the file is stored in the root of this project/output.

    Args:
        data: the data to be stored
        filename: the filename to be used

    """
    output_file = os.path.abspath(filename)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(str(data))
    print(f"Successfully written to: '{output_file}'")


def xml2json(xml_str, indent=2):
    """Convert xml to json.

    Args:
        xml_str: the xml string
        indent: amount of spaces to indent. Default = 2.

    Returns:
        json format of the xml

    """
    parsed = xmltodict.parse(xml_str.replace(']]>]]>', ''))
    return json.dumps(parsed, sort_keys=True, indent=indent, separators=(',', ': '))


def dict2json2file(dict_obj, filename, indent=2):
    """Save the dictionary to a file.

        Args:
            dict_obj: the dictionary
            filename: If provided the output is stored to that file.
            indent: amount of spaces to indent. Default = 2.

        """
    parsed = json.dumps(dict_obj, sort_keys=True, indent=indent, separators=(',', ': '))
    save_file(parsed, filename=filename)


def json2object(filename):
    """Read a json file.

    Args:
        filename: The filename to read

    Returns:
        dictionary

    """
    with open(filename) as json_file:
        return json.load(json_file)


def jsontxt2object(data):
    """Read a json text string.

    Args:
        data: the textual string with JSON

    Returns:
        dictionary

    """
    return json.loads(data)


def object2json(data):
    """Save data in json format.

    Args:
        data: any data

    Returns:
        json formatted variable

    """
    return json.dumps(data)


def pickle2file(data, filename):
    """Save data in a pickle file.

    Args:
        data: any data
        filename: Output filename

    """
    with open(f"{filename}", 'wb') as f:
        pickle.dump(data, f)


def file2pickle(filename):
    """Read from a pickle file.

    Args:
        filename: input filename

    Returns:
        the contents of the pickle

    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def minimal_recurring(character, string):
    """Find the minimal length of a recurring character
    Regular expression is used to find the minimal repeated set of characters.

    example:
    minimal_recurring("\n", '\n\n\nabc_abc\n\nabc_abc_abc\n\n\n\n')
    would return: '\n\n'

    Args:
        character: The repeated character to be found
        string: the text to be found in

    :Returns:
        the smallest group of found characters if found. Else the character itself.
    """
    amount_new_lines = re.compile(r'(%s+)' % character)
    found = amount_new_lines.findall(string)
    return min(found) if found else character
    # if found:
    #     return min(found)
    # else:
    #     return character


def maxlength(l1):
    """Getting the max length value of an iterable"""
    i = 0
    for x in l1:
        if len(x) > i:
            i = len(x)
    return i
