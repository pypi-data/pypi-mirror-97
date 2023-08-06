import socket
import datetime
import requests
import json

class remoteLog():

    def get_dynamic_filename(self):
        exec("print(__file__)")

    def __init__(self,scriptname=None):
        self.scriptname = scriptname
        self.url = 'http://127.0.0.1'
        self.test = 'abced'



    def set_url(self,url):
        self.url = url

    def get_ip(self):

        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]

        finally:

            s.close()

        return ip

    def get_scriptname(self):

        return self.scriptname
    def Script_name(self):
        a=str(self.get_scriptname()).split("/")
        return a

    def log(self,url,execution_tb):
            try:
                data = {'script_update':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'ip':str(self.get_ip()),'location':self.get_scriptname(),"script_name":self.Script_name()[-1],"execution_time":execution_tb,
                        }
                data_a = json.dumps(data)
                a=requests.post(url, data_a,timeout=5)
                return ({"msg":"信息发送成功","code":0})
            except:
                return ({"msg":"信息发送失败","code":1})

def dgta(f,url_a,execution_time):
    try:
        a = remoteLog(f)
        msg=a.log(url_a, execution_time)

        return msg

    except:
        return ({"msg": "获取硬件信息失败", "code": 0})

if __name__ == '__main__':

    a=dgta(__file__,"http:219.130.112.112:8888/post_sp",60)
    print(a)





