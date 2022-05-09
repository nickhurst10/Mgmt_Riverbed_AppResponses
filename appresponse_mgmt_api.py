#from re import L
#from xmlrpc.client import boolean
from curses import initscr
from logging.handlers import MemoryHandler
import requests
import json
import re



class Appresponse_Mgmt:
    api_url = "/api/common/1.0/info"

    def is_host_address_valid(self,received_data,received_min_string_length,received_max_string_length):
        if received_data == None:
            return False
        elif received_data == "":
            return False
        elif " " in received_data:
            return False
        elif " .." in received_data:
            return False
        elif len(received_data) > received_max_string_length:
            print(f"string too long, should be min {received_max_string_length} chars, current length is {len(received_data)}")
            return False
        elif len(received_data) < received_min_string_length:
            print(f"string too short, should be min {received_min_string_length} chars, current length is {len(received_data)}")
            return False
        else:
            for char in received_data:
                if not re.search(r"[a-zA-Z0-9_.]",char):
                    print (f"this char '{char}' is not allowed in host address")
                    return False
            if received_data.endswith('.'):
                print(f"'{received_data}' host address can't end with a dot")
                return False
            return True

    def is_it_a_decimal_if_required_convert_decimal_string_to_integer(self,received_data_to_check,received_data_key_name):
        if not isinstance(received_data_to_check,int):
            if not received_data_to_check.isdecimal():
                print(f"ERROR -- For data key '{received_data_key_name}', expected data type is decimal interger")
                return False,received_data_to_check
            else:
                return True,int(received_data_to_check)

        else:
            return(True,received_data_to_check)

    def check_ip_addr(self,received_ip_addr):
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if(re.search(regex, received_ip_addr)):
            #print(f"'{received_ip_addr}' Valid Ip address")
            return True
        else:
            print(f"'{received_ip_addr}' Invalid Ip address")
            return False
        
    def is_it_a_boolean(self,received_boolean_to_test,received_data_key_name):
        if not isinstance(received_boolean_to_test,bool):
            print(f"error -- '{received_data_key_name}' expected input it a boolean, recieved date type is '{type(received_boolean_to_test)}'")
            return False
        else:
            return True

    def print_old_and_new_config(self):
        print("####################################################################################")
        print("\t##########################################")
        print(f"\tOriginal Coniguration for {self.ar_ip_addr}  ")
        print("\t##########################################\n")
        print(json.dumps(self.old_config, sort_keys=False, indent=4))
        print("\n\t##########################################")
        print(f"\t## New Coniguration for {self.ar_ip_addr}  #")
        print("\t##########################################\n")
        print(json.dumps(self.new_config, sort_keys=False, indent=4))
        print("####################################################################################\n")
        print("####################################################################################\n")

    def __init__(self,received_ar_ip_addr,received_ar_bearer_token):
        self.ar_ip_addr=received_ar_ip_addr
        self.ar_bearer_token=received_ar_bearer_token

    def api_call(self,received_api_method,received_api_url,received_payload):
        url = f"https://{self.ar_ip_addr}{received_api_url}"
        print(received_payload)
        payload = received_payload
        headers = {
            'Authorization': f'Bearer {self.ar_bearer_token}',
            'Content-Type': 'application/json'
            }
        response = requests.request(received_api_method, url, headers=headers, data=payload,verify=False)
        return response

    def get_data_with_api_call(self): 
        repsonse = (self.api_call("GET",self.api_url,""))
        self.orginal_config = repsonse.json()
        print(json.dumps(self.orginal_config, sort_keys=False, indent=4))
        return self.orginal_config

    def put_new_config_with_api_call(self):
        url = f"https://{self.ar_ip_addr}{self.api_url}"
        payload = json.dumps(self.new_config)
        headers = {
            'Authorization': f'Bearer {self.ar_bearer_token}',
            'Content-Type': 'application/json'
            }

        response = requests.request("PUT", url, headers=headers, data=payload,verify=False)
        print (response)
 
    def post_new_config_with_api_call(self):
        url = f"https://{self.ar_ip_addr}{self.api_url}"
        
        payload = json.dumps(self.new_config)
        print (url)
        print (payload)
        
        headers = {
            'Authorization': f'Bearer {self.ar_bearer_token}',
            'Content-Type': 'application/json'
            }

        response = requests.request("POST", url, headers=headers, data=payload,verify=False)
        print (response)

    def push_data_with_api_call(self):
        repsonse = (self.api_call("PUT",self.api_url,""))
        print(json.dumps(repsonse, sort_keys=False, indent=4))
        return repsonse

    def post_new_config(self,received_new_config,received_old_config):
        self.new_config=received_new_config
        self.old_config=received_old_config
  
        #print(self.api_call("POST",self.api_url,(json.dumps(self.new_config))))

    def update_previous_data_in_items_list(self):
        for item in self.new_config['items']:
            if item.get('id'):
                url = f"https://{self.ar_ip_addr}{self.api_url}items/{item['id']}"
                payload = json.dumps(item)
                headers = {
                    'Authorization': f'Bearer {self.ar_bearer_token}',
                    'Content-Type': 'application/json'
                    }

                response = requests.request("PUT", url, headers=headers, data=payload,verify=False)
                print (response)

    #def add_new_data_in_items_list(self,received_request_type):
