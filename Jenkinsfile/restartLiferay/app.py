#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 10:57:32 2019

@author: Heberson Aguiar <heberson.aguiar@hepta.com.br>
"""

from zabbix_api import ZabbixAPI
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

ZBX_SERVER     = "http://srv217/zabbix"
ZBX_USER       = sys.argv[1]
ZBX_PASS       = sys.argv[2]


def getTriggers(ZBX_SERVER, ZBX_USER, ZBX_PASS):
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
        
    triggerid = []

    for y in triggers:
        nome_host = y["hosts"][0]["host"]
        severity = int(y["priority"])
        triggerid.append(y["triggerid"])
        description = y["description"]

        idade = time.time() - float(y["lastchange"])
        pegadia = "{0.tm_yday}".format(time.gmtime(idade))
        dia = int(pegadia) - 1
        duracao = "dias {0.tm_hour} horas {0.tm_min} minutos".format(time.gmtime(idade))
        ultima_alteracao = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(y["lastchange"])))

        if severity >= 2:
            #print("Descricao: " + description + " Nome Host: " + nome_host + " Serveridade: "+ str(severity))       
            print description       


getTriggers(ZBX_SERVER, ZBX_USER, ZBX_PASS)

