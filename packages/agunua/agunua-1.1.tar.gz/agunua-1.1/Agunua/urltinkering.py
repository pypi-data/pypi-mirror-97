#!/usr/bin/python3

import urllib.parse
import codecs

import Agunua

encoding = "UTF-8"

def delete_first_segment(path):
    first_slash = path.find("/")
    if first_slash == -1:
        return (path, "")
    elif first_slash == 0:
        (first, rest) = delete_first_segment(path[1:])
    else:
        first = path[0:first_slash]
        rest = path[first_slash:]
    if not first.startswith("/"):
        first = "/" + first
    if first == "/.":
        first = ""
    elif first == "/":
        first = ""
    return (first, rest)
    
def delete_last_segment(path):
    last_slash = path.rfind("/")
    return path[0:last_slash]

def urlmerge(base, reference):
    reference_components = urllib.parse.urlparse(reference)
    if reference_components.scheme != "":
        # Not a relative link, just replace 
        return reference
    base_components = urllib.parse.urlparse(base)
    if base_components.scheme == "":
        raise Exception("Base is not an absolute URI \"%s\"" % base)
    base_path = base_components.path
    if base_path == "":
        base_path += "/"
    elif not base_path.endswith("/"):
        last_slash = base_path.rfind("/")
        base_path = base_path[0:last_slash+1] # RFC 3986, section 5.2.3.
    if base_components.query == "" or base_components.query is None:
        if reference_components.query  == "" or reference_components.query is None:
            query = ""
        else:
            query = reference_components.query
    else:
        if reference_components.query  == "" or reference_components.query is None:
            query = "" # Well, the RFC says we must use
                       # base_components.query but only if
                       # reference_components.path which must be very
                       # rare
        else:
            query = reference_components.query
    # We ignore fragments, since they are never sent to the server
    base = "%s://%s" % (base_components.scheme, base_components.netloc)
    if not reference_components.path.startswith("/"): # If relative path
        path = base_path + reference_components.path
    else:
        path = reference_components.path
    # Now, let's follow RFC 3986, section 5.2.4.
    result = ""
    end_slash = path.endswith("/")
    while path != "":
        if path.startswith("./"):
            path = path[2:]
        if path.startswith("../"):
            path = path[3:]
        if path.startswith("/./"):
            path = path[2:]
        if path.startswith("/.") and (len(path) == 2 or path[2] == "/"):
            path = "/" + path[2:]
        if path.startswith("/../"):
            path = path[3:]
            result = delete_last_segment(result)
        if path.startswith("/..") and (len(path) == 3 or path[3] == "/"):
            path = "/" + path[3:]
            result = delete_last_segment(result)
        if path == "." or path == "..":
            path = ""
        (first, path) = delete_first_segment(path)
        result += first
    if end_slash and not result.endswith("/"):
        result += "/"
    return urllib.parse.urlunsplit((base_components.scheme, base_components.netloc, result, query, None))

def iri_to_uri(iri):
    components = urllib.parse.urlsplit(iri)
    if components.port != None :
        if ":" in components.hostname:
            # Literal IPv6 address
            authority = "[" + components.hostname + "]" + \
                ":%s" % components.port
        else:
            authority = codecs.encode(components.hostname, encoding = "idna").decode() + \
                ":%s" % components.port
    else:
        authority = codecs.encode(components.netloc, encoding = "idna").decode()
    # No problem if it is already percent-encoded
    path = urllib.parse.quote(
        components.path.encode(encoding), 
        safe="/;%[]=:$&()+,!?*@'~"
    )
    query = urllib.parse.quote(
        components.query.encode(encoding), 
        safe="/;%[]=:$&()+,!?*@'~"
    )
    frag = urllib.parse.quote(
        components.fragment.encode(encoding), 
        safe="/;%[]=:$&()+,!?*@'~"
    )
    return urllib.parse.urlunsplit((components.scheme, authority,
                                   path, query, frag))

def uri_to_iri(uri):
    components = urllib.parse.urlsplit(uri)
    host = bytes(components.netloc, encoding)
    try:
        authority = codecs.decode(host, encoding="idna")
    except UnicodeDecodeError:
        raise Agunua.AlreadyIriOrWrongEncoding
    path = urllib.parse.unquote(components.path)
    # Trick to preserve percent-encoded question marks. Not ideal.
    query = components.query.replace("%3F", "%253F")
    query = urllib.parse.unquote(query)
    frag = urllib.parse.unquote(components.fragment)
    return urllib.parse.urlunsplit((components.scheme, authority,
                                   path, query, frag))
