from interpreter import Interpreter

Interpreter()

from browser import bind, document, websocket, html
from browser.widgets.dialog import InfoDialog


def on_open():
    # document['sendbtn'].disabled = False
    # document['closebtn'].disabled = False
    # document['openbtn'].disabled = True
    InfoDialog("websocket", f"Connection open")    

def on_message(evt):
    # message received from server
    InfoDialog("websocket", f"Message received : {evt.data}")

def on_close():
    # websocket is closed
    InfoDialog("websocket", "Connection is closed")
    # document['openbtn'].disabled = False
    # document['closebtn'].disabled = True
    # document['sendbtn'].disabled = True
    
def on_error():
    # websocket is closed
    InfoDialog("websocket", f"Error: {evt.data}")

document <= html.BUTTON(id='btn')
    
ws = None
@bind("#btn", 'click')
def _open(ev):
    if not websocket.supported:
        InfoDialog("websocket", "WebSocket is not supported by your browser")
        return
    global ws
    # open a web socket
    if ws is not None:
        # return
        ws = websocket.WebSocket("ws://127.0.0.1:5000/ws/console")
        # bind functions to web socket events
        ws.bind('open',on_open)
        ws.bind('message',on_message)
        ws.bind('close',on_close)
        ws.bind('error',on_error)
    
    ws.send("hola")

# @bind('#sendbtn', 'click')
# def send(ev):
    # data = document["data"].value
    # if data:
        # ws.send(data)

# _open(None)