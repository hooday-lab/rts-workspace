import json,sys,urllib.request,datetime
sys.path.insert(0,sys.argv[1]); import fs
def put(path,js,by):
    body={"fields":{"json":{"stringValue":js},"uploadedAt":{"stringValue":datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.000Z')},"by":{"stringValue":by}}}
    url=fs.URL.rsplit('/data/stats',1)[0]+'/'+path
    req=urllib.request.Request(url,data=json.dumps(body).encode(),method='PATCH',headers={"Authorization":"Bearer "+fs.token(),"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(req))["updateTime"]
S=sys.argv[1]
print('backup', put('data/stats_backup_k10', open(S+'/stats_k10.json').read(), 'claude (kopia przed K11)'))
print('stats', put('data/stats', open(S+'/stats_k11.json').read(), 'claude (delta K11, 2/9)'))
