import socket
from datetime import datetime
import time
import psycopg2
import psycopg2.extras
from connectpyse.service import tickets_api,ticket,boards_api,board

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
time_stamp=datetime.now().replace(microsecond=0).isoformat()
hostname = "nocdbserver.southafricanorth.cloudapp.azure.com"
port_id = "5432"
database = "integraDB"
username = "postgres"
pwd = "war49jik#"
cwm_url= 'https://api-eu.myconnectwise.net/v4_6_release/apis/3.0'
cwm_auth={'Authorization': 'Basic dHVycml0bytwRkNIZ0Q3M0dWWU1SckJkOlgzZEF1QVpLTDAwOWZubVg=', 'clientId': '7682c495-9be9-4f25-a4a2-91f0a65184ba'}
cwm_api=tickets_api.TicketsAPI(url=cwm_url,auth=cwm_auth)
cwm_board_api=boards_api.BoardsAPI(url=cwm_url,auth=cwm_auth)


def getLinkState(ip_addy):
        conn=None
        cur=None

        try:
                conn = psycopg2.connect(
                        host=hostname, dbname=database, password=pwd, port=port_id, user=username
                )
                cur = conn.cursor() 
                query = "SELECT * FROM respublica WHERE ip_address like %s"
                cur.execute(query,(ip_addy,))
                return cur.fetchone()
                
        except Exception as error:
                print(error)
        finally:
                if cur is not None:
                        cur.close()
                if conn is not None:
                        conn.close()


def updateLinkState(t_stamp,lstatus,ip_addy):       

        conn = None
        cur = None
        try:
                conn = psycopg2.connect(
                        host=hostname, dbname=database, password=pwd, port=port_id, user=username
                )
                conn.autocommit = True
                cur = conn.cursor() 
                query = "UPDATE respublica SET is_time = %s,link_state = %s WHERE ip_address = %s"
                updated_rows=cur.rowcount
                cur.execute(query,(t_stamp,lstatus,ip_addy  ))
                
        except Exception as error:
                print(error)
        finally:
                if cur is not None:
                        cur.close()
                if conn is not None:
                        conn.close()
        return updated_rows

def saveLinkState(t_stamp,site,ip_address, lstatus):       

        conn = None
        cur = None
        try:
                conn = psycopg2.connect(
                        host=hostname, dbname=database, password=pwd, port=port_id, user=username
                )
                conn.autocommit = True
                cur = conn.cursor() 
                query = """INSERT INTO respublica(is_time,alert_site,ip_address,link_state) VALUES (%s,%s,%s,%s)"""
                query_values = (t_stamp,site,ip_address,lstatus)
                cur.execute(query,query_values)
                
        except Exception as error:
                print(error)
        finally:
                if cur is not None:
                        cur.close()
                if conn is not None:
                        conn.close()

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

def link_ticket(summary,initialDescription,board_ref,company_ref):        
        ticket_details = ticket.Ticket({"summary":summary, "initialDescription":initialDescription,"board": board_ref, "company":company_ref })
        cwm_api.create_ticket(ticket_details)
        

#for row in getLinkState():
#        print("Time Stamp =" , row[1])
#        print("Site = ", row[2])
#        print("IP Addy = ", row[3])
#        print("Link State = ", row[4],"\n")
#sd_board=cwm_board_api.get_board_by_id(35)

for ip in sitedict:
    #print(sitedict.get(ip))
    old_state=getLinkState(sitedict.get(ip))
    print("Old Link State = ", old_state)
   
    if old_state:
        if checkHost(sitedict.get(ip), port) and old_state[4]!="UP" :
                print ('\x1b[6;30;42m' + ip + ' [' + sitedict.get(ip) + '] is UP'+ '\x1b[0m')
                updateLinkState(time_stamp,"UP", sitedict.get(ip))
        elif old_state[4]=="UP":
                print ('\x1b[4;37;41m' + ip + ' [' + sitedict.get(ip) + '] is Down')                
                link_ticket(f"Critical-Link Degraded: {ip}",f"The link with IP address {sitedict.get(ip)} appears to be down, HTTPS connection on port {port} not possible at this moment", board_ref={"id":35},company_ref={"id":20591})
                updateLinkState(time_stamp,"Down",sitedict.get(ip))
                
    else:
                if checkHost(sitedict.get(ip), port):
                        print ('\x1b[6;30;42m' + ip + ' [' + sitedict.get(ip) + '] is UP'+ '\x1b[0m')
                        saveLinkState(time_stamp, ip,sitedict.get(ip), "UP")
                else:
                        print ('\x1b[4;37;41m' + ip + ' [' + sitedict.get(ip) + '] is Down')
                        saveLinkState(time_stamp, ip,sitedict.get(ip), "Down")
