#!/usr/bin/python
# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI
import time
#from conf.vars import *

ZBX_SERVER = "http://172.16.1.50:8080/zabbix"
ZBX_USER = "Admin"
ZBX_PASS = "zabbix"

zapi = ZabbixAPI(server=ZBX_SERVER)
zapi.login(ZBX_USER, ZBX_PASS)

triggers = zapi.trigger.get ({
            "output": ["description", "lastchange", "triggerid", "priority"],
            "selectHosts": ["hostid", "host"],
            "selectLastEvent": ["eventid", "acknowledged", "objectid", "clock", "ns"],
            "sortfield" : "lastchange",
            "monitored": "true",
            "only_true": "true",
            "maintenance":  "false",
            "expandDescription": True,
            "filter":{"value":1}
            })

for y in triggers:
    nome_host = y["hosts"][0]["host"]
    severity = int(y["priority"])
    triggerid = y["triggerid"]

    idade = time.time() - float(y["lastchange"])
    pegadia = "{0.tm_yday}".format(time.gmtime(idade))
    dia = int(pegadia) - 1
    duracao = "dias {0.tm_hour} horas {0.tm_min} minutos".format(time.gmtime(idade))
    ultima_alteracao = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(y["lastchange"])))
    #print nome_host, "- ", y["description"], "- ", ultima_alteracao, "- ", dia, duracao

    if severity == 3:
        severityHost = "Average"
        print "---------------------------------------"
        print "Host: ", nome_host, "- Trigger ID:", triggerid, "- Severity: ", severityHost
        print "---------------------------------------"
    else:
        print "Unknown Severity "

