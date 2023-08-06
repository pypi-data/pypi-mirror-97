import os
import json

class database:
    def __init__(self, database_name):
        self.database_name = database_name
        print(f'Database initialized with name {self.database_name}')
        if os.path.exists('db') == False:
            os.mkdir('db')
        if os.path.exists(os.path.join(os.path.join(os.getcwd(), 'db'), self.database_name)) == False:
            os.mkdir(os.path.join(os.path.join(os.getcwd(), 'db'), self.database_name))
    def set(self, key, value):
        if value == None:
            raise Exception('Can\'t make an empty key.')
        file = open(os.path.join(os.path.join(os.path.join(os.getcwd(), 'db'), self.database_name), str(key) + ".frost"), 'w+')
        if type(value) == type('string'):
            file.write('{"value": "' + value + "\"}")
        else:
            file.write('{"value": ' + value + "}")
        file.close()

    def get(self, key):
        try:
            file = open(os.path.join(os.path.join(os.path.join(os.getcwd(), 'db'), self.database_name), str(key) + ".frost"), 'r+')
            return JSON.load(file.readlines())["value"]
            file.close()
        except Exception as e:
            return None

    def delete(self, key):
        try:
            os.remove(os.path.join(os.path.join(os.path.join(os.getcwd(), 'db'), self.database_name), str(key) + ".frost"))
        except Exception as e:
            print('WARN : The following key doesn\'t exist, useless delete function has been used.')

    def inc(self, key, value=1):
        try:
            set(key, int(get(key)) + value)
        except:
            print(f'Error : Unable to increment type {type(get(key))}')