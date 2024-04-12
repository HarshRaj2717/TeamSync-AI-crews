from fastapi import FastAPI, HTTPException

from typing import List
import json

app = FastAPI()

# Email Read and Draft Agent
@app.get("/email_draft_responses", response_model=List[List[dict]])
async def get_emails():
    try:
        with open("EmailReadAndDraftAgent/draftResponses.json", "r") as file:
            data = json.load(file)
            return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")


# Meeting Planner Agent
@app.get("/meeting_summary")
async def get_meeting_summary():
    try:
        # Read the contents of output.txt
        with open("MeetingPlannerCrew/meeting_brief.txt", 'r') as file:
            output_text = file.read()

        return {"message": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    

# @app.get("/meeting_strategy")
# async def get_meeting_strategy():
#     try:
#         # Read the contents of output.txt
#         with open("MeetingPlannerCrew/meeting_strategy.txt", 'r') as file:
#             output_text = file.read()

#         return {"message": output_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    

# @app.get("/industry_analysis")
# async def get_industry_analysis():
#     try:
#         # Read the contents of output.txt
#         with open("MeetingPlannerCrew/industry_analysis.txt", 'r') as file:
#             output_text = file.read()

#         return {"message": output_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    


# Instagram Crew
@app.get("/product_competitors")
async def get_product_competitors():
    try:
        # Read the contents of output.txt
        with open("InstagramCrew/competitor_analysis.txt", 'r') as file:
            output_text = file.read()

        return {"message": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    

@app.get("/product_analysis")
async def get_product_analysis():
    try:
        # Read the contents of output.txt
        with open("InstagramCrew/product_analysis.txt", 'r') as file:
            output_text = file.read()

        return {"message": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    

@app.get("/product_campaign")
async def get_product_campaign():
    try:
        # Read the contents of output.txt
        with open("InstagramCrew/campaign.txt", 'r') as file:
            output_text = file.read()

        return {"message": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    

@app.get("/product_ad")
async def get_product_ad():
    try:
        # Read the contents of output.txt
        with open("InstagramCrew/instagram_ad.txt", 'r') as file:
            output_text = file.read()

        return {"message": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    

@app.get("/photo_review")
async def get_photo_review():
    try:
        # Read the contents of output.txt
        with open("InstagramCrew/photo_prompts.txt", 'r') as file:
            output_text = file.read()

        return {"message": output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke workflow: {str(e)}")    


# Job Posting Crew


# Cold Email Agent

