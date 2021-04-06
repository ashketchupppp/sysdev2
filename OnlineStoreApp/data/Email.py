import smtplib, ssl

class EmailTemplate:
    @classmethod
    def orderProcessedEmail(self, customerName, items, orderRef):
        itemString = ""
        longestItemName = int(max([len(item['name']) for item in items]))
        for item in items:
            paddedItemName = item['name'] + " "*(longestItemName - len(item['name'])) + " | "
            itemString += f'{paddedItemName}{item["price"]}\n'
            
        return f"""Hello, {customerName}

Your order is now being processed.

{itemString}

Your order reference is {orderRef}
Thank you for choosing us.
"""
    

class EmailHandler:
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