from pushbullet.pushbullet import Pushbullet
#import wolframalpha
import json
import tungsten

pb = Pushbullet(api_key="PUSHBULLET_API_KEY")

wolf_api = "WOLFRAMALPHA_API_KEY"
#client = wolframalpha.Client(wolf_api)
client = tungsten.Tungsten(wolf_api)
pushes = pb.get_pushes()

f=open("sent.json")
sent = json.loads(f.read())
f.close()

for push in pushes:
   if 'body' in push.keys() and push['body'].startswith('Hey Jarvis') and push['iden'] not in sent:
    try:
      sent.append(push['iden'])
      res = client.query(push['body'][11:])
      if res.success:
        print "Success"
        print [pod.format['plaintext'][0] for pod in res.pods]
        results = [pod.format['plaintext'][0] for pod in res.pods if type(pod.format['plaintext'][0]) is not None]
        if len(results) != 0:
          pb.push_note(title=push['body'][11:],body='\n\n'.join(results[:5]))
        else:
          pb.push_note(title=push['body'][11:],body="I cannot answer this.")
      else:
        print "Query failed"
        pb.push_note(title=push['body'][11:], body= "Query Failed. :-(")
    except:
      pb.push_note(title=push['body'][11:], body= "Something went wrong.")
f=open("sent.json","w")
f.write(json.dumps(sent))
f.close()
