#!/usr/bin/env python

import os, sys
import cattle
import requests
import socket
import time

RANCHER_API_VERSION = 1
HOSTNAME = socket.gethostname()

print('Local hostname: '+HOSTNAME)
print('RANCHER_URL='+os.environ['RANCHER_URL'] + '/v' + str(RANCHER_API_VERSION))

for k in ['http_proxy', 'https_proxy', 'no_proxy']:
    if os.environ.has_key(k):
        print(k+'='+os.environ[k])

try:
    client = cattle.Client(url=os.environ['RANCHER_URL'] + '/v' + str(RANCHER_API_VERSION),
                           access_key=os.environ['RANCHER_ACCESS_KEY'],
                           secret_key=os.environ['RANCHER_SECRET_KEY'])
except ValueError:
    print("I'm sorry Dave.")

if len(client.list_host(name=HOSTNAME)) > 0:
    host_id = client.list_host(name=HOSTNAME)[0]['id']
else:
    print('No hosts found, assuming already removed, skipping.')
    sys.exit()

print('Rancher host ID: ' + host_id)
print('Initial actions available:')
print(client.by_id_host(host_id).actions)

for x in range(0, 3):
    if 'deactivate' in client.by_id_host(host_id).actions:
        print('Deactivating host...')
        client.by_id_host(host_id).deactivate()
    elif 'remove' in client.by_id_host(host_id).actions:
        print('Removing host...')
        client.by_id_host(host_id).remove()
    elif 'purge' in client.by_id_host(host_id).actions:
        print('Purging host....')
        client.by_id_host(host_id).purge()
    else:
        if x == 0:
            print('No removable actions found.')
        break
    time.sleep(2)
