import os, platform, subprocess
import sched, time
import mysql.connector
from mysql.connector import errorcode
import sys
import re

# Function to pass in a web address to ping 
def ping_test():

    hostname = input("Please enter a website to ping: ")
    param = "-n" if platform.system() == "Windows" else "-c"
    command = ["ping", param, "5", hostname]
    out = open("ping.txt", "a")

    return subprocess.call(command, stdout = out) == 0

# Ping class for grouping all of the data, making a ping object
class PingData():

    alldata, ipaddress, response, replyi = ([] for i in range(4))

    def __init__(self, ipaddr, resp, reply):
        self.ipaddr = ipaddr
        self.resp = resp
        self.reply = reply
        PingData.ipaddress.append(ipaddr)
        PingData.response.append(resp)
        PingData.replyi.append(reply)
        PingData.alldata.append(self)

# Function for parsing through the file  
def parse_file(pingFile):

    # Initialized empty lists
    resp_data, ipaddr, resp, reply = ([] for i in range(4))

    # pattern_list = ["ping statistics for", "packets", "minimum"]
    
    # Try catch for catching any errors when parsing through the lists/file
    try:

        ping_test()

        with open(pingFile, "rt") as in_file:
            # for linenum, line in enumerate(in_file):
            #     for i in pattern_list:
            #         pattern = re.compile(i, re.IGNORECASE)
            #         if pattern.search(line) != None:
            #             resp_data.append((linenum, line.rstrip("\n")))
            #             parse = re.compile("\d+")
            #             values.append(parse.findall(line))
            
            # For loop designed to implement a switch case type of design from C#
            for linenum, line in enumerate(in_file):
                resp_data.append((linenum, line.rstrip("\n")))
                for i in range(0,3):
                    parse = re.compile("\d+")
                    if i == 0:
                        arg = 0
                        pattern = re.compile(switch_case(arg), re.IGNORECASE)
                        if pattern.search(line) != None:
                            ipaddr.append(".".join(parse.findall(line)))
                    elif i == 1:
                        arg = 1
                        pattern = re.compile(switch_case(arg), re.IGNORECASE)
                        if pattern.search(line) != None:
                            resp.append(" ".join(parse.findall(line)))
                    elif i == 2:
                        arg = 2
                        pattern = re.compile(switch_case(arg), re.IGNORECASE)
                        if pattern.search(line) != None:
                            reply.append(" ".join(parse.findall(line)))
                    else:
                        break
            
            pinglist = []
            for i in range(0,len(ipaddr)):
                ping = PingData(ipaddr[i], resp[i], reply[i])
                pinglist.append(ping)

            db_conn(pinglist)

    except FileNotFoundError:
        print("Log file not found.")

    return

# Database connection & insertion function
def db_conn(pinglist):

    try:
        conn = mysql.connector.connect(host="192.168.26.139", database="demodb",
        user="lindahlish", password="xanthosis627")

        cursor = conn.cursor()

        add_data = ("INSERT INTO Connection"
        "(IP_Address, Sent, Received, Lost, Min, Max, Avg)"
        "VALUES (%(IP_Address)s, %(sent)s, %(rec)s, %(lost)s, %(min)s, %(max)s, %(avg)s)")

        add_file = ("INSERT IGNORE INTO pingtxt (id, data) VALUES (%s, %s)")

        with open("ping.txt", "rt") as in_file:
            for linenum, line in enumerate(in_file):
                id = int(linenum)
                data = line.rstrip("\n")
                data_text = (id, data)
                cursor.execute(add_file, data_text)

        for ping in pinglist:
            for ip in ping.ipaddress:
                IP_Address = ip
            for resp in ping.response:
                sent = resp[0]
                rec = resp[2]
                lost = resp[4]
            for rep in ping.replyi:
                min = rep[0]
                max = rep[2]
                avg = rep[4]

        data_ping = {
            'IP_Address': IP_Address,
            'sent': sent,
            'rec': rec,
            'lost': lost,
            'min': min,
            'max': max,
            'avg': avg
        }

        cursor.execute(add_data, data_ping)

        if conn.is_connected():
            print("connection successful")

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password...")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist...")
        else:
            print(err)

# Switch case arguments to search through the ping data file
def switch_case(arg):

    switcher = {
        0: "ping statistics for",
        1: "packets",
        2: "minimum"
    }

    return switcher.get(arg, "Result not found.")

parse_file("ping.txt")