import logging
import time

import requests

from app.core.config import settings

logger = logging.getLogger("vapi")


class VapiHandler:
    """
    this method handle communicating with various payment gateways
    """

    def __init__(self):
        self.public_key = settings.VAPI_API_PUBLIC_KEY
        self.secret_key = settings.VAPI_API_PRIVATE_KEY
        self.context = {}

    def get_header(self):
        return {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.secret_key}",
        }

    async def get_call_details(self, call_id: str) -> dict:
        url = f"https://api.vapi.ai.call/{call_id}"

        counter = 1
        status = True
        context = {"status": False}
        while status:
            response = requests.get(url, headers=self.get_header())
            result = response.json()
            if result["status"] in ["ended"]:
                data = {
                    "id": result["id"],
                    "createdAt": result["createdAt"],
                    "updatedAt": result["updatedAt"],
                    "type": result["type"],
                    "status": result["status"],
                    "startedAt": result["startedAt"],
                    "endedAt": result["endedAt"],
                    "analysis": result["analysis"],
                    "transcript": result["transcript"],
                    "assistantId": result["assistantId"],
                }
                context.update({"data": data, "status": True})
                break
            if counter == 3:
                break
            counter = counter + 1
            time.sleep(3)
        return context


vapi_handler = VapiHandler()
