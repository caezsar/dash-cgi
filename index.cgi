#!/bin/bash
echo "Content-type: text/html"

VHOST_PATTERN="ubuntu.lan"
APACHE_ACCESS_LOG_FILE="/var/log/apache2/ubuntu.lan-access.log"


bper=`/bin/cat 2>/dev/null $APACHE_ACCESS_LOG_FILE | /bin/grep -v "(internal dummy connection)" 2>/dev/null | head -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1 2>/dev/null | sed 's/\//./g' 2>/dev/null`
fper=`/bin/cat 2>/dev/null $APACHE_ACCESS_LOG_FILE | /bin/grep -v "(internal dummy connection)" 2>/dev/null | tail -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1 2>/dev/null | sed 's/\//./g' 2>/dev/null`
uniq=`cat $APACHE_ACCESS_LOG_FILE | /usr/bin/awk '{print $1}'| sort | uniq -c |wc -l`
hits=`/bin/cat $APACHE_ACCESS_LOG_FILE | grep -v "::1" | /usr/bin/awk '{print $1}' | sort | wc -l 2>/dev/null`
eth0_rx=`/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $3, $4}'| cut -d"(" -f2 | cut -d")" -f1 2>/dev/null`
eth0_tx=`/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $7, $8}'| cut -d"(" -f2 | cut -d")" -f1 2>/dev/null`
connections=`netstat -tun | /usr/bin/awk '{print $5}' | cut -d: -f1 | grep -v servers | grep -v Address | sort -nr | uniq -c`

disk_info() {
filesystem=`df -h | awk '{print $1}' | awk 'NR==1'`
size=`df -h | awk '{print $2}' | awk 'NR==1'`
avail=`df -h | awk '{print $4}' | awk 'NR==1'`
percent=`df -h | awk '{print $5}' | awk 'NR==1'`
mounted=`df -h | awk '{print $6}' | awk 'NR==1'`

echo "<table class="table">"
echo "  <tr>"
echo "    <td><h4>`echo $filesystem`</h4></td>"
echo "    <td><h4>`echo $size`</h4></td>"	
echo "    <td><h4>`echo $avail`</h4></td>"
echo "    <td><h4>`echo $percent`</h4></td>"
echo "    <td><h4>`echo $mounted`</h4></td>"
echo "    <td><h4>Type</h4></td>"	
echo " </tr>"
 
for i in `mount | grep "^/" | awk '{print $3}'`; do
echo "  <tr>"
first=`df -h $i  | awk '{print $1}' | awk 'NR==2'`
sec=`df -h $i  | awk '{print $2}' | awk 'NR==2'`
th=`df -h $i  | awk '{print $4}' | awk 'NR==2'`
four=`df -h $i  | awk '{print $5}' | awk 'NR==2'`
five=`df -h $i  | awk '{print $6}' | awk 'NR==2'`
six=`df -T $i | awk '{print $2}' | grep -v "Type"`

echo "	  <td>`echo $first`</td>"
echo "    <td>`echo $sec`</td>"		
echo "    <td>`echo $th`</td>"
echo "    <td>`echo $four`</td>"
echo "    <td>`echo $five`</td>"
echo "    <td>`echo $six`</td>"
echo "  </tr>"
done

echo "</table>"
}


servers() {
result=`/bin/netstat -tuln | grep -v "Active" | grep -v "Proto" | awk '{print $1,$4,$6}' | sed 's/\ /      /g'`
        while read -r line; do
        echo  "<table>"
        echo "<pre><strong> $line</strong>"
        done <<< "$result"               
		echo "</font></h5></pre> </table>"
}		

users_online() {
result=`who`
        while read -r line; do
        echo  "<table>"
        echo "<pre><strong> $line</strong>"
        done <<< "$result"               
		echo "</pre> </table>"
}

ip() {

echo "<table class="table">"
echo " <tr>"
echo "    <td><strong>Interface</strong></td>"
echo "    <td><strong>IP</td></strong>"	
echo " </tr>"
 
for i in `/sbin/ifconfig -a | cut -d" " -f1`; do
echo "  <tr>"
echo "	  <td>`/sbin/ifconfig $i | /usr/bin/awk '{print $1}' | awk 'NR==1'` </td>"
echo "	  <td>`/sbin/ifconfig $i | grep inet | /usr/bin/awk '{print $2}' | /usr/bin/cut -d: -f2` </td>"
echo "  </tr>"
done
echo "</table>"
}

