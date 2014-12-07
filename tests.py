#!/usr/bin/env python

import hostagent


hostname = 'http://10.94.140.71'
username = 'admin'
passwd = 'PASS'

ctrlr = hostagent.Agent(hostname, username, passwd)

print "### Service Discovery ###"
print "=" * 40
print "List all services provided by the fabric"
print ctrlr.list_services()
print "Who is consuming what"
print "=" * 40

for service in ctrlr.list_services():
    if len(ctrlr.whoisconsuming(service)) > 0:
        print "Consumers of service %s: " % service, ctrlr.whoisproviding(service)
    else:
        print "No consumers found for %s" % service

print "What Services is an IP is providing"
print "=" * 40
print "IP 192.168.10.2 is currently providing: ", ctrlr.ip_provides('192.168.10.2')

print "What Services is an IP is consuming"
print "=" * 40
print "IP 192.168.10.2 is currently consuming:", ctrlr.ip_consumes('192.168.10.2')

print "Who is providing what"
print "=" * 40
for service in ctrlr.list_services():
    if len(ctrlr.whoisproviding(service)) > 0:
        print "Providers of service %s: " % service, ctrlr.whoisproviding(service)
    else:
        print "No providers found for %s" % service

print "What IP address are providing a service"
print "=" * 40
print "uni/tn-tenant1/ap-app1/epg-db has members", ctrlr.epg_endpoints('uni/tn-mgmt/ap-mgmt-applications/epg-server-management')

print "IP 192.168.10.2 is currently providing: ", ctrlr.ip_provides('192.168.10.2')

# # set's some sample inputs for the next section
dn = ctrlr.endpointbyip('192.168.10.2')
epg = ctrlr.md.lookupByDn(dn).parentDn

print epg



print "#### SERVICE CONSUMPTION ####"
print "=" * 40
print '\n\n'
print "IP 192.168.10.2 is currently consuming: ", ctrlr.ip_consumes('192.168.10.2')
print "Adding consumed service"
ctrlr.consumeservice(epg, 'uni/tn-common/brc-default', True)
# ctrlr.subscribe(epg, 'uni/tn-common/brc-default')
print "IP 192.168.10.2 is currently consuming: ", ctrlr.ip_consumes('192.168.10.2')
print "Removing consumed service"
#ctrlr.unsubscribe(epg, 'uni/tn-common/brc-default')
ctrlr.consumeservice(epg, 'uni/tn-common/brc-default', False)
print "IP 192.168.10.2 is currently consuming: ", ctrlr.ip_consumes('192.168.10.2')
print '\n\n'
print "### SERVICE ADVERTISEMENT ###"
print "=" * 40
print '\n\n'
print "IP 192.168.10.2 is currently providing: ", ctrlr.ip_provides('192.168.10.2')
print "Adding provided service"
ctrlr.provideservice(epg, 'uni/tn-common/brc-default', True)
print "IP 192.168.10.2 is currently providing: ", ctrlr.ip_provides('192.168.10.2')
print "Removing provided service"
ctrlr.provideservice(epg, 'uni/tn-common/brc-default', False)
print "IP 192.168.10.2 is currently providing: ", ctrlr.ip_provides('192.168.10.2')
