from dotenv import load_dotenv

import asyncio

import os

from textwrap import dedent
from crewai import Agent, Crew
from langchain_groq import ChatGroq

from crewai import Process
from InstagramCrew.tasks import MarketingAnalysisTasks
from InstagramCrew.agents import MarketingAnalysisAgents


async def run():
    load_dotenv()
    tasks = MarketingAnalysisTasks()
    agents = MarketingAnalysisAgents()

    manager = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="mixtral-8x7b-32768",
    )

    # TODO hardcoded
    print("## Welcome to the marketing Crew")
    print("-------------------------------")
    product_website = "https://devfolio.co"
    product_details = "Devfolio is a platform that hosts hackathons and provides tools for developers to showcase their projects, collaborate with others, and find opportunities. It's popular among the developer community for its user-friendly interface and the wide range of hackathons it hosts, covering various themes and technologies. Devfolio also offers features for organizers to manage their hackathons effectively, including participant registration, project submission, judging, and prizes. Overall, it's a hub for developers to engage in coding challenges, build innovative projects, and network with like-minded individuals."

    # Create Agents
    product_competitor_agent = agents.product_competitor_agent()
    strategy_planner_agent = agents.strategy_planner_agent()
    creative_agent = agents.creative_content_creator_agent()
    # Create Tasks
    website_analysis = tasks.product_analysis(
        product_competitor_agent, product_website, product_details
    )
    market_analysis = tasks.competitor_analysis(
        product_competitor_agent, product_website, product_details
    )
    campaign_development = tasks.campaign_development(
        strategy_planner_agent, product_website, product_details
    )
    write_copy = tasks.instagram_ad_copy(creative_agent)

    # Create Crew responsible for Copy
    copy_crew = Crew(
        agents=[product_competitor_agent, strategy_planner_agent, creative_agent],
        tasks=[website_analysis, market_analysis, campaign_development, write_copy],
        verbose=True,
        process=Process.hierarchical,
        manager_llm=manager,
        output_log_file=True,
    )

    ad_copy = copy_crew.kickoff()

    # Create Crew responsible for Image
    senior_photographer = agents.senior_photographer_agent()
    chief_creative_diretor = agents.chief_creative_diretor_agent()
    # Create Tasks for Image
    take_photo = tasks.take_photograph_task(
        senior_photographer, ad_copy, product_website, product_details
    )
    approve_photo = tasks.review_photo(
        chief_creative_diretor, product_website, product_details
    )

    image_crew = Crew(
        agents=[senior_photographer, chief_creative_diretor],
        tasks=[take_photo, approve_photo],
        verbose=True,
    )

    image = image_crew.kickoff()

    # Print results
    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("Your post copy:")
    print(ad_copy)
    print("'\n\nYour midjourney description:")
    print(image)