last_logins() {
result=`last -i`
        while read -r line; do
        echo  "<table>"
        echo "<pre><strong> $line</strong>"
        done <<< "$result"               
		echo "</pre> </table>"
}

net_conn() {
result=`netstat -tun | /usr/bin/awk '{print $1,$5,$6}' | sort -nr | grep -v "servers" | grep -v "Address" | uniq -c | sed 's/\ / --> /g'| /usr/bin/awk '{print $7,$9,$10,$11,$12,$13}' | sort -nr | uniq 2>/dev/null`
        while read -r line; do
        echo  "<table>"
        echo "<pre><strong> $line</strong>"
        done <<< "$result"               
		echo "</pre> </table>"
}

process() {
result=`ps aux`
        while read -r line; do
        echo  "<table>"
        echo "<pre><strong> $line</strong>"
        done <<< "$result"               
		echo "</pre> </table>"
}


traffic() {

echo "<table class="table">"
echo " <tr>"
echo "    <td><strong>Interface</strong></td>"
echo "    <td><strong>UP</strong></td>"	
echo "    <td><strong>Down</strong></td>"	
echo " </tr>"
 
for i in `/sbin/ifconfig | cut -d" " -f1`; do
echo "  <tr>"
echo "	  <td>`/sbin/ifconfig $i | /usr/bin/awk '{print $1}' | awk 'NR==1'` </td>"
echo "	  <td>`/sbin/ifconfig $i| grep "RX bytes" | head -1 | /usr/bin/awk '{print $3, $4}'| cut -d"(" -f2 | cut -d")" -f1 2>/dev/null` </td>"
echo "	  <td>`/sbin/ifconfig $i| grep "RX bytes" | head -1 | /usr/bin/awk '{print $7, $8}'| cut -d"(" -f2 | cut -d")" -f1 2>/dev/null`	</td>"
echo "  </tr>"
done
echo "</table>"
}

traffic_info() {

for i in `/sbin/ifconfig | grep -v "lo" | cut -d" " -f1`; do
echo "<table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `vnstat -i $i` </font></h5></pre> </table>"
done
}

no_gzip_logs() {
echo "<table class="table">"
echo " <tr>"
echo "<td><strong> Log Start Date </strong></td>"
echo "<td><strong> End Date </strong></td>"		
echo "<td><strong> Uniq IP </strong></td>"
echo "<td><strong> Total Hits </strong></td>"
echo "  </tr>"

for i in `ls /var/log/apache2/ | grep $VHOST_PATTERN | grep -v error | grep -v gz`; do

start_date=`/bin/cat 2>/dev/null /var/log/apache2/$i | /bin/grep -v "(internal dummy connection)" 2>/dev/null | head -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1`
end_date=`/bin/cat 2>/dev/null /var/log/apache2/$i | /bin/grep -v "(internal dummy connection)" 2>/dev/null | tail -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1`
uniq_ip=`cat /var/log/apache2/$i | grep -v "internal dummy connection" | cut -d" " -f1 | sort -nr | uniq -c | wc -l`
hits=`/bin/cat /var/log/apache2/$i| grep -v "::1" | /usr/bin/awk '{print $1}' | sort | wc -l 2>/dev/null`

echo "<table class="table">"
echo " <tr>"
echo "	  <td>`echo $start_date`</td>"
echo "    <td>`echo $end_date`</td>"		
echo "    <td>`echo $uniq_ip`</td>"
echo "    <td>`echo $hits`</td>"
echo "  </tr>"

echo "</table>"

done
}

gzip_logs() {
for i in `ls /var/log/apache2/ | grep $VHOST_PATTERN | grep -v error | grep gz`; do

start_date=`/bin/zcat 2>/dev/null /var/log/apache2/$i | /bin/grep -v "(internal dummy connection)" 2>/dev/null | head -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1`
end_date=`/bin/zcat 2>/dev/null /var/log/apache2/$i | /bin/grep -v "(internal dummy connection)" 2>/dev/null | tail -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1`
uniq_ip=`zcat /var/log/apache2/$i | grep -v "internal dummy connection" | cut -d" " -f1 | sort -nr | uniq -c | wc -l`
hits=`/bin/zcat /var/log/apache2/$i| grep -v "::1" | /usr/bin/awk '{print $1}' | sort | wc -l 2>/dev/null`
#echo
#printf "Period: $start_date - $end_date   Uniq: $uniq_ip   Total Hits: $hits  "
#echo
echo "<table class="table">"
echo " <tr>"
echo "	  <td>`echo $start_date`</td>"
echo "    <td>`echo $end_date`</td>"		
echo "    <td>`echo $uniq_ip`</td>"
echo "    <td>`echo $hits`</td>"
echo "  </tr>"

echo "</table>"
done
}


