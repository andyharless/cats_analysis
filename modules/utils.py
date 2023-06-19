"""
Utilities used by CAT Analysis programs
"""

def make_url(base, verb, params=None):
    """Generate a URL to query a REST API"""

    param_string = ''
    if params is not None:
        param_string = '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
    return base + verb + param_string
