bind = "0.0.0.0:443"
workers = 4
threads = 2
timeout = 30

forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-Forwarded-Proto': 'https'
}