total_gip() {
cd /var/log/apache2/
string=`ls | grep $VHOST_PATTERN | grep -v error | grep gz | xargs echo -n`
uniq_ip=`zcat $string | grep -v "internal dummy connection" | cut -d" " -f1 | sort -nr | uniq -c | wc -l`
echo $uniq_ip
}

total_ip() {
cd /var/log/apache2/
string=`ls | grep $VHOST_PATTERN | grep -v error | grep -v gz | xargs echo -n`
uniq_ip=`cat $string | grep -v "internal dummy connection" | cut -d" " -f1 | sort -nr | uniq -c | wc -l`
echo $uniq_ip
}

total_ips() {
echo "`total_gip` + `total_ip`" | bc
}


total_ghits() {
cd /var/log/apache2/

string=`ls | grep $VHOST_PATTERN | grep -v error | grep gz | xargs echo -n`
uniq_hits=`/bin/zcat /var/log/apache2/$string | grep -v "::1" | /usr/bin/awk '{print $1}' | sort | wc -l`
echo $uniq_hits
}

total_hits() {
cd /var/log/apache2/
string=`ls | grep $VHOST_PATTERN | grep -v error | grep -v gz | xargs echo -n`
uniq_hits=`/bin/cat /var/log/apache2/$string | grep -v "::1" | /usr/bin/awk '{print $1}' | sort | wc -l`
echo $uniq_hits
}

total_apache_hits() {
echo "`total_ghits` + `total_hits`" | bc
}


#hack_tries() {
#cat $APACHE_ACCESS_LOG_FILE | grep HEAD | grep fckeditor | awk '{print $1, $4}' | cut -d: -f1| sed 's/\[/\ /g' | uniq -c | sort -nr
#}

#hack_tries1() {
#cat $APACHE_ACCESS_LOG_FILE | grep GET | grep phpmyadmin | awk '{print $1, $4}' | cut -d: -f1| sed 's/\[/\ /g' | uniq -c | sort -nr
#}

#hack_tries2() {
#cat $APACHE_ACCESS_LOG_FILE | grep GET | grep HNAP1 | awk '{print $1, $4}' | cut -d: -f1| sed 's/\[/\ /g' | uniq -c | sort -nr
#}

#hack_proxy() {
#cat $APACHE_ACCESS_LOG_FILE | grep "GET http://" | awk '{print $1, $4}' | cut -d: -f1| sed 's/\[/\ /g' | uniq -c | sort -nr
#}

#hack_xml() {
#cat $APACHE_ACCESS_LOG_FILE | grep "xmlrpc.php" | awk '{print $1, $4}' | cut -d: -f1| sed 's/\[/\ /g' | uniq -c | sort -nr
#}

#hack_ckfinder() {
#cat $APACHE_ACCESS_LOG_FILE | grep "ckfinder" | awk '{print $1, $4}' | cut -d: -f1| sed 's/\[/\ /g' | uniq -c | sort -nr
#}


404_ips() {
cat $APACHE_ACCESS_LOG_FILE | grep 404 | awk '{print $1, $4, $9, $7}' | grep -v 200 | awk '{print $1, $2}'  | cut -d: -f1| sed 's/\[/\ /g' | uniq -c | sort -nr
}

404_ips_files() {
cat $APACHE_ACCESS_LOG_FILE | grep 404 | awk '{print $1, $9, $7, $4}' | grep -v 200 | sed 's/\[/\ /g' | cut -d: -f1 | awk '{print $4, $1, $3}' | uniq -c | sort -nr
 }