#
    #    for item in self.new_config['items']:
    #        print("Going throufh items")
    #        if not item.get('id'):
    #            print("adding new item which has no id")
    #            print(f"config for it is {item}")
    #            url = f"https://{self.ar_ip_addr}{self.api_url}"
    #            payload = json.dumps(item)
    #            headers = {
    #                'Authorization': f'Bearer {self.ar_bearer_token}',
    #                'Content-Type': 'application/json'
    #                }
    #            response = requests.request(received_request_type, url, headers=headers, data=payload,verify=False)
    #            print (response)

    def add_new_data_in_items_list(self):

        for item in self.new_config['items']:
            print("Going throufh items")
            if not item.get('id'):
                print("adding new item which has no id")
                print(f"config for it is {item}")
                url = f"https://{self.ar_ip_addr}{self.api_url}"
                payload = json.dumps(item)
                headers = {
                    'Authorization': f'Bearer {self.ar_bearer_token}',
                    'Content-Type': 'application/json'
                    }
                response = requests.request("POST", url, headers=headers, data=payload,verify=False)
                print (response)

    def delete_data_in_items_list(self):
        #create list of grouphost id from old list
        old_config_id_list =[]
        for item in self.old_config['items']:
            old_config_id_list.append(item['id'])
        
        #loop though new config and remove grouphost id's that are still in the new config
        for item in self.new_config['items']:
            if item.get('id') in old_config_id_list:
                old_config_id_list.remove(item.get('id'))

        print(f"old host group {old_config_id_list}")
        #delete what left of old hostgroup list
        if len(old_config_id_list)>0:
            for id in old_config_id_list:
                print(f"delete host id {id}")
                url = f"https://{self.ar_ip_addr}{self.api_url}items/{id}"
                payload = ""
                headers = {
                    'Authorization': f'Bearer {self.ar_bearer_token}',
                    'Content-Type': 'application/json'
                    }
                response = requests.request("DELETE", url, headers=headers, data=payload,verify=False)
                print (response)

    def is_data_valid_cant_have_spaces(self,received_data,received_min_string_length,received_max_string_length,received_data_key_name):
        if received_min_string_length == 0:
            if received_data == None:
                print(f"{received_data_key_name} can't be empty")
                return False
            elif received_data == "":
                print(f"{received_data_key_name} can't be empty")
                return False

        if " " in received_data:
            print(f"{received_data_key_name} - can't have spaces - '{received_data}'")
            return False
        elif len(received_data) > received_max_string_length:
            print(f"{received_data_key_name} - string too long, should be min {received_max_string_length} chars, current length is {len(received_data)}")
            return False
        elif len(received_data) < received_min_string_length:
            print(f"{received_data_key_name} - string too short, should be min {received_min_string_length} chars, current length is {len(received_data)}")
            return False
        else:
            return True

    def is_data_valid_and_can_have_spaces(self,received_data,received_min_string_length,received_max_string_length,received_data_key_name):

        if received_min_string_length == 0:
            if received_data == None:
                print(f"{received_data_key_name} can't be empty")
                return False
            elif received_data == "":
                print(f"{received_data_key_name} can't be empty")
                return False

        if len(received_data) > received_max_string_length:
            print(f"{received_data_key_name} string too long, should be max {received_max_string_length} chars, current length is {len(received_data)}")
            return False
        elif len(received_data) < received_min_string_length:
            print(f"{received_data_key_name} string too short, should be min {received_min_string_length} chars, current length is {len(received_data)}")
            return False
        else:
            return True

    def affirm_new_config(self,received_new_config,received_old_config,received_ar_ip_addr):
        self.new_config=received_new_config
        self.old_config=received_old_config
        if self.is_new_config_logic_correct():
            return True
        else:
            print ("########################################################################")
            print(f"There is an error with the new config for {received_ar_ip_addr}")
            print(json.dumps(self.new_config, sort_keys=False, indent=4))
            print ("########################################################################")
            print ("########################################################################")
            return False

class Ar_Capture_Jobs(Appresponse_Mgmt):
    api_url = "/api/npm.packet_capture/3.0/jobs"
    
