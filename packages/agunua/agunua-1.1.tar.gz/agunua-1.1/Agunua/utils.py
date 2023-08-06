#!/usr/bin/env python3

# https://github.com/netaddr/netaddr
import netaddr

def _get_certificate_san(x509cert):
    san = ""
    ext_count = x509cert.get_extension_count()
    for i in range(0, ext_count):
        ext = x509cert.get_extension(i)
        if "subjectAltName" in str(ext.get_short_name()):
            san = str(ext)
    return san

# Try one possible name. Names must be already canonicalized.
def _match_hostname(hostname, possibleMatch):
    if possibleMatch.startswith("*."): # Wildcard
        base = possibleMatch[1:] # Skip the star
        # RFC 6125 says that we MAY accept left-most labels with
        # wildcards included (foo*bar). We don't do it here.
        try:
            (first, rest) = hostname.split(".", maxsplit=1)
        except ValueError: # One-label name
            rest = hostname
        if rest == base[1:]:
            return True
        if hostname == base[1:]:
            return True
        return False
    else:
        return hostname == possibleMatch

def format_x509_name(n):
    result = ""
    components = n.get_components()
    for (k, v) in components:
        result += "/%s=%s" % (k.decode(), v.decode())
    return result

def canonicalize(hostname, idn=True):
    if len(hostname) < 1:
        raise Exception("Internal error: empty hostname cannot be canonicalized")
    result = hostname.lower()
    if idn:
        try:
            result = result.encode('idna').decode()
        except UnicodeError:
            result = hostname
    if result[len(result)-1] == '.':
        result = result[:-1]
    return result

def is_valid_ip_address(addr):
    """ Return True and the address family if the IP address is valid. """
    try:
        baddr = netaddr.IPAddress(addr)
    except netaddr.core.AddrFormatError:
        return (False, None)
    return (True, baddr.version)

# Try all the names in the certificate
def validate_hostname(hostname, cert, idn=True):
    # Complete specification is in RFC 6125. It is long and
    # complicated and I'm not sure we do it perfectly.
    (is_addr, family) = is_valid_ip_address(hostname)
    hostname = canonicalize(hostname, idn)
    for alt_name in _get_certificate_san(cert).split(", "):
        if alt_name.startswith("DNS:") and not is_addr:
            (start, base) = alt_name.split("DNS:")
            base = canonicalize(base, idn)
            found = _match_hostname(hostname, base)
            if found:
                return True
        elif alt_name.startswith("IP Address:") and is_addr:
            host_i = netaddr.IPAddress(hostname)
            (start, base) = alt_name.split("IP Address:")
            if base.endswith("\n"):
                base = base[:-1]
            try:
                base_i = netaddr.IPAddress(base)
            except netaddr.core.AddrFormatError:
                continue # Ignore broken IP addresses in certificates. Are we too liberal?
            if host_i == base_i:
                return True
        else:
            pass # Ignore unknown alternative name types. May be
                 # accept URI alternative names for DoH,
    # According to RFC 6125, we MUST NOT try the Common Name before the Subject Alternative Names.
    cn = canonicalize(cert.get_subject().commonName, idn)
    found = _match_hostname(hostname, cn)
    if found:
        return True
    return False