cat << EOF

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>linux-dash : Server Monitoring Web Dashboard on `hostname -f` </title>
       <!-- <meta http-equiv="refresh" content="5" /> -->
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Monitor your Linux server through a simple web dashboard. Open source and free!">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
        <link rel="icon" href="favicon.ico" type="image/x-icon">
        <link href="css/bootstrap.min.css" rel="stylesheet" type="text/css">
        <link href="css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css">
        <link href="css/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
        <link href="css/style.css" rel="stylesheet" type="text/css">
        <link href="css/pages/dashboard.css" rel="stylesheet" type="text/css">
        <link href="css/odometer.css" rel="stylesheet" type="text/css">
        <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
        <!--[if lt IE 9]>
          <script src="https://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
    </head>

	
    <body>
        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
	
                    <a class="brand" href="./">`hostname -f`</a>
               
		<div class="nav-collapse">

                <ul class="nav pull-right">
                            <li>
                      <a target="_blank" href="/m">
                      <i class="lead icon-home"></i>
                    <span class="lead">Go Home</span>
                    </a>
                            </li>

                            <li>
                      <a target="_blank" href="../logs.cgi">
                      <i class="lead icon-info"></i>
                    <span class="lead">Logs</span>
                    </a>
                            </li>

                            <li>
                      <a target="_blank" href="../logwatch.cgi">
                      <i class="lead icon-info"></i>
                    <span class="lead">Logwatch</span>
                    </a>
                            </li>


                            <li>
                      <a target="_blank" href="../webalizer/index.html">
                      <i class="lead icon-info"></i>
                    <span class="lead">Webalizer</span>
                    </a>
                            </li>
                            <li>
                      <a target="_blank" href="../sysinfo/">
                      <i class="lead icon-info"></i>
                    <span class="lead">Graphics</span>
                    </a>
                            </li>
                        </ul>
					</div>
                </div>
            </div>
        </div>	
		
     <div class="subnavbar">
            <div class="subnavbar-inner">

             <a class="btn btn-navbar btn-info visible-phone" data-toggle="collapse" data-target=".nav-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </a>

                <div class="container nav-collapse">

                    <ul class="mainnav">
                        <li>
                            <a class="js-smoothscroll" href="#refresh-os"><i class="icon-dashboard"></i><span>General</span></a>
                        </li>
                        <li>
                            <a class="js-smoothscroll" href="#refresh-df"><i class="icon-list-alt"></i><span>Disk</span></a>
                        </li>
                        <li>
                            <a class="js-smoothscroll" href="#cpu"><i class="icon-list-alt"></i><span>CPU</span></a>
                        </li>
                        <li>
                            <a class="js-smoothscroll" href="#refresh-ram"><i class="icon-list-alt"></i><span>RAM</span></a>
                        </li>
                         <li>
                            <a class="js-smoothscroll" href="#online"><i class="icon-list-alt"></i><span>Users</span></a>
                        </li>
                  
                         <li>
                            <a class="js-smoothscroll" href="#process"><i class="icon-list-alt"></i><span>Process</span></a>
                        </li>
                        <li>						
                            <a class="js-smoothscroll" href="#refresh-ispeed"><i class="icon-exchange"></i><span>Network</span></a>
                        </li>
                        <li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                    <i id="closed-widget-count">0</i>
                <span> Closed Widgets <i class="icon-caret-down"></i></span>
                </a>
                            <ul class="dropdown-menu" id="closed-widget-list">
                    <li id="close-all-widgets">
                    <a> <i class="icon-remove lead pull-left"></i> Close All Widgets</a>
                </li>
                <li id="open-all-widgets">
                    <a> <i class="icon-plus lead pull-left"></i> Open All Widgets</a>
                </li>
                <li class=""><hr></li>
                </ul>
            </li>
             <li class="dropdown">
    
                    </ul>
                </div><!-- /container -->
            </div><!-- /subnavbar-inner -->
        </div><!-- /subnavbar -->
		
		
		
        <div class="main">
            <div class="main-inner">
                <div class="container">
                    <div class="lead" style="text-align: center;">
                        <div>
                           Information generated at `date`
                        </div>
                    </div>
                    <div id="widgets" class="row">

                        <div class="span3">
                                <div id="general-info-widget" class="widget widget-table action-table">
                                    <div class="widget-header">
                                        <i class="icon-info-sign"></i>
                                        <h3>
                                            General Info
                                        </h3>
                                        <div id="refresh-os" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <div class="general-info-item">
                                            <span class="general-title">OS</span>
                                            <span class="general-data" id="os-info"> `cat /etc/issue.net` </span>
                                        </div>

                                       <div class="general-info-item">
                                            <span class="general-title">Machine</span>
                                            <span class="general-data" id="os-info"> `uname -a` </span>
                                        </div>

                                        <div class="general-info-item">
                                            <span class="general-title">Uptime</span>
                                            <span id="os-uptime"> `uptime | cut -d"p" -f2|cut -d"," -f1` </span>
                                        </div>
                                      <!--  <div class="general-info-item">
                                            <span class="general-title">Server Time</span>
                                            <span id="os-time"> `date` </span>
                                        </div> -->
                                        <div class="general-info-item">
                                            <span class="general-title">Hostname</span>
                                            <span id="os-hostname"> `hostname -f` </span>
                                        </div>
                                       <div class="general-info-item">
                                            <span class="general-title">Last Reboot</span>
                                            <span class="general-data" id="os-info"> `who -b` </span>
                                        </div>
                                    </div>
                                </div><!-- /widget -->
                            </div> <!-- /span3 -->

			
							
                        <div class="span5">
                                <div id="ram-widget" class="widget widget-nopad">
                                    <div class="widget-header">
                                        <i class="icon-list-alt"></i>
                                        <h3>
                                            RAM
                                        </h3>
                                        <div id="refresh-ram" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <div class="big-stats-container">
                                            <div class="widget-content">
                                                <div class="cf big_stats">
                                                    <div class="stat">
