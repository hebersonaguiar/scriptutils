#!/usr/bin/python
# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI
from pyotrs import Client, Article, Ticket, DynamicField
from mysql.connector import Error
import mysql.connector
import time


ZBX_SERVER     = "http://172.16.1.50:8080/zabbix"
ZBX_USER       = "Admin"
ZBX_PASS       = "zabbix"
OTRS_SERVER    = "http://172.16.1.50"
OTRS_USER      = "admin"
OTRS_PASS      = "admin"
OTRS_DB_NAME   = "otrs"
OTRS_DB_USER   = "otrs"
OTRS_DB_PASS   = "123456"
OTRS_DB_SERVER = "172.16.1.50"
QUEUE 		   = "Junk"
STATE 		   = "new"
PRIORITY 	   = "3 normal"
CUSTOMERUSER   = "test"


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
             # triggerid = y["triggerid"]
             triggerid.append(y["triggerid"])
    
             idade = time.time() - float(y["lastchange"])
             pegadia = "{0.tm_yday}".format(time.gmtime(idade))
             dia = int(pegadia) - 1
             duracao = "dias {0.tm_hour} horas {0.tm_min} minutos".format(time.gmtime(idade))
             ultima_alteracao = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(y["lastchange"])))

    
        return triggerid

def getTriggersDB(OTRS_DB_NAME, OTRS_DB_USER, OTRS_DB_PASS, OTRS_DB_SERVER):

	connection = mysql.connector.connect(host=OTRS_DB_SERVER,
                         database=OTRS_DB_NAME,
                         user=OTRS_DB_USER,
                         password=OTRS_DB_PASS)

        query = "SELECT \
                TB2.value_text AS triggerid \
            FROM dynamic_field TB1 \
                INNER JOIN dynamic_field_value TB2 ON TB2.field_id = TB1.id \
                INNER JOIN ticket TB3 ON TB3.id = TB2.object_id \
            WHERE TB1.name = 'TriggerID' AND TB1.valid_id = 1 AND TB3.ticket_state_id = 1  AND TB2.value_text;"

        rows = []

        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
        	rows.append(row[0])

        return rows

def buildTicket(OTRS_SERVER, OTRS_USER, OTRS_PASS, HOST, TRIGGERID, SEVERITY, DESCRIPTION, QUEUE, STATE, PRIORITY, CUSTOMERUSER):

	client = Client(OTRS_SERVER, OTRS_USER, OTRS_PASS)
	client.session_create()
	new_ticket = Ticket.create_basic(Title="Server "+ HOST +" Down",
                             Queue="" +  QUEUE + "",
                             State=u"" +  STATE + "",
                             Priority=u"" +  PRIORITY + "",
                             CustomerUser="" +  CUSTOMERUSER + "")
	first_article = Article({"Subject": "Server " + HOST + " Down"  , "Body": "Host: " + HOST + " Trigger ID: " + TRIGGERID +" Severity: " + SEVERITY + "Descricao: " + DESCRIPTION })
	dynamic_field = DynamicField("TriggerID", value="" + TRIGGERID + "")
	client.ticket_create(new_ticket, first_article, None ,dynamic_fields=[dynamic_field])

	return "Ticket Build"


def createTicket(ZBX_SERVER, ZBX_USER, ZBX_PASS):
	triggerszabbix = getTriggers(ZBX_SERVER, ZBX_USER, ZBX_PASS)
	triggersotrs   = getTriggersDB(OTRS_DB_NAME, OTRS_DB_USER, OTRS_DB_PASS, OTRS_DB_SERVER)

	difftriggers = list(set(triggerszabbix) - set(triggersotrs))

	for TRIGGERID in difftriggers:
		if not TRIGGERID:
			print "Lista vazia"
		else:
			zapi = ZabbixAPI(server=ZBX_SERVER)
			zapi.login(ZBX_USER, ZBX_PASS)

			triggers = zapi.trigger.get ({
		            "output": ["description", "lastchange", "triggerid", "priority"],
		            "search": {"triggerid": 15700},
		            "selectHosts": ["hostid", "host"],
		            "selectLastEvent": ["eventid", "acknowledged", "objectid", "clock", "ns"],
		            "sortfield" : "lastchange",
		            "monitored": "true",
		            "only_true": "true",
		            "maintenance":  "false",
		            "expandDescription": True,
		            "filter":{
		            	"value":1,
		            	"triggerid": ""+ TRIGGERID +""}
		            })

		    	for y in triggers:
		             HOST = y["hosts"][0]["host"]
		             severity = int(y["priority"])
		             TRIGGERID = y["triggerid"]
		             DESCRIPTION = y["description"]

		             if severity == 0:
		             	SEVERITY = "Not Classified"
		             elif severity == 1:
		             	SEVERITY = "Information"
		             elif severity == 2:
		             	SEVERITY = "Warning"
		             	buildTicket(OTRS_SERVER, OTRS_USER, OTRS_PASS, HOST, TRIGGERID, SEVERITY, DESCRIPTION, QUEUE, STATE, PRIORITY, CUSTOMERUSER)
		             elif severity == 3:
		             	SEVERITY = "Average"
		             	buildTicket(OTRS_SERVER, OTRS_USER, OTRS_PASS, HOST, TRIGGERID, SEVERITY, DESCRIPTION, QUEUE, STATE, PRIORITY, CUSTOMERUSER)
		             elif severity == 4:
		             	SEVERITY = "High"
		             	buildTicket(OTRS_SERVER, OTRS_USER, OTRS_PASS, HOST, TRIGGERID, SEVERITY, DESCRIPTION, QUEUE, STATE, PRIORITY, CUSTOMERUSER)
		             elif severity == 5:
		             	SEVERITY = "Disaster"
		             else:
		             	print "Unknown Severity"

	return "Chamado criado com sucesso!"

createTicket(ZBX_SERVER, ZBX_USER, ZBX_PASS)

