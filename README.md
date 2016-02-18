# Student Summer Intership APO 2016
* Week 1:
  * Get to know how alma works and the main job of APO. 
  * Configuring development enviroment: installing RHEL6, and other packages.
  * Thursday: Getting the idea of my project.
* Week 2:
  * Looking into APO's monitoring systems. ZENOSS, Ganglia, Nagios, EMS, PRTG, and Ducksboard.
  * Reading some of the Ducksboard scripts, specially Backlog from Arcs. Mauricio found a bug in the script database connection that left some zombie queries (Adding (ENABLE=BROKEN) and CONNECT_TIMEOUT to the connection Description fix it).
  * Starting making scripts to retrieve data (specially SO Uptime).
* Week 3:
  * Changed the monitoring architecture of APO, trying to *merge* all the monitoring system in one, using Nagios.
  *  Installed and cofigure Nagios in development enviroment, tested version 3.5.1, and 4.1.1.
    * Nagios 3.5.1: Comes in the RHEL6 repositories, so is easier to install. Doens't have a way to retrieve the current status of the service or host without parsing the status.dat file or webpage manually.
    * Nagios 4.1.1: Doesn't exists in RHEL6 repositories, but comes in RHEL7. To install you need to compile it. The configuration is the same as the older version. Comes with an restful API to get the status of a service or a host in json.The documentation says that this version has improved performance, uses smaller processes to make the checks
* Week 4:

