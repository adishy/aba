class routeEventManager:
    def __init__(self):
        self.eventsList = {}

    def addEvent(self, *args):
        function_names_provided = []

        for some_event_name_provided in args:
            if isinstance(some_event_name_provided, str) and not some_event_name_provided in self.eventsList:
                self.eventsList[some_event_name_provided] = []
                function_names_provided.append(some_event_name_provided)

            elif callable(some_event_name_provided):
                self.eventsList[function_names_provided[-1]].append(some_event_name_provided)

    def removeEvent(self, some_event_name_provided):
        if some_event_name_provided in self.eventsList:
            del self.eventsList[some_event_name_provided]
            return True

        return False

    def registerEventFunction(self, some_event_provided, *args):
       if not some_event_provided in self.eventsList:
           self.addEvent(some_event_provided)

       for some_function_provided in args:
           if some_function_provided in self.eventsList[some_event_provided]:
               continue

           self.eventsList[some_event_provided].append(some_function_provided)
       
       return True

    def removeEventFunction(self, some_event_provided, *args):
        if not some_event_provided in self.eventsList:
            return False

        for some_function_provided in args:
           if some_function_provided in self.eventsList[some_event_provided]:
               self.eventsList[some_event_provided].remove(some_function_provided)

        return True

    def event(self, some_event_name_provided, *args):
        try:
            for some_event_function in self.eventsList[some_event_name_provided]:
                try:
                    some_event_function(*args)
                except:
                    print('Could not run function', some_event_function.__name__)

            return True

        except:
            print('No route name:', some_event_name_provided, 'in event list')

            return False

    def __call__(self, some_event_name_provided, *args):
        self.event(some_event_name_provided, *args)

#some_events = routeEventManager()


#def somefunctionprovided(some_arguments_provided):
#    print(some_arguments_provided)

#def somefunctionroute(some_arguments_provided):
#    print('sdjkfnsndfnvksd')
    
#some_events.addEvent('routeevent', somefunctionprovided, somefunctionroute, 'nsgjnfdfnj', somefunctionprovided)

#some_events('routeevent', 'nfsdkjfnskjnblsndfk')