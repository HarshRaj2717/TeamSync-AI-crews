import os
import time
import csv
from crewai import Crew
from langchain_groq import ChatGroq
from ColdEmailAgent.agents import EmailPersonalizationAgents
from ColdEmailAgent.tasks import PersonalizeEmailTask

import asyncio

# 0. Setup environment
from dotenv import load_dotenv

async def run():
    load_dotenv()

    email_template = """
    Dear [Name],

    Allow me to introduce InnoVest - a game-changing platform designed to revolutionize the startup ecosystem. Our comprehensive solution offers:

    A Startup Marketplace to buy/sell startups or equity; Shark Tank competitions for live investor pitching; AI Idea Evaluation to refine pitches and value ideas; Business Knowledge chatbot for entrepreneurial guidance; and an Idea Showcase to connect with investors/collaborators.

    InnoVest empowers entrepreneurs at every stage - from ideation to funding to business growth. Our suite of tools addresses key challenges faced by startups. I'd be delighted to discuss how we can support your entrepreneurial journey and provide a personalized demo.

    Please let me know if you'd like to explore partnering with InnoVest. I look forward to the opportunity.

    Best regards,
    HR Manager
    InnoVest
    """

    # 1. Create agents
    agents = EmailPersonalizationAgents()

    email_personalizer = agents.personalize_email_agent()
    ghostwriter = agents.ghostwriter_agent()

    # 2. Create tasks
    tasks = PersonalizeEmailTask()

    personalize_email_tasks = []
    ghostwrite_email_tasks = []

    # Path to the CSV file containing client information
    csv_file_path = "ColdEmailAgent/data/clients.csv"

    # Open the CSV file
    with open(csv_file_path, mode="r", newline="") as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Access each field in the row
            recipient = {
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "bio": row["bio"],
            }

            # Create a personalize_email task for each recipient
            _personalize_email_task = tasks.personalize_email(
                agent=email_personalizer, recipient=recipient, email_template=email_template
            )

            # Create a ghostwrite_email task for each recipient
            _ghostwrite_email_task = tasks.ghostwrite_email(
                agent=ghostwriter, draft_email=_personalize_email_task, recipient=recipient
            )

            # Add the task to the crew
            personalize_email_tasks.append(_personalize_email_task)
            ghostwrite_email_tasks.append(_ghostwrite_email_task)


    # Setup Crew
    crew = Crew(
        agents=[email_personalizer, ghostwriter],
        tasks=[*personalize_email_tasks, *ghostwrite_email_tasks],
        max_rpm=29,
        output_log_file=True,
    )

    # Kick off the crew
    start_time = time.time()

    results = crew.kickoff()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Crew kickoff took {elapsed_time} seconds.")
    # print("Crew usage", crew.usage_metrics)
