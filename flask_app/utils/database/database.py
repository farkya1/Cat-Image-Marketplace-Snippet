import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow


class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users','images','wallet','tokens','blockchain','hashes']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id
    

    #returns a nested dictionary of allthe resume data
    def getResumeData(self):

        
        institutions = self.query("SELECT * FROM institutions")    

        finalDic = dict()

        #goes through each institution
        for countInst, institution in enumerate(institutions):
            
            tempDicInst = dict()
            tempDicInst["city"] = institution["city"]
            tempDicInst["address"] = institution["address"]
            tempDicInst["state"] = institution["state"]
            tempDicInst["type"] = institution["type"]
            tempDicInst["zip"] = institution["zip"]
            tempDicInst["department"] = institution["department"]
            tempDicInst["name"] = institution["name"]
            tempDicInst["positions"] = {}

            positionQuery = "SELECT * FROM positions WHERE inst_id ="+str(institution["inst_id"])

            positions = self.query(positionQuery)
            
            #goes through each position for the institution
            for countPosition, position in enumerate(positions):
                tempDicPos = dict()
                tempDicPos["end_date"] = position["end_date"]
                tempDicPos["start_date"] = position["start_date"]
                tempDicPos["title"] = position["title"]
                tempDicPos["responsibilities"] = position["responsibilities"]
                tempDicPos["experiences"] = {}

                experienceQuery = "SELECT * FROM experiences WHERE position_id ="+str(position["position_id"])

                experiences = self.query(experienceQuery)

                #goes through each experience for the position
                for countExperience, experience in enumerate(experiences):
                    tempDicExp = dict()

                    tempDicExp["description"] = experience["description"]
                    tempDicExp["start_date"] = experience["start_date"]
                    tempDicExp["end_date"] = experience["end_date"]
                    tempDicExp["name"] = experience["name"]
                    tempDicExp["hyperlink"] = experience["hyperlink"]
                    tempDicExp["skills"] = {}

                    skillQuery = "SELECT * FROM skills WHERE experience_id ="+str(experience["experience_id"])

                    skills = self.query(skillQuery)
            
                    #goes through each skill for the experience
                    for countSkills, skill in enumerate(skills):
                        
                        tempDicSkill = dict()
                        tempDicSkill["name"] = skill["name"]
                        tempDicSkill["skill_level"] = skill["skill_level"]

                        tempDicExp["skills"][countSkills+1] = tempDicSkill

                    tempDicPos["experiences"][countExperience+1] = tempDicExp

                tempDicInst["positions"][countPosition+1] = tempDicPos

            finalDic[countInst+1] = tempDicInst


        return finalDic
    
    #returns a nested dictionary of one of the jobs
    def getSpecificResumeData(self, institutionName):

        
        institutions = self.query(f"SELECT * FROM institutions WHERE name = '{institutionName}'")    

        finalDic = dict()

        #goes through each institution
        for countInst, institution in enumerate(institutions):
            
            tempDicInst = dict()
            tempDicInst["inst_id"] = institution["inst_id"]
            tempDicInst["city"] = institution["city"]
            tempDicInst["address"] = institution["address"]
            tempDicInst["state"] = institution["state"]
            tempDicInst["type"] = institution["type"]
            tempDicInst["zip"] = institution["zip"]
            tempDicInst["department"] = institution["department"]
            tempDicInst["name"] = institution["name"]
            tempDicInst["positions"] = {}

            positionQuery = "SELECT * FROM positions WHERE inst_id ="+str(institution["inst_id"])

            positions = self.query(positionQuery)
            
            #goes through each position for the institution
            for countPosition, position in enumerate(positions):
                tempDicPos = dict()
                tempDicPos["inst_id"] = position["inst_id"]
                tempDicPos["end_date"] = position["end_date"]
                tempDicPos["start_date"] = position["start_date"]
                tempDicPos["title"] = position["title"]
                tempDicPos["responsibilities"] = position["responsibilities"]
                tempDicPos["experiences"] = {}

                experienceQuery = "SELECT * FROM experiences WHERE position_id ="+str(position["position_id"])

                experiences = self.query(experienceQuery)

                #goes through each experience for the position
                for countExperience, experience in enumerate(experiences):
                    tempDicExp = dict()

                    tempDicExp["description"] = experience["description"]
                    tempDicExp["start_date"] = experience["start_date"]
                    tempDicExp["end_date"] = experience["end_date"]
                    tempDicExp["name"] = experience["name"]
                    tempDicExp["hyperlink"] = experience["hyperlink"]
                    tempDicExp["skills"] = {}

                    skillQuery = "SELECT * FROM skills WHERE experience_id ="+str(experience["experience_id"])

                    skills = self.query(skillQuery)
            
                    #goes through each skill for the experience
                    for countSkills, skill in enumerate(skills):
                        
                        tempDicSkill = dict()
                        tempDicSkill["name"] = skill["name"]
                        tempDicSkill["skill_level"] = skill["skill_level"]

                        tempDicExp["skills"][countSkills+1] = tempDicSkill

                    tempDicPos["experiences"][countExperience+1] = tempDicExp

                tempDicInst["positions"][countPosition+1] = tempDicPos

            finalDic[countInst+1] = tempDicInst


        return finalDic
    

    #removes a specified job
    def removeJob(self, institutionName):

        insts = self.query(f"SELECT * from institutions where name = '{institutionName}'")

        
        for inst in insts:

            inst_id = inst["inst_id"]
            

            positions = self.query(f"SELECT * from positions where inst_id = '{inst_id}'")

            #goes through each position for the institution
            for position in positions:
                position_id = position["position_id"]
                

                experiences = self.query(f"SELECT * from experiences where position_id = '{position_id}'")

                #goes through each experience for each position
                for experience in experiences:
                    experience_id = experience["experience_id"]
                    
                    #deletes all the skills
                    self.query(f"DELETE from skills where experience_id = '{experience_id}'")

                    #deletes all the experiences
                    self.query(f"DELETE from experiences where experience_id = '{experience_id}'")

                #deletes all the positions
                self.query(f"DELETE from positions where position_id = '{position_id}'")

            #deletes the institution
            self.query(f"DELETE from institutions where name = '{institutionName}'")


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################

    #adds a user to the database
    def createUser(self, email='me@email.com', password='password', role='user'):
        
        emailTest = self.query(f"""SELECT * FROM users WHERE email = \"{email}\"""")

        if emailTest:
            return {'success': 0}


        
        try:
            encPassword = self.onewayEncrypt(password)

            query = f"""INSERT IGNORE INTO users (role, email, password) VALUES (\"{role}\",\"{email}\",\"{encPassword}\");"""

            self.query(query)

            return {'success': 1}
        
        except:
            
            return {'success': 0}

    #authentication to see if the login is in the database
    def authenticate(self, email='me@email.com', password='password'):

        encPassword = self.onewayEncrypt(password)
        result = self.query(f"SELECT * FROM users WHERE email = '"+email+"' AND password = '" + encPassword + "';")
        if len(result):
            return {'success': 1}
        else:
            return {'success': 0}

    #one way encription for the passwords
    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string

    #reversible encription for the emails
    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


