from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get(request: Request):
    """Загружает основную страницу"""
    return templates.TemplateResponse("home.html", {"request": request})


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    """
    Обрабатывает подключение.
    Получает сообщение в фомате JSON.
    Добавляет порядковый номер.
    Отправляет сообщение в формате JSON.
    Обрабатывает отсоединение от сервера WebSocket.
    """
    msg_id = 0
    await websocket.accept()
    try:
        while True:
            msg_id += 1
            data = await websocket.receive_json()
            data["id"] = msg_id
            print(data)
            await websocket.send_json(data)
    except WebSocketDisconnect:
        pass
