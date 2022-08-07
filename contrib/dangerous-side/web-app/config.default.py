

# Link to HiddenService with TorLinkRotator backend
TOR_LINK_ROTATION_URL = 'http://<URL>.onion'

# Tor Socks5 proxy
# Can be specified as string or list of strings(if you need use more than 1 port for balance load)
TOR_SOCKS5_PROXY = '127.0.0.1:9050'

# Your public domain name
SERVER_NAME = '<DOMAIN.ZONE>'

# If needed index page, can be specifies here as string with minified html code
# Replace statements:
# * {query_params} -> for put queryparams
# * {alias_subdomain_name} -> for aliased subdomain
# * {subdomain} -> subdomain, by default ''
# Example: 
# <p>Its {alias_subdomain_name} domain. <a href="http://{subdomain}someoniondomain.onion{query_params}">Link</a></p>
INDEX_HTML = None

# If you are use subdomain system, you can specify here subdomain alias for template
ALIAS_SUBDOMAIN_NAME = {}
