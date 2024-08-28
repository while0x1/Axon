import subprocess
import time
import os

#fastApi uvicorn server access log fail2Banish script - parses uvicorn access_log file and addes UFW rules for ips which try to access 
#BLOCKED_CODES on the DENY_PORT more than 3 times use a sudo cron job to allow subprocess to add UFW rules - be careful to not lock yourself out of essential services.

BLOCK_CODES = ['404']
DENY_PORT = "8090"
access_log_path = '<YOUR ACCESS LOG PATH HERE>'
with open(access_log_path, 'r') as f:
    lines = f.readlines()
#fin
uniqueIps = []
for l in lines:
    contents = l.split(':')
    ip = contents[0]
    #print(ip)
    if ip not in uniqueIps:
        uniqueIps.append(ip)
#fin
banish = []
result = subprocess.run(["ufw","status"],capture_output=True, text=True)
ufwstatus = result.stdout.split('\n')
alreadyBanished = []
for u in ufwstatus:
    if u.find('DENY') > -1:
        ip = u.split('DENY')[1].strip()
        alreadyBanished.append(ip)

for i in uniqueIps:
    count = 0
    for l in lines: 
        contents = l.split(':')
        ip = contents[0]  
        code = contents[1][len(contents)-6:].strip()
        if code in BLOCK_CODES and i == ip and i not in alreadyBanished:
            count += 1
    if count >= 3:
        #print(f'Banish {i} for {count} 404 attempts')
        banish.append(i)

for b in banish:
    result = subprocess.run(["ufw","deny","from",b,"to","any","port",DENY_PORT],capture_output=True, text=True)
    print(f'{result.stdout.strip()} to DENY {b} PORT {DENY_PORT} access' )
#Sudo Crontab Every 15 minutes    
#   */15 * * * * python3 /home/fail2Banish.py >> /home/banished.log 2>&1
