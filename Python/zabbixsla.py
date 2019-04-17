#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Mon Out 22 10:57:32 2018

@author: Heberson Aguiar <heberson.aguiar@hepta.com.br>
"""

from zabbix_api import ZabbixAPI
from datetime import datetime, timezone
import time
import sys

# from mysql.connector import Error
# import mysql.connector

ZBX_SERVER = ''
ZBX_USER = ''
ZBX_PASS = ''


def conn(ZBX_SERVER, ZBX_USER, ZBX_PASS):

    zapi = ZabbixAPI(server=ZBX_SERVER)
    zapi.login(ZBX_USER, ZBX_PASS)

    return zapi


def convertTime(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time

    # print("d:h:m:s-> %d:%d:%d:%d" % (day, hour, minutes, seconds))

    return '%d:%d:%d:%d' % (day, hour, minutes, seconds)


def getSLA(ZBX_SERVER, ZBX_USER, ZBX_PASS):

    zapi = conn(ZBX_SERVER, ZBX_USER, ZBX_PASS)

    services = {
        'ICS::Sites': 26,
        'ICS::Sistemas': 25,
        'ICS::Virtualizacao': 23,
        'ICS::SRV_Web': 22,
        'ICS::SRV_Sistemas': 21,
        'ICS::Seguranca': 20,
        'ICS::Monitoramento': 19,
        'ICS::Gerencia_Servicos': 18,
        'ICS::Gerencia_Infra': 17,
        'ICS::Backup': 16,
        'ICS::VoIP': 263,
        'ICS::Roteadores': 12,
        'ICS::Switches': 11,
        'ICS::Ativos_Wifi': 10,
        }

    ServiceItems = services.items()
    wstart = datetime(2019, 3, 1, 0, 0)
    wend = datetime(2019,3,31,23,59,59,)
    timestampstart = wstart.replace(tzinfo=timezone.utc).timestamp()
    timestampend = wend.replace(tzinfo=timezone.utc).timestamp()

    print("\n Disponibilidade dos ICs:  " + str(wstart) + " ---- " + str(wend) + "\n")

    for Service in ServiceItems:
        sid = Service[1]
        sidstr = str(sid)

        servicessla = zapi.service.getsla({'serviceids': ['' + sidstr
                + ''], 'intervals': [{'from': timestampstart,
                'to': timestampend}]})

        for y in servicessla:
            mygsla = servicessla[y]
            timedisponibilidade = mygsla['sla'][0]['okTime'] - mygsla['sla'][0]['problemTime']
            disponibilidade = convertTime(timedisponibilidade)
            timeproblem = convertTime(mygsla['sla'][0]['problemTime'])
            timeok = convertTime(mygsla['sla'][0]['okTime'])
            timedowntime = convertTime(mygsla['sla'][0]['downtimeTime'])
            timeincidente = int(mygsla['sla'][0]['okTime']) - int(mygsla['sla'][0]['problemTime'])
            timeincidenteC = convertTime(timeincidente)

            print(Service[0] + ' SLA Aceitavel 97  SLA: ' + str(mygsla['sla'][0]['sla']) + ' Disponibilidade: ' + str(disponibilidade) + " Manutencao: " + str(timedowntime) + ' Incidente: ' +  str(timeproblem))


getSLA(ZBX_SERVER, ZBX_USER, ZBX_PASS)

