import socket
import time

sitedict={
    "Bryanston New Head Office - 100 Meg DIA": "105.22.45.26",
    "Eastwood Hatfield - Primary 200 Meg DIA": "105.27.152.106",
    "Hatfield Square - Primary 1 Gig DIA":"105.27.171.94",
    "Hatfield Square - Secondary 5Meg":"197.234.191.170",
    "Lincoln House - Primary 300 Meg DIA":"197.159.42.2",
    "Princeton House - 500Meg":"105.27.176.242",
    "Roscommon House - Primary 500 Meg DIA":"196.250.54.42",
    "Saratoga Village - Primary 500 Meg DIA":"196.250.39.82",
    "The Fields - Primary 100 Meg DIA":"105.29.89.179",
    "Urban Nest - 200MB Fibre":"105.27.144.78",
    "West City - Primary 500 Meg DIA":"196.250.48.202",
    "Yale Village - Primary 300 Meg DIA":"105.27.202.198",
    "Eastwood Hatfield - Secondary 20 Meg DIA":"102.134.218.177",
    "Lincoln House - Secondary 20 Meg DIA":"102.134.218.163",
    "Princeton House - Secondary 20 Meg DIA":"154.73.208.206",
    "Roscommon House - Secondary 20 Meg DIA":"197.234.162.34",
    "Saratoga Village - Secondary 20 Meg DIA":"102.134.218.165",
    "The Fields - Secondary 20 Meg DIA":"102.134.218.95",
    "Urban Nest - Secondary 20 Meg DIA":"102.134.218.179",
    "West City - Secondary 20 Meg DIA":"102.134.218.181",
    "Yale Village - Secondary 20 Meg DIA":"102.134.217.242"
}

port = 9898
retry = 5
delay = 2
timeout = 3

def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup


for ip in sitedict:
    #print(sitedict.get(ip))
    if checkHost(sitedict.get(ip), port):
        print ('\x1b[6;30;42m' + ip + ' [' + sitedict.get(ip) + '] is UP'+ '\x1b[0m')
    else:
        print ('\x1b[4;37;41m' + ip + ' [' + sitedict.get(ip) + '] is Down')
