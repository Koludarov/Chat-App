from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    """
    Класс для подключения и отключения
    пользователя к серверу по WebSocket
    """
    def __init__(self):
        """Создаёт пустой список активных подключений"""
        self.active_connections: List[WebSocket] = []

    @staticmethod
    async def send_message(message: dict, websocket: WebSocket):
        """Отправляет сообщение"""
        await websocket.send_json(message)

    async def connect(self, websocket: WebSocket):
        """
        Подключение к Websocket.
        Добавляет WS в список актиных подключений.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Отключение от Websocket.
        Удаляет WS из списка актиных подключений.
        """
        self.active_connections.remove(websocket)


manager = ConnectionManager()


@app.get("/")
async def get(request: Request):
    """Загружает основную страницу"""
    return templates.TemplateResponse("home.html", {"request": request})


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    """
    Обрабатывает подключение.
    Получает сообщение.
    Обрабатывает отсоединение от сервера WebSocket.
    """
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_message(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