class Ar_Snmp(Appresponse_Mgmt):
    api_url = '/api/npm.snmp/1.0/snmp/config'

    COMMUNITY_STRING_MIN_LENGTH = 1
    COMMUNITY_STRING_MAX_LENGTH = 32
    USERNAME_STRING_MIN_LENGTH = 1
    USERNAME_STRING_MAX_LENGTH = 32
    AUTH_PASSPHRASE_STRING_MIN_LENGTH = 8
    AUTH_PASSPHRASE_STRING_MAX_LENGTH = 100
    PRIVACYPASSPHRASE_STRING_MIN_LENGTH = 8
    PRIVACYPASSPHRASE_STRING_MAX_LENGTH = 100
    LOCATION_STRING_MIN_LENGTH = 1
    LOCATION_STRING_MAX_LENGTH = 255
    DESCRIPTION_STRING_MIN_LENGTH = 1
    DESCRIPTION_STRING_MAX_LENGTH = 255
    CONTACT_STRING_MIN_LENGTH = 1
    CONTACT_STRING_MAX_LENGTH = 255

    def deploy_new_config(self):
        self.put_new_config_with_api_call()

    def check_authentication_data_is_correct(self,bool_auth_passphrase_can_be_blank):
        if self.new_config['version_configuration']['auth_protocol'] not in ("MD5", "SHA"):
            print(f"wrong auth protocol - should be MD5 or SHA - entered was '{self.new_config['version_configuration']['auth_protocol']}' please check")
            return False
        elif bool_auth_passphrase_can_be_blank == True and self.new_config['version_configuration']['authentication_passphrase'] == None:
            del self.new_config['version_configuration']['authentication_passphrase']
            return True
        elif not self.is_data_valid_and_can_have_spaces(self.new_config['version_configuration']['authentication_passphrase'],self.AUTH_PASSPHRASE_STRING_MIN_LENGTH,self.AUTH_PASSPHRASE_STRING_MAX_LENGTH,"authentication_passphrase"):
            print("authentication_passphrase is incorrect")
            return False
        else:
            return True
    
    def check_privacy_data_is_correct(self,bool_priv_passphrase_can_be_blank):
        if self.new_config['version_configuration']['privacy_protocol'] not in ("DES","AES"):
            print(f"wrong privacy_protocol - should be DES or AES - entered was '{self.new_config['version_configuration']['privacy_protocol']}' please check")
            return False
        elif bool_priv_passphrase_can_be_blank == True and self.new_config['version_configuration']['privacy_passphrase'] == None:
            del self.new_config['version_configuration']['privacy_passphrase']
            return True
        elif not self.is_data_valid_and_can_have_spaces(self.new_config['version_configuration']['privacy_passphrase'],self.PRIVACYPASSPHRASE_STRING_MIN_LENGTH,self.PRIVACYPASSPHRASE_STRING_MAX_LENGTH,"privacy_passphrase"):
                print("privacy_passphrase is incorrect")
                return False
        else:
            return True

    def is_no_auth_no_priv_input_correct(self):
        #we know username has already been checked, so for this function we're going to insure all the none user data entries are empty
        if not self.new_config['version_configuration']["auth_protocol"]==None:
            print("auth_protocol should be empty")
            return False
        elif not self.new_config['version_configuration']["authentication_passphrase"]==None:
            print("authentication_passphrase should be empty")
            return False
        elif not self.new_config['version_configuration']["privacy_protocol"]==None:
            print("privacy_protocol should be empty")
            return False
        elif not self.new_config['version_configuration']["privacy_passphrase"]==None:
            print("privacy_passphrase should be empty")
            return False   
        elif not self.new_config['version_configuration']["community_string"]==None:
            print("community should be empty")
            return False
        else:
            return True

    def is_auth_no_priv_input_correct(self):
        if not self.check_authentication_data_is_correct(False):
            return False
        elif not self.new_config['version_configuration']["privacy_protocol"]==None:
            print("privacy_protocol should be empty")
            return False
        elif not self.new_config['version_configuration']["privacy_passphrase"]==None:
            print("privacy_passphrase should be empty")
            return False   
        elif not self.new_config['version_configuration']["community_string"]==None:
            print("community should be empty")
            return False
        else:
            return True

    def is_auth_priv_input_correct(self):
        if not self.check_authentication_data_is_correct(False):
            return False
        elif not self.check_privacy_data_is_correct(False):
            return False
        elif not self.new_config['version_configuration']["community_string"]==None:
            print("community should be empty")
            return False
        else:
            return True
        
    def is_all_snmp_v3_config_bank(self):
        if not self.new_config['version_configuration']["username"] == None:
            print("username has data in it")
            return False
        elif not self.new_config['version_configuration']["security_model"] == None:
            print("security_model has data in it")
            return False
        elif not self.new_config['version_configuration']["auth_protocol"] == None:
            print("auth_protocol has data in it")
            return False
        elif not self.new_config['version_configuration']["authentication_passphrase"] == None:
            print("authentication_passphrase has data in it")
            return False
        elif not self.new_config['version_configuration']["privacy_protocol"] == None:
            print("privacy_protocol has data in it")
            return False
        elif not self.new_config['version_configuration']["privacy_passphrase"] == None:
            print("privacy_passphrase has data in it")
            return False    
        else:
            return True    

    def check_v3_config_is_correct_when_moving_from_v2(self):
        
        if self.new_config['version_configuration']['security_model'] not in ["AuthPriv","AuthNoPriv","NoAuthNoPriv"]:
            return False
        elif not self.is_data_valid_cant_have_spaces(self.new_config['version_configuration']['username'],self.USERNAME_STRING_MIN_LENGTH,self.USERNAME_STRING_MAX_LENGTH,"username"): 
            print("username is not good")
            return False
        else:
            if self.new_config['version_configuration']['security_model'] =="NoAuthNoPriv":
                if not self.is_no_auth_no_priv_input_correct():
                    return False
                else:
                    return True
            elif self.new_config['version_configuration']['security_model'] =="AuthNoPriv":
                if not self.is_auth_no_priv_input_correct():
                    return False
                else:
                    return True
            elif self.new_config['version_configuration']['security_model'] =="AuthPriv":
                if not self.is_auth_priv_input_correct():
                    return False
                else:
                    return True

    def check_v2c_config_is_correct(self):
        if not self.is_all_snmp_v3_config_bank():
            print("there should no V3 data")
            return False
        elif not self.is_data_valid_and_can_have_spaces(self.new_config['version_configuration']['community_string'],self.COMMUNITY_STRING_MIN_LENGTH,self.COMMUNITY_STRING_MAX_LENGTH):
            print("bad community string")
            return False
        else:
            return True

    def remove_snmp_v3_data_from_config_dictioary(self):
        del self.new_config['version_configuration']['username']
        del self.new_config['version_configuration']['security_model']
        del self.new_config['version_configuration']['auth_protocol']
        del self.new_config['version_configuration']['authentication_passphrase']
        del self.new_config['version_configuration']['privacy_protocol']
        del self.new_config['version_configuration']['privacy_passphrase']

    def is_stadard_input_location_description_contact_enabled_correct(self):
        print (type(self.new_config["enabled"]))
        if not self.is_data_valid_and_can_have_spaces(self.new_config["contact"],self.CONTACT_STRING_MIN_LENGTH,self.CONTACT_STRING_MAX_LENGTH,"contact"):
            print("error in contact information")
            return False
        elif not self.is_data_valid_and_can_have_spaces(self.new_config["location"],self.LOCATION_STRING_MIN_LENGTH,self.LOCATION_STRING_MAX_LENGTH,"location"):
            print("error in location information")
            return False
        elif not self.is_data_valid_and_can_have_spaces(self.new_config["description"],self.DESCRIPTION_STRING_MIN_LENGTH,self.DESCRIPTION_STRING_MAX_LENGTH,"description"):
            print("error in description information")
            return False
        elif not isinstance(self.new_config["enabled"], bool):
            print("error in enabled inforamtion - not a boolean")
            return False
        return True
    
    def check_v3_to_v3_config_is_correct(self):
        
        #check that security mode and username are to correct standard
        if self.new_config['version_configuration']['security_model'] not in ["AuthPriv","AuthNoPriv","NoAuthNoPriv"]:
            return False
        elif not self.is_data_valid_cant_have_spaces(self.new_config['version_configuration']['username'],self.USERNAME_STRING_MIN_LENGTH,self.USERNAME_STRING_MAX_LENGTH,"username"): 
            print("username is not good")
            return False
        
        else:
            #based on what the old configuration was we need to check certain config parmiters 
            if self.old_config['version_configuration']['security_model']== 'NoAuthNoPriv':
                #if same security mode NoAuthNoPriv, then we don't need the other config option, so thare removed from the config ductionary
                if self.new_config['version_configuration']['security_model']== 'NoAuthNoPriv':
                    del self.new_config['version_configuration']['auth_protocol']
                    del self.new_config['version_configuration']['authentication_passphrase']
                    del self.new_config['version_configuration']['privacy_protocol']
                    del self.new_config['version_configuration']['privacy_passphrase']
                    return True

                elif self.new_config['version_configuration']['security_model']== 'AuthNoPriv':
                    del self.new_config['version_configuration']['privacy_protocol']
                    del self.new_config['version_configuration']['privacy_passphrase']
                    if not self.check_authentication_data_is_correct(False):
                        return False
                    else:
                        return True
                elif self.new_config['version_configuration']['security_model']== 'AuthPriv':
                    if not self.check_authentication_data_is_correct(False):
                        return False
                    elif not self.check_privacy_data_is_correct(False):
                        return False
                    else:
                        return True

            elif self.old_config['version_configuration']['security_model']== 'AuthNoPriv':
                if self.new_config['version_configuration']['security_model']== 'NoAuthNoPriv':
                    del self.new_config['version_configuration']['auth_protocol']
                    del self.new_config['version_configuration']['authentication_passphrase']
                    del self.new_config['version_configuration']['privacy_protocol']
                    del self.new_config['version_configuration']['privacy_passphrase']
                    return True

                elif self.new_config['version_configuration']['security_model']== 'AuthNoPriv':
                    del self.new_config['version_configuration']['privacy_protocol']
                    del self.new_config['version_configuration']['privacy_passphrase']
                    if not self.check_authentication_data_is_correct(True):
                        return False
                    else:
                        return True

                elif self.new_config['version_configuration']['security_model']== 'AuthPriv':
                    if not self.check_authentication_data_is_correct(True):
                        return False
                    elif not self.check_privacy_data_is_correct(False):
                        return False
                    else:
                        return True
                
            elif self.old_config['version_configuration']['security_model']== 'AuthPriv':
                if self.new_config['version_configuration']['security_model']== 'NoAuthNoPriv':
                    del self.new_config['version_configuration']['auth_protocol']
                    del self.new_config['version_configuration']['authentication_passphrase']
                    del self.new_config['version_configuration']['privacy_protocol']
                    del self.new_config['version_configuration']['privacy_passphrase']
                    return True

                elif self.new_config['version_configuration']['security_model']== 'AuthNoPriv':
                    del self.new_config['version_configuration']['privacy_protocol']
                    del self.new_config['version_configuration']['privacy_passphrase']
                    if not self.check_authentication_data_is_correct(True):
                        return False
                    else:
                        return True

                elif self.new_config['version_configuration']['security_model']== 'AuthPriv': 
                    if not self.check_authentication_data_is_correct(True):
                        return False
                    elif not self.check_privacy_data_is_correct(True):
                        return False
                    else:
                        return True


    def is_new_config_logic_correct(self):
        print("checking SNMP config")
        if self.is_stadard_input_location_description_contact_enabled_correct():
            #we use the old config version to check certain parts to understand what option are required and not required.
            #if the version number has changed from V2 to V3, then there are certain part we need to check.
            if self.old_config['version_configuration']['version'] in ('V2C','V1') and self.new_config['version_configuration']['version'] == 'V3':
                #when moving to V3 we must have a username and/or privacy_passphares and/or authentication 
                print('\t\tchange in version from V2c to V3\n\n')
                if not self.check_v3_config_is_correct_when_moving_from_v2():
                    print("V3 setting aren't correct")
                    return False
                else:
                    del self.new_config['version_configuration']['community_string']
                    return True
            #if the version number has changed from V3 to V2C, then there are certain part we need to check.   
            elif self.old_config['version_configuration']['version'] == 'V3' and self.new_config['version_configuration']['version'] in ('V2C','V1'):
                print('\t\tchange in version from V3 to V2C\n\n')
                if not self.check_v2c_config_is_correct():
                    return False
                else:
                    self.remove_snmp_v3_data_from_config_dictioary()
                    return True
            #if the version has stayed the same (V1 or V2C) or changed from V1 to V2C
            elif self.old_config['version_configuration']['version'] in ('V2C','V1') and self.new_config['version_configuration']['version'] in ('V2C','V1'):
                print("V2 config update")
                if not self.check_v2c_config_is_correct():
                    print("snmpv2 data incorrect")
                    return False
                else:
                    self.remove_snmp_v3_data_from_config_dictioary()
                    return True
            #if the version has stayed the same V3
            elif self.old_config['version_configuration']['version'] in ('V3') and self.new_config['version_configuration']['version'] in ('V3'):
                print("V3 conig update")
                #no community string is required in SNMP V3 config
                del self.new_config['version_configuration']['community_string']
                
                if not self.check_v3_to_v3_config_is_correct():
                    print("SNMP V3 configuration error")
                    return False
                else:        
                    print(json.dumps(self.old_config, sort_keys=False, indent=4))   
                    print(json.dumps(self.new_config, sort_keys=False, indent=4))            
                    return True

