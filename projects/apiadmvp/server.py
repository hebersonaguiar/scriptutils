import sys, ast, re, ldap, json, random
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from ldap3 import *
from ldap3.core.exceptions import LDAPCursorError

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

def conn():
    server_name = ''
    user_name   = 'CN=,OU=Usuarios,OU=CGTI,OU=MME,DC=mme,DC=gov,DC=br'
    password    = ''
    server      = Server(server_name, get_info=ALL)
    conn        = Connection(server, user=user_name, password=password)
    c           = conn.bind()
    return conn

# FUNCTION TO SEARCH USER IN AD, METHOD POST
@app.route('/checkuser', methods=['POST'])
def getUser():

        keyword     = str(request.json.get('login_p', None))
        domain_name = 'mme.gov.br'
        domain      = domain_name.split('.')
        connect     = conn()

        try:
           connect.search('dc={},dc={},dc={}'.format(domain[0], domain[1], domain[2]), '(sAMAccountName={})'.format(keyword), attributes = [ 'sAMAccountName' ], search_scope=SUBTREE )
           obj  = connect.entries[0].sAMAccountName.value
           user = str(obj)

           return jsonify({'login': user}), 200

        except Exception as error_message:
            # print(error_message)
            return jsonify('undefined'), 200

# FUNCTION TO ADD USER IN AD, METHOD POST
@app.route('/adduser', methods=['POST'])
def addUser():

        login       = str(request.json.get('login_p', None))
        firstname   = str(request.json.get('firstname_p', None))
        lastname    = str(request.json.get('lastname_p', None))
        department  = str(request.json.get('department_p', None))
        cpf         = str(request.json.get('cpf_p', None))
        rg          = str(request.json.get('rg_p', None))
        phone       = str(request.json.get('phone_p', None))
        room        = str(request.json.get('room_p', None))

        name = firstname + ' ' + lastname

        domain_name = 'mme.gov.br'
        domain  = domain_name.split('.')
        connect = conn()
        default_passwd = "MME@123456"

        try:
            connect.add('CN={},OU=Usuarios,OU=CGTI,OU=MME,DC=mme,DC=gov,DC=br'.format(name),
            attributes = { 'objectClass':  ['person', 'organizationalPerson', 'top', 'user'],
                           'sAMAccountName': login,
                           'userPrincipalName': "{}@{}".format(login, domain_name),
                           'name': name,
                           'displayName': name,
                           'department': department,
                           'info': cpf,
                           'givenName': firstname,
                           'sn': lastname,
                           'comment': rg,
                           'telephoneNumber': phone,
                           #'userAccountControl': '512',
                           'physicalDeliveryOfficeName': room })
           
            connect.extend.microsoft.modify_password('CN={},OU=Usuarios,OU=CGTI,OU=MME,DC=mme,DC=gov,DC=br'.format(name), default_passwd)

            return jsonify({'login': login}), 200
        except Exception as error_message:
            # print(error_message)
            return jsonify(error_message), 400

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002')

