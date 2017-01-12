from twilio.rest import TwilioRestClient

account_sid='AC15657cdfb72f4e648a06da9e8edd7ff2'
auto_token='3ad103223eaa0d9f3a6a70db444ce62d'
client=TwilioRestClient(account_sid,auto_token)

message=client.sms.messages.create(
        body='My name is zhao tingting',
        to='+8613161827451',
        from_='+16366420027',
        )
