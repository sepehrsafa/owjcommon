import os
from twilio.rest import Client as TwilioClient
from sms_ir import SmsIr


class SMS:
    def __init__(
        self,
        twilio_account_sid,
        twilio_auth_token,
        twilio_number,
        payamak_panel_user_name,
        payamak_panel_password,
        payamak_panel_number,
    ):
        self.twilio_number = twilio_number
        self.payamak_panel_user_name = payamak_panel_user_name
        self.payamak_panel_password = payamak_panel_password
        self.payamak_panel_number = payamak_panel_number
        self.twilio_client = TwilioClient(twilio_account_sid, twilio_auth_token)

    def send_twilio_sms(self, text, to):
        message = client.messages.create(
            from_=self.twilio_number, body=text, to=phone_number
        )
        return True

    async def send_otp(self, phone_number, code):
        TEMPLATE = f"Your verification code is {code} \n{agency_name} \n{agency_domain}"
        # check for iran phone number
        try:
            if phone_number[0:3] == "+98":
                return True
            elif phone_number[0:2] == "+1":
                await twilio_send_sms(TEMPLATE, phone_number)
                return True
            else:
                return False
        except Exception as e:
            return False
