"""Some utility functions module."""


def camel_to_snake(s):
    """ converts CamelCase string to camel_case\
        taken from https://stackoverflow.com/a/44969381

        :param s: some string
        :type s: str:

        :return: a camel_case string
        :rtype: str:
    """
    no_camel = ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')
    return no_camel.replace('__', '_')


def create_query_sting(param_dict):
    """ turns a dict into a query string

    :param param_dict: a dictionary
    :type param_dict: dict

    :return: a clean query string
    :rtype: str
    """
    params = "&".join(
        [
            f"{key}={value}" for key, value in param_dict.items()
        ]
    )
    return params.replace('#', '%23')


def id_from_uri(uri):
    """ extracts the id from an ARCHE-URL like https://whatever.com/123 -> 123

    :param uri: some ARCHE-URL
    :type uri: str

    :return: the actual ID, e.g. 123
    :rtype: str:
    """
    if uri.endswith('/'):
        uri = uri[:-1]
    a_id = uri.split('/')[-1]
    try:
        return f"{int(a_id)}"
    except ValueError:
        return ""
