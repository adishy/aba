#########################################################################################
#FLASK MODULES
#########################################################################################
from flask import session

#Sets a new session key from the tuple provided for the current session
def setSessionKey(some_tuple_provided):
	   session[some_tuple_provided[0]] = some_tuple_provided[1]

#Checks whether a given key already exists in the current session
def sessionKeyValid(some_session_key_provided):
	   return some_session_key_provided in session

#Removes a key from the current session
def removeSessionKey(some_session_key_provided):
		del session[some_session_key_provided]