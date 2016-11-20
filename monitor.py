import os
import time
import _mysql
from remote.mail import send_mail

delayed = ""
delay = 0

def check_delay(hosts, cust):

        delayed = ""
        delay = 0
        count = 0

        for host in hosts:
                #print "Running Delay Check on Host: "+ str(host)
                count = 0

                try:
                        con = _mysql.connect(host = host, user = "root", passwd = "em7admin", port=int(7706), db = "master_events")


                        con.query("select e.id,e.tid,e.Xid,e.Xname,e.date_last,e.date_first,e.date_active,t.date_create,TIMEDIFF(t.date_create,e.date_active) as time from master_events.events_active  e JOIN master_biz.ticketing t where e.tid=t.tid and t.date_create > e.date_active and t.date_create > subdate(now(),interval 1 hour) and e.ecounter=1  order by time desc;")
                        result1 = con.store_result()
                        total = result1.num_rows()

                        con.query("select e.id,e.tid,e.Xid,e.Xname,e.date_last,e.date_first,e.date_active,t.date_create,TIMEDIFF(t.date_create,e.date_active) as time from master_events.events_cleared  e JOIN master_biz.ticketing t where e.tid=t.tid and t.date_create > e.date_active and t.date_create > subdate(now(),interval 1 hour) and e.ecounter=1  order by time desc;")
                        result2 = con.store_result()
                        total += result2.num_rows()


                        delayed += "<tr bgcolor=#DAF7A6><td colspan=9><b><center> "+cust[host]+" --  Total: "+str(total)+" Delayed: COUNTED</td></tr> HEADER"


                        for row in result1.fetch_row(1000):
                                get = list(row)
                                if((int(get[8].split(":")[1]) > 1) or (int(get[8].split(":")[0]) >0)):
                                        delay = 1
                                        delayed+= "<tr bgcolor=#E4E2DF>"
                                        for each in get:
                                                delayed+= "<td>"+each+"</td>"
                                        delayed+= "</tr>\n"
                                        count += 1

                        for row in result2.fetch_row(1000):
                                get = list(row)
                                if((int(get[8].split(":")[1]) > 1) or (int(get[8].split(":")[0]) >0)):
                                        delay = 1
                                        delayed+= "<tr bgcolor=#E4E2DF>"
                                        for each in get:
                                                delayed+= "<td>"+each+"</td>"
                                        delayed+= "</tr>\n"
                                        count +=1

                        delayed = delayed.replace("COUNTED",str(count))

                        if(count > 0):
                                delayed = delayed.replace("HEADER","<tr bgcolor=#D2B4DE><td><b>Event ID</td><td><b> Ticket ID </td><td><b> Device ID </td><td><b> Device Name </td><td><b>Event Last Occurred </td><td><b> Event Fisrt Occurred </td><td><b> Event Activated </td><td><b> Ticket Created </td><td><b> Delay in Ticket Creation </td></tr>")
                        else:
                                delayed = delayed.replace("HEADER","")

                        con.close()

                except _mysql.Error, e:
                        #print "Error %d: %s" % (e.args[0], e.args[1])
                        x=1


        if(delay == 1):
                html = open("html_new.txt","r")
                report = html.read()
                report = report.replace("REPORT",delayed)
                send = ['rorajpal@cisco.com','kasharie@cisco.com']

                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "kasharie@cisco.com" ,"")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "rakmenon@cisco.com" ,"")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "sshnmuga@cisco.com" ,"")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "anababu@cisco.com","")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "nbhalla@cisco.com","")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "johnevan@cisco.com","")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "cstg-cms-incmgmt@cisco.com","")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "arnsengu@cisco.com","")
                send_mail(report, "QS Ticketing Delay Report for Last 1hr", "qs-automation-reports@cisco.com", "rorajpal@cisco.com","")

if __name__ == "__main__":

        while(1):
                data = open("hosts","r").readlines()
                html  = open("html_new.txt","r")

                report = html.read()
                cust = {}
                hosts = []

                for i in range(0,len(data),2):
                        key = data[i+1].rstrip("\n")
                        value = data[i].rstrip("\n")

                        hosts.append(key)
                        cust[key]=value

                table = check_delay(hosts, cust)
                #break
                time.sleep(3600)


