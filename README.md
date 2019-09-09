# Snacker
String metrics + RL for finding privs. 

### Quick Start
```
pip install -r requirements.txt
python -t 5 -c will
```

### Help
```
-u, --users -> Users file (default: .\users.txt)
-c, --hosts -> Hosts file (default: .\hosts.txt)
-r, --compromised_users -> Compromised user(s)
-t, --threshold -> Number of scores to return
-v, --verbose ->Print results of each update to Q table
```
