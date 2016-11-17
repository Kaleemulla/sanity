import sys
import math
import _mysql

from remote.connection import ssh_collect
from remote.pconnection import pssh_collect
from remote.mail import send_mail

user = "em7admin"
port = "22"
timeout = "15"
command1 = "nproc --all"
command2 = "cat /proc/meminfo|grep MemTotal| sed 's/ \+/ /g'"
command3 = "df | sed 's/ \+/ /g'"
command4 = "df -h | sed 's/ \+/ /g' |grep / |head -1"
command5 = "df -h | sed 's/ \+/ /g' |grep opt"
command6 = "df -h | sed 's/ \+/ /g' |grep /var/log"
command7 = "df -h | sed 's/ \+/ /g' |grep /tmp"
command8 = "vgs |sed 's/ \+/ /g' |grep em7|head -1"

def sanity_check(server, user, port, timeout):

                ret = ""
                final = ""
                count = 3

                '''try:
                        con = _mysql.connect(host = "172.19.254.21",user = "root",passwd = "em7admin",port=int(7706),db = "standards")

                        if ("em7pr" in server):
                                con.query("select * from a_portals")
                        elif ("em7mc" in server):
                                con.query("select * from m_collector")
                        elif ("em7dc" in server):
                                con.query("select * from d_collector")
                        elif ("em7db" in server):
                                con.query("select * from e_database")
                        elif ("splin" in server):
                                con.query("select * from s_index")
                        elif ("splsrc" in server):
                                con.query("select * from s_head")
                        elif ("splm" in server or "spld" in server):
                                con.query("select * from s_masdep")
                        elif ("rly" in server):
                                con.query("select * from relay")

                        result = con.store_result()
                        row = result.fetch_row()

                except  _mysql.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])

                finally:
                        if con:
                                con.close()

                        vcpu = row[0][0]
                        ram = row[0][1]
                        hd = row[0][2]
                        root = row[0][3]

                        if ("splin" in server or "rly" in server):
                                opt = row[0][4]
                                data01 = row[0][5]
                                data02 = row[0][6]
                        if ("splm" in server or "spld" in server or "splsr" in server):
                                opt = row[0][4]


                stdin1, stdout1, stderr1, ssh1 = ssh_collect(server, user, port, timeout, command6)
                stdin2, stdout2, stderr2, ssh2 = ssh_collect(server, user, port, timeout, command7)
                '''

                if (sys.argv[1] == "1"):
                        print "\n************** Working on Host "+ server +"\n"

                '''if (int(stdout1[0]) == int(vcpu)):
                        ret+= "" + str(server) + "</td><td> vCPU Cores </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Count:"+vcpu+"<br> Current Count:"+ stdout1[0] +"</td></tr>\n"
                else:
                        ret+= "" + str(server) + "</td><td> vCPU Cores </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Count:"+vcpu+"<br> Current Count:"+ stdout1[0] +"</td></tr>\n"

                if (round(float(stdout2[0].split(" ")[1])/1024/1000) >= float(ram)):
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> Ram Size </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:"+ram+"<br>Current Size:"+ str(round(float(stdout2[0].split(" ")[1])/1024/1000))+ "</td></tr>\n"
                else:
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> Ram Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:"+ram+"<br>Current Size:"+ str(round(float(stdout2[0].split(" ")[1])/1024/1000))+ "</td></tr>\n"

                out_hd=0
                stdout3 = stdout3[1:]
                for line in stdout3:
                        out_hd+= long(line.split(" ")[1])
                out_hd = out_hd/1024/1024

                if (float(out_hd) >= float(hd)):
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> HD Size </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td>Actual Size:" + str(hd) +"G <br>Current Size:"+ str(out_hd) +"G </td></tr>\n"
                else:
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> HD Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td>Actual Size:" + str(hd) +"G <br>Current Size:"+ str(out_hd) +"G </td></tr>\n"

                if (float(stdout4[0].split(" ")[1][:-1]) >= float(root)):
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /root Size </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" + str(root) +"G <br> Current Size:"+ str(stdout4[0].split(" ")[1])+ "</td></tr>\n"
                else:
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /root Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" + str(root) +"G <br> Current Size:"+ str(stdout4[0].split(" ")[1])+ "</td></tr>\n"

                ssh1.close()
                ssh2.close()
                ssh3.close()
                ssh4.close()

                if ("splm" in server or "spld" in server or "splsr" in server or "splin" in server or "rly" in server):
                        count = 5
                        stdin5, stdout5, stderr5, ssh5 = ssh_collect(server, user, port, timeout, command5)
                        if(len(stdout5) == 0):
                                ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /opt Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Partition Not Found </td></tr>\n"
                        else:
                                if (float(stdout5[0].split(" ")[1][:-1]) >= float(opt)):
                                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /opt Size </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" + str(opt)+ "G <br> Current Size:"+ str(stdout5[0].split(" ")[1])+ "</td></tr>\n"
                                else:
                                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /opt Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" + str(opt)+ "G <br> Current Size:"+ str(stdout5[0].split(" ")[1])+ "</td></tr>\n"
                        ssh5.close()

                if ("splin" in server or "rly" in server):
                        count = 7'''
                stdin6, stdout6, stderr6, ssh6 = ssh_collect(server, user, port, timeout, command6)
                stdin7, stdout7, stderr7, ssh7 = ssh_collect(server, user, port, timeout, command7)
                stdin8, stdout8, stderr8, ssh8 = pssh_collect(server, user, port, timeout, command8)

                if(len(stdout6) == 0):
                        ret+= "" + str(server) + "</td><td> /var/log Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Partition Not Found </td></tr>\n"
                else:
                        if (float(stdout6[0].split(" ")[1][:-1]) >= float(5)):
                                ret+= "" + str(server) + "</td><td> /var/log Size </td><td>  Current Size:"+ str(stdout6[0].split(" ")[1])+ "</td></tr>\n"
                        else:
                                ret+= "" + str(server) + "</td><td> /var/log Size </td><td>  Current Size:"+ str(stdout6[0].split(" ")[1])+ "</td></tr>\n"

                if(len(stdout7) == 0):
                        ret+= "<tr><td> /tmp Size </td><td> Partition Not Found </td></tr>\n"
                else:
                        if (float(stdout7[0].split(" ")[1][:-1]) >= float(20)):
                                ret+= "<tr><td> /tmp Size </td><td>  Current Size:"+ str(stdout7[0].split(" ")[1])+ "</td></tr>\n"
                        else:
                                ret+= "<tr><td> /tmp Size </td><td>  Current Size:"+ str(stdout7[0].split(" ")[1])+ "</td></tr>\n"



                ret+= "<tr><td> vgdisplay Size </td><td>  VSize:"+str(stdout8.split("\n")[1].split(" ")[6]) +" <br> VFree:"+ str(stdout8.split("\n")[1].split(" ")[7])+ "</td></tr>\n"

                ssh6.close()
                ssh7.close()
                ssh8.close()

                if (count in (5,7)):
                        ret+= "<tr></tr>"
                ret+= "<tr bgcolor=#b5bedb><td></td><td></td><td></td><td></td></tr>"

                final = "<tr><td rowspan=\""+ str(count) + "\">" + ret
                return final



