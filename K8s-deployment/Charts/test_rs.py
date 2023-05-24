import re
import requests,json,time
from requests.structures import CaseInsensitiveDict
import pytest

def token(clientId,clientSecret,data,url):
        print("Retrieving Token", end="")
        headers = CaseInsensitiveDict()
        headers["clientId"] = clientId
        headers["clientSecret"] = clientSecret
        headers["Content-Type"] = "application/json"
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        json_object = json.loads(resp.text)
        print("   Done")
        return (json_object["results"]["accessToken"])

def request(request_method,Api_Token,Api_Url,info,files,name):

        headers = CaseInsensitiveDict()
        headers["token"] = Api_Token
        headers["Content"] = "application/json"
        resp = requests.request(request_method,Api_Url, headers=headers, data=info,files=files, verify=False)
        return (resp)


## @pytest.mark.parametrize("server", ["REDIS","ES","PSQL", "ImmuDB"])


server= ["REDIS","ES","PSQL", "ImmuDB"]

@pytest.mark.parametrize("server", server)
def test_rs(config, server):
    for info in config["Info"]["RS"]:
        if info["Test-Name"]== server:
            if info["Type"] == "private":
                auth_token = token(config["clientID"],config["clientSecret"],info["Auth-Request-Body"],config["Auth-Server-Url"])
                req = request(info["Request-Method"],str(auth_token),info["Server-Url"],info["Request-Body"],"",info["Test-Name"]) 
                print(req)
                status_code = str(req.status_code)
            elif info["Type"] == "array_check":
                req = request(info["Request-Method"],"",info["Server-Url"],info["Request-Body"],"",info["Test-Name"])
                json_object = json.loads(req.text)
                # If results array is empty, set status code to 204
                if req.status_code == 200 and  len(json_object["results"]) == 0:
                    status_code = "204", "results array is empty"
                else:
                    status_code = str(req.status_code)
                                
            else:
                req = request(info["Request-Method"],"",info["Server-Url"],info["Request-Body"],"",info["Test-Name"])
                status_code = str(req.status_code)
            assert status_code == "200"