class Ar_Ntp(Appresponse_Mgmt):

    NTP_KEY_STRING_MIN_LENGTH = 1
    NTP_KEY_STRING_MAX_LENGTH = 255
    NTP_ADDR_STRING_MIN_LENGTH = 1
    NTP_ADDR_STRING_MAX_LENGTH = 33
    NTP_ENCRYPTION_OPTIONS_LIST = ["MD5","SHA1","none"]
    MAX_NTP_SERVERS = 16
    MAX_NUMBER_OF_KEY_IDS = 65534

    api_url = '/api/mgmt.time/1.0/ntp/servers'
    ntp_items_url = '/api/mgmt.time/1.0/ntp/servers/items'
    
    def delete_old_config_with_api_call(self,received_server_id):
        url = f"https://{self.ar_ip_addr}{self.ntp_items_url}/{str(received_server_id)}"
        payload = ""
        headers = {
            'Authorization': f'Bearer {self.ar_bearer_token}',
            'Content-Type': 'application/json'
            }

        response = requests.request("DELETE", url, headers=headers, data=payload,verify=False)
        print (response)

    def delete_current_config(self):
        #get ntp server id
        server_id_list = []
        if len(self.old_config['items']) > 0:
            for item in self.old_config['items']:
                print (f"\t\t\t\t\tloop through server ID's = {item['server_id']}")
                server_id_list.append(item['server_id'])

            print (server_id_list)
            #run DELETE API request for each server id
            for server_id in server_id_list:
                print (server_id)
                self.delete_old_config_with_api_call(server_id)

    def post_new_config_with_api_call(self,ntp_server_config):
        url = f"https://{self.ar_ip_addr}{self.api_url}"
        payload = json.dumps(ntp_server_config)
        headers = {
            'Authorization': f'Bearer {self.ar_bearer_token}',
            'Content-Type': 'application/json'
            }
        response = requests.request("POST", url, headers=headers, data=payload,verify=False)
        print (response)

    def deploy_new_config(self):
        self.delete_current_config()
        for item in self.new_config['items']:
            self.post_new_config_with_api_call(item)

    def correct_data_type_for_ntp_configuration(self):
        for item in self.new_config['items']:

            if not isinstance(item['prefer'],bool):
                print (f"'{item['prefer']}' is wrong data type, data type should be a boolean")
                return False

            if not isinstance(item['server_id'],int):
                print(f"A server id is the wrong data type:- {item['server_id']}")
                return False
            elif item['server_id'] > self.MAX_NTP_SERVERS:
                print(f"A server id has to be less than or equal to {self.MAX_NTP_SERVERS}")
                return False

            if not isinstance(item['address'],str):
                print(f"A NTP address is wrong data type:-l {item['address']}")
                return False
            elif not self.is_host_address_valid(item['address'],self.NTP_ADDR_STRING_MIN_LENGTH,self.NTP_ADDR_STRING_MAX_LENGTH):
                print (f"Error in NTP address '{item['address']}'")
                return False

            if not isinstance(item['version'],int):
                print(f"version should be a number:- {item['version']}")
                return False
            elif not item['version'] in [1,2,3,4]:
                print (f"not a compatiable version number :- {item['version']}")
                return False

            if not isinstance(item['encryption'],str):
                print (f"'{item['encryption']}'not a compatiable encryption option options are {self.NTP_ENCRYPTION_OPTIONS_LIST} :- ")
                return False
            elif not item['encryption'] in self.NTP_ENCRYPTION_OPTIONS_LIST:
                print (f"'{item['encryption']}'not a compatiable encryption option options are {self.NTP_ENCRYPTION_OPTIONS_LIST} :- ")
                return False
            elif item['encryption'] != "none":

                if not isinstance(item['key_id'],int):
                    print (f"'{item['key_id']}' key id with wrong data type, it should be an interger")
                    return False
                elif item['key_id'] > self.MAX_NUMBER_OF_KEY_IDS:
                    print (f"'{item['key_id']}' key id is to large, should be less that{self.MAX_NUMBER_OF_KEY_IDS}") 
                    return False
                elif item['key_id'] < 1:
                    print (f"'{item['key_id']}' key id is to large, should be less that 0") 
                    return False

                if not isinstance(item['secret'],str):
                    print (f"'{item['secret']}' isn't a key secret, its the wrong data type, it should be an string")
                    return False
                elif not self.is_data_valid_and_can_have_spaces(item['secret'],self.NTP_KEY_STRING_MIN_LENGTH,self.NTP_KEY_STRING_MAX_LENGTH,"secret"):
                    return False
                
            elif item['encryption'] == "none":
                del item['key_id']
                del item['secret']

        return True
            
    def is_new_config_logic_correct(self):
        print ("checking NTP config")
        return self.correct_data_type_for_ntp_configuration()
        
    def is_new_config_correct(self):
        print("##############")
        print("testing config")
        print("##############")
        for ntp_config in self.new_config:
            print (ntp_config)

            if (type(ntp_config['server_id']) != int or 
                type(ntp_config['address']) != str or 
                type(ntp_config['prefer']) != bool or 
                type(ntp_config['encryption']) != str or 
                type(ntp_config['version']) != int
                ):
                print("\tBad base config")
                return False
            #check if there is a encryption
            if ntp_config['encryption'] != 'none':
                if (ntp_config['encryption'] == 'md5' or
                    ntp_config['encryption'] == 'sha1'):
                    print("\t\t\t\twe have encrytion")
                    if (type(ntp_config['key_id'])!= int or
                        type(ntp_config['secret'])!= str):
                        
                        print("\t\t\t\tencrytion is bad")
                        print("False 3")
                        return False
                else:
                    print("False 2")
                    return False

        return True

