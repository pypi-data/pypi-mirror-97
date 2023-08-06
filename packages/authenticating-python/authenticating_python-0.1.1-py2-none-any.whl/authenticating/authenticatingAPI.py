import requests
import json
from xml.etree import ElementTree
from types import SimpleNamespace
from .URLs import URLs
from .utils import Header, requests_exception_handling

class AuthenticatingAPI:

    def __init__(self, api_key, res_format='json', timeout=100):
        self.api_key = api_key
        self.format = res_format
        self.timeout = timeout
        self.url = URLs()
        self.headers = self.__create_headers(self.api_key, self.format)

    def __create_headers(self, api_key, format):
        headers = Header(api_key, format)
        return headers.get_headers()

    def __to_format(self, response):
        if self.format == 'json':
            return response.json()
        else:
            return ElementTree.fromstring(response.content)

    def __get_data(self, url):
        return self.__to_format(requests.get(url, headers=self.headers, timeout=self.timeout))

    def __post_data(self, url, data):
        return self.__to_format(requests.post(url, headers=self.headers, timeout=self.timeout, data=data))

    def __update_data(self, url, data):
        return self.__to_format(requests.put(url, headers=self.headers, timeout=self.timeout, data=data))

    @requests_exception_handling
    def create_user(self, payload):
        if payload is not dict():
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.firstName:
                raise "missing first name."
            elif not vars.lastName: 
                raise "missing last name."
            elif not vars.dob:
                raise "missing date of birth"
            elif not vars.email:
                raise "missing emai address"
            else:
                return self.__post_data(self.url.create_user_url, payload)

    @requests_exception_handling
    def submit_user_consent(self, payload):
        if payload is not dict():
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing User Access Code."
            elif not vars.isBackgroundDisclosureAccepted:
                raise "required isBackgroundDisclosureAccepted field."
            elif not vars.GLBPurposeAndDPPAPurpose:
                raise "required GLBPurposeAndDPPAPurpose field."
            elif not vars.FCRAPurpose:
                raise "required FCRAPurpose field"
            elif not vars.fullName:
                raise "required full name"
            else:
                return self.__post_data(self.url.submit_user_consent_url, payload)

    @requests_exception_handling
    def get_user(self, payload):
        if payload is not dict():
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            else:
                return self.__post_data(self.url.get_user_url, payload)

    @requests_exception_handling
    def update_user(self, payload):
        if payload is not dict():
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            else:
                return self.__update_data(self.url.get_user_url, payload)

    @requests_exception_handling
    def get_motor_vehicle_record_verification(self, payload):
        if payload is not dict():
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            elif not vars.license_number:
                raise "missing license_number"
            elif not vars.state_abbr:
                raise "missing state_abbr"
            else:
                return self.__post_data(self.url.mvr_v_url, payload)

    @requests_exception_handling
    def create_criminal_background(self, payload):
        if payload is not dict():
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            else:
                return self.__post_data(self.url.generate_criminal_background_url, payload)

    @requests_exception_handling
    def upload_id(self, payload):
        if payload is not dict:
            return  "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            ##add base64 encoded verification
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            else:
                return self.__post_data(self.url.upload_id_url, payload)
    
    @requests_exception_handling
    def upload_id_enhanced(self, payload):
        if payload is not dict:
            return  "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            else:
                return self.__post_data(self.url.upload_id_enhanced_url, payload)

    @requests_exception_handling
    def ssn_verify(self, payload):
        if payload is not dict:
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            else:
                return self.__post_data(self.url.ssn_verify_url, payload)

    @requests_exception_handling
    def get_criminal_history(self, payload):
        if payload is not dict:
            return "params need to be in dict format, key must match API docs input format."
        else:
            vars = SimpleNamespace(**payload)
            if not vars.userAccessCode:
                raise "missing userAccessCode"
            else:
                return self.__post_data(self.url.seven_criminal_report_url, payload)
            



    
