"""
ChainBreakerClient
"""
import requests
import getpass
import pandas as pd
#import matplotlib.pyplot as plt
#from PIL import Image

class ChainBreakerClient():

    def __init__(self, endpoint):
        self.__endpoint = endpoint
        self.__name = None
        self.__email = None
        self.__permission = None
        self.__token = None
        
   
    def get_status(self):
        """
        Get endpoint status.
        """
        try:
            res = requests.get(self.__endpoint + "/api/status").status_code
            if res == 200:
                return "Endpoint is online"
        except: 
            return "Endpoint is offline. Check our website for more information."

    def enter_password(self):
        """
        Enter new password function.
        """
        new_password = getpass.getpass("New password: ")
        repeat_password = getpass.getpass("Repeat new password: ")
        if new_password != repeat_password: 
            print("New passwords don't match")
            print("")
            return self.enter_password()
        return new_password

    
    def login(self):
        """
        This function lets the user to connect to ChainBreaker Service.
        """
        email = input("Email: ")
        password = getpass.getpass("Password: ")
        #expiration = input("Set session expiration in minutes (enter 0 for no expiration): ")
        expiration = 0
        data = {"email": email, "password": password, "expiration": expiration}
        res = requests.post(self.__endpoint + "/api/user/login", data)
        if res.status_code == 200:
            res = res.json()
            self.__token = res["token"]
            self.__name = res["name"]
            self.__email = res["email"]
            self.__permission = res["permission"]
            return "Hi {}! You are now connected to ChainBreaker API. Your current permission level is '{}'. If you have any questions don't hesitate to contact us!".format(self.__name, self.__permission)
        print(res.text)
    
    def logout(self):
        """
        This functions lets the users to logout from their account.
        """
        if self.__token != None:
            self.__token = None
            self.__email = None
            self.__name = None
            self.__permission = None
            print("Session closed.")
        else: 
            print("You are not logged.")

    def change_password(self):
        """
        This function lets the user to change her/his password.
        """
        if self.__token != None:
            old_password = getpass.getpass("Old password: ")
            new_password = self.enter_password()
            headers = {"x-access-token": self.__token}
            data = {"recover_password": "False", "old_password": old_password, "new_password": new_password}
            res = requests.put(self.__endpoint + "/api/user/change_password", data = data, headers = headers).json()["message"]
            return res
        return "You are not logged. If you want to use this function, you have to be logged into your account."
    
    def recover_password(self):
        """
        This function lets the user to recover her/his password, if the user forgot it.
        """
        if self.__token == None: 
            
            # Send email.
            email = input("Email: ")
            data = {"email": email}
            res = requests.post(self.__endpoint + "/api/user/recover_password", data = data).text
            
            # Change password.
            token = input("Enter Recovery token  (check your email): ")
            new_password = self.enter_password()
            headers = {"x-access-token": token}
            data = {"recover_password": "True", "new_password": new_password}
            res = requests.put(self.__endpoint + "/api/user/change_password", data = data, headers = headers).json()["message"]
            return res
        return "You are logged into your account. Use this function only if you forgot your password and you are not logged into your account."
            
    def create_user(self):
        """
        This functions allows administrators to create new users.
        """
        if self.__token != None and self.__permission == "admin":
            name = input("User name: ")
            email = input("User email: ")
            permission = input("User permission: ")
            
            headers = {"x-access-token": self.__token}
            data = {"name": name, "email": email, "permission": permission}
            res = requests.put(self.__endpoint + "/api/user/create_user", data = data, headers = headers).json()["message"]
            return res
        else: 
            print("You can't execute this function.")
            
    def get_account_info(self):
        """
        Print account information.
        """
        print("-- ChainBreaker Account Information --")
        print("")
        print("Name: ", self.__name)
        print("Email: ", self.__email)
        print("Permission: ", self.__permission)

    def get_token(self):
        """
        Return the token.
        """
        return self.__token
    
    def get_ads(self, language = "", website = "", filter_by_phones = False, filter_by_location = False): #, features = True, locations = False, comments = False, emails = False, names = False, phone = False, whatsapp = False):
        """
        This function returns ads data from ChainBreaker Database.
        - language can be: "spanish", "english" or "" (all).
        - website can be: 
          - "mileroticos", "skokka" or "" (all) (for "spanish")
          - "leolist" or "" (all) (for "english")
        - filter_by_phones: Boolean. Default value: False
          - If True, you will recieve only the ads that contain a phonenumber.
        - filter_by_location: Boolean. Default value: False
          - If True, you will recieve only the ads that contain a location
        """
        if self.__token != None:
            #data = {"features": str(features), "locations": str(locations), "comments": str(comments), "emails": str(emails), "names": str(names), "phone": str(phone), "whatsapp": str(whatsapp)}
            filter_by_phones = 0 if filter_by_phones == False else 1
            filter_by_location = 0 if filter_by_location == False else 1
            
            data = {"language": language, "website" : website, "filter_by_phones": filter_by_phones, "filter_by_location": filter_by_location}
            headers = {"x-access-token": self.__token}
            res = requests.post(self.__endpoint + "/api/data/get_ads", data = data, headers = headers).json()["ads"]
            df = pd.DataFrame(res)
            columns = ["id_ad", "data_version", "author", "language", "link", "id_page", "title", "text", "category", "post_date", "extract_date", "website", "whatsapp", "verified_ad", "prepayment", "promoted_ad", "external_website", "reviews_website"]
            df = df[columns]
            df.set_index("id_ad", inplace = True)
            return df
        else: 
            return "You are not logged!"

    def get_glossary(self, domain = ""):
        """
        This function returns the glossary of terms contained in ChainBreaker Database.
        - domain can be: "sexual", "general" or "" (all).
        This glossary were shared by Lena Garrett from Stop The Traffik.
        For more information please contact her: Lena.Garrett@stopthetraffik.org
        """
        if self.__token != None:
            data = {"domain": domain}
            headers = {"x-access-token": self.__token}
            res = requests.post(self.__endpoint + "/api/data/get_glossary", data = data, headers = headers).json()["glossary"]
            df = pd.DataFrame(res)
            columns = ["id_term", "domain", "term", "definition"]
            df = df[columns]
            df.set_index("id_term", inplace = True)
            return df
        else: 
            return "You are not logged!"

    def get_keywords(self, language = ""):
        """
        This function returns the set of keywords contained in ChainBreaker Database
        - language can be: "english", "spanish", "portuguese", "russian" or "" (all).
        These keywords were shared by Lena Garrett from Stop The Traffik.
        For more information please contact her: Lena.Garrett@stopthetraffik.org
        """
        if self.__token != None:
            data = {"language": language}
            headers = {"x-access-token": self.__token}
            res = requests.post(self.__endpoint + "/api/data/get_keywords", data = data, headers = headers).json()["keywords"]
            df = pd.DataFrame(res)
            columns = ["id_keyword", "language", "keyword", "english_translation", "meaning", "age_flag", "trafficking_flag", "movement_flag"]
            df = df[columns]
            df.set_index("id_keyword", inplace = True)
            return df