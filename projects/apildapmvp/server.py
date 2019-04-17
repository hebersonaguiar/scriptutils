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

# FUNCAO PARA ADICIOMAR USUARIO NO LDAP VIA POST
@app.route('/adduser', methods=['POST'])
def addUser():
        address = "ldap"
        user = "cn=admin,dc=my-company,dc=com"
        password = "JonSn0w"

        connection = ldap.initialize("ldap://%s"%address)
        connection.protocol_version = ldap.VERSION3  #define versao 3 do protocolo ldap (recomendado)
        connection.bind(user,password)


        login = str(request.json.get('login_p', None))
        firstname = str(request.json.get('firstname_p', None))
        lastname = str(request.json.get('lastname_p', None))
        department = str(request.json.get('department_p', None))
        cpf = str(request.json.get('cpf_p', None))
        rg = str(request.json.get('rg_p', None))
        phone = str(request.json.get('phone_p', None))
        room = str(request.json.get('room_p', None))

        cn = firstname + ' ' + lastname
        uidNumber = random.randint(1001,1999)

        loginB = bytes('%s' % login, 'utf-8')
        cnB = bytes('%s' % cn, 'utf-8')
        departmentB = bytes('%s' % department, 'utf-8')
        cpfB = bytes('%s' % cpf, 'utf-8')
        rgB = bytes('%s' % rg, 'utf-8')
        phoneB = bytes('%s' % phone, 'utf-8')
        roomB = bytes('%s' % room, 'utf-8')
        uidNumberB = bytes('%s' % uidNumber, 'utf-8')

        try:
                add_user = [
                 ('objectclass', [b'person',b'organizationalperson',b'posixAccount',b'top']),
                 ('uid', [loginB]),
                 ('cn', [cnB]),
                 ('sn', [b'User'] ),
                 ('gidNumber', [b'1001']),
                 ('uidNumber', [uidNumberB]),
                 ('homeDirectory', [departmentB]),
                 ('description', [cpfB]),
                 ('localityName', [rgB]),
                 ('telephoneNumber', [phoneB]),
                 ('title', [roomB]),
                ]
                connection.add_s('uid=%s,dc=my-company,dc=com'%str(login), add_user)
                return jsonify({'useradd': '%s'%str(login)}), 200
        except ldap.LDAPError as error_message:
                print(error_message)
                return jsonify(error_message), 400

# FUNCAO PARA CONSULTA NO LDAP VIA POST
@app.route('/checkuser', methods=['POST'])
def getUser():
        # if not request.json or not 'login_p' in request.json:
        #       abort(400)

        address = "ldap"
        user = "cn=admin,dc=my-company,dc=com"
        password = "JonSn0w"
        keyword = str(request.json.get('login_p', None))

        connection = ldap.initialize("ldap://%s"%address)
        connection.protocol_version = ldap.VERSION3  #define versao 3 do protocolo ldap (recomendado)
        connection.bind(user,password)

        base = "dc=my-company,dc=com"
        scope = ldap.SCOPE_SUBTREE
        filter = "uid=" + keyword
        retrieve_attributes = None
        count = 0
        result_set = []
        timeout = 0
        try:
                result_id = connection.search(base, scope, filter, retrieve_attributes)
                while 1:
                        result_type, result_data = connection.result(result_id, timeout)
                        if (result_data == []):
                                break
                        else:
                                if result_type == ldap.RES_SEARCH_ENTRY:
                                        result_set.append(result_data)
                if len(result_set) == 0:
                        # print("No Results.")
                        return jsonify(result_set), 200
                for i in range(len(result_set)):
                        for entry in result_set[i]:
                                try:
                                        name = entry[1]['uid'][0],
                                        count = count + 1
                                        # print(name)
                                        # print("Name: %s" %(name))
                                        return json.dump(name)
                                except:
                                        pass
        except ldap.LDAPError as error_message:
                print(error_message)

        name_str = str(name)
        chars = "')(,"
        for char in chars:
                name_str = name_str.replace(char,"")

        uid = ''.join(name_str.split('b', 1))


        return jsonify({'login': uid}), 200


if __name__ == '__main__':
     app.run(host='0.0.0.0', port='80')