<i class="icon-#">Total&nbsp;</i> <span  id="ram-total"></span>  <h2><font color="#303A34"> `free -h | grep Mem | /usr/bin/awk '{print $2}' 2>/dev/null`</font></h2>
                                                    </div><!-- .stat -->
                                                    <div class="stat">
<i class="icon-#">Used&nbsp;</i> <span id="ram-used"></span> <h2><font color="#303A34"> `free -h | grep cache | /usr/bin/awk '{print $3}' | head -n 2 | sed 's/free/ /g' 2>/dev/null `</font></h2><br>                                                    
                                                    </div><!-- .stat -->
                                                    <div class="stat">
<i class="icon-#">Free&nbsp;</i> <span id="ram-free"></span><h2><font color="#303A34"> `free -h | grep cache | /usr/bin/awk '{print $4}' | head -n 2 | sed 's/shared/ /g' 2>/dev/null`</font></h2><br>                                                 
                                                    </div><!-- .stat -->
                                                </div>
                                            </div><!-- /widget-content -->
                                        </div>
                                    </div>
                                </div>
                            </div> <!-- /span5 -->

							
                        <div class="span4">
                            <div id="load-average-widget" class="widget">
                                <div class="widget-header">
                                    <i class="icon-laptop"></i>
                                    <h3>
                                        Load average
                                    </h3>
                                    <div id="refresh-load" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content">
                                    <div style="text-align:center;">
                                        <b>Number of cores:</b> <span class="lead" id="core-number"> `nproc` </span>
                                    </div>
                                    <div class="cf big_stats">
                                        <div class="stat">
<i class="icon-#">1 min&nbsp;</i> <span id="cpu-1min-per"></span> <h2><font color="#303A34"> `/bin/cat /proc/loadavg | /usr/bin/awk '{print $1}' 2>/dev/null ` % </font></h2><br>
                                            <span class="value" id="cpu-1min"></span>
                                        </div><!-- .stat -->
                                        <div class="stat">
<i class="icon-#">5 min&nbsp;</i> <span  id="cpu-5min-per"></span> <h2><font color="#303A34"> `/bin/cat /proc/loadavg | /usr/bin/awk '{print $2}' 2>/dev/null` % </font></h2><br>
                                            <span class="value" id="cpu-5min"></span>
                                        </div><!-- .stat -->
                                        <div class="stat">
