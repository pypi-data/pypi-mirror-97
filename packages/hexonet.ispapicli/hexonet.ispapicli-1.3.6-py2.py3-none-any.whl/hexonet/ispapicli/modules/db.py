import os
import sys
import json
from tinydb import TinyDB, Query


class DB:

    def __init__(self) -> None:
        self.__initAppDirectories()
        print(self.db_file_path)
        self.initDB()

    def initDB(self):
        # check for first use of the tool
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
            f = open(self.db_file_path, 'w')
            f.close()

        self.db = TinyDB(self.db_file_path)
        self.query = Query()

    def __initAppDirectories(self):
        '''
        Check whether the app is running from the editor or from an executable file

        Returns:
        --------
        Null
        '''
        if getattr(sys, 'frozen', False):
            self.absolute_dirpath = os.path.dirname(sys.executable)
            # try:
            #    self.absolute_dirpath = sys._MEIPASS
            # except Exception:
            #    self.absolute_dirpath = os.path.abspath(".")
            self.db_path = os.path.join(self.absolute_dirpath, 'db')
            self.db_file_path = os.path.join(self.absolute_dirpath, 'db/db.json')
        elif __file__:
            self.absolute_dirpath = os.path.dirname(__file__)
            self.db_path = os.path.join(self.absolute_dirpath, '../db/')
            self.db_file_path = os.path.join(self.absolute_dirpath, '../db/db.json')

    def getAllCommands(self, table):
        pass

    def getLoginInfo(self, table):
        pass

    def getAllData(self, table):
        pass
