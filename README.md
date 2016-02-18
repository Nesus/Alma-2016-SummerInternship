# Student Summer Intership APO 2016

#Documentation:
* [Graphite & Grafana Installation](Graphite+Grafana.md) 
* [Nagios Plugins](nagios_plugins/README.md)

## Week 1:
* Get to know how ALMA works and the main job of APO. 
* Configuring development enviroment: installing RHEL6, and other packages.
* Thursday: Getting the idea of my project.

## Week 2:
* Looking into APO's monitoring systems. ZENOSS, Ganglia, Nagios, EMS, PRTG, and Ducksboard.
* Reading some of the Ducksboard scripts, especially Backlog from Arcs. Mauricio found a bug in the script database connection that left some zombie queries (Adding (ENABLE=BROKEN) and CONNECT_TIMEOUT to the connection Description fix it).
* Starting making scripts to retrieve data (especially SO Uptime).
* Created a form and a view to create Hardware Failure Events.

## Week 3:
* Downloaded SQL Developer, and tested the Backlog Query locally (not with the DBLink, and using different dates ranges for the same table), tested a "left join", "not in" and "minus" query, the "left join" one get the best performance, but in production (using DB Links), but that is the one getting stucked in the script, the second one is the "not one" 
* Changed the monitoring architecture of APO, trying to **merge** all the monitoring system in one, using Nagios.
*  Installed and cofigure Nagios in development enviroment, tested version 3.5.1, and 4.1.1.
  * Nagios 3.5.1: Comes in the RHEL6 repositories, so is easier to install. Doesn't have a way to retrieve the current status of the service or host without parsing the status.dat file or webpage manually.
  * Nagios 4.1.1: Doesn't exists in RHEL6 repositories, but comes in RHEL7. To install you need to compile it. The configuration is the same as the older version. Comes with an restful API to get the status of a service or a host in json (Can be consulted with an AJAX query or a Websocket in another page to get the data and display it).The documentation says that this version has improved performance, uses smaller processes to make the checks
* Also tested [PNP4Nagios](https://docs.pnp4nagios.org/), and [Check_MK](https://mathias-kettner.de/check_mk.html), to visualize data, the first one is already installed in production, is easy to take the graph image and put it in a webpage, but to make custom graphs is cryptic. The second one, is hard to install (Does not comes in any repository, the requierments are incomplete, the only way I made it work is using [OMD](http://omdistro.org/)
* Created a simple plugin that checks ngas status, more info in the [README file](nagios_plugins/README.md) 

## Week 4:
* Started implementing an interactive Dashboard to show graphs, and Statistics.
* Wednesday: Realized that creating an interactive Dashboard from scratch will use much more time that I thought, so I decided to change the perspective and look for a tool to visualize the data from Nagios better than PNP4Nagios. 
* Thursday: Lost day making the high altitude exams (At home, installed in my local machine, Nagios 4.1.1, Graphite, and Grafana).
* Friday: Installed and configured Graphite and Grafana locally, start testing some of the panels. Created a nagios plugin to check the ARCS pings, using PRTG HTTP API, more info in [README file](nagios_plugins/README.md).

## Week 5:
* Monday: Flight to San Pedro de Atacama.
* Tuesday: Testing Annotations in Grafana, to show hardware_failures. Using Elasticsearch documents. Trying to change the view to show hardware_failures to retrieve data from Elasticsearch instead of Mongodb, need to change the creation method and add a delete and edit functions to the view, to have all CRUD options. First meeting here in San Pedro, Alejandro asked me to write down a documentation to replicate what I have done.
* Wednesday: Started the documentation of [Graphite & Grafana Installation](Graphite+Grafana.md), [Nagios Plugins](nagios_plugins/README.md).
