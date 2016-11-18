#!/usr/bin/python

import os
import sys
import time
import _mysql
from remote.mail import send_mail
import cgi, cgitb
from multiprocessing.pool import ThreadPool as Pool

delayed = ""
delay = 0

pool = Pool(100)

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def sql_crawl(host, sql, cust, col):

        fetched = ""
        count = 0


        try:
                con = _mysql.connect(host = host, user = "root", passwd = "em7admin", port=int(7706), db = "master_events")

                con.query(sql)
                result = con.store_result()

                #if(avg is not None):
                fetched += "<tr bgcolor=#DAF7A6><td colspan=\""+ str(len(col)) +"\"><center><b>"+cust[host]+"</td></tr> HEADER"

                for row in result.fetch_row(1000):
                        get = list(row)
                        fetched+= "<tr bgcolor=#E4E2DF>"
                        for each in get:
                                fetched += "<td>"+each+"</td>"
                        fetched += "</tr>\n"
                        count +=1


                heading = "<tr bgcolor=#D2B4DE>"

                for c in col:
                        if("as" in c):
                                heading +="<td><b>" + c.split("as")[1] +"</td>"
                        else:
                                heading +="<td><b>" + c +"</td>"

                heading +="</tr>"
                #fetched = fetched.replace("ROWCOUNT",4)

                if(count > 0):
                        fetched = fetched.replace("HEADER",heading)
                else:
                        fetched = fetched.replace("HEADER","")


                con.close()

        except _mysql.Error, e:
                return "<br><h2><font color=red><center><b>SQL Query Error !!!!!!! </h2>"

        return fetched


if __name__ == "__main__":

        form = cgi.FieldStorage()

        get = form.getvalue("query")
        get = str(get)
        #get = get.replace("select","")
        get = get.replace(";","")
        #get = 'max(time) from (select TIMEDIFF(t.date_create,e.date_active) as time from master_events.events_active  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active and t.date_create > e.date_last and t.date_create > subdate(now(),interval 1 day) UNION ALL select TIMEDIFF(t.date_create,e.date_active) as time from master_events.events_cleared  e JOIN master_biz.ticketing t  where e.tid=t.tid and t.date_create > e.date_active and t.date_create > e.date_last and t.date_create > subdate(now(),interval 1 day)) s'


        print "Content-type:text/html\r\n\r\n"
        #print "Hello"

        if ("select" in get.lower()[:9]):
                get = get
        else:
                get = 'select ' + get

        if ("limit" in get.lower()):
                sql = get
        else:
                sql = get + ' limit 500'

        data = open("hosts","r").readlines()
        html  = open("html_sql.txt","r")

        report = html.read()
        cust = {}
        hosts = []
        check_list = ""

        if (("delete" in sql.lower()) or ("update" in sql.lower()) or ("select *" in sql.lower()) ):
                check_list = "<br><h2><font color=red><center><b>This Query is Restricted !!!!!!! </h2>"
        else:
                for i in range(0,len(data),2):
                        key = data[i+1].rstrip("\n")
                        value = data[i].rstrip("\n")

                        hosts.append(key)
                        cust[key]=value

                r = get.replace("select","")
                x = r.split("from" or "From" or "FROM")[0]
                col = x.split(",")

                for host in hosts:
                        pool.apply_async(sql_crawl, (host,sql,cust,col,), callback = log_result)


                pool.close()
                pool.join()

                for table_row in result_list:
                        check_list += str(table_row)


        report = report.replace("SQLQ",sql)
        report = report.replace("REPORT", check_list)


        fw = open("/opt/lampp/htdocs/sql.html","w")
        fw.write(report)
        fw.close()

        print "<meta http-equiv=\"refresh\" content=\"0; url=http://alln1qssntyp01/sql.html\" />"


