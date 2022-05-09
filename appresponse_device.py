#from xmlrpc.client import boolean
import requests
import json
import appresponse_mgmt_api

class AppResponse:
    
    num_of_ars = int(0)
    
    def __init__(self,ip_addr,bearer_token):
        self.ip_addr=ip_addr
        self.bearer_token=bearer_token
        self.new_config = False

        self.ntp_class = appresponse_mgmt_api.Ar_Ntp(self.ip_addr,self.bearer_token)
        self.ntp_original_data = self.ntp_class.get_data_with_api_call()
        print("=====================================================================================")
        self.snmp_class = appresponse_mgmt_api.Ar_Snmp(self.ip_addr,self.bearer_token)
        self.snmp_original_data = self.snmp_class.get_data_with_api_call()
        print("=====================================================================================")
        self.common_class = appresponse_mgmt_api.Appresponse_Mgmt(self.ip_addr,self.bearer_token)
        self.common_original_data = self.common_class.get_data_with_api_call()
        print("=====================================================================================")
        self.vifgs_class = appresponse_mgmt_api.Ar_Vifgs(self.ip_addr,self.bearer_token)
        self.vifgs_original_data = self.vifgs_class.get_data_with_api_call()
        print("=====================================================================================")
        self.cap_job_class = appresponse_mgmt_api.Ar_Capture_Jobs(self.ip_addr,self.bearer_token)
        self.cap_job_original_data = self.cap_job_class.get_data_with_api_call()
        print("=====================================================================================")
        self.dns_class = appresponse_mgmt_api.Ar_Dns(self.ip_addr,self.bearer_token)
        self.dns_original_data = self.dns_class.get_data_with_api_call()
        print("=====================================================================================")
        self.phy_int_class = appresponse_mgmt_api.Ar_Phy_Int(self.ip_addr,self.bearer_token)
        self.phy_int_original_data = self.phy_int_class.get_data_with_api_call()
        print("=====================================================================================")
        self.ar_apps_class = appresponse_mgmt_api.Ar_Applications(self.ip_addr,self.bearer_token)
        self.ar_apps_original_data = self.ar_apps_class.get_data_with_api_call()
        print("=====================================================================================")
        self.hostgroups_class = appresponse_mgmt_api.Ar_Hostgroups(self.ip_addr,self.bearer_token)
        self.hostgroups_original_data = self.hostgroups_class.get_data_with_api_call()
        print("=====================================================================================")
        self.urls_class = appresponse_mgmt_api.Ar_Urls(self.ip_addr,self.bearer_token)
        self.urls_original_data = self.urls_class.get_data_with_api_call()
    
        AppResponse.num_of_ars += 1
      

    def update_ar_device_config(self,received_new_config_option):
        if "snmp" in received_new_config_option: 
            self.snmp_class.deploy_new_config()
        elif "dns" in received_new_config_option:
            self.dns_class.deploy_new_config()
        elif "ntp" in received_new_config_option:
            self.ntp_class.deploy_new_config()
        elif "hostgroups" in received_new_config_option:
            self.hostgroups_class.deploy_new_config()
        elif "urls" in received_new_config_option:
            self.urls_class.deploy_new_config()
        elif "apps" in received_new_config_option:
            self.ar_apps_class.deploy_new_config()
        
    def affirm_new_config_is_good(self,received_new_config_options):
        print(received_new_config_options)
        if "snmp" in received_new_config_options:
            self.conifg_status = self.snmp_class.affirm_new_config(received_new_config_options['snmp'],self.snmp_original_data,self.ip_addr)
            return self.conifg_status
        elif "dns" in received_new_config_options:
            self.conifg_status = self.dns_class.affirm_new_config(received_new_config_options['dns'],self.dns_original_data,self.ip_addr)
            return self.conifg_status
        elif "ntp" in received_new_config_options:
            self.conifg_status = self.ntp_class.affirm_new_config(received_new_config_options['ntp'],self.ntp_original_data,self.ip_addr)
            return self.conifg_status
        elif "hostgroups" in received_new_config_options:
            self.conifg_status = self.hostgroups_class.affirm_new_config(received_new_config_options['hostgroups'],self.hostgroups_original_data,self.ip_addr)
            return self.conifg_status
        elif "urls" in received_new_config_options:
            self.conifg_status = self.urls_class.affirm_new_config(received_new_config_options['urls'],self.urls_original_data,self.ip_addr)
            return self.conifg_status
        elif "apps" in received_new_config_options:
            self.conifg_status = self.ar_apps_class.affirm_new_config(received_new_config_options['apps'],self.ar_apps_original_data,self.ip_addr)
            return self.conifg_status

    def print_old_and_new_config_plus_config_status(self,received_new_config_option):

        if self.conifg_status:
            print("\t\t\t#####################")
            print("\t\t\tNew Config is correct")
            print("\t\t\t#####################")
        else:
            print("\t\t\t*************************")
            print("\t\t\tNew Config is not correct")
            print("\t\t\t*************************")
        if "snmp" in received_new_config_option: 
            self.snmp_class.print_old_and_new_config()
        elif "dns" in received_new_config_option:
            self.dns_class.print_old_and_new_config()
        elif "ntp" in received_new_config_option:
            self.ntp_class.print_old_and_new_config()
        elif "hostgroups" in received_new_config_option:
            self.hostgroups_class.print_old_and_new_config()
        elif "urls" in received_new_config_option:
            self.urls_class.print_old_and_new_config()
        elif "apps" in received_new_config_option:
            self.ar_apps_class.print_old_and_new_config()


    def push_out_new_config(self,received_new_config_options):
        #print(json.dumps(received_new_config_options, sort_keys=False, indent=6))
        pass
