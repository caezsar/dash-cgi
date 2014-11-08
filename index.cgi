#!/bin/bash
echo ""

bper=`/bin/cat 2>/dev/null /var/log/apache2/access.log | /bin/grep -v "(internal dummy connection)" 2>/dev/null | head -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1 2>/dev/null | sed 's/\//./g' 2>/dev/null`
fper=`/bin/cat 2>/dev/null /var/log/apache2/access.log | /bin/grep -v "(internal dummy connection)" 2>/dev/null | tail -1 | /usr/bin/awk '{print $4}' | /usr/bin/cut -d"[" -f2 2>/dev/null | /usr/bin/cut -d: -f1 2>/dev/null | sed 's/\//./g' 2>/dev/null`
uniq=`/bin/cat /var/log/apache2/access.log | /usr/bin/awk '{print $1}'| sort | uniq -c |wc -l 2>/dev/null `
eth0_rx=`/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $3, $4}'| cut -d"(" -f2 | cut -d")" -f1 2>/dev/null`
eth0_tx=`/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $7, $8}'| cut -d"(" -f2 | cut -d")" -f1 2>/dev/null`

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
                  <a class="brand" target="_blank" href="http://`echo $SERVER_ADDR`"> Server IP `echo $SERVER_ADDR`</a>    
		<div class="nav-collapse">

                <ul class="nav pull-right">
                            <li>
                      <a target="_blank" href="/">
                      <i class="lead icon-home"></i>
                    <span class="lead">Go Home</span>
                    </a>
                            </li>

                            <li>
                      <a target="_blank" href="https://github.com/caezsar/dash-cgi/">
                      <i class="lead icon-github"></i>
                    <span class="lead">GitHub</span>
                    </a>
                            </li>

                        <!--    <li>
                      <a target="_blank" href="link_2">
                      <i class="lead icon-info"></i>
                    <span class="lead">Link2</span>
                    </a>
                            </li>


                            <li>
                      <a target="_blank" href="link3.html">
                      <i class="lead icon-info"></i>
                    <span class="lead">Link3</span>
                    </a>
                            </li>
							
                            <li>
                      <a target="_blank" href="link4.cgi">
                      <i class="lead icon-info"></i>
                    <span class="lead">Link4</span>
                    </a>
                            </li> -->
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
<i class="icon-#">Used&nbsp;</i> <span id="ram-used"></span> <h2><font color="#303A34"> `free -h | grep Mem | /usr/bin/awk '{print $3}' 2>/dev/null `</font></h2><br>                                                    
                                                    </div><!-- .stat -->
                                                    <div class="stat">
<i class="icon-#">Free&nbsp;</i> <span id="ram-free"></span><h2><font color="#303A34"> `free -h | grep Mem | /usr/bin/awk '{print $4}' 2>/dev/null`</font></h2><br>                                                 
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
<table id="df_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h4><font color="#303A34"> `df -h 2>/dev/null` </font></h4></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->
							
							

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
                                </div><!-- /widget-content -->
                            </div><!-- /widget -->
                        </div><!-- /span3 --> 
						
						

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
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Server: `echo $SERVER_ADDR` </font></h4></pre></table>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Remote: `echo $REMOTE_ADDR` </font></h4></pre></table>
                                </div><!-- /widget-content -->
                            </div><!-- /widget -->
                        </div><!-- /span3 --> 
												


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
                                            <span class="general-data" id="os-info"> `runlevel` </span>
                                        </div>
                                        <div class="general-info-item">
                                            <span class="general-title">Swap Usage</span>
                                            <span id="os-uptime"> `free -m | awk '/Swap/ { printf("%3.1f%%", $3/$2*100) }'` </span>
                                        </div>
                                     <div class="general-info-item">
                                            <span class="general-title">Total Processes</span>
                                            <span id="os-time"> `ps aux | wc -l` </span>
                                        </div> 
                                        <div class="general-info-item">
                                            <span class="general-title">Boot Services</span>
<span class="general-data" id="os-info"> `ls /etc/rc2.d/ | grep S | wc -l` / `ls /etc/rc2.d/ | grep -v README | wc -l` </span>											
                                            <span id="os-hostname"> <pre> `ls /etc/rc2.d/ | grep S | cut -d"S" -f2 | cut -b 3-20` </pre></span>
                                        </div>
                                    </div>
                                </div><!-- /widget -->
                            </div> <!-- /span3 -->
							


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
<table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `netstat -tun | /usr/bin/awk '{print $1,$5,$6}' | sort -nr | grep -v "servers" | grep -v "Address" | uniq -c | sed 's/\ / --> /g'| /usr/bin/awk '{print $7,$9,$10,$11,$12,$13}' | sort -nr | uniq 2>/dev/null` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->



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
				

                            <div class="span14">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Network Servers
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content"><p> </p>
<table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `netstat -tuln 2>/dev/null` </font></h5></pre> </table>
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
                                        <pre><h5><font color="#303A34"> `w -s` </font></h5></pre>
                                    </div>
                                </div>
                            </div>
                        </div> <!-- /span6 -->
						
							
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
<table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `last -i 2>/dev/null` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->
							
							
			
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
<table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `vnstat -i eth0 2>/dev/null`  </font></h5></pre> </table>
<table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `vnstat -i tun0 2>/dev/null`  </font></h5></pre> </table>            
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
<table id="ps_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `ps axu 2>/dev/null` </font></h5></pre> </table>
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
