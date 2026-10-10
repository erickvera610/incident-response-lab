"""HTTP integration checks against a temporary SQLite database."""
import unittest,subprocess,tempfile,socket,os,json,urllib.request,urllib.error
from pathlib import Path
class HttpTests(unittest.TestCase):
 def test_persistence_endpoint_and_conflict(self):
  with tempfile.TemporaryDirectory() as tmp:
   with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
   env={**os.environ,'PORT':str(port),'INCIDENT_DB':str(Path(tmp)/'api.db')}
   server=subprocess.Popen(['python','app.py'],cwd=Path(__file__).parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
   try:
    self.assertIn('Open http',server.stdout.readline())
    def call(path,p=None):
     request=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=json.dumps(p).encode() if p else None,headers={'Content-Type':'application/json'})
     try:
      with urllib.request.urlopen(request,timeout=3) as response:return response.status,json.load(response)
     except urllib.error.HTTPError as response:return response.code,json.load(response)
    status,r=call('/api/incidents',{'title':'Fictional API outage','service':'API','severity':'High'});self.assertEqual(status,201)
    payload={'id':r['id'],'state':'Investigating','version':1,'request_key':'first'}
    self.assertEqual(call('/api/events',payload)[0],200);self.assertEqual(call('/api/events',payload)[0],200)
    self.assertEqual(call('/api/events',{**payload,'state':'Resolved','request_key':'stale'})[0],409)
    self.assertEqual(len(call('/api/incidents')[1]['incidents'][0]['history']),2)
   finally:
    server.terminate();server.communicate(timeout=3)
