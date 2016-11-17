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
        l = []

        for host in hosts:
                #print "Running Delay Check on Host: "+ str(host)


                try:
                        con = _mysql.connect(host = host, user = "root", passwd = "em7admin", port=int(7706), db = "master_events")

                        con.query("select min(time),max(time),avg(time) from (select TIMEDIFF(t.date_create,e.date_active) as time from master_events.events_active  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active  and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1 UNION ALL select TIMEDIFF(t.date_create,e.date_active) as time from master_events.events_cleared  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active and t.date_create > e.date_last and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1) s")
                        result1 = con.store_result()
                        row = result1.fetch_row(1)
                        mini = row[0][0]
                        maxi = row[0][1]

                        con.query("select avg(time) from (select TIME_TO_SEC(TIMEDIFF(t.date_create,e.date_active)) as time from master_events.events_active  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active  and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1 UNION ALL select TIME_TO_SEC(TIMEDIFF(t.date_create,e.date_active)) as time from master_events.events_cleared  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active and t.date_create > e.date_last and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1) s")

                        result2 = con.store_result()
                        row = result2.fetch_row(1)
                        avg = row[0][0]

                        if(avg is not None):
                                avg = float('%.3f'%(float(avg)/60.0))

                        con.query("select count(*) from (select e.id id,e.tid tid,e.Xid Xid,e.Xname Xname,e.date_last date_last,e.date_first date_first,e.date_active date_active,t.date_create date_create,TIMEDIFF(t.date_create,e.date_active) time from master_events.events_active  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1 group by e.id UNION ALL select e.id id,e.tid tid,e.Xid Xid,e.Xname Xname,e.date_last date_last,e.date_first date_first,e.date_active date_active,t.date_create date_create,TIMEDIFF(t.date_create,e.date_active) time from master_events.events_cleared  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1 group by e.id ) s")
                        result3 = con.store_result()
                        total = result3.fetch_row(1)[0][0]




                        con.query("select count(*) from (select e.id id,e.tid tid,e.Xid Xid,e.Xname Xname,e.date_last date_last,e.date_first date_first,e.date_active date_active,t.date_create date_create,TIMEDIFF(t.date_create,e.date_active) time from master_events.events_active  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1 group by e.id having time > \"00:02:00\" UNION ALL select e.id id,e.tid tid,e.Xid Xid,e.Xname Xname,e.date_last date_last,e.date_first date_first,e.date_active date_active,t.date_create date_create,TIMEDIFF(t.date_create,e.date_active) time from master_events.events_cleared  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active  and t.date_create > subdate(now(),interval 1 day) and e.ecounter=1 group by e.id having time > \"00:02:00\" ) s")
                        result4 = con.store_result()
                        dela = result4.fetch_row(1)[0][0]

                        if(avg is not None):
                                if (avg < 3):
                                        delayed += "<tr bgcolor=#89F39E><td><b>"+cust[host]+"</td><td> "+str(mini)+"</td><td>"+str(maxi)+"</td><td>"+str(total)+" </td><td>"+str(dela)+"</td><td>"+str(avg)+ "</td></tr>\n"
                                elif(avg > 3 and avg < 8):
                                        delayed += "<tr bgcolor=#F3EC0C><td><b>"+cust[host]+"</td><td> "+str(mini)+"</td><td>"+str(maxi)+"</td><td>"+str(total)+" </td><td>"+str(dela)+"</td><td>"+str(avg)+ "</td></tr>\n"
                                elif(avg >=8):
                                        delayed += "<tr bgcolor=#F43308><td><b>"+cust[host]+"</td><td> "+str(mini)+"</td><td>"+str(maxi)+"</td><td>"+str(total)+" </td><td>"+str(dela)+"</td><td>"+str(avg)+ "</td></tr>\n"
                        else:
                                delayed += "<tr bgcolor=#89F39E><td><b>"+cust[host]+"</td><td> "+str(mini)+"</td><td>"+str(maxi)+"</td><td>"+str(total)+" </td><td>"+str(dela)+"</td><td>"+str(avg)+ "</td></tr>\n"




                        con.close()

                except _mysql.Error, e:
                        #print "Error %d: %s" % (e.args[0], e.args[1])
                        x=1


        html = open("html_summary.txt","r")
        report = html.read()
        report = report.replace("REPORT",delayed)

        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "rakmenon@cisco.com" ,"")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "sshnmuga@cisco.com" ,"")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "johnevan@cisco.com","")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "cstg-cms-incmgmt@cisco.com","")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "nbhalla@cisco.com","")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "ggarg@cisco.com","")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "anababu@cisco.com","")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "kasharie@cisco.com","")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "arnsengu@cisco.com","")
        send_mail(report, "QS Ticketing Delay 24hrs Summary", "qs-automation-reports@cisco.com", "rorajpal@cisco.com","")

if __name__ == "__main__":

        while(1):
                data = open("hosts_mngr","r").readlines()
                html  = open("html_summary.txt","r")

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
                time.sleep(86400)