class Ar_Dns(Appresponse_Mgmt):

    HOSTNAME_STRING_MIN_LENGTH = 1
    HOSTNAME_STRING_MAX_LENGTH = 70
    DNS_DOMAIN_STRING_MIN_LENGTH = 1
    DNS_DOMAIN_STRING_MAX_LENGTH = 60

    api_url = '/api/mgmt.networking/1.1/settings/host'

    def deploy_new_config(self):
        pass

    def correct_data_type_for_dns_configuration(self):

        if not isinstance(self.new_config['hostname'],str):
            return False
        elif not self.is_host_address_valid(self.new_config['hostname'],self.HOSTNAME_STRING_MIN_LENGTH,self.HOSTNAME_STRING_MAX_LENGTH):
            return False
        
        for dns_server_ip in self.new_config['dns_servers']:
            if not isinstance(dns_server_ip,str):
                print(f"'{dns_server_ip}' ip address var type should be string")
                return False
            if not self.check_ip_addr(dns_server_ip):
                return False
        
        if len(self.new_config['dns_domains']) > 0:
            for dns_domain in self.new_config['dns_domains']:
                if not self.is_host_address_valid(dns_domain,self.DNS_DOMAIN_STRING_MIN_LENGTH,self.DNS_DOMAIN_STRING_MAX_LENGTH):
                    print("bad dns domain")
                    return False

        

        return True

        

    def is_new_config_logic_correct(self):
        print ("checking NTP config")
        return self.correct_data_type_for_dns_configuration()

class Ar_Phy_Int(Appresponse_Mgmt):
    api_url = "/api/npm.packet_capture/3.0/interfaces"

