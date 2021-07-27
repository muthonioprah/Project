# works with both python 2 and 3
from __future__ import print_function


import africastalking, os


# USERNAME = os.environ.get("AT_USERNAME")
# API_KEY = os.environ.get("AT_API_KEY")

USERNAME = "CocoL"
API_KEY = "asdasda"

class SMS:

    def __init__(self):

        self.username = USERNAME
        self.api_key = API_KEY

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, recipients:list, message:str):
            # Set the numbers you want to send to in international format
            recipients = recipients

            # Set your message
            message = message;

            # Set your shortCode or senderId
            # sender = "shortCode or senderId"
            try:
				# Thats it, hit send and we'll take care of the rest.
                response = self.sms.send(message, recipients)
                print (response)
            except Exception as e:
                print ('Encountered an error while sending: %s' % str(e))

# if __name__ == '__main__':
#     SMS().send()

sms = SMS()