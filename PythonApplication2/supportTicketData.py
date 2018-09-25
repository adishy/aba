import datetime
import pprint
from databaseStorageList import databaseStorageList
from mainview import db
from dataModels import supportticketslist

class someDatabaseValue(databaseStorageList):
    def __init__(self):
        super().__init__(database = db, databasemodel = supportticketslist)

someticketlist = someDatabaseValue()

someticketlist.update({'supportid': 'eMIoL7iuu'}, 
                      {'supportstatustype': 'Ongoing'})

pp = pprint.PrettyPrinter(indent = 4)

pp.pprint(someticketlist.currentData)

pp.pprint(someticketlist[{'supportid': 'eMIoL7iuu'}])

someticketlist.remove(supportid = 'cnVDv21nv')

print({'supportid' : 'eMIoL7iuu'} in someticketlist)

someticketlist[{'supportid': 'cnVDv21nv'}] = {'supportdatetime': datetime.datetime.now(),
                                              'supportdescription': 'Some text provided',
                                              'supportid': 'cnVDv21nv',
                                              'supportlocation': 'Location Provided A',
                                              'supportstaffassigned': 'Unassigned to staff',
                                              'supportstaffemail': 'Unassigned to staff',
                                              'supportstaffimage': 'Unassigned to staff',
                                              'supportstaffname': 'Unassigned to staff',
                                              'supportstatusdescription': 'Processing ticket',
                                              'supportstatustype': 'Ongoing',
                                              'supporttype': 'Issue category 2',
                                              'ticketsubmissiondatetime': datetime.datetime.now(),
                                              'user_email': 'aditya.manjushashylesh@gmail.com',
                                              'user_id': '103827197448037535734',
                                              'user_image': 'https://lh6.googleusercontent.com/-d1jI9WYJnCc/AAAAAAAAAAI/AAAAAAAASS4/O0F7pmvs3Ag/s96-c/photo.jpg',
                                              'user_name': 'Aditya Manjusha Shylesh'}

for some_value in someticketlist:
    print(some_value)