class Ar_Applications(Appresponse_Mgmt):
    api_url = "/api/npm.classification/3.2/applications/"
    
    APP_NAME_STRING_MIN_LENGTH = 1
    APP_NAME_STRING_MAX_LENGTH = 70
    TRAFFIC_MATCH_MODE_LIST = ['HIGH','MEDIUM','LOW']
    DESCRIPTION_STRING_MIN_LENGTH = 0
    DESCRIPTION_STRING_MAX_LENGTH = 300
    MIN_TCP_AND_UDP_PORT_NUMBER = 0
    MAX_TCP_AND_UDP_PORT_NUMBER = 65535
    PORT_IP_PROTOCOL_LIST = ["TCP","UDP"]
    FULL_IP_PROTOCOLS_LIST = ["TCP","UDP","FC","RSVP-EZE-IGNORE","Mobility Header","UDPLite","MPLS-in-IP","manet","HIP","Shim6","WESP","PTP","ISIS","FIRE","CRTP","CRUDP","SSCOPMCE","IPLT","SPS","PIPE","SCTP","AOHP","L2TP","DDX","IATP","STP","SRP","UTI","SMP","SM","SCPS","ONX","A/N","IPComp","I SNP","/ Compaq-Peer","IPX-in-IP","VRRP","PGM","SCC-SP","ETHERIP","ENCAP","APES","GMTP","IFMP","PNNI","PIM","ARIS","TCE","EIGRP","OSPFIGP","Sprite-RPC","LARP","MTP","AX.25","IPIP","MICP","WB-MON","WB-EXPAK","ISO-IP","VMTP","SECURE-VMTP","VINES","TTP","INSENET-IGP","DGP","ADES","SAT-MON","VISA","IPCV","CPNX","CPHB","WSN","PVP","BR-SAT-MON","SUN-ND","IPv6-CM","IPv6-NoNxt","IPv6-Opts","AHIP","CFTP","ALN","SAT-EXPAK","KRYPTOLAN","RVD","IPPC","BNA","ESP","AH","I-NLSP","SWIPE","NARP","MOBILE","TLSP","SKIP","TP++","IPv6","SDRP","IPv6-Route","IPv6-Frag","IDRP","RSVP","GRE","DSR","IL","ISO-TP4","NETBLT","MEE-NSP","MERIT-INP","DCCP","3PC","IDPR","XTP","DoP","IDPR-CMTP","ISO-TP4","NETBLT","MEE-NSP","MERIT-INP","DCCP","3PC","IDPR","XTP","DoP","IDPR-CMTP","BBN-RCC-MON","NVP-Il","PUP","ARGUS","EMCON","XNET","CHAOS","MUX","DCN-MEAS","HOPOPT","ICMP","IGMP","GGP","IPV4","ST","CBT","EGP","IGP","Other"]

    def deploy_new_config(self):
        print("\n\n\n\t\t\t\t\t\t\t\t\tready to deploy")
        self.update_previous_data_in_items_list()
        self.add_new_data_in_items_list()
        self.delete_data_in_items_list()
    
    def correct_data_type_for_applications_configuration(self):
        #print(json.dumps(self.new_config, sort_keys=False, indent=4))
        for item in self.new_config['items']:

            if not isinstance(item['name'],str):
                print(f"App name wrong data type, it should be a string -> '{item['name']}'")
                return False
            elif not self.is_data_valid_and_can_have_spaces(item['name'],self.APP_NAME_STRING_MIN_LENGTH,self.APP_NAME_STRING_MAX_LENGTH,"name"):
                return False


            if item['desc'] == None:
                del item['desc']
            elif not isinstance(item['desc'],str):
                print(f"App description is wrong data type, it should be a string -> '{item['desc']}'")
                return False
            elif not self.is_data_valid_and_can_have_spaces(item['desc'],self.DESCRIPTION_STRING_MIN_LENGTH,self.DESCRIPTION_STRING_MAX_LENGTH,"desc"):
                return False

            if not isinstance(item['enabled'],bool):
                print(f"enabled variable date type should be boolean -> {item['enabled']}")
                return False

            if not isinstance(item['traffic_match_mode'],str):
                print(f"traffic_match_mode variable date type should be string -> {item['traffic_match_mode']}")
                return False
            elif not item['traffic_match_mode'] in self.TRAFFIC_MATCH_MODE_LIST:
                print(f"{item['traffic_match_mode']} is a incorrect traffic mode it should one of {self.TRAFFIC_MATCH_MODE_LIST}")

            if item['include_dpi_tags'] == None:
                del item['include_dpi_tags']
            elif not isinstance(item['include_dpi_tags'],bool):
                print(f"include_dpi_tags variable date type should be boolean -> {item['enabled']}")
                return False

            if not self.is_application_definitions_correct(item):
                print("test")
                return False
            

        #print("old config")
        #print("====================================================")
        #print(json.dumps(self.old_config, sort_keys=False, indent=4))
        #print("====================================================")
        #print("new config")
        #print("====================================================")
        #print(json.dumps(self.new_config, sort_keys=False, indent=4))

        return True

    def is_application_definitions_correct(self,received_definitions_items):
        #print (f"\ndef rule is\t{received_definitions_items['definitions']['items']}")

        for definition_item in received_definitions_items['definitions']['items']:
            print(f"def items are {definition_item}\n")


            #go through config transport rules
            for transport_rule in definition_item['transport_rules']:
                print (f"\t\tthe trans rule is {transport_rule}")

                
                if transport_rule.get('ports'):
                    #a port must have an ip_protocol or its not valid
                    if not transport_rule.get('ip_protocol'):
                        print ("no ip_protocol with port")
                        return False
                    # and the port must be with either a UDP or TCP ip protocol
                    elif not transport_rule.get('ip_protocol') in self.PORT_IP_PROTOCOL_LIST:
                        print(f"port can only be with a TCP or UDP protocol no {transport_rule.get('ip_protocol')} protocol")
                        return False

                    #port must formated correctly
                    if not self.port_config_format_is_correct(transport_rule.get('ports')):
                       return False
                #print(f"\t\t\t\t port is :- {transport_rule.get('ports')}")
        return True

    def port_config_format_is_correct(self,received_formated_port_config):
        #there are two way to present port information
        #option 1 single number ports from 0 to 65535 separted by a coma... example 8080,8888
        #option 2 inbetween two number from 0 to 65535 space with a minus sign... example 8080-8085
        #results should be in string format
    
        
        if "-" in received_formated_port_config:
            two_port_list = received_formated_port_config.split("-")
            
            #if " " in received_formated_port_config:
            #    print(f"'{received_formated_port_config}' port config can't contain any spaces")
            #    return False

            #should only be two element list from split, if there are more, then port config is incorrect
            if len(two_port_list) == 2:
                #check that string is string of numbers
                if (two_port_list[0].isdecimal()) and (two_port_list[1].isdecimal()):
                    #check number are in correct order, small to largest
                    if int(two_port_list[0]) > int(two_port_list[1]):
                        print (f"{received_formated_port_config} is formated incorrectly. Smallest then largest number")
                        return False

                    #ensure port number are with the range of TCP and UDP ports
                    elif int(two_port_list[0]) < self.MIN_TCP_AND_UDP_PORT_NUMBER or int(two_port_list[0]) > self.MAX_TCP_AND_UDP_PORT_NUMBER or int(two_port_list[1]) < self.MIN_TCP_AND_UDP_PORT_NUMBER or int(two_port_list[1]) > self.MAX_TCP_AND_UDP_PORT_NUMBER:
                        print(f"{received_formated_port_config} port option are out of range, should between {self.MIN_TCP_AND_UDP_PORT_NUMBER} and {self.MAX_TCP_AND_UDP_PORT_NUMBER}")
                        return False

                else:
                    print(f"{received_formated_port_config} port config is not formatted correctly")
                    return False
            else:
                print(f"'{received_formated_port_config}' port config is not formatted correctly")
                return False
        else:

            received_formated_port_config = received_formated_port_config.replace(" ", "")
            ports_list = received_formated_port_config.split(",")
            for port in ports_list:

                if not port.isdecimal():
                    print(f"{port} port config is not formatted correctly...")
                    return False

                elif int(port) < self.MIN_TCP_AND_UDP_PORT_NUMBER or int(port) > self.MAX_TCP_AND_UDP_PORT_NUMBER:
                    print(f"{port} option are out of range, should between {self.MIN_TCP_AND_UDP_PORT_NUMBER} and {self.MAX_TCP_AND_UDP_PORT_NUMBER}")
                    return False

        return True

    def is_new_config_logic_correct(self):
        print ("checking Applications config")
        return self.correct_data_type_for_applications_configuration()

