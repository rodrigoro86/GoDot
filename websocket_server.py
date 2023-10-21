from fastapi import FastAPI, WebSocket
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError
import json

app = FastAPI()

# Esta lista armazenará todas as conexões WebSocket ativas
websockets_connections = []

postion_airplane = None

@app.get("/")
def read_text():
    global postion_airplane
    text = f"{postion_airplane}"
    return {"text": text}


# Rota WebSocket que envia dados recebidos via POST de volta para o cliente
@app.websocket("/ws_text")
async def websocket_endpoint(websocket: WebSocket):
    global postion_airplane
    await websocket.accept()
    websockets_connections.append(websocket)  # Armazena a conexão na lista
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            print(data)

            await websocket.send_text(json.dumps(data))


    except websockets.exceptions.ConnectionClosed:
        websockets_connections.remove(websocket)
    except:
        websockets_connections.remove(websocket)
        print(websockets_connections)


# Rota WebSocket que envia dados recebidos via POST de volta para o cliente
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global postion_airplane
    await websocket.accept()
    websockets_connections.append(websocket)  # Armazena a conexão na lista

    try:
        while True:
            print(await websocket.receive_text())
            data = await websocket.receive_bytes()
            # Decodificar os dados binários para uma string
            json_str = data.decode('utf-8')

            # Analisar a string JSON para obter o dicionário
            parsed_dict = json.loads(json_str)
            #print(parsed_dict['key1'])
            postion_airplane = parsed_dict['key1']
            #await websocket.send_bytes(f"Client #{data} says: ")
            # Processa os dados recebidos, se necessário
    except websockets.exceptions.ConnectionClosed:
        # Remove a conexão da lista quando o cliente se desconecta
        websockets_connections.remove(websocket)
    except:
        # Remove a conexão da lista quando o cliente se desconecta
        websockets_connections.remove(websocket)
        print(websockets_connections)

# Rota POST para receber dados e encaminhar para as conexões WebSocket
@app.post("/send_data/")
async def send_data(data: str):
    print(data)
    for connection in websockets_connections:
        await connection.send_text(data)


    return {"message": "Data sent to connected WebSocket clients"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test:app", host="0.0.0.0", port=8000, reload=True)