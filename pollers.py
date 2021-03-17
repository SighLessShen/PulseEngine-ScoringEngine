import socket
import requests
import os
from ftplib import FTP
import json
import ast
import subprocess
import hashlib
import random
from nslookup import Nslookup
import smtplib
import re

"""
Name: pollPort
Description: Will poll for a specific port and see if it is online
Parameters: ip - ip address to poll, port - port number
"""

def pollPort(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((ip,int(port)))
    if result == 0:
      return True
    else:
      return False

"""
Name: pollHTTP
Description: Will query a url and verify that it is reachable and the md5 content of the page is what is expected
Parameters: url - complete url of the page to query (ex. https://192.168.0.1/login.html), pageHash - expected md5 hash of the page
"""

def pollHTTPS(host, md5):
    try:
        if(hashlib.md5(requests.get(host, timeout=3, verify=False).content).hexdigest() == md5):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def pollHTTP(host, md5):
    try:
        if(hashlib.md5(requests.get(host, timeout=3).content).hexdigest() == md5):
            return True
        #content = requests.get("http://" + host, timeout=5).headers
        #print(content)
        #store = re.search("Content-Length': '(\d+)'(})",str(content))
        #store = re.search("Content-Length': ('\d+')",str(content))
        #test = store.group(1)

        else:
            return False
    except requests.exceptions.RequestException as e:
        print(e)
        return False

"""
Name: pollSSH
Description: Will verify that the SSH service is running on the specific port
Parameters: ip - ip address to poll, port - port number to poll, users - Array of strings of format "username:password" to verify are valid
"""

def pollSSH(ip, port, users):
    try:
        for user in users:
            if ":" not in user:
                continue
            username = user.split(":")[0]
            password = user.split(":")[1]
            pollCommand = "sshpass -p \"" + password + "\" ssh -q -o \"UserKnownHostsFile=/dev/null\" -o \"StrictHostKeyChecking=no\" " + username + "@" + ip + " -p " + port + " exit"
            if(subprocess.call(pollCommand, shell=True) != 0):
                    return False
        return True
    except:
        return False

"""
Name: pollFTP
Description: Will verify that the FTP service is running on the specific port
Parameters: ip - ip address to poll, port - port number to poll, users - Array of strings of format "username:password" to verify are valid
"""

def pollFTP(ip, port, users):
    try:
        ftp = FTP()
        ftp.connect(ip, int(port))
        ftp.set_pasv(False)
        for user in users:
            if ":" not in user:
                continue
            username = user.split(":")[0]
            password = user.split(":")[1]
        ftp.login(username, password)
        ftp.cwd('PC_Box/')
        filename = '025 - Pikachu.txt'
        if(ftp.size(filename) == 32):
            return True
        ftp.close()
        return False
    except:
        return False

records = {
    "globalterminal.goldenrod.city": "['192.168.220.21']",
    "billshouse.goldenrod.city": "['192.168.220.24']",
    "gym.goldenrod.city": "['192.168.220.22']",
    "pcbox.goldenrod.city": "['192.168.220.23']",
    "pokecom.goldenrod.city": "['192.168.220.14']",
    "pokemart.goldenrod.city": "['192.168.220.17']",
    "pokemon-center.goldenrod.city": "['192.168.220.16']"
}
key_list = list(records)
def pollDNS(dnsServer):
    try:
        dns_query = Nslookup(dns_servers=[dnsServer])
        rand = random.randint(0,6)
        ips_record = dns_query.dns_lookup(key_list[rand])

        if ips_record.answer == []:
            return False
        elif ips_record.answer == ast.literal_eval(records[key_list[rand]]):
                return True
        return False
    except Exception as e:
        print(e)
        return False

def pollSMTP(ip, from_addr, to_addr):
    try:
        with smtplib.SMTP(ip, 25) as server:
            server.sendmail(from_addr, to_addr, 'Hey there!')
        return True
    except:
        return False
