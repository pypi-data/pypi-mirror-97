class URLs:
    def __init__(self):
        self.base_url = "https://api-v3.authenticating.com/"
        self.create_user = "user/create"
        self.submit_user_consent = "user/consent"
        self.get_user = "user/summary"
        self.update_user = "user/update"
        self.verify_phone = "user/verifyPhone"
        self.verify_phone_code = "user/verifyPhoneCode"
        self.verify_email = "user/verifyEmail"
        self.verify_email_code = "user/verifyEmailCode"
        self.compate_photos = "user/comparePhotos"
        self.ssn_verify = "user/verify/ssn"
        self.fein_verify = "identity/business/verification"
        self.business_search = "identity/business/verification/comprehensive"
        self.upload_id = "identity/document/scan"
        self.upload_id_enhanced = "identity/document/scan/enhanced"
        self.check_upload_id = "identity/document/scan/status"
        self.verify_upload_id = "identity/document/scan/data"
        self.motor_vehicle_record_verification = "identity/mvr"
        self.generate_criminal_background = "user/generateCriminalReport"
        self.seven_year_criminal_history = "identity/request/criminal/report/seven"

    def base_url(self):
        return self.base_url

    def create_user_url(self):
        return self.base_url + self.create_user

    def submit_user_consent_url(self):
        return self.base_url + self.submit_user_consent
    
    def get_user_url(self):
        return self.base_url + self.get_user

    def update_user_url(self):
        return self.base_url + self.update_user

    def mvr_v_url(self):
        return self.base_url + self.motor_vehicle_record_verification
    
    def generate_criminal_background_url(self):
        return self.base_url + self.generate_criminal_background

    def upload_id_url(self):
        return self.base_url + self.upload_id

    def upload_id_enhanced_url(self):
        return self.base_url + self.upload_id_enhanced
    
    def ssn_verify_url(self):
        return self.base_url + self.ssn_verify
        
    def seven_criminal_report_url(self):
        return self.base_url + self.seven_year_criminal_history