import re
import math
import _mysql

from remote.connection import ssh_collect

user = "em7admin"
port = "22"
timeout = "5"
command1 = "nproc --all"
command2 = "cat /proc/meminfo|grep MemTotal| sed 's/ \+/ /g'"
command3 = "df | sed 's/ \+/ /g'"
command4 = "df -h | sed 's/ \+/ /g' |grep / |head -1"
command5 = "df -h | sed 's/ \+/ /g' |grep opt"
command6 = "df -h | sed 's/ \+/ /g' |grep data01"
command7 = "df -h | sed 's/ \+/ /g' |grep data02"


def final(count, ret):
        if (count in (5,7)):
                ret+= "<tr></tr>"
        ret+= "<tr></tr><tr bgcolor=#b5bedb><td></td><td></td><td></td><td></td></tr>"

        final = "<tr><td rowspan=\""+ str(count) + "\">" + ret
        return final


def sanity_check(server, user, port, timeout):

                ret = ""
                count = 4

                try:
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


                #stdin1, stdout1, stderr1, ssh1 = ssh_collect(server, user, port, timeout, command1)
                #stdin2, stdout2, stderr2, ssh2 = ssh_collect(server, user, port, timeout, command2)
                #stdin3, stdout3, stderr3, ssh3 = ssh_collect(server, user, port, timeout, command3)
                #stdin4, stdout4, stderr4, ssh4 = ssh_collect(server, user, port, timeout, command4)

                print "\n************** Details on Host "+ server +"\n"
                '''if (int(stdout1[0]) == int(vcpu)):
                        ret+= "<center>" + str(server) + "</td><td><center> vCPU Cores </td><td> <span class='badge bg-green'> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td><center> Actual Count:"+vcpu+"<br> Current Count:"+ stdout1[0] +"</td></tr>"
                else:
                        ret+= "<center>" + str(server) + "</td><td><center> vCPU Cores </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td><center> Actual Count:"+vcpu+"<br> Current Count:"+ stdout1[0] +"</td></tr>"

                if (round(float(stdout2[0].split(" ")[1])/1024/1000) >= float(ram)):
                        ret+= "<tr><td> Ram Size </td><td> <span class='badge bg-green'> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:"+ram+"<br>Current Size:"+ str(round(float(stdout2[0].split(" ")[1])/1024/1000))+ "</td></tr>"
                else:
                        ret+= "<tr><td> Ram Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:"+ram+"<br>Current Size:"+ str(round(float(stdout2[0].split(" ")[1])/1024/1000))+ "</td></tr>"

                out_hd=0
                stdout3 = stdout3[1:]
                for line in stdout3:
                        out_hd+= long(line.split(" ")[1])
                out_hd = out_hd/1024/1024

                if (float(out_hd) >= float(hd)):
                        ret+= "<tr><td> HD Size </td><td> <span class='badge bg-green'> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td>Actual Size:" + str(hd) +"G <br>Current Size:"+ str(out_hd) +"G </td></tr>"
                else:
                        ret+= "<tr><td> HD Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td>Actual Size:" + str(hd) +"G <br>Current Size:"+ str(out_hd) +"G </td></tr>"

                if (float(stdout4[0].split(" ")[1][:-1]) >= float(root)):
                        ret+= "<tr><td> /root Size </td><td> <span class='badge bg-green'> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" + str(root) +"G <br> Current Size:"+ str(stdout4[0].split(" ")[1])+ "</td></tr>"
                else:
                        ret+= "<tr><td> /root Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" + str(root) +"G <br> Current Size:"+ str(stdout4[0].split(" ")[1])+ "</td></tr>"

                ssh1.close()
                ssh2.close()
                ssh3.close()
                ssh4.close() '''

                errors= {"Error1":"Default Password Not Working", "Error2":"Server Not Found"}
                if ("em7" in server or "spld" in server or "splsr" in server or "splin" in server or "rly" in server):
                        count = 5
                        stdin, stdout, stderr, ssh = ssh_collect(server, user, port, timeout, command7)
                        if((len(stdout) == 0) or ("Error" in stdout)):
                                ret+= "<tr><td> /opt Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td>"+errors[stdout] +"</td></tr>"
                                return final(count, ret)

                        elif (float(stdout[0].split(" ")[1][:-1]) >= float(data02)):
                                ret+= "<tr><td> /opt Size </td><td> <span class='badge bg-green'> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" + str(opt)+ "G <br> Current Size:"+ str(stdout[0].split(" ")[1])+ "</td></tr>"
                        else:
                                ret+= "<tr><td> /opt Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" + str(opt)+ "G <br> Current Size:"+ str(stdout[0].split(" ")[1])+ "</td></tr>"
                        ssh.close()

                if ("splin" in server or "rly" in server):
                        count = 7
                        stdin6, stdout6, stderr6, ssh6 = ssh_collect(server, user, port, timeout, command6)
                        stdin7, stdout7, stderr7, ssh7 = ssh_collect(server, user, port, timeout, command7)

                        if((len(stdout) == 0) or ("Error" in stdout)):
                                ret+= "<tr><td> /opt Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td>"+errors[stdout] +"</td></tr>"

                        elif (float(stdout6[0].split(" ")[1][:-1]) >= float(data01)):
                                ret+= "<tr><td> /data01 Size </td><td> <span class='badge bg-green'> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" + str(data01) +"G <br> Current Size:"+ str(stdout6[0].split(" ")[1])+ "</td></tr>"
                        else:
                                ret+= "<tr><td> /data01 Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" + str(data01) +"G <br> Current Size:"+ str(stdout6[0].split(" ")[1])+ "</td></tr>"

                        if((len(stdout) == 0) or ("Error" in stdout)):
                                ret+= "<tr><td> /opt Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td>"+errors[stdout] +"</td></tr>"

                        elif (float(stdout7[0].split(" ")[1][:-1]) >= float(data02)):
                                ret+= "<tr><td> /data02 Size </td><td> <span class='badge bg-green'> &nbsp&nbsp Passed &nbsp&nbsp</span></td><td> Actual Size:" +str(data02) +"G <br> Current Size:"+ str(stdout7[0].split(" ")[1])+ "</td></tr>"
                        else:
                                ret+= "<tr><td> /data02 Size </td><td> <span class='badge bg-red'> &nbsp&nbsp Failed &nbsp&nbsp</span></td><td> Actual Size:" +str(data02) +"G <br> Current Size:"+ str(stdout7[0].split(" ")[1])+ "</td></tr>"

                        ssh6.close()
                        ssh7.close()

                return final(count, ret)



