#!/usr/bin/python
# Create a connection

import xmlrpclib
import pprint
import ConfigParser
import csv

config = ConfigParser.ConfigParser()
config.read("conf/connection.conf")

url = config.get('connection', 'url')
db = config.get('connection', 'db')
password = config.get('connection', 'password')
username = config.get('connection', 'username')

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

pprint.pprint(common.version())

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

with open('data/employee.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        print "Create username: " + row[0]

        #        employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{

        #            'name': "Martin",
        #           'mobile_phone': "+467676"

        # }])

        address_ids = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                        [[['name', '=', 'My Company'], ]],
                                        )
        print address_ids

        employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{

            'name': row[0],
            'work_email': row[1],
            'address_id': address_ids[0],
            'mobile_phone': ''.join(e for e in row[2] if e.isalnum() or e == '+')
        }])


# employee_info = models.execute_kw(db, uid, password, 'hr.employee', 'read', [employee_id], {'fields': ['mobile_phone']})
#
# mobile_ph = employee_info[0]['mobile_phone'][0]
#
# print mobile_ph
#
# mobile_phone = row[2],
#
# print "Create username: " + row[1]
# models.execute_kw(db, uid, password, 'hr.employee', 'write', [[mobile_phone], {
#     'mobile_phone': mobile_phone,
#     'work_email': row[1]
# }])
