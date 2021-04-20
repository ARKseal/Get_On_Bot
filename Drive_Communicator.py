import signal as _signal
import threading as _threading
import time as _time

from pydrive.auth import GoogleAuth as _GoogleAuth
from pydrive.drive import GoogleDrive as _GoogleDrive


class Drive_Communicator(_threading.Thread):
    
    def __init__(self, fileId):
        super().__init__()
        self.fileId = fileId
        #self.folderId = folderId

        #_signal.signal(_signal.SIGINT, self.killer)
        #_signal.signal(_signal.SIGTERM, self.killer)

        self._setup()
        #self.getData()
        #_time.sleep(20)
        self.start()

    def killer(self, signum, stack_frame):
        self.sendData()

    def _setup(self):
        self.gauth = _GoogleAuth()

        self.gauth.LoadCredentialsFile("_credentials")
        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()

        self.gauth.SaveCredentialsFile("_credentials")
        self.drive = _GoogleDrive(self.gauth)
        self.data_file = self.drive.CreateFile({'id': self.fileId})

    def getData(self):
        print('getting file')
        self._download()

    def sendData(self):
        self._upload()

    def _download(self):
        download_file = self.drive.CreateFile({'id': self.fileId})
        download_file.GetContentFile('data.json')
        

    def _upload(self):
        update_file = self.drive.CreateFile({'id': self.fileId})
        update_file.SetContentFile('data.json')
        update_file.Upload()
        '''
        file_list = self.drive.ListFile({'q':"'{}' in parents and trashed=False".format(self.folderId)}).GetList()
        for file1 in file_list:
            if file1['title'] == 'data.json':
                file1.Delete()'''

    def run(self):
        try:
            while True:
                print('send')
                self.sendData()
                print('after send')
                _time.sleep(60)
        except:
            self.data_file = None