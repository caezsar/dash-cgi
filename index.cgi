#!/bin/bash
echo "Content-type: text/html"

bper=`cat /var/log/apache2/access.log | grep -v "(internal dummy connection)" | head -1 | /usr/bin/awk '{print $4}' | cut -d"[" -f2 | cut -d: -f1 | sed 's/\//./g'`
fper=`cat /var/log/apache2/access.log | grep -v "(internal dummy connection)" | tail -1 | /usr/bin/awk '{print $4}' | cut -d"[" -f2 | cut -d: -f1 | sed 's/\//./g'`
uniq=`cat /var/log/apache2/access.log | /usr/bin/awk '{print $1}'| sort | uniq -c |wc -l`
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
                      <a target="_blank" href="http://tools.tecmint.com">
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
                      <a target="_blank" href="../info.cgi">
                      <i class="lead icon-info"></i>
                    <span class="lead">Info</span>
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
                            <a class="js-smoothscroll" href="#refresh-ps"><i class="icon-list-alt"></i><span>CPU</span></a>
                        </li>
                        <li>
                            <a class="js-smoothscroll" href="#refresh-ram"><i class="icon-list-alt"></i><span>RAM</span></a>
                        </li>
                       <!--  <li>
                            <a class="js-smoothscroll" href="#refresh-users"><i class="icon-group"></i><span>Users</span></a>
                        </li> -->
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
                       <!-- <div class="btn icon-refresh js-refresh-info" data-title="Refresh all widgets!" data-toggle="tooltip" id="refresh-all"></div> -->
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
                                        <div  class="btn icon-refresh js-refresh-info"></div>
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
                                            <span id="os-uptime"> `uptime | /usr/bin/awk '{print $3, $4}'`</span>
                                        </div>
                                      <!--  <div class="general-info-item">
                                            <span class="general-title">Server Time</span>
                                            <span id="os-time"> `date` </span>
                                        </div> -->
                                        <div class="general-info-item">
                                            <span class="general-title">Hostname</span>
                                            <span id="os-hostname"> `hostname` </span>
                                        </div>
                                       <div class="general-info-item">
                                            <span class="general-title">Last Reboot</span>
                                            <span class="general-data" id="os-info"> `who -b` </span>
                                        </div>


                                    </div>
                                </div><!-- /widget -->
                            </div> <!-- /span3 -->

                        <div class="span4">
                            <div id="load-average-widget" class="widget">
                                <div class="widget-header">
                                    <i class="icon-laptop"></i>
                                    <h3>
                                        Load average
                                    </h3>
                                    <div id="refresh-cpu" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content">
                                    <div style="text-align:center;">
                                        <b>Number of cores:</b> <span class="lead" id="core-number"> `nproc` </span>
                                    </div>
                                    <div class="cf big_stats">
                                        <div class="stat">
                                            <i class="icon-#">1 min&nbsp;</i> <span id="cpu-1min-per"></span> <h2><font color="#303A34"> `/bin/cat /proc/loadavg | /usr/bin/awk '{print $1}'` % </font></h2><br>
                                            <span class="value" id="cpu-1min"></span>
                                        </div><!-- .stat -->
                                        <div class="stat">
                                            <i class="icon-#">5 min&nbsp;</i> <span  id="cpu-5min-per"></span> <h2><font color="#303A34"> `/bin/cat /proc/loadavg | /usr/bin/awk '{print $2}'` % </font></h2><br>
                                            <span class="value" id="cpu-5min"></span>
                                        </div><!-- .stat -->
                                        <div class="stat">
                                            <i class="icon-#">15 min&nbsp;</i> <span id="cpu-15min-per"></span> <h2><font color="#303A34"> `/bin/cat /proc/loadavg | /usr/bin/awk '{print $3}'` % </font></h2><br>
                                            <span class="value" id="cpu-15min"></span>
                                        </div><!-- .stat -->
                                    </div>
                                </div><!-- /widget-content -->
                            </div><!-- /widget -->
                        </div> <!-- /span4 -->

						
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
                                                        <i class="icon-#">Total&nbsp;</i> <span  id="ram-total"></span>  <h2><font color="#303A34"> `free -h | grep Mem | /usr/bin/awk '{print $2}'`</font></h2>
                                                    </div><!-- .stat -->
                                                    <div class="stat">
                                                        <i class="icon-#">Used&nbsp;</i> <span id="ram-used"></span> <h2><font color="#303A34"> `free -h | grep Mem | /usr/bin/awk '{print $3}'`</font></h2><br>
                                                     
                                                    </div><!-- .stat -->
                                                    <div class="stat">
                                                        <i class="icon-#">Free&nbsp;</i> <span id="ram-free"></span><h2><font color="#303A34"> `free -h | grep Mem | /usr/bin/awk '{print $4}'`</font></h2><br>
                                                     
                                                    </div><!-- .stat -->
                                                </div>
                                            </div><!-- /widget-content -->
                                        </div>
                                    </div>
                                </div>
                            </div> <!-- /span5 -->

                        <div class="span6">
                                <div id="disk-usage-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-list"></i>
                                        <h3>
                                            Disk Usage
                                        </h3>
                                        <div id="refresh-df" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="df_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h4><font color="#303A34"> `df -h` </font></h4></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->
                       
					   <div class="span6">
                                <div id="software-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-list"></i>
                                        <h3>
                                            Network Interfaces
                                        </h3>
                                        <div id="refresh-ispeed" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="whereis_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `/sbin/ifconfig` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->

							
                       <div class="span3">
                            <div id="ip-widget" class="widget widget-table">
                                <div class="widget-header">
                                    <i class="icon-monitor"></i>
                                    <h3>
                                        Apache Uniq
                                    </h3>
                                    <div id="refresh-ip" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content">
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> `echo $bper` - `echo $fper` </font></h4></pre></table>
								
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Uniq Visitors: `echo $uniq` </font></h4></pre></table>

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
                                <div class="widget-content">
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Server: `echo $SERVER_ADDR` </font></h4></pre></table>
<table id="ip_dashboard" class="table table-hover table-condensed table-bordered"><pre><h4><font color="#303A34"> Remote: `echo $REMOTE_ADDR` </font></h4></pre></table>

                                </div><!-- /widget-content -->
                            </div><!-- /widget -->
                        </div><!-- /span3 --> 


                    <!--    <div class="span4">
                                <div id="netstat-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Network Statistics
                                        </h3>
                                        <div id="refresh-netstat" class="btn icon-refresh js-refresh-info"></div>
                                    </div>
                                    <div class="widget-content">								
