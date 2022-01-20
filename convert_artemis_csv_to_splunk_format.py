#!/usr/bin/python

import csv
import os.path
import logging

header = []
file_to_read = "/opt/ngp/artemis.csv"
file_to_write = "/opt/ngp/send_to_splunk.csv"
splunk_server = "10.4.30.137"
grep_filter = 'NAME|flowDataChannel|policyFlowDataChannel|probeSipFlowDataChannel|detentionCenterNorthboundChannel|probeSipInviteDataChannel'

def sendSyslog():
     cmd = 'logger -n ' + splunk_server + ' -p user.notice -f ' + file_to_write
     try:
          os.system(cmd)
          #print(cmd)
     except:
          logging.exception("Logger command failed...")

def createCsv():
     cmd = '/opt/ngp/apache-artemis/bin/artemis queue stat | grep -E \'' + grep_filter + '\' | /bin/sed -e \'s/\s*|/,/g; s/^,\|,$//g\' > ' + file_to_read
     try:
          os.system(cmd)
          #print(cmd)
     except:
          logging.exception("Syslog send failed...")

def getHeaderAndRows(fn):
     file = open(fn)
     type(file)
     csvreader = csv.reader(file)
     header = next(csvreader)

     rows = []
     for row in csvreader:
          x = 0
          result = ""
          for item in row:
               result = result + header[x] + "=\"" + row[x] + "\";"
               x = x + 1
          rows.append(result)
     file.close()
     return rows

def writeFile(rows):
     f = open(file_to_write, "w")
     for i in rows:
          f.write(i)
          f.write('\n')
     f.close()

def main():
     createCsv()
     
     if os.path.exists(file_to_read):
        rows = getHeaderAndRows(file_to_read)
        writeFile(rows)
     else:
        print("Rekt.  The file '" + file_to_read + "' does not exist.")
        print("Check the 'file_to_read' variable in the code.")
     
     sendSyslog()

if __name__ == "__main__":
    main()
