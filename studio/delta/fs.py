import json,os,time,jwt,urllib.request,sys
sa=json.loads(os.environ['FIREBASE_SERVICE_ACCOUNT'])
def token():
    now=int(time.time())
    a=jwt.encode({"iss":sa["client_email"],"scope":"https://www.googleapis.com/auth/datastore","aud":"https://oauth2.googleapis.com/token","iat":now,"exp":now+3600},sa["private_key"],algorithm="RS256")
    r=urllib.request.urlopen("https://oauth2.googleapis.com/token",data=("grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion="+a).encode())
    return json.load(r)["access_token"]
URL=f"https://firestore.googleapis.com/v1/projects/{sa['project_id']}/databases/(default)/documents/data/stats"
def get():
    r=urllib.request.urlopen(urllib.request.Request(URL,headers={"Authorization":"Bearer "+token()}))
    return json.load(r)
if __name__=="__main__":
    doc=get(); f=doc["fields"]
    print({k:(v.get("stringValue","")[:80] if k!="json" else len(v["stringValue"])) for k,v in f.items()}, doc.get("updateTime"))
    open(sys.argv[1],"w").write(f["json"]["stringValue"])
