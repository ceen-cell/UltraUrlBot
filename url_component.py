import os
from pyshorteners import Shortener
import segno
import unshortenit


class UrlService:
    
    def __init__(self, error_message="Service Failed\nTry Again"):
        self.error_message = error_message

    
    def shorten_url(self, url: str):
        shortener = Shortener().tinyurl #Use tinyurl shortening service
        try:
            return shortener.short(url) #Return shortened url if able to else return error msg
        except Exception as e:
            return e

    
    def expand_url(self, url: str) -> str:
        """
        use the unshortenit module to get the actual url from the shortened one
        Default timeout is set to 60 seconds
        """
        expander = unshortenit.UnshortenIt(default_timeout=60)
        try:
            return expander.unshorten(url)
        except:
            return self.error_message



class QRCodeMaker:

    # this is the default filename that will be used for saving qrcodes
    #  and also deleting them
    file_name='qrcode.png' 


    def __init__(self, version=9):
        self.version = version #The version indicates the version of QRCode to use
    

    def create_qr(self, qr_content):
        qr = segno.make_qr(qr_content, version=self.version)
        qr.save(QRCodeMaker.file_name, scale=10)


    @staticmethod
    def delete_qr():
        os.remove(QRCodeMaker.file_name)        #Deletes the stored QRCode.
        