<i class="icon-#">15 min&nbsp;</i> <span id="cpu-15min-per"></span> <h2><font color="#303A34"> `/bin/cat /proc/loadavg | /usr/bin/awk '{print $3}' 2>/dev/null` % </font></h2><br>
                                            <span class="value" id="cpu-15min"></span>
                                        </div><!-- .stat -->
                                    </div>
                                </div><!-- /widget-content -->
                            </div><!-- /widget -->
                        </div> <!-- /span4 -->

						

                        <div class="span3">
                            <div id="ip-widget" class="widget widget-table">
                                <div class="widget-header">
                                    <i class="icon-monitor"></i>
                                    <h3>
                                        IP
                                    </h3>
                                    <div id="refresh-ip" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content"><p> </p>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> External: ` wget -qO- http://ipecho.net/plain ; echo 2 >/dev/null` </font></h4></pre></table>								
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Remote: `echo $REMOTE_ADDR` </font></h4></pre></table>
										`ip`
                                </div><!-- /widget-content -->
                            </div><!-- /widget -->
                        </div><!-- /span3 --> 
												
												

						<div class="span3">
                            <div id="ip-widget" class="widget widget-table">
                                <div class="widget-header">
                                    <i class="icon-monitor"></i>
                                    <h3>
                                        Apache Unique
                                    </h3>
                                    <div id="refresh-ip" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content"><p> </p>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> `echo $bper` - `echo $fper 2>/dev/null` </font></h4></pre></table>								
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Uniq Visitors: `echo $uniq 2>/dev/null` </font></h4></pre></table>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Total Hits: `echo $hits 2>/dev/null` </font></h4></pre></table>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Total Server IPs: `total_ips` </font></h4></pre></table>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Total Server Hits: `total_apache_hits` </font></h4></pre></table>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Apache Logs Space: `du -sh /var/log/apache2 | awk '{print $1}'` </font></h4></pre></table>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Total Logs Space: `du -sh /var/log | awk '{print $1}'` </font></h4></pre></table>

                             </div><!-- /widget-content -->
                            </div><!-- /widget -->
                        </div><!-- /span3 --> 
					

							<div class="span6">
                                <div id="disk-usage-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-list"></i>
                                        <h3>
                                            Disk Usage
                                        </h3>
                                        <div id="refresh-df" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
							`disk_info`
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->
							


							<div class="span6">
                                <div id="disk-usage-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-list"></i>
                                        <h3>
                                            Apache Log Statistics
                                        </h3>
                                        <div id="refresh-df" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
									`no_gzip_logs`
									`gzip_logs`
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->
																					

                       <div class="span3">
                                <div id="general-info-widget" class="widget widget-table action-table">
                                    <div class="widget-header">
                                        <i class="icon-info-sign"></i>
                                        <h3>
                                            System
                                        </h3>
                                        <div id="refresh-os" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <div class="general-info-item">
                                            <span class="general-title">Runlevel</span>
                                            <span class="general-data" id="os-info"> `/sbin/runlevel` </span>
                                        </div>
                                        <div class="general-info-item">
                                            <span class="general-title">Cache RAM</span>
                                            <span class="general-data" id="os-info"> `free -h | grep Mem | /usr/bin/awk '{print $7}'` </span>
                                        </div>										
										
                                        <div class="general-info-item">
                                            <span class="general-title">Swap Usage</span>
                                            <span id="os-uptime"> `free -m | awk '/Swap/ { printf("%3.1f%%", $3/$2*100) }'` from `free -h | grep Swap | awk '{print $2}'` </span>
                                        </div>
                                     <div class="general-info-item">
                                            <span class="general-title">Total Processes</span>
                                            <span id="os-time"> `ps aux | wc -l` </span>
                                        </div> 
                                        <div class="general-info-item">
                                            <span class="general-title">Boot Services</span>
<span class="general-data" id="os-info"> `ls /etc/rc2.d/ | grep S | wc -l` / `ls /etc/rc2.d/ | grep -v README | wc -l` </span>											
                                            <span id="os-hostname"> <pre> `ls /etc/rc2.d/ | grep S | cut -d"S" -f2 | cut -b 3-20 | sort` </pre></span>
                                        </div>
                                    </div>
                                </div><!-- /widget -->
                            </div> <!-- /span3 -->



						
							<div class="span3">
                                <div id="disk-usage-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-list"></i>
                                        <h3>
                                            Traffic
                                        </h3>
                                        <div id="traffici" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
							`traffic`
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->	

							
                            <div class="span14">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Servers
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
							`servers`
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->
							
							
	                       <div class="span16">
                            <div id="memcached-widget" class="widget widget-nopad">
                                <div class="widget-header">
                                    <i class="icon-list-alt"></i>
                                    <h3>
                                        Hackers IPs
                                    </h3>
                                    <div id="online" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content">
                                    <div class="big-stats-container"><p> </p>
					<pre>`404_ips`</pre>
                                    </div>
                                </div>
                            </div>
                        </div> <!-- /span6 -->							
							
							
                            <div class="span16">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Network Connections
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
								`net_conn`
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->

						
                       <div class="span16">
                            <div id="memcached-widget" class="widget widget-nopad">
                                <div class="widget-header">
                                    <i class="icon-list-alt"></i>
                                    <h3>
                                        Users Online
                                    </h3>
                                    <div id="online" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content">
                                    <div class="big-stats-container"><p> </p>
                                    `users_online`
                                    </div>
                                </div>
                            </div>
                        </div> <!-- /span6 -->
						
						
							<div class="span4">
                                <div id="users-widget" class="widget widget-table action-table">
                                    <div class="widget-header">
                                        <i class="icon-group"></i>
                                        <h3>
                                            CPU Info
                                        </h3>
                                        <div id="refresh-users" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
