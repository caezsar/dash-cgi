
Linux-dash server monitoring for apache/nginx CGI gateway environment
=======
Linux-dash server monitoring for Apache CGI gateway environment for Ubuntu && Debian in raw format.

- Default logs that application reads: `/var/log/apache2/access.log`
- Default Network Interfaces: `eth0 && tun0`

Install `sysstat, vnstat, wget`tools.

Installation:

- Clone the app into your apache webroot host (Ex: `/var/www/html/`) with using Git cmd line:

`git clone https://github.com/caezsar/dash-cgi.git`

- Visit `http://your_fqdn or server address/dash-cgi/`

![alt text](https://raw.githubusercontent.com/caezsar/dash-cgi/master/screenshot.jpg "screenshot")



