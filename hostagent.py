#!/usr/bin/env python

import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.fv
from cobra.mit.request import DnQuery, ClassQuery


class Agent:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

        self.ls = cobra.mit.session.LoginSession(self.host, self.user, self.passwd)
        self.md = cobra.mit.access.MoDirectory(self.ls)
        self.md.login()

    def list_services(self):
        services_list = []
        for service in self.md.lookupByClass('vzBrCP'):
            services_list.append(str(service.dn))
        return services_list

    def endpointbyip(self, ip):
        """
        :param ip: sstring IP address
        :return: fvCEp object
        """
        c = ClassQuery('fvCEp')
        c.propFilter = 'and(eq(fvCEp.ip, "%s"))' % ip
        dn = self.md.query(c)
        if len(dn) > 1:
            raise ValueError('More than one CEP with IP address')
        else:
            return dn[0].dn

    def ip_provides(self, ip):
        """

        :param ip:
        :return:
        """
        mydn = self.endpointbyip(ip)
        myparent = self.md.lookupByDn(mydn).parentDn
        myprovidedsvcs = self.epg_provides(myparent)
        return myprovidedsvcs

    def ip_consumes(self, ip):
        """
        :param ip: string IP address
        :return: list of string dn's
        """
        mydn = self.endpointbyip(ip)
        myparent = self.md.lookupByDn(mydn).parentDn
        myprovidedsvcs = self.epg_consumes(myparent)
        return myprovidedsvcs

    def whoisproviding(self, servicedn):
        """
        :param servicedn:
        :return:
        """
        providers = self.md.lookupByClass('fvRsProv', propFilter='and(eq(fvRsProv.tDn,"%s""))' % servicedn)
        provider_list = []
        for provider in providers:
            provider_list.append(str(provider.parentDn))
        return provider_list

    def whoisconsuming(self, servicedn):
        """
        Returns a
        :param servicedn:
        :return:
        """
        consumers = self.md.lookupByClass('fvRsCons', propFilter='and(eq(fvRsCons.tDn,"%s""))' % servicedn)
        consumer_list = []
        for consumer in consumers:
            consumer_list.append(str(consumer))
        return consumer_list

    def epg_provides(self, epg):
        q = DnQuery(epg)
        q.queryTarget = 'children'
        q.subtree = 'full'
        q.classFilter = 'fvRsProv'
        children = self.md.query(q)
        provided = []
        for contract in children:
            provided.append(contract.tDn)
        return provided

    def epg_consumes(self, epg):
        q = DnQuery(epg)
        q.queryTarget = 'children'
        q.subtree = 'full'
        q.classFilter = 'fvRsCons'
        children = self.md.query(q)
        consumedsvcs = []
        for contract in children:
            consumedsvcs.append(contract.tDn)
        return consumedsvcs

    def epg_endpoints(self, epg):
        q = DnQuery(epg)
        q.queryTarget = 'children'
        q.subtree = 'full'
        q.classFilter = 'fvCEp'
        children = self.md.query(q)
        endpoints = []
        for ep in children:
            endpoints.append(ep.ip)
        return endpoints

    def consumeservice(self, dn, contractdn, svcflag):
        """
        :param dn: dn of epg
        :param contractdn: dn of contract
        :param svcflag: boolean add/delete fvRsProv
        :return:
        """
        epg, contract = self.md.lookupByDn(dn), self.md.lookupByDn(contractdn)
        if svcflag:
            fvrscons = cobra.model.fv.RsCons(epg, tnVzBrCPName=contract.name)
        else:
            fvrscons = cobra.model.fv.RsCons(epg, tnVzBrCPName=contract.name).delete()
        c1 = cobra.mit.request.ConfigRequest()
        c1.addMo(epg)
        self.md.commit(c1)
        return fvrscons

    def provideservice(self, dn, contractdn, svcflag):
        """
        :param dn: dn of epg
        :param contractdn: dn of contract
        :param svcflag: boolean add/delete fvRsProv
        :return:
        """
        epg, contract = self.md.lookupByDn(dn), self.md.lookupByDn(contractdn)
        if svcflag:
            fvrsprov = cobra.model.fv.RsProv(epg, tnVzBrCPName=contract.name)
        else:
            fvrsprov = cobra.model.fv.RsProv(epg, tnVzBrCPName=contract.name).delete()
        c1 = cobra.mit.request.ConfigRequest()
        c1.addMo(epg)
        return fvrsprov