if __name__ == "__main__":

        search = raw_input("Enter Customer Name: ")
        try:
                '''con = _mysql.connect(host = "172.19.254.21",user = "root",passwd = "em7admin",port=int(7706),db = "master_dev")

                con.query("select * from standards.cust_octet where cust_name like '%" + search +"%'")
                result = con.store_result()
                octet = result.fetch_row()[0][1]

                con.query("select distinct(device) from legend_device where ip like '" +octet+ "%' and (device like '%em7pr%' or device like '%em7mc%' or device like '%em7dc%' or device like '%em7db%') order by id desc ")
                result_1 = con.store_result()

                con.query("select distinct(device) from legend_device where ip like '" +octet+ "%' and (device like '%spld%' or device like '%splm%' or device like '%splsr%' or device like '%splin%' or device like '%rly%') order by id desc ")
                result_2 = con.store_result()


                print "****"
                for row in result_1.fetch_row(100):
                        check_list+= sanity_check(row[0], user, port, timeout)

                print "****"
                for row in result_2.fetch_row(100):
                        check_list+= sanity_check(row[0], "root", port, timeout)'''


                html  = open("sanity_html.txt","r")
                display = html.read()
                check_list = ""

                check_list+= sanity_check(search, "root", port, timeout)
                display = display.replace("Checklist Table", check_list)

                if (display.count("Failed") > display.count("Passed")):
                        display = display.replace("32CD32","E50000")

                display = display.replace("Sanity Results","Sanity Results - &nbsp&nbsp&nbspPassed: "+str(display.count("Passed"))+ "&nbsp&nbsp&nbspFailed: "+str(display.count("Failed")))

                fw = open("/opt/em7/gui/ap/www/cms_negative_test.html","w")
                fw.write(display)
                fw.close()


        except _mysql.Error, e:

                print "Error %d: %s" % (e.args[0], e.args[1])


