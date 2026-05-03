"""
WebSocket handlers for real-time patient monitoring
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: dict = {}
    
    async def connect(self, websocket: WebSocket, patient_id: str):
        await websocket.accept()
        if patient_id not in self.active_connections:
            self.active_connections[patient_id] = []
        self.active_connections[patient_id].append(websocket)
        logger.info(f"Patient {patient_id} connected")
    
    def disconnect(self, patient_id: str, websocket: WebSocket):
        if patient_id in self.active_connections:
            self.active_connections[patient_id].remove(websocket)
            if not self.active_connections[patient_id]:
                del self.active_connections[patient_id]
        logger.info(f"Patient {patient_id} disconnected")
    
    async def broadcast(self, patient_id: str, message: dict):
        if patient_id in self.active_connections:
            for connection in self.active_connections[patient_id]:
                await connection.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/patient/{patient_id}")
async def websocket_endpoint(websocket: WebSocket, patient_id: str):
    """WebSocket endpoint for real-time patient monitoring"""
    await manager.connect(websocket, patient_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Echo back the data
            await websocket.send_json({"patient_id": patient_id, "data": data})
    except WebSocketDisconnect:
        manager.disconnect(patient_id, websocket)
    except Exception as e:
        logger.error(f"WebSocket error for patient {patient_id}: {e}")
        manager.disconnect(patient_id, websocket)
