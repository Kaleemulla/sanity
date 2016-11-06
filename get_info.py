import sys
import math
import _mysql
import re,ConfigParser

from remote.connection import ssh_collect

user = "em7admin"
port = "22"
timeout = "15"
debug = 0
command1 = "nproc --all"
command2 = "cat /proc/meminfo|grep MemTotal| sed 's/ \+/ /g'"
command3 = "df | sed 's/ \+/ /g'"
command4 = "df -h | sed 's/ \+/ /g' |grep / |head -1"
command5 = "df -h | sed 's/ \+/ /g' |grep opt"
command6 = "df -h | sed 's/ \+/ /g' |grep data01"
command7 = "df -h | sed 's/ \+/ /g' |grep data02"


def final(count, ret):
        if (count in (1,5,7)):
                ret+= "<tr></tr>"
        ret+= "<tr></tr><tr bgcolor=#b5bedb><td></td><td></td><td></td><td></td></tr>"

        final = "<tr><td rowspan=\""+ str(count) + "\">" + ret
        return final


def sanity_check(debug, server, user, port, timeout):

                ret = ""
                count = 4


                if (debug == "1"):
                        print "\n************** Working on Host "+ server +"\n"


                try:
                        con = _mysql.connect(host = "172.19.254.21", user = "root", passwd = "em7admin", port=int(7706), db = "standards")

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


                stdin1, stdout1, stderr1, ssh1 = ssh_collect(server, user, port, timeout, command1)

                if((len(stdout1) == 0) or ("Error" in stderr1)):
                        ret+= "" + str(server) + "</td><td> Server Check </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td>"+stderr1 +"</td></tr>"
                        return final(1, ret)


                stdin2, stdout2, stderr2, ssh2 = ssh_collect(server, user, port, timeout, command2)
                stdin3, stdout3, stderr3, ssh3 = ssh_collect(server, user, port, timeout, command3)
                stdin4, stdout4, stderr4, ssh4 = ssh_collect(server, user, port, timeout, command4)


                if (int(stdout1[0]) >= int(vcpu)):
                        ret+= "" + str(server) + "</td><td> vCPU Cores </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Count:"+vcpu+"<br> Current Count:"+ stdout1[0] +"</td></tr>\n"
                else:
                        ret+= "" + str(server) + "</td><td> vCPU Cores </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Count:"+vcpu+"<br> Current Count:"+ stdout1[0] +"</td></tr>\n"

                if (round(float(stdout2[0].split(" ")[1])/1024/1000) >= float(ram)):
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> Ram Size </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:"+ram+"<br>Current Size:"+ str(round(int(stdout2[0].split(" ")[1])/1024/1000))+ "</td></tr>\n"
                else:
                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> Ram Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:"+ram+"<br>Current Size:"+ str(round(int(stdout2[0].split(" ")[1])/1024/1000))+ "</td></tr>\n"

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
                        count = 7
                        stdin6, stdout6, stderr6, ssh6 = ssh_collect(server, user, port, timeout, command6)
                        stdin7, stdout7, stderr7, ssh7 = ssh_collect(server, user, port, timeout, command7)

                        if(len(stdout6) == 0):
                                ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /data01 Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Partition Not Found </td></tr>\n"
                        else:
                                if (float(stdout6[0].split(" ")[1][:-1]) >= float(data01)):
                                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /data01 Size </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" + str(data01) +"G <br> Current Size:"+ str(stdout6[0].split(" ")[1])+ "</td></tr>\n"
                                else:
                                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /data01 Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" + str(data01) +"G <br> Current Size:"+ str(stdout6[0].split(" ")[1])+ "</td></tr>\n"

                        if(len(stdout7) == 0):
                                ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /data02 Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Partition Not Found </td></tr>\n"
                        else:
                                if (float(stdout7[0].split(" ")[1][:-1]) >= float(data02)):
                                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /data02 Size </td><td> <font color=green> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" +str(data02) +"G <br> Current Size:"+ str(stdout7[0].split(" ")[1])+ "</td></tr>\n"
                                else:
                                        ret+= "<tr><td style=display:none>"+ str(server) +"</td><td> /data02 Size </td><td> <font color=red> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" +str(data02) +"G <br> Current Size:"+ str(stdout7[0].split(" ")[1])+ "</td></tr>\n"

                        ssh6.close()
                        ssh7.close()


                return final(count, ret)



if __name__ == "__main__":

        search = raw_input("Enter Customer Name: ")
        vm_count = 0

        if(len(sys.argv)>1):
                debug = sys.argv[1]
        else:
                debug = 0

        try:
                con = _mysql.connect(host = "172.19.254.21", user = "root", passwd = "em7admin", port=int(7706), db = "master_dev")

                con.query("select * from standards.cust_octet where cust_name like '%" + search +"%'")
                result = con.store_result()
                octet = result.fetch_row()[0][1]

                con.query("select distinct(device) from legend_device where ip like '" +octet+ "%' and (device like '%em7pr%' or device like '%em7mc%' or device like '%em7dc%' or device like '%em7db%') order by id desc ")
                result_1 = con.store_result()

                con.query("select distinct(device) from legend_device where ip like '" +octet+ "%' and (device like '%spld%' or device like '%splm%' or device like '%splsr%' or device like '%splin%' or device like '%rly%') order by id desc ")
                result_2 = con.store_result()

                html  = open("sanity_html_old.txt","r")
                display = html.read()
                check_list = ""

                print "****"
                for row in result_1.fetch_row(100):
                        check_list+= sanity_check(debug, row[0], user, port, timeout)
                        vm_count+=1

                print "****"
                for row in result_2.fetch_row(100):
                        check_list+= sanity_check(debug, row[0], "root", port, timeout)
                        vm_count+=1

                if (debug == 1):
                        print "Checklist completed ...... \n\n"

                display = display.replace("Checklist Table", check_list)

                if (display.count("Failed") > display.count("Passed")):
                        display = display.replace("32CD32","E50000")

                display = display.replace("Sanity Results","Sanity Results - &nbsp&nbsp&nbsp Total VMs: "+ str(vm_count) +"&nbsp&nbsp&nbsp Passed: "+ str(display.count("Passed")) + "&nbsp&nbsp&nbsp Failed: "+ str(display.count("Failed")))

                if (debug == 1):
                        print "Writing output to HTML File...... \n\n"

                fw = open("/opt/em7/gui/ap/www/cms_op.html","w")
                fw.write(display)
                fw.close()


        except _mysql.Error, e:

                print "Error %d: %s" % (e.args[0], e.args[1])

        finally:
                if con:
                        con.close()