<table id="cpu" class="table table-hover table-bordered table-condensed"><pre><h5><font color="#303A34"> `lscpu 2>/dev/null` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span4 -->

				
							<div class="span17">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Last logins
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
								`last_logins`
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->


						<div class="span6">
                                <div id="arp-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-list"></i>
                                        <h3>
                                            I/O Stats
                                        </h3>
                                        <div id="refresh-arp" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
										<div class="widget-content"><p> </p>
<table id="arp_dashboard" class="table table-hover table-condensed table-bordered"><pre><h5><font color="#303A34"> `iostat -hm 2>/dev/null` </font></h5></pre></table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->
							
							
							<div class="span4">
                                <div id="bandwidth-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-exchange"></i>
                                        <h3>
                                            Bandwidth
                                        </h3>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <div style="padding:10px;text-align:center;">
<i style="color:#19bc9c; font:20px/2em 'Open Sans',sans-serif;" class="icon-#" >eth0:</i>&nbsp; <h4><font color="#303A34"> RX: <span> `echo $eth0_rx 2>/dev/null` </span>&nbsp;&nbsp;|&nbsp;&nbsp; TX: <span> `echo $eth0_tx 2>/dev/null` </span></h4></font> 
                                        </div>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span4 -->
							

					   <div class="span6">
                                <div id="software-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-list"></i>
                                        <h3>
                                            Network Interfaces
                                        </h3>
                                        <div id="refresh-ispeed" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
<table id="whereis_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `/sbin/ifconfig 2>/dev/null` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->
												
                            <div class="span16">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Traffic Info
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
							`traffic_info`
									</div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->


                       <div class="span12">
                                <div id="process-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Processes
                                        </h3>
                                        <div id="process" class="btn icon-refresh js-refresh-info"></div>
                                        <div class="pull-right">
                                       
                                        </div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
<table id="ps_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `process` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span12 -->
							
							
                        <div class="span12">
                                <div id="process-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Environment
                                        </h3>
                                        <div id="refresh-env" class="btn icon-refresh js-refresh-info"></div>
                                        <div class="pull-right">

                                        </div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
<table id="ps_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `env` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span12 -->

	                       <div class="span16">
                            <div id="memcached-widget" class="widget widget-nopad">
                                <div class="widget-header">
                                    <i class="icon-list-alt"></i>
                                    <h3>
                                        Hackers IPs
                                    </h3>
                                    <div id="online" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content">
                                    <div class="big-stats-container"><p> </p>
					<pre>`404_ips_files`</pre>
                                    </div>
                                </div>
                            </div>
                        </div> <!-- /span6 -->
						
                    </div><!-- #/widgets -->
                </div>
            </div><!-- /main-inner -->
        </div><!-- /main -->

        <div class="footer">
            <div class="footer-inner">
                <div class="container">
                    <div class="row">
                        <div class="span12">
                            Modified by: <a target="_blank" href="https://github.com/caezsar/dash-cgi/">caezsar</a>
                        </div><!-- /span12 -->
                    </div><!-- /row -->
                </div><!-- /container -->
            </div><!-- /footer-inner -->
        </div><!-- /footer -->

        <!-- Javascript-->
        <!-- Placed at the end of the document so the pages load faster -->
        <script src="js/jquery.js" type="text/javascript"></script>
        <script src="js/jquery-ui.min.js" type="text/javascript"></script>
        <script src="js/bootstrap.js" type="text/javascript"></script>
        <script src="js/jquery.dataTables.min.js" type="text/javascript"></script>
        <script src="js/odometer.js" type="text/javascript"></script>
    
        <script src="js/base.js" type="text/javascript"></script>
    </body>
</html>

EOF
