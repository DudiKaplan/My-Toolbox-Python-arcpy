import json
import urllib
import urllib2

def gentoken(url, username, password, expiration=60):
    query_dict = {'username':   username,
                  'password':   password,
                  'expiration': str(expiration),
                  'client':     'requestip'}
    query_string = urllib.urlencode(query_dict)
    return json.loads(urllib.urlopen(url + "?f=json", query_string).read())['token']

def deleteservice(server, servicename, username, password, token=None, port=6080):
    if token is None:
        token_url = "http://{}/arcgis/tokens/?request=gettoken&username={}&password={}".format(server,username,password)
        token = gentoken(token_url, username, password)
    delete_service_url = "http://{}:{}/arcgis/admin/services/{}/delete?token={}".format(server, port, servicename, token)
    urllib2.urlopen(delete_service_url, ' ').read() # The ' ' forces POST

#server = "10.237.72.50"
#servicename = "Taibe_Main.MapServer"
#username = "comploteditor"
#password = "Eunpkuy123"
# if you need a token, execute this line:
#deleteservice('10.237.72.50', 'Taibe_Main.MapServer', 'comploteditor', 'Eunpkuy123')

#deleteservice("10.237.72.50", "Taibe_Main.MapServer", None, None, token='0qhKTEGEK97XKECx2MfIAIJyFHKANuP5O39N93D_Sgo.')



deleteservice("<10.237.72.50>", "<Taibe_Main>.MapServer", "<comploteditor>", "<Eunpkuy123>")
