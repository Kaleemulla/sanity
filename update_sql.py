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
                con = _mysql.connect(host = host, user = "root", passwd = "em7admin", port=int(7706), db = "master")

                con.query(sql)

                con.close()

        except _mysql.Error, e:
                return "<br><h2><font color=red><center><b>SQL Query Error !!!!!!! </h2>"

        return fetched


if __name__ == "__main__":

        #form = cgi.FieldStorage()

        #get = form.getvalue("query")
        #get = str(get)
        #get = get.replace("select","")
        #get = get.replace(";","")
        #get = 'UPDATE master.policies_events mpe SET expiry_time = 240 WHERE eseverity = 0 AND expiry_time = 0;'
        sql = get


        print "Content-type:text/html\r\n\r\n"
        #print "Hello"

        '''if ("select" in get.lower()[:9]):
                get = get
        else:
                get = 'select ' + get

        if ("limit" in get.lower()):
                sql = get
        else:
                sql = get + ' limit 500'''

        data = open("hosts_update","r").readlines()
        html  = open("html_sql.txt","r")

        report = html.read()
        cust = {}
        hosts = []
        check_list = ""

        if (("delete" in sql.lower()) or ("select *" in sql.lower()) ):
                check_list = "<br><h2><font color=red><center><b>This Query is Restricted !!!!!!! </h2>"
        else:
                for i in range(0,len(data),2):
                        key = data[i+1].rstrip("\n")
                        value = data[i].rstrip("\n")

                        hosts.append(key)
                        cust[key]=value

                x = get.split("from" or "From" or "FROM")[0]
                col = x.split(",")

                for host in hosts:
                        pool.apply_async(sql_crawl, (host,sql,cust,col,), callback = log_result)


                pool.close()
                pool.join()

                for table_row in result_list:
                        check_list += str(table_row)


        report = report.replace("SQLQ",sql)
        report = report.replace("REPORT", check_list)


        fw = open("/opt/lampp/htdocs/sql_update.html","w")
        fw.write(report)
        fw.close()

        #print "<meta http-equiv=\"refresh\" content=\"0; url=http://alln1qssntyp01/sql.html\" />"


