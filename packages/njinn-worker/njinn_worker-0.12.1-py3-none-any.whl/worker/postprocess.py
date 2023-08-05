import re
from io import BytesIO
from tokenize import tokenize, STRING, NUMBER
from ast import literal_eval

SET_VARIABLE = "SET_VARIABLE"
SET_VARIABLE_LIST = "SET_VARIABLE_LIST"
SET_VARIABLE_DICT = "SET_VARIABLE_DICT"
PARSING_REGEX = (
    f"^\\s*({SET_VARIABLE}|{SET_VARIABLE_LIST}|{SET_VARIABLE_DICT})\\((.*)\\)\\s*$"
)


def insertion_point(result_dict, path):
    """
    Helper function to create the nested dict structure needed to insert a value at a certain dot-separated path.

    For example, to insert a value at path "foo.bar.baz" inside an an empty dict, we have to turn the dict
    into {"foo":{"bar":{}}}, and insert the value into the innermost dict.
    
    This function will create the nested dict structure, and return it together with the innermost key, i.e. "baz":

    >>> d = {}
    >>> inner_key, inner_dict = insertion_point(d, "foo.bar.baz")
    >>> d, inner_key, inner_dict
    ({'foo': {'bar': {}}}, 'baz', {})
    >>> # now we can insert a value
    >>> inner_dict[inner_key] = "value"
    >>> d
    {'foo': {'bar': {'baz': 'value'}}}

    In simpler cases, no structure needs to be created:
    >>> d = {"bar":"baz"}
    >>> inner_key, inner_dict = insertion_point(d, "foo")
    >>> inner_dict[inner_key] = "value"
    >>> d
    {'bar': 'baz', 'foo': 'value'}
    """
    key_parts = path.split(".")
    current = result_dict
    # create path to result
    for key_part in key_parts[:-1]:
        next_level = current.setdefault(key_part, {})
        if isinstance(next_level, dict):
            current = next_level
        else:
            # overwrite non-dict values
            current[key_part] = {}
            current = current[key_part]

    return key_parts[-1], current


def postproces_output(output):
    """
    Postprocess output to extract variable declarations, allowing path style keys.

    Examples for legal variable declarations
    SET_VARIABLE('foo','bar')
    SET_VARIABLE("bar","bar bar")
    SET_VARIABLE("baz.baz","baz baz")
    SET_VARIABLE_LIST('foo', 'bar')
    SET_VARIABLE_DICT('foo', 'bar', 'baz')
    """
    result = {}
    for definition, argument_list in re.findall(
        PARSING_REGEX, output, flags=re.MULTILINE
    ):
        argument_list = argument_list.strip()
        try:

            # Use python tokenizer for robust parsing including escapes
            tokens = list(tokenize(BytesIO(argument_list.encode("utf-8")).readline))

            # Discard unneeded parser tokens - we only care about the strings
            parsed_arguments = [
                tokval
                for (toknum, tokval, _, _, _) in tokens
                if toknum in [STRING, NUMBER] or tokval in ["True", "False"]
            ]

            # Strings can be quoted and escaped - literal_eval takes care of that
            if definition == SET_VARIABLE_DICT and len(parsed_arguments) == 3:
                [k, inner_k, v] = parsed_arguments
                # SET_VARIABLE_DICT('foo', 'bar', 'baz') is the same as SET_VARIABLE('foo.bar', 'baz')
                key = literal_eval(k) + "." + literal_eval(inner_k)
                value = literal_eval(v)
            elif len(parsed_arguments) == 2:
                [k, v] = parsed_arguments
                key = literal_eval(k)
                value = literal_eval(v)
            else:
                continue
            last_part_of_key, dict_to_update = insertion_point(result, key)
            if definition in [SET_VARIABLE, SET_VARIABLE_DICT]:
                dict_to_update[last_part_of_key] = value
            elif definition == SET_VARIABLE_LIST:
                dict_to_update.setdefault(last_part_of_key, []).append(value)
        except:
            continue
    return result
