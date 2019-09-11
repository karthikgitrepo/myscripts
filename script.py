import json
import requests
import sys
import socket
import getpass

user = input("enter your long account:")
passwd = getpass.getpass("enter your intra password:")
shortaccount = input("enter your shortaccount:")

url = "https://forest-api.intra.rakuten-it.com/porta/v1/auth/token"
try:
    auth_values = (user,passwd)
    forest_token=requests.post(url, auth=auth_values)
    token=forest_token.json()["token"]
    headers = {"Authorization": "Bearer " + token}
except Exception as e:
    print("OOPS! your username and password is not correct:")
    sys.exit(0)

flag ="true"
while (flag=="true"):
    ipaddress = input('enter vip ipaddr:')
    try:
        if socket.gethostbyaddr(ipaddress):
            print ("ip resolved")
            flag ="false"
    except:
        continue

vipport = int(input('enter vip port:'))
if vipport < 65534:
    print("accepted:")
else:
    print("enter valid one:")
    sys.exit(0)

def writejsonfile():
    list = ["tcp", "http", "https_balancer", "https_server"]
    servicetype = input('enter service type as "tcp" "http"  "https_balancer" "https_server"')
    balancer = input("enter balancer (slb)name:")
    authority = input("enter authority group ex: ORG004833:")
    xff = bool(input("enter xff true or just press enter dont enter any value:"))
    if servicetype in str(list):
        data = {}
        data['vip_address'] = ipaddress
        data['vip_port'] = vipport
        data['service_type'] = servicetype
        data['balancer'] = balancer
        data['authority'] = authority
        data['x_forwarded_for'] = xff

        filename = 'vipcreate' + ipaddress + '_' + str(vipport)
        filepath = filename + '.json'
        with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
            json.dump(data, fp)
    else:
        print("not matched service type run script again:")
        sys.exit(0)

def getvipcontent():
    flag = "true"
    while (flag=="true"):
        method = input("enter get method to see current vip info:")
        try:
            if method == 'get':
                req = requests.get('https://forest-api.intra.rakuten-it.com/v1/vips/' + ipaddress, headers=headers)
                print(req.text)

                flag ="false"
        except:
            continue

def vipregister():
    flag="true"
    while(flag=="true"):
        method = input("enter post method to add vip on slb:")
        try:
            if method == 'post':
                filename = 'vipcreate' + ipaddress + '_' + str(vipport)
                filepath = filename + '.json'
                with open('/home/' + shortaccount + '/' + filepath, "rb") as fp:
                    data_json = json.load(fp)
                    req = requests.post('https://forest-api.intra.rakuten-it.com/v1/vips', headers=headers,data=json.dumps(data_json))
                    print(req.text)

                    flag ="false"
        except:
            continue
 
def gethealthcheck():
    flag = "true"
    while (flag == "true"):
        method = input("enter get method to see current healthcheck info:")
        try:
            if method == 'get':
                req = requests.get('https://forest-api.intra.rakuten-it.com/v1/vips/' + ipaddress + '/' + str(vipport) + '/health_monitor', headers=headers)
                print(req.text)

                flag = "false"
        except:
            continue
            
def skipupdatehealth():
    print("No need to update health default is tcp_monitor")

def healthcheckwritedata():
    filename = 'healthcheck' + ipaddress + '_' + str(vipport)
    health = input("enter slb_hm_name contents if you want to add hostheader dont write any value just press enter:")
    protocol = input("enter protocol which you want if you don't want to add hostheader don't write any value just press enter:")
    header = input("enter host header if you don't want just  press enter:")
    contentpath = input("if you have host header plese enter content_path ex:/wwwcheck.html or just press enter:")
    if not header:
        data = {'slb_hm_name': health}
        filepath = filename + '.json'
        with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
            json.dump(data, fp)
    else:
        data = {'protocol':protocol,'content_path':contentpath,'hostheader': header}
        filepath = filename + '.json'
        with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
            json.dump(data, fp)