class Ar_Hostgroups(Appresponse_Mgmt):
    api_url = "/api/npm.classification/3.2/hostgroups/"


    HOSTGROUP_NAME_STRING_MIN_LENGTH = 1
    HOSTGROUP_NAME_STRING_MAX_LENGTH = 70
    HOSTGROUP_DESCRIPTION_STRING_MIN_LENGTH = 0
    HOSTGROUP_DESCRIPTION_STRING_MAX_LENGTH = 300
    HOSTGROUP_SPEEP_UNIT_LIST = ["Mbps","kbps","Gbps"]
    HOSTGROUP_MIN_SPEED_NUMBER = 0
    HOSTGROUP_MAX_SPEED_NUMBER = 1000
    HOSTGROUP_MAX_ID_NUMBER = 1024

    def update_previous_hostgroups(self):
        for item in self.new_config['items']:
            if item.get('id'):
                url = f"https://{self.ar_ip_addr}/api/npm.classification/3.2/hostgroups/items/{item['id']}"
                payload = json.dumps(item)
                headers = {
                    'Authorization': f'Bearer {self.ar_bearer_token}',
                    'Content-Type': 'application/json'
                    }

                response = requests.request("PUT", url, headers=headers, data=payload,verify=False)
                print (response)

    def add_new_hostgroups(self):
        for item in self.new_config['items']:
            if not item.get('id'):
                print("adding new item")
                url = f"https://{self.ar_ip_addr}/api/npm.classification/3.2/hostgroups"
                payload = json.dumps(item)
                headers = {
                    'Authorization': f'Bearer {self.ar_bearer_token}',
                    'Content-Type': 'application/json'
                    }
                response = requests.request("POST", url, headers=headers, data=payload,verify=False)
                print (response)

    def delete_hostgroup(self):
        #create list of grouphost id from old list
        old_host_group_id_list =[]
        for item in self.old_config['items']:
            old_host_group_id_list.append(item['id'])
        
        #loop though new config and remove grouphost id's that are still in the new config
        for item in self.new_config['items']:
            if item.get('id') in old_host_group_id_list:
                old_host_group_id_list.remove(item.get('id'))

        print(f"old host group {old_host_group_id_list}")
        #delete what left of old hostgroup list
        if len(old_host_group_id_list)>0:
            for id in old_host_group_id_list:
                print(f"delete host id {id}")
                url = f"https://{self.ar_ip_addr}/api/npm.classification/3.2/hostgroups/items/{id}"
                payload = ""
                headers = {
                    'Authorization': f'Bearer {self.ar_bearer_token}',
                    'Content-Type': 'application/json'
                    }
                response = requests.request("DELETE", url, headers=headers, data=payload,verify=False)
                print (response)

    def deploy_new_config(self):
        print("update previous")
        self.update_previous_data_in_items_list()
        print("add new")
        self.add_new_data_in_items_list()
        print("delete old")
        self.delete_data_in_items_list()


    def correct_data_type_for_host_group_configuration(self):
        

        for item in self.new_config['items']:
            #check host group name is correct
            if not isinstance(item['name'], str):
                print(f"hostgroup name '{item['name']}' is wrong data type, should be a string")
                return False
            elif len(item['name']) < self.HOSTGROUP_NAME_STRING_MIN_LENGTH or len(item['name']) > self.HOSTGROUP_NAME_STRING_MAX_LENGTH:
                print(f"host group name '{item['name']}' is either to short or long, max length - {self.HOSTGROUP_NAME_STRING_MAX_LENGTH}")
                return False

            #check host group desc is correct
            if not item['desc'] == None:
                if len(item['desc'])>self.HOSTGROUP_DESCRIPTION_STRING_MAX_LENGTH:
                    print(f"host group enabled '{item['desc']}' is to long, max length - {self.HOSTGROUP_DESCRIPTION_STRING_MAX_LENGTH}")
                    return False
            else:
                del item['desc']

            #check enabled is correct
            if not isinstance(item['enabled'],bool):
                print(f"hostgroup name '{item['enabled']}' is wrong data type, should be a boolean")
                return False

            #check id correct
            if item.get('id'):
                if not isinstance(item['id'], int):
                    print(f"hostgroup ID '{item['id']}' is wrong data type, should be a integer")
                    return False
                elif item['id'] > self.HOSTGROUP_MAX_ID_NUMBER:
                    print(f"hostgroup ID '{item['id']}' is to big, should be less than {self.HOSTGROUP_MAX_ID_NUMBER}")
                    return False                

            #check utilization bandwidth config
            if item.get('in_speed_unit'):
                if not item['in_speed_unit'] in self.HOSTGROUP_SPEEP_UNIT_LIST:
                    print(f" wrong speed unit entered '{item['in_speed_unit']}' - should be one of the following {self.HOSTGROUP_SPEEP_UNIT_LIST}")
                    return False
            if item.get('out_speed_unit'):
                if not item['out_speed_unit'] in self.HOSTGROUP_SPEEP_UNIT_LIST:
                    print(f" wrong speed unit entered '{item['out_speed_unit']}' - should be one of the following {self.HOSTGROUP_SPEEP_UNIT_LIST}")
                    return False
            if item.get('out_speed_unit') and item.get('in_speed_unit'):
                if item['in_speed'] < self.HOSTGROUP_MIN_SPEED_NUMBER or item['in_speed'] > self.HOSTGROUP_MAX_SPEED_NUMBER or item['out_speed'] < self.HOSTGROUP_MIN_SPEED_NUMBER or item['out_speed'] > self.HOSTGROUP_MAX_SPEED_NUMBER:
                        print(f" wrong speed entered  - should be between {self.HOSTGROUP_MIN_SPEED_NUMBER} and {self.HOSTGROUP_MAX_SPEED_NUMBER}")
                        return False

            #check memeber hostgroup config
            if item.get('member_hostgroups'):
                if not isinstance(item['member_hostgroups'],list):
                    print(f"memeber_hostgroups is wrong datga type")
                    return False
                else:
                    for i in range(0, len(item['member_hostgroups'])):

                        if item['member_hostgroups'][i] == "None":
                            del item['member_hostgroups']
                        elif not item['member_hostgroups'][i].isdecimal():
                            print(f'error member group should be an interger')
                            return False
                        else:
                            #received list is a list of strings, we need to convert it to a list of integers
                            item['member_hostgroups'][i] = int(item['member_hostgroups'][i])

            #check ip host information is correct
            #two option for ip host information
            #option 1 - single ip address e.g. 192.168.1.1  
            #option 2 - ip range e.g. 10.0.0.1-10.0.0.255
            for host_ip in item['hosts']:
                if host_ip.count("-") > 1:
                    print(f"ip address range is incorrect - {host_ip}")
                    return False
                elif host_ip.count("-") == 1: 
                    ip_host_list = host_ip.split("-")
                    if not self.check_ip_addr(ip_host_list[0]):
                        return False
                    elif not self.check_ip_addr(ip_host_list[1]):
                        return False
                    elif " " in ip_host_list[0] or " " in ip_host_list[1]:
                        print(f"this '{host_ip} can't contain spaces")
                        return False
                elif host_ip.count("-") == 0:
                    if not self.check_ip_addr(host_ip):
                        return False

        return True            

    def there_are_no_hostgroups_with_the_same_id(self):
        hostgroup_id_list = []
        for item in self.new_config["items"]:
            if item.get('id'):
                if item['id'] in hostgroup_id_list:
                    print("ERROR - There are duplicate hostgroup id's")
                    return False
                hostgroup_id_list.append(item['id'])
        return True

    def no_hostgroup_ids_that_werent_there_before(self):
        old_config_host_ids_list = []
        
        for item in self.old_config['items']:
            old_config_host_ids_list.append(item['id'])


        for item in self.new_config['items']:
            if item.get('id'):
                if not item['id'] in old_config_host_ids_list:
                    print("ERROR - A hostgroup id found that wasn't in oirginal config")
                    return False
        return True

    def is_new_config_logic_correct(self):
        print ("checking Host Group config")
        if not self.correct_data_type_for_host_group_configuration():
            return False
        elif not self.no_hostgroup_ids_that_werent_there_before():#
            return False
        elif not self.there_are_no_hostgroups_with_the_same_id():
            return False
        else:
            return True

