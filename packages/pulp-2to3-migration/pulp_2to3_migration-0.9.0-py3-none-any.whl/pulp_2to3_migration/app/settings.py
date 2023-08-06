PULP2_MONGODB = {
    'name': 'pulp_database',
    'seeds': '172.17.0.1:27017',
    'username': 'ci_cd',
    'password': 'ci_cd',
    'replica_set': '',
    'ssl': False,
    'ssl_keyfile': '',
    'ssl_certfile': '',
    'verify_ssl': True,
    'ca_path': '/etc/pki/tls/certs/ca-bundle.crt',
}

ALLOWED_CONTENT_CHECKSUMS = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
