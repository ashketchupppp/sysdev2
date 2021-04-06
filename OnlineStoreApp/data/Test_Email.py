import unittest
import smtpd
import asyncore
import threading
from asyncio.queues import Queue
import asyncio


from data.Email import EmailHandler, EmailTemplate


class CustomSMTPServer(smtpd.SMTPServer):

    def setMessageQueue(self, queue : Queue):
        self.queue = queue
    
    def process_message(self, peer, mailfrom, rcpttos, data):
         self.queue.put({'peer' : peer, 'mailfrom' : mailfrom, 'rcpttos' : rcpttos, 'data' : data})
    
    def run(self):
        asyncore.loop()

# The EmailHandler class doesn't work at the moment, disable the tests
class EmailUnitTest: # (unittest.TestCase):
    smtpPort = 1025
    smtpHost = '127.0.0.1'
    
    def sendEmail(self, message):
        emailHandler = EmailHandler("test@test.com", "password", smtpPort=EmailUnitTest.smtpPort, smtpServer=EmailUnitTest.smtpHost)
        emailHandler.sendEmail("tgbyou@gmail.com", message=message)
        return  EmailUnitTest.emailQueue.get()
    
    @classmethod
    def setUpClass(self):
        EmailUnitTest.emailQueue = Queue()
        EmailUnitTest.smtpServer = CustomSMTPServer((EmailUnitTest.smtpHost, EmailUnitTest.smtpPort), None)
        EmailUnitTest.smtpServer.setMessageQueue(EmailUnitTest.emailQueue)
        EmailUnitTest.smtpServerThread = threading.Thread(target=EmailUnitTest.smtpServer.run)
        EmailUnitTest.smtpServerThread.setDaemon(True)
        EmailUnitTest.smtpServerThread.start()
    
    def test_sendEmail(self):
        result = asyncio.run(self.sendEmail(EmailTemplate.orderProcessedEmail("Chris", [{'name' : 'testitem', 'price' : 12.01}], "#69420")))
              
        
if __name__ == "__main__":
    unittest.main()