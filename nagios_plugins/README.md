# Simple Nagios Plugins - Summer Internship 2016
## check_ngas.py
Check NGAS status.
### How it works
Sends a HTTP GET request to http://$NGAS_HOST$:$PORT$/STATUS and parse the response XML to see if the process is UP or DOWN.

Uses two parameters, the host address (without http://) and the port. For example: 
```
./check_ngas.py ngasXX.site.alma.cl 7777
```

### Configuring in Nagios
Add the following command
```
define command {
        command_name check_ngas_status
        command_line $USER1$/check_ngas.py $HOSTNAME$ $ARG1$
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
### Configuring in Nagios
Add the command to Nagios.
```
define command {
        command_name check_prtg_ping
        command_line $USER1$/check_prtg_ping.py $ARG1$ $ARG2$ $ARG3$
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
