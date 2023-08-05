from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit


def simple_urljoin(*parts, append_slash=False):
    """Normalize url parts and join them with a slash."""
    parts = list(map(str, parts))
    schemes, netlocs, paths, queries, fragments = zip(*(urlsplit(part) for part in parts))
    scheme = _last(schemes)
    netloc = _last(netlocs)
    paths = [x for x in paths if x]
    if scheme and not netloc and paths:
        netloc, *paths = paths
    path = '/'.join((x.strip('/') for x in paths if x.strip('/')))

    if paths and parts[0].startswith('/'):
        path = '/' + path
    if append_slash or (paths and parts[-1].endswith('/')):
        path += '/'
    query = _last(queries)
    fragment = _last(fragments)
    return urlunsplit((scheme, netloc, path, query, fragment))


def _last(sequence, default=''):
    not_empty = [x for x in sequence if x]
    return not_empty[-1] if not_empty else default


def add_query(url: str, **params: str):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params.update(params)
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
