import os, platform, subprocess
import sched, time
import mysql.connector
from mysql.connector import errorcode
import sys
import re

# Function to pass in a web address to ping 
def ping(hostname):

    param = "-n" if platform.system() == "Windows" else "-c"
    command = ["ping", param, "5", hostname]
    out = open("ping.txt", "a")

    return subprocess.call(command, stdout = out) == 0

# Ping class for grouping all of the data, making a ping object
class PingData():

    alldata = []

    def __init__(self, ipaddr, sent, rec, lost, min, max, avg):
        self.ipaddr = ipaddr
        self.sent = sent
        self.rec = rec
        self.lost = lost
        self.min = min
        self.max = max
        self.avg = avg
        PingData.alldata.append(self)

# Function for parsing through the file  
def parse_file(pingFile):

    # Initialized empty lists
    resp_data, ipaddr, resp, reply = ([] for i in range(4))

    # pattern_list = ["ping statistics for", "packets", "minimum"]
    
    # Try catch for catching any errors when parsing through the lists/file
    try:
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

    except FileNotFoundError:
        print("Log file not found.")

    return

# Database connection & insertion function
def db_conn():

    try:
        conn = mysql.connector.connect(host="192.168.26.139", database="demodb",
        user="lindahlish", password="xanthosis627")

        cursor = conn.cursor()

        add_data = ("INSERT INTO Connection"
        "(IP_Address, Sent, Received, Lost, Min, Max, Avg)"
        "VALUES (%s, %(sent)s, %(rec)s, %(lost)s, %(min)s, %(max)s, %(avg)s)")

        add_file = ("INSERT IGNORE INTO pingtxt (id, data) VALUES (%s, %s)")

        with open("ping.txt", "rt") as in_file:
            for linenum, line in enumerate(in_file):
                id = int(linenum)
                data = line.rstrip("\n")
                data_text = (id, data)
                cursor.execute(add_file, data_text)

        # file = open("ping.txt", "rt")
        # file_content = file.readlines()
        # for line in file_content:
        #     cursor.execute(add_file, (line.rstrip("\n"),))
        # file.close()

        #data_ping = 

        #cursor.execute(add_data, data_ping)

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

#ping("www.google.com")
parse_file("ping.txt")
db_conn()