<table id="netstat_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h4><font color="#303A34"> Eth0 Received: `/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $3, $4}'| cut -d"(" -f2 | cut -d")" -f1` </font></h4></pre></table>
<table id="netstat_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h4><font color="#303A34"> Eth0 Transmited: `/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $7, $8}'| cut -d"(" -f2 | cut -d")" -f1` </font></h4></pre></table>
                                    </div>
                                </div>
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
<i style="color:#19bc9c; font:20px/2em 'Open Sans',sans-serif;" class="icon-#" >eth0:</i>&nbsp; <h4><font color="#303A34"> RX: <span> `/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $3, $4}'| cut -d"(" -f2 | cut -d")" -f1` </span>&nbsp;&nbsp;|&nbsp;&nbsp; TX: <span>`/sbin/ifconfig | grep "RX bytes" | head -1 | /usr/bin/awk '{print $7, $8}'| cut -d"(" -f2 | cut -d")" -f1`</span></h4></font> 
                                        </div>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span4 -->

                        <div class="span4">
                                <div id="users-widget" class="widget widget-table action-table">
                                    <div class="widget-header">
                                        <i class="icon-group"></i>
                                        <h3>
                                            CPU Info
                                        </h3>
                                        <div id="refresh-users" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="users_dashboard" class="table table-hover table-bordered table-condensed"><pre><h5><font color="#303A34"> `lscpu` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span4 -->



                        <div class="span12">
                                <div id="process-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Processes
                                        </h3>
                                        <div id="refresh-ps" class="btn icon-refresh js-refresh-info"></div>
                                        <div class="pull-right">
                                       
                                        </div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="ps_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `ps axu` </font></h5></pre> </table>
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
                                        <div id="refresh-ps" class="btn icon-refresh js-refresh-info"></div>
                                        <div class="pull-right">

                                        </div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="ps_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `env` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span12 -->
                            



                            <div class="span16">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Network Servers
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `netstat -tuln` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->

                            <div class="span16">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Traffic Info
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `vnstat -i eth0`  </font></h5></pre> </table>
                        	  <table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `vnstat -i tun0`  </font></h5></pre> </table>            
			</div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->


                            <div class="span16">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Network Connections
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `netstat -tun` </font></h5></pre> </table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span9 -->

							
              <div class="span17">
                                <div id="swap-widget" class="widget widget-table">
                                    <div class="widget-header">
                                        <i class="icon-dashboard"></i>
                                        <h3>
                                            Last logins
                                        </h3>
                                        <div id="refresh-swap" class="btn icon-refresh js-refresh-info"></div>
                                    </div><!-- /widget-header -->
                                    <div class="widget-content">
                                        <table id="swap_dashboard" class="table table-hover table-condensed table-bordered"> <pre><h5><font color="#303A34"> `last -i` </font></h5></pre> </table>
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
                                    <div class="widget-content">
                                        <table id="arp_dashboard" class="table table-hover table-condensed table-bordered"><pre><h5><font color="#303A34"> `iostat -hm` </font></h5></pre></table>
                                    </div><!-- /widget-content -->
                                </div><!-- /widget -->
                            </div><!-- /span6 -->

                        <div class="span16">
                            <div id="memcached-widget" class="widget widget-nopad">
                                <div class="widget-header">
                                    <i class="icon-list-alt"></i>
                                    <h3>
                                        Users Online
                                    </h3>
                                    <div id="refresh-memcached" class="btn icon-refresh js-refresh-info"></div>
                                </div><!-- /widget-header -->
                                <div class="widget-content">
                                    <div class="big-stats-container">
                                        <pre><h5><font color="#303A34"> `w -s` </font></h5></pre>
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
                            Modified by: <a href="http://tools.tecmint.com/m/">Matei Cezar</a>
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
