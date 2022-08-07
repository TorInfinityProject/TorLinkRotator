import collections


# Django

SECRET_KEY = 'django-insecure-<50N_lower>'
DJANGO_DOMAIN = '<DOMAIN.ZONE>'
DJANGO_PORT = "80"
DJANGO_DEBUG = False


# Database

DATABASE_NAME = "<DB_NAME>"          # database name
DATABASE_USER = "<DB_USER>"          # username
DATABASE_PASSWORD = "<DB_PASSWORD>"  # password
DATABASE_HOST = "<DB_ADDRESS>"       # ip address like 127.0.0.1
DATABASE_PORT = "<DB_PORT>"          # any port, default port for postgres is 5432


# Redis-server

REDIS_PROTOCOL = '<REDIS_PROTOCOL>'  # redis, rediss, unix
REDIS_USERNAME = '<REDIS_USERNAME>'  # auth username or ''
REDIS_PASSWORD = '<REDIS_PASSWORD>'  # auth password or None
REDIS_HOST = '<REDIS_ADDRESS>'       # unix path or ip
REDIS_PORT = '<REDIS_PORT>'          # Port number or None when UNIX proto, default port 6379
REDIS_DB_INDEX = '0'                 # Index of redis database, default 0


# Tor

# Array of lists with format 
# [((<address:string>, <control port:integer>), <authenticate password:string>), ...]
# (<address:string>, <control port: integer>) can be replaced by <unix:string>
# of the Tor in which the link will be created. If there is no password, then None.
# Please note that if you use multiple processes, the created link 
# will be accessible only from the process on the port of which it was created.
# 
# If more than 1 is specified, the site will select the port 
# with the fewest hidden services created to evenly load between them
#
# If you have a large range of ports, they can be specified using the range function.
# Man: https://docs.python.org/3/library/functions.html#func-range
# Examples:
# [(('127.0.0.1', 9050 + i), None) for i in range(1000)]
# [(('127.0.0.1', 9050), None), (('127.0.0.1', 9051), 'password_fish')]
# [(('127.0.0.1', 9051), 'password_fish'), ('/var/run/tor_control_1.sock', 'password_fish')]
TOR_CONTROL_PORTS = [
    (('127.0.0.1', 9051), None)
]


# Dictionary where you specify the source port of the hidden service and the target.
# Note: The dictionary must be created using OrderedDict
# (<target_address:string>, <target_port:integer>) can be replaced by <target_unix:string>
# Format: {<source_port:integer>: (<target_address:string>, <target_port:integer>), ...}
# Format: {<source_port:integer>: '<target_unix:string>', ...}
TOR_HIDDEN_SERVICE_PORTS = collections.OrderedDict({
    80: ('127.0.0.1', 80),
})


# How long in seconds the link will be active before it is deleted. 
# If set to 0, links will not be removed.
TOR_HIDDEN_SERVICE_EXPIRE = 60 * 60 * 8


# If None, then when created, hidden services will be stored only in process memory. 
# When this process is restarted, all previously created hidden services will be removed. 
# To prevent this, specify the path where they should be stored. 
# Please note that if your site is highly loaded, it may
# work slower due to the need to write/read/delete data from disk
# Note: If specified, the path must end with /
# Note: You need specify absolute path
# Don't forget to set the same path for torrc
# HiddenService Folder name format: /some/path/to/dir/<randomstring>/
TOR_HIDDEN_SERVICE_FOLDER = None


# Schema of your website. http/https
TOR_HIDDEN_SERVICE_SCHEME = 'http'


# The maximum number of simultaneous streams (connections) per rendezvous circuit. 
# The maximum value allowed is 65535. (Setting this to None will allow an unlimited number 
# of simultaneous streams.)
# Note that if you have a low value for Keep-Alive, the user needs to open several streams
TOR_HIDDEN_SERVICE_MAX_STREAMS = 10
