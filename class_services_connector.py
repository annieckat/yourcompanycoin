import os
import pymysql
import pygsheets

class ServicesConnector:
    
    def __init__(self):
        self.DB_HOST=os.environ.get('DB_HOST')
        self.DB_NAME=os.environ.get('DB_NAME')
        self.DB_USER=os.environ.get('DB_USER')
        self.DB_PASSWRD=os.environ.get('DB_PASSWRD')
        self.SERVICE_ACCOUNT_FILE_ADDRESS = os.environ.get('SERVICE_ACCOUNT_FILE_ADDRESS')
        self.SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    def mysql_connect(self):
        mysql_cn = pymysql.connect(host=self.DB_HOST, 
                    port=3306, user=self.DB_USER, passwd=self.DB_PASSWRD, 
                    db=self.DB_NAME, autocommit=False)
        return(mysql_cn)

    def gs_connect(self):
        gs_cn = pygsheets.authorize(service_account_file=self.SERVICE_ACCOUNT_FILE_ADDRESS ,scopes=self.SCOPES)
        return(gs_cn)