class Ar_Urls(Appresponse_Mgmt):
    api_url = "/api/npm.classification/3.2/urls/"
    
    URLS_NAME_STRING_MIN_LENGTH = 1
    URLS_NAME_STRING_MAX_LENGTH = 70
    URLS_DESCRIPTION_STRING_MIN_LENGTH = 0
    URLS_DESCRIPTION_STRING_MAX_LENGTH = 300
    URLS_STRING_MIN_LENGTH = 1
    URLS_STRING_MAX_LENGTH = 60
    
    def deploy_new_config(self):
        self.update_previous_data_in_items_list()
        self.add_new_data_in_items_list()
        self.delete_data_in_items_list()

    def is_new_config_logic_correct(self):
        print ("checking URL definitions config")
        return self.correct_data_type_for_urls_configuration()

    
    def correct_data_type_for_urls_configuration(self):

        for item in self.new_config['items']:
            print (item)
            print("=========================================")

            #check URLS name is correct
            if not self.is_data_valid_and_can_have_spaces(item['name'],self.URLS_NAME_STRING_MIN_LENGTH,self.URLS_NAME_STRING_MAX_LENGTH,"name"):
                return False

            #check description is correct
            if not self.is_data_valid_and_can_have_spaces(item['desc'],self.URLS_DESCRIPTION_STRING_MIN_LENGTH,self.URLS_DESCRIPTION_STRING_MAX_LENGTH,"desc"):
                return False

            #check enabled is correct
            if not self.is_it_a_boolean(item['enabled'],"enabled"):
                return False

            #check preferred it correct
            if not self.is_it_a_boolean(item['preferred'],"preferred"):
                return False

            #check id is correct
            print(f"item id is {item['id']}")
            if not item['id'] == None:
                id_is_it_a_decimal,item['id'] = self.is_it_a_decimal_if_required_convert_decimal_string_to_integer(item['id'],'id')
                if not id_is_it_a_decimal:
                    return False
            else:
                del item['id']

            for url in item['urls']:
                if not self.is_data_valid_cant_have_spaces(url,self.URLS_STRING_MIN_LENGTH,self.URLS_STRING_MAX_LENGTH,"url"):
                    return False


        print('happy days')
        return True

class Ar_Vifgs(Appresponse_Mgmt):
    api_url = "/api/npm.packet_capture/3.0/vifgs"

    VIFG_NAME_STRING_MIN_LENGTH = 1
    VIFG_NAME_STRING_MAX_LENGTH = 70
    VIFG_DESCRIPTION_STRING_MIN_LENGTH = 0
    VIFG_DESCRIPTION_STRING_MAX_LENGTH = 300
    VIFG_STRING_MIN_LENGTH = 1
    VIFG_STRING_MAX_LENGTH = 60

    def is_new_config_logic_correct(self):
        print ("checking vifgs definitions config")
        return self.correct_data_type_for_vifgs_configuration()

    def correct_data_type_for_vifgs_configuration(self):

        print(json.dumps(self.old_config, sort_keys=False, indent=4))
        print(json.dumps(self.new_config, sort_keys=False, indent=4))