import json
import os

class EasyDB:
    path = ''
    mode = 'buffer' # or 'file'
    data = []
    status = False
    def __init__(self,path=''):
        try:
            if path != '':
                self.path = path
                self.mode = 'file'
                if os.path.isfile(path):
                    with open(path) as f:
                        content = f.read()
                        self.data = json.loads(content) if content != '' else []
            else:
                self.mode = 'buffer'
            self.status = True
        except:
            self.status = False

    def table(self,tableList:list):
        try:
            if len(self.data) == 0:
                self.data.append(tableList)
            else:
                self.data[0] = tableList
            return True
        except:
            return False

    def insert(self,record:list):
        try:
            if len(self.data[0]) == len(record):
                self.data.append(record)
                return True
            else:
                return False
        except:
            return False
        

    def fetch_all(self):
        return self.data

    def fetch(self,call:dict): #call:查询条件
        request = {}
        response = []
        for i in range(0,len(self.data[0])):
            if self.data[0][i] in call.keys():
                request[i] = call[self.data[0][i]]
        total = len(self.data)
        if total == 0:
            return response
        for i in range(0,len(self.data)):
            for key,value in request.items():
                sign = False
                if self.data[i][key] == value:
                    sign = True
            if sign:
                response.append(self.data[i])
        return response

    def delete(self,call):
        try:
            request = {}
            for i in range(0,len(self.data[0])):
                if self.data[0][i] in call.keys():
                    request[i] = call[self.data[0][i]]
            total = len(self.data)
            if total == 0:
                return True
            for i in range(0,len(self.data)):
                for key,value in request.items():
                    sign = False
                    if self.data[i][key] == value:
                        sign = True
                if sign:
                    self.data.pop(i)
            return True
        except:
            return False

    def save(self):
        if self.mode == 'file':
            try:
                with open(self.path,'w+') as f:
                    f.write(json.dumps(self.data))
                return True
            except:
                return False
        else:
            return False