def patchhealthcheck():
    flag="true"
    while(flag=="true"):
        method = input("enter patch method to update current healthcheck for vip:")
        try:
            if method == 'patch':
                filename = 'healthcheck' + ipaddress + '_' + str(vipport)
                filepath = filename + '.json'
                with open('/home/' + shortaccount + '/' + filepath, "rb") as fp:
                    data_json1 = json.load(fp)
                    req = requests.patch(
                        'https://forest-api.intra.rakuten-it.com/v1/vips/' + ipaddress + '/' + str(vipport) + '/health_monitor',
                        headers=headers, data=json.dumps(data_json1))
                    print(req.text)
                    
                    flag ="false"
        except:
            continue

def AddRealspecific():
    condition = "true"
    while (condition=="true"):
        value = int(input("enter number of servers range :"))
        filename = 'addrealserver' + ipaddress + '_' + str(vipport)
        filepath = filename + '.json'
        data = {}
        data['members'] = []
        i =0
        while i < value:
            try:
                ip_addr = input("enter hostnames:")
                sport = int(input("enter realserver port:"))
                host = (socket.gethostbyname(ip_addr))
                data['members'].append({'server_address': host, 'server_port': sport})
                with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
                    json.dump(data, fp)
                    i+=1
                    condition = "false"
            except:
                print("OOPS!  something went wrong in addrealservers try again:")
                continue

def Addrealserversdata():
    condition = "true"
    while (condition=="true"):
        data = {}
        data['members'] = []
        try:
            number =int(input("enter hostname number ex your host is stg-zed1101 and number is 1101:"))
            range = int(input("enter number of server range:"))
            sport = int(input("enter realserever port:"))
            name = input("enter hostname is like stg-zed:")
            fqdn = input("enter fqdn is like z.stg.jp.local if global z.at.jp.local:")
            filename = 'addrealserver' + ipaddress + '_' + str(vipport)
            filepath = filename + '.json'
            count = 0
            while count < range:
                ip_addr = (socket.gethostbyname(name + str(number) + fqdn))
                data['members'].append({'server_address': ip_addr, 'server_port': sport})
                count+= 1
                number += 1
            with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
                json.dump(data, fp)

                condition = "false"
        except:
             print ("OOPS!  something went wrong in addrealservers try again:")
             continue

def getrealservers():
    flag = "true"
    while (flag == "true"):
        method = input("enter get method to see current realservers info:")
        try:
            if method == 'get':
                req = requests.get('https://forest-api.intra.rakuten-it.com/v1/vips/'+ ipaddress + '/' + str(vipport) + '/members?status=true', headers=headers)
                print(req.text)

                flag ="false"
        except:
            continue

def postrealservers():
    flag="true"
    while(flag=="true"):
        method = input("enter post method to add realservers for vip:")
        try:
            if method == 'post':
                filename = 'addrealserver' + ipaddress + '_' + str(vipport)
                filepath = filename + '.json'
                with open('/home/' + shortaccount + '/' + filepath, "rb") as fp:
                    data_json2 = json.load(fp)
                    req = requests.post('https://forest-api.intra.rakuten-it.com/v1/vips/'+ ipaddress + '/' + str(vipport) + '/members', headers=headers,data=json.dumps(data_json2))
                    print(req.text)

                    flag ="false"
        except:
            continue

def sinwritespecific():
    condition = "true"
    while (condition=="true"):
        value = int(input("enter number of servers range for s-in:"))
        filename = 'sinip' + ipaddress + '_' + str(vipport)
        filepath = filename + '.json'
        data = {}
        data['members'] = []
        i =0
        while i < value:
            try:
                ip_addr = input("eneter hostnames with fqdn:")
                sport = int(input("enter realserver port:"))
                host = (socket.gethostbyname(ip_addr))
                portenable = bool(input("enter true:"))
                data['members'].append({'server_address': host, 'server_port': sport, 'port_enabled': portenable})
                with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
                    json.dump(data, fp)
                    i+=1
                    condition = "false"
            except:
                print("OOPS!something went wrong: SIN try again")
                continue

def sinwrite():
    condition = "true"
    while (condition=="true"):
        data = {}
        data['members'] = []
        try:
            number =int(input("enter hostname number ex your host is stg-zed1101 and number is 1101 for s-in:"))
            range = int(input("enter number of servers range for s-in:"))
            sport = int(input("enter realserver port:"))
            name = input("enter hostname like stg-zed:")
            fqdn=input("enter fqdn is like z.stg.jp.local/z.at.jp.local:")
            portenable = bool(input("enter true for s-in:"))
            filename = 'sinip' + ipaddress + '_' + str(vipport)
            filepath = filename + '.json'
            count = 0
            while count < range:
                ip_addr = (socket.gethostbyname(name + str(number) + fqdn))
                data['members'].append({'server_address': ip_addr,'server_port': sport,'port_enabled':portenable})
                count+= 1
                number += 1
            with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
                json.dump(data, fp)

            condition = "false"
        except:
            print("OOPS!something went wrong: SIN try again")
            continue

