# cloudutils

# vault_client


#### install
```
pip uninstall -y viant-cloudutils; pip install retry && pip install viant-cloudutils
wget -q https://github.vianttech.com/raw/techops/cloudutils/master/bin/vault_client.py -O /opt/stage/bin/vault_client.py
chmod +x /opt/stage/bin/vault_client.py
```

#### update rc.local
set -s/--service to pin the service if it's actually dynamic
```
export VAULT_TOKEN=$(/opt/stage/bin/vault_client.py -t -s frontend-stage)
```
