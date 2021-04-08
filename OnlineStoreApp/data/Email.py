import smtplib, ssl

class EmailTemplate:
    """ Helper class for generating email template strings using classmethods.
    """
    @classmethod
    def orderProcessedEmail(self, customerName, items, orderRef):
        itemString = ""
        longestItemName = int(max([len(item['name']) for item in items]))
        for item in items:
            paddedItemName = item['name'] + " "*(longestItemName - len(item['name']))
            itemString += f'{paddedItemName}'
            
        return f"""Hello, {customerName}

Your order has now been processed and will be shipped.

{itemString}

Your order reference is {orderRef}
Thank you for choosing us.
"""
    

class EmailHandler:
    """ !!! This class is a work in progress and not used anywhere !!!
        A class to handle sending emails to customers using an smtp server.
    """
    
    def __init__(self, orderUpdateEmail, 
                 orderUpdatePassword, 
                 smtpServer = "smtp.gmail.com", 
                 smtpPort = 587):
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.orderUpdateEmail = orderUpdateEmail
        self.orderUpdatePassword = orderUpdatePassword

    
    def sendEmail(self, toAddress, message):
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(self.smtpServer, self.smtpPort)
            server.connect()
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(self.orderUpdateEmail, self.orderUpdatePassword)
            server.sendmail(from_addr=self.orderUpdateEmail, 
                            to_addrs=[toAddress],
                            msg=message)
        except Exception as e:
            print(e)
        finally:
            server.quit() 
            return True