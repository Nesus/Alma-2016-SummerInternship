# Simple Nagios Plugins - Summer Internship 2016
## check_ngas.py
Check NGAS status.
### How it works
Sends a HTTP GET request to http://$NGAS_HOST$:$PORT$/STATUS and parse the response XML to see if the process is UP or DOWN.

Uses two parameters, the host address (without http://) and the port. For example: 
```
./check_ngas.py -H ngasXX.site.alma.cl -p 7777
```

for more info run 

```
./check_ngas.py -h
```

** Requirements ** : python-requests

### Configuring in Nagios
Add the following command
```
define command {
        command_name check_ngas_status
        command_line $USER1$/check_ngas.py -H $HOSTNAME$ -p $ARG1$
}
```
And define a service for each port.
```
define service{
        use                             long-monitoring-service
        hostgroup_name                  ngas-servers
        service_description             NGAS_status:7777
        check_command                   check_ngas_status!7777
}
define service{
        use                             long-monitoring-service
        hostgroup_name                  ngas-servers
        service_description             NGAS_status:7778
        check_command                   check_ngas_status!7778
}

define service{
        use                             long-monitoring-service
        hostgroup_name                  ngas-servers
        service_description             NGAS_status:7779
        check_command                   check_ngas_status!7779
}

define service{
        use                             long-monitoring-service
        hostgroup_name                  ngas-servers
        service_description             NGAS_status:7780
        check_command                   check_ngas_status!7780
}
```
Optional: Create a template for the service to request the status in bigger time intervals. In this example is long-monitoring-service and a hostgroup with all the ngas hosts (ngas-servers).

## check_prtg_ping.py
Check the ARC status, and latency using PRTG API.

### How it Works
Sends a HTTP GET request to PRTG sensor status API, and parse the json response.

This plugin is meant to be use locally (localhost), and has three parameters, the sensor_id from the prtg ping sensor, the warning latency and a critical latency (both used by nagios to send notifications). Doesnt work with other sensors.

*Configuration*: Add prtg username and password to PRTG_USERNAME and PRTG_PASSWORD enviroment variables to .bashrc (export PRTG_USERNAME='username') 

For more info about the plugin parameters run
```
./check_prtg_ping.py -h
```
** Requirements ** : python-requests

### Configuring in Nagios
Add the command to Nagios.
```
define command {
        command_name check_prtg_ping
        command_line $USER1$/check_prtg_ping.py $ARG1$ -w $ARG2$ -c $ARG3$
}
```
And then create a service for each sensor_id.
```
define service{
        use                             long-monitoring-service
        host_name                       PRTG
        service_description             PING NAOJ
        check_command                   check_prtg_ping!4710!500!700
}
```

## check_backlog.py

### How it works

Using Alejandro's Script, consults the production and ARC database to see how many files and size are in the local db and not the external.

The query in the script uses the NOT IN statement, further work have to check if there is a way to obtain a better performance changing the query.

To run the plguin just pass the ARC Shortname as argument to the script. For example:
```
./check_backlog.py eu
```
Is case insensitive, so don't worry to use lower case.

For default it show OK status if there's no files older than a day (configurable with -ol flag). To send critical notifications add a warning flag, with a size in gb and a critical flag with the amount of files.
```
./check_backlog.py arc -w size_in_gb -c files

```
To see other options 

```
./check_backlog.py -h
``` 

**Requirements:** import cx_Oracle

## Configuring in Nagios

* Create a command
```
define command {
        command_name check_backlog
        command_line $USER1$/check_backlog.py $ARG1$ -ol $ARG2$ -d $ARG3$ -hs $ARG4$ -w $ARG5$ -c $ARG6$
}
```

* Create a service for each Arc

```
define service{
        use                             long-monitoring-service
        host_name                       localhost
        service_description             Backlog EU
        check_command                   check_backlog!EU!1!2!0!200
}
```


# Other Plugins
* [check_uptime](https://exchange.nagios.org/directory/Plugins/System-Metrics/Uptime/check_uptime--2F-check_snmp_uptime/details):
Check the uptime from the remote server, used with check_nrpe.
  * Download check_uptime.pl to each remote server, and put in plugin folder
  * Add command to nrpe.cfg, use -f to get uptime in minutes and -w, -c for warning and critical notifications if uptime is less than a value.
  ```
    command[check_uptime]=/usr/local/nagios/libexec/check_uptime.pl -f -c 5
  ```
  * Create service using check_nrpe command and pass the arguments (**if using xinetd to run nrpe, install it to support arguments**).
  ```
  define service{
        use                             generic-service
        host_name                       host
        service_description             Uptime
        check_command                   check_nrpe!check_uptime
  } 
  ```

