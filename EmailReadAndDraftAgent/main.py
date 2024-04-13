from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from EmailReadAndDraftAgent.src.graph import WorkFlow

import asyncio

from typing import List
import json

async def run():
    app = FastAPI()

    class EmailInput(BaseModel):
        emailID: str

    @app.post("/invoke_workflow/")
    def invoke_workflow(email_input: EmailInput):
        try:
            mail = email_input.emailID
            workflow_app = WorkFlow(emailID=mail).app
            workflow_app.invoke({})

            # Read the contents of output.txt
            with open('EmailReadAndDraftAgent/output.txt', 'r') as file:
                output_text = file.read()

            with open('crew.log', 'w') as file:
                logged_data = output_buffer.getvalue()
                file.write(logged_data)

            return {"message": "Workflow invoked successfully!",
                    "output_text": output_text}
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Failed to invoke workflow: {str(e)}")

    @app.get("/responses", response_model=List[List[dict]])
    async def get_emails():
        try:
            with open("EmailReadAndDraftAgent/draftResponses.json", "r") as file:
                data = json.load(file)
                return data

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")