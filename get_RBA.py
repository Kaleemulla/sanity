import re
import _mysql

from remote.connection import ssh_collect
from remote.mail import send_mail


command1 = "find /backup/em7/config -size +10k -exec ls -lRth {} \+"
command2 = "find /backup/em7/full -size +10k -exec ls -lRth {} \+"
user = "root"
port = "22"
timeout = "15"


def get_RBA(host):

        map_cust = {100:'Customer0', 101:'Macquire Bank', 102:'Microsoft', 103:'ADM', 104:'BSE', 105:'MQB DR', 107:'BMO', 108:'Timken', 109:'CHoA', 111:'IBCH', 112:'Vodafone', 113:'KPN', 115:'DTVOps', 116:'DTV DR', 117:'Optus', 118:'Ford', 119:'Emaas', 122:'SAP', 123:'BTSIG', 124:'ISAT', 125:'CNA', 126:'Caas', 128:'CHI', 129:'Zurich', 130:'CHI-DR', 131:'Western Union', 133:'Live Nation', 138:'WayFair', 139:'MTN-Ericsson', 82:'BaskDunk', 85:'Cox', 88:'Rogers', 91:'TWC', 120:'Baxalta'}

        ret = ""
        server = host
        if(int(host.split(".")[1]) == 19):
                octet = int(host.split(".")[2])
        else:
                octet = int(host.split(".")[3])

        try:

                con = _mysql.connect(host = host, user = "root", passwd = "em7admin", port=int(7706), db = "master_logs")


                con.query("select left(message, 90), count(*) Cnt from master_logs.notifier_log where date_time >= DATE_ADD(CURDATE(), INTERVAL - 10 DAY) group by left(message, 90) order by Cnt desc limit 15;")
                result = con.store_result()


                delayed = ""
                delay = 0
                full_row = "<tr><td colspan=2><b><font color=brown; size=6px><center>Results for "+map_cust[octet]+"</td></tr><tr><td><b>Automation Policy</td><td><b> Trigger Count </td></tr>"
                column = ""

                for row in result.fetch_row(100):
                        get = list(row)
                        #print get
                        full_row+= "<tr>"
                        column = ""
                        for each in get:
                                column+= "<td>"+each+"</td>"
                        full_row+= column+"</tr>\n"

                con.close()
        except _mysql.Error, e:

                print "Error %d: %s" % (e.args[0], e.args[1])


        return full_row



if __name__ == "__main__":
        hosts = open("hosts_RBA","r")
        html  = open("html_RBA.txt","r")

        report = html.read()
        table = ""

        for host in hosts:
                print "Running RBA Check on Host: "+ str(host)
                table+= get_RBA(host)

        report = report.replace("REPORT",table)


        send_mail(report, "RBA Report", "qs-automation-reports@cisco.com", "kasharie@cisco.com", "")
        send_mail(report, "RBA Report", "qs-automation-reports@cisco.com", "nbhalla@cisco.com", "")
        send_mail(report, "RBA Report", "qs-automation-reports@cisco.com", "anababu@cisco.com", "")
        send_mail(report, "RBA Report", "qs-automation-reports@cisco.com", "rorajpal@cisco.com", "")
        #send_mail(report, "Customer Backup Report", "qs-automation-reports@cisco.com", "cstg-cms-servicedesk@cisco.com", "")


