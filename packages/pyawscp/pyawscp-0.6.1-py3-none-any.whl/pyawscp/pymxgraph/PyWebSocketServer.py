import asyncio
import datetime
import random
import websockets
import sys
import json
import signal
import sys

signal.signal(signal.SIGINT, signal.SIG_DFL)

RESET = '\033[0m'
GREEN = '\033[32m'

class WsServer:

    def __init__(self):
        print("I am listening at " + GREEN +  "ws://" + self.get_host() + ":" + self.get_port() + RESET + "...")
        self.loop = asyncio.get_event_loop()
       
    def get_port(self):
        return '5678'

    def get_host(self):
        return 'localhost'

    def init_server(self):
        return websockets.serve(self.handler, self.get_host(), self.get_port())

    def start(self):
        try:
            self.loop.run_until_complete(self.init_server())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            pass

    async def handler(self, websocket, path):
        async for message in websocket:
            print('Path: ' + path + ', Received:'+ str(message) )
            request = json.loads(message)
            if   request["action"] == "message":
               obj = {}
               obj["aws"] = {}
               obj["aws"]["message"] = request["text"] + " Pong!"
               await websocket.send(json.dumps(obj)) 
            elif request["action"] == "listVpc":  
               response = self.listVpc(request)  
               await websocket.send(json.dumps(response)) 
            elif request["action"] == "close":
               print("Closing Socket...") 
               await websocket.close()
               print("Closed!") 
               sys.exit()

    def listVpc(self,request):
         response = {}
         response["aws"] = {}
         response["aws"]["vpcs"] = []
         response["aws"]["vpcs"].append({"vpcId":"vpc-123456789"})
         response["aws"]["vpcs"].append({"vpcId":"vpc-01457"})
         response["aws"]["vpcs"].append({"vpcId":"vpc-789456"})
         return response
               
            
if __name__ == '__main__':
  ws = WsServer()
  ws.start()
  

