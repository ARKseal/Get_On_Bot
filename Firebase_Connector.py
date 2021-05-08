import firebase_admin as _firebase_admin
from firebase_admin import credentials as _credentials
from firebase_admin import db as _db
import json as _json


class Firebase_Connector(object):

    def __init__(self, cred_path, database_URL, filename):
        self._filename = filename
        self._cred = _credentials.Certificate(cred_path)
        self._default_app = _firebase_admin.initialize_app(self._cred, {'databaseURL':database_URL})
        self._ref = _db.reference("/get-on-bot/")

        self.getData()

    def getData(self):
        print('get')
        self._download()

    def sendData(self):
        print('send')
        self._upload()

    def _download(self):
        with open(self._filename, 'w') as f:
            _json.dump(self._ref.get(), f)

    def _upload(self):
        with open(self._filename, 'r') as f:
            self._ref.set(_json.load(f))