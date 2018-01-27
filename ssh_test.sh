#!usr/bin
# use expect to excecute the command, output the ssh log
expect ./ssh_text >router_ssh.log

# sed1: get text1 from file
# sed2: get text2 from text1
# awk1: split text2 by ":" and get second column
# awk2: read the first column from awk1 

wanip=`sed -n '/eth0.2    Link encap:Eth*/,/ifb0*/p' ./router_ssh.log |sed -n '/inet addr*/p' |awk -F ":" '{print $2}'|awk '{print $1}'`
rm -r router_ssh.log

# this is for router, extract ip directly, but the router does not support pip.:
#ifconfig |sed -n '/eth0.2    Link encap:Eth*/,/ifb0*/p' |sed -n '/inet addr*/p' |awk -F ":" '{print $2}'|awk '{print $1}'

echo $wanip
