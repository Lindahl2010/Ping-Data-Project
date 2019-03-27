import os, platform, subprocess
import sched, time
import mysql.connector
from mysql.connector import errorcode
import sys
import re

def ping(hostname):

    param = "-n" if platform.system() == "Windows" else "-c"
    command = ["ping", param, "5", hostname]
    out = open("ping.txt", "a")

    return subprocess.call(command, stdout = out) == 0

def parse_file(pingFile):

    resp_data = list()  
    pattern_list = ["ping statistics for", "packets", "minimum"]
    ip_addr = list()
    
    try:
        with open(pingFile, "rt") as in_file:
            for linenum, line in enumerate(in_file):
                for i in pattern_list:
                    pattern = re.compile(i, re.IGNORECASE)
                    if pattern.search(line) != None:
                        resp_data.append((linenum, line.rstrip("\n")))
                        if i == pattern_list[0]:
                            ip_addr.append(line.rstrip("\n"))
                        if i == pattern_list[1]:
                            ip_addr.append(line.rstrip("\n"))
            for linenum, line in resp_data:
                print("Line ", linenum, ": ", line)

        with open("resp_data.txt", "w") as out_file:
            for linenum, line in resp_data:
                out_file.write("%s\n" % line)

        print(ip_addr)

    except FileNotFoundError:
        print("Log file not found.")

    return

def db_conn():

    try:
        conn = mysql.connector.connect(host="192.168.26.139", database="demodb",
        user="lindahlish", password="xanthosis627")

        cursor = conn.cursor()

        #with open("resp_data.txt", "rt") as in_file:


        add_data = ("INSERT INTO Connection"
        "(IP_Address, Sent, Received, Lost, Min, Max, Avg)"
        "VALUES (%s, %(sent)s, %(rec)s, %(lost)s, %(min)s, %(max)s, %(avg)s)")

        #data_ping = 


        cursor.execute(add_data, data_ping)

        if connection.is_connected():
            print("connection successful")

        conn.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password...")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist...")
        else:
            print(err)



#ping("www.google.com")
parse_file("ping.txt")
#db_conn()