def patchsinservers():
    flag ="true"
    while(flag=="true"):
        method = input("enter patch method for update sin:")
        try:
            if method == 'patch':
                filename = 'sinip' + ipaddress + '_' + str(vipport)
                filepath = filename + '.json'
                with open('/home/' + shortaccount + '/' + filepath, "rb") as fp:
                    data_json3 = json.load(fp)
                    req = requests.patch('https://forest-api.intra.rakuten-it.com/v1/vips/'+ ipaddress + '/' + str(vipport) + '/members', headers=headers,
                             data=json.dumps(data_json3))
                    print(req.text)

                    flag ="false"
        except:
            continue

def soutwritespecific():
    condition = "true"
    while (condition=="true"):
        value = int(input("enter number of servers range for s-out:"))
        filename = 'soutip' + ipaddress + '_' + str(vipport)
        filepath = filename + '.json'
        data = {}
        data['members'] = []
        i =0
        while i < value:
            try:
                ip_addr = input("eneter hostnames with fqdn:")
                sport = int(input("enter realserver port:"))
                host = (socket.gethostbyname(ip_addr))
                portenable = bool(input("for s-out just press enter don't enter any key:"))
                data['members'].append({'server_address': host, 'server_port': sport, 'port_enabled': portenable})
                with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
                    json.dump(data, fp)
                    i+=1
                    condition = "false"
            except:
                print("OOPS!something went wrong: SOUT try again")
                continue

def soutwrite():
    condition = "true"
    while (condition=="true"):
        data = {}
        data['members'] = []
        try:
            number =int(input("enter hostname number ex your host is stg-zed1101 and number is 1101 for s-out:"))
            range = int(input("enter number of servers range for s-out:"))
            sport = int(input("enter realserver port:"))
            name = input("enter hostname ex:stg-zed:")
            fqdn=input("enter fqdn is like z.stg.jp.local/z.at.jp.local:")
            portenable = bool(input("for s-out just press enter don't enter any key:"))
            filename = 'soutip' + ipaddress + '_' + str(vipport)
            filepath = filename + '.json'
            count = 0
            while count < range:
                ip_addr = (socket.gethostbyname(name + str(number) + fqdn))
                data['members'].append({'server_address': ip_addr,'server_port': sport,'port_enabled':portenable})
                count+= 1
                number += 1
            with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
                json.dump(data, fp)

            condition = "false"
        except:
            print("OOPS!something went wrong: SOUT try again")
            continue

def patchsoutservers():
    flag ="true"
    while(flag=="true"):
        method = input("enter patch method for update sout:")
        try:
            if method == 'patch':
                filename = 'soutip' + ipaddress + '_' + str(vipport)
                filepath = filename + '.json'
                with open('/home/' + shortaccount + '/' + filepath, "rb") as fp:
                    data_json5 = json.load(fp)
                    req = requests.patch('https://forest-api.intra.rakuten-it.com/v1/vips/'+ ipaddress + '/' + str(vipport) + '/members', headers=headers,
                             data=json.dumps(data_json5))
                    print(req.text)

                    flag ="false"
        except:
            continue

def Addbusy():
    filename = 'busy' + ipaddress + '_' + str(vipport)
    data = {'busy_servers':bool(busyservers)}
    filepath = filename + '.json'
    with open('/home/' + shortaccount + '/' + filepath, "w") as fp:
        json.dump(data, fp)

def postbusyservers():
    flag = "true"
    while (flag == "true"):
        method = input("enter post method to add busyservers:")
        try:
           if method == 'post':
               filename = 'busy' + ipaddress + '_' + str(vipport)
               filepath = filename + '.json'
               with open('/home/' + shortaccount + '/' + filepath, "rb") as fp:
                   data_json4 = json.load(fp)
                   req = requests.post('https://forest-api.intra.rakuten-it.com/v1/vips/' + ipaddress + '/' + str(vipport) + '/members',
                            headers=headers, data=json.dumps(data_json4))
                   print(req.text)

                   flag = "false"

        except:
            continue
            
def Deleterealservers():
    flag="true"
    while(flag=="true"):
        method = input("enter delete method to delete realservers:")
        try:
            if method == 'delete':
                filename = 'addrealserver' + ipaddress + '_' + str(vipport)
                filepath = filename + '.json'
                with open('/home/' + shortaccount + '/' + filepath, "rb") as fp:
                    data_json = json.load(fp)
                    req = requests.delete('https://forest-api.intra.rakuten-it.com/v1/vips/'+ ipaddress + '/' + str(vipport) + '/members', headers=headers,data=json.dumps(data_json))
                    print(req.json())

                    flag ="false"
        except:
            continue

def Delvip():
    flag="true"
    while(flag=="true"):
        method = input("enter delete method to delete vip:")
        try:
            if method == 'delete':
                req = requests.delete('https://forest-api.intra.rakuten-it.com/v1/vips/' + ipaddress + '/' + str(vipport), headers=headers)
                print(req.json())

            flag ="false"
        except:
            continue

if __name__ == '__main__':
    vipreg = input("do you want register vip and realservers or only realservers  yes or no:")
    if vipreg == 'yes':
        writejsonfile()
        print("please check your vipcreate file in your home directory before post")
        getvipcontent()
        vipregister()
        gethealthcheck()
        skiphealth= input("do you want to skip update healthcheck by default helathcheck is monitor_tcp then you press just 'yes' else press 'no' to update health:")
        if skiphealth == 'yes':
            skipupdatehealth()
        else:
            healthcheckwritedata()
            print("please check healthcheck file in your home directory before executing further methods")
            patchhealthcheck()
            gethealthcheck()
        specific = input("if you want to add specific realservers enter yes or no:")
        if specific == 'yes':
            AddRealspecific()
            print("please cross check your realserversdata file in your homedirectory before exexuting methods")
            getrealservers()
            postrealservers()
            sinwritespecific()
            print("please cross check your sin file in your home directory before executing further")
            patchsinservers()
        else:
            Addrealserversdata()
            print("please cross check your realserversdata file in your homedirectory before exexuting methods")
            getrealservers()
            postrealservers()
            sinwrite()
            print("please cross check your sin file in your home directory before executing further")
            patchsinservers()

        busyservers = input("do you want to add busy servers true/false:")
        if busyservers == 'true':
            Addbusy()
            print("please check your busy file in your home directory before executing")
            postbusyservers()
            print("busy servers has been added succesfully")
        else:
            print("no busy servers you've selected")
            
        undooperation = input("do you want to rollback your operation yes/no:")
        if undooperation == 'yes':
            soutspec = input("do you want to s-out specific servers yes/no:")
            if soutspec == 'yes':
                soutwritespecific()
                patchsoutservers()
                Deleterealservers()
                Delvip()
                print("your script executed sucessfully")
            else:
                soutwrite()
                patchsoutservers()
                Deleterealservers()
                Delvip()
                print("your script executed sucessfully")
        else:
            print("your script executed successfully")
            sys.exit(0)

    else:
        specific = input("do you want to add specific real servers or group of realservers enter yes or no:")
        if specific == 'yes':
            AddRealspecific()
            print("please cross check your realserversdata file in your home directory before exexuting methods")
            getrealservers()
            postrealservers()
            sinwritespecific()
            print("please cross check your sin file in your home directory before executing further")
            patchsinservers()
        else:
            Addrealserversdata()
            print("please cross check your realserversdata file in your homedirectory before exexuting methods")
            getrealservers()
            postrealservers()
            sinwrite()
            print("please cross check your sin file in your home directory before executing further")
            patchsinservers()
            undooperation = input("do you want to rollback your operation yes/no:")
            if undooperation == 'yes':
                soutspec = input("do you want to s-out specific servers yes/no:")
                if soutspec == 'yes':
                    soutwritespecific()
                    patchsoutservers()
                    Deleterealservers()
                    print("your script executed sucessfully")
                else:
                    soutwrite()
                    patchsoutservers()
                    Deleterealservers()
                    print("your script executed sucessfully")
            else:
                print("your script executed successfully")
                sys.exit(0)
