from sqlalchemy import literal

class databaseStorageListIter:
    def __init__(self, some_database_storage_list):
        self.databaseStorageListValues = some_database_storage_list
        self.currentListValueIndex = 0

    def __iter__(self):
        return self

    def __next__(self):
        currentListValue = ''

        try:
            currentListValue = self.databaseStorageListValues \
                                   .currentData[self.currentListValueIndex]

        except IndexError:
            raise StopIteration()

        self.currentListValueIndex += 1

        return currentListValue

class databaseStorageList:
    def __init__(self, **kwargs):
        self.currentData = []
        self.database = kwargs['database']
        self.databaseModel = kwargs['databasemodel']

        #https://stackoverflow.com/a/1960546/9274990
        #Creates a dictionary from an object of a model
        self.rowToDict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        
        self.getCurrentDatabaseValues()

    def getCurrentDataEntry(self, some_value):
        return self.rowToDict(some_value)

    def updateDataEntry(self, some_current_value, some_new_value):
        pass

    def getCurrentDatabaseValues(self):
        try:
            self.currentData = []

            current_values_provided = self.databaseModel.query.all()

            for some_value in current_values_provided:
                self.currentData.append(self.getCurrentDataEntry(some_value))

        except Exception as database_error:
            print('Could not get current values from database')
            
            print(database_error)

            raise ValueError

    def append(self, *args):
        for some_value_provided in args:
            try:
                self.database.session.add(self.databaseModel(**some_value_provided))
                    
            except Exception as database_error:
                print('Could not add value to database')

                print(database_error)

                raise ValueError

        self.database.session.commit()

        self.getCurrentDatabaseValues()

    def remove(self, **kwargs):
        try:
            self.databaseModel \
                .query \
                .filter_by(**kwargs) \
                .delete()

            self.database.session.commit()

            self.getCurrentDatabaseValues()
        
        except Exception as database_error:
            print('Could not remove value')

            print(database_error)

            raise ValueError

    def update(self, old_value_provided, new_value_provided):
        try:
            current_value_stored = self.databaseModel \
                                       .query \
                                       .filter_by(**old_value_provided) \
                                       .first()

            for some_key_for_update, \
                some_value_for_update \
                in new_value_provided.items():
                setattr(current_value_stored, 
                        some_key_for_update, 
                        some_value_for_update)

            self.updateDataEntry(current_value_stored, 
                                 new_value_provided)

            self.database.session.commit()

            self.getCurrentDatabaseValues()

        except Exception as database_error:
            print('Could not update values')
            
            print(database_error)

            raise ValueError

    def getValue(self, *args, **kwargs):
        try:
            if len(args) != 1 \
               and ('search_values' not in kwargs \
                    or 'search_text' not in kwargs):
                print('Invalid arguments')
                raise ValueError

            some_value_provided = ''

            if 'search_values' in kwargs and 'search_text' in kwargs:
                print('Search values')

                some_value_provided = []

                query_provided = self.databaseModel.query

                if len(args):
                        query_provided = query_provided.filter_by(**args[0])

                some_search_results = []

                for some_value in kwargs['search_values']:
                    some_search_results.append(query_provided \
                                        .filter(getattr(self.databaseModel, 
                                                        some_value)
                                                .contains(kwargs['search_text'])) \
                                        .all())

                for some_search_values in some_search_results:
                    for some_value in some_search_values:
                        if some_value not in some_value_provided:
                            some_value_provided.append(some_value)

            else:
                query_provided = self.databaseModel \
                                     .query.filter_by(**args[0])

                if 'not_equal' in kwargs:
                    for some_value_name, some_value in kwargs['not_equal'].items():
                        query_provided = query_provided.filter(getattr(self.databaseModel, some_value_name) != some_value)

                some_value_provided = query_provided.all()

            if len(some_value_provided):
                some_values = []
                
                for some_value in some_value_provided:
                    some_values.append(self.rowToDict(some_value))

                return some_values

            return []

        except Exception as database_error:
            print('Could not get value at:', database_error)

            raise IndexError

    def __len__(self):
        return len(self.currentData)

    def __getitem__(self, some_value_provided):
        some_value  = self.getValue(some_value_provided)

        if some_value == {}:
            raise ValueError

        return some_value[0]
    
    def __iter__(self):
        return databaseStorageListIter(self)

    def __contains__(self, some_value_provided):
        print(some_value_provided)
        print(self.databaseModel.query.filter_by(**some_value_provided).count() > 0)
        return self.databaseModel.query.filter_by(**some_value_provided).count() > 0

    def __setitem__(self, some_key_for_value, some_value_provided):
        try:
            self.update(some_key_for_value, some_value_provided)

        except Exception as some_error_updating_value:
            some_key_for_value.update(some_value_provided)
            self.append(some_key_for_value)