import streamlit as st
from streamlit_chat import message
import hashlib
import hmac
import base64
import time
import requests
import json

class ChatbotMessageSender:
    ep_path = 'https://n5n6w6fc1c.apigw.ntruss.com/team3_introduction/beta/'
    secret_key = 'VVVXZlRCY3VtdFBpTlNqenJVSHFRSVRCenl1SXFidEM='

    def req_message_send(self, user_input='안녕'):
        timestamp = self.get_timestamp()
        request_body = {
            'version': 'v2',
            'userId': 'instructor3',
            'timestamp': timestamp,
            'bubbles': [
                {
                    'type': 'text',
                    'data': {
                        'description': user_input
                    }
                }
            ],
            'event': 'send'
        }

        encode_request_body = json.dumps(request_body).encode('UTF-8')
        signature = self.make_signature(self.secret_key, encode_request_body)
        custom_headers = {
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-CHATBOT_SIGNATURE': signature
        }

        response = requests.post(headers=custom_headers, url=self.ep_path, data=encode_request_body)

        return response

    @staticmethod
    def get_timestamp():
        timestamp = int(time.time() * 1000)
        return timestamp

    @staticmethod
    def make_signature(secret_key, request_body):
        secret_key_bytes = bytes(secret_key, 'UTF-8')
        signing_key = base64.b64encode(hmac.new(secret_key_bytes, request_body, digestmod=hashlib.sha256).digest())
        return signing_key