if __name__ == "__main__":

        connect_hosts = ['172.29.4.88','172.29.4.82','172.29.4.85','172.29.4.91']

        try:
                con = _mysql.connect(host = "172.19.254.21",user = "root",passwd = "em7admin",port=int(7706),db = "master_dev")

                fp = open("hosts_size","r")
                hosts = fp.readlines()

                for search in hosts:
                        search = search[:-1]
                        #print search[:-1]
                        con.query("select * from standards.cust_octet where cust_name like '%%" + search +"%%'")
                        result = con.store_result()
                        #print "-----------"+ result.fetch_row()[0][1]+"-------------"
                        octet = result.fetch_row()[0][1]
                        print octet

                        con.query("select distinct(device) from legend_device where ip like '" +octet+ "%' and (device like '%em7pr%' or device like '%em7mc%' or device like '%em7dc%' or device like '%em7db%') order by id desc ")
                        result_1 = con.store_result()

                        for row in result_1.fetch_row(100):
                                connect_hosts.append(row[0])

                html  = open("html_size.txt","r")
                display = html.read()
                check_list = ""

                print "****"
                for host in connect_hosts:
                        check_list+= sanity_check(host, user, port, timeout)

                if (sys.argv[1] == "1"):
                        print "Checklist completed ...... \n\n"

                display = display.replace("Checklist Table", check_list)

                if (display.count("Failed") > display.count("Passed")):
                        display = display.replace("32CD32","E50000")

                display = display.replace("Sanity Results","Sanity Results - &nbsp&nbsp&nbspPassed: "+str(display.count("Passed"))+ "&nbsp&nbsp&nbspFailed: "+str(display.count("Failed")))

                if (sys.argv[1] == "1"):
                        print "Writing output to HTML File...... \n\n"

                fw = open("/opt/em7/gui/ap/www/cms.html","w")
                fw.write(display)
                fw.close()


                send_mail(display, "Report for QS Customers", "qs-automation-reports@cisco.com", "kasharie@cisco.com" ,"")

        except _mysql.Error, e:

                print "Error %d: %s" % (e.args[0], e.args[1])

        finally:
                if con:
                        con.close()


