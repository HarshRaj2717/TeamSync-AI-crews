from dotenv import load_dotenv

from crewai import Crew

import asyncio

from Job_posting_crew.tasks import Tasks
from Job_posting_crew.agents import Agents


async def run():
    load_dotenv()
    tasks = Tasks()
    agents = Agents()

    # TODO hardcoded
    company_description = "Devfolio is a platform that hosts hackathons and provides tools for developers to showcase their projects, collaborate with others, and find opportunities. It's popular among the developer community for its user-friendly interface and the wide range of hackathons it hosts, covering various themes and technologies. Devfolio also offers features for organizers to manage their hackathons effectively, including participant registration, project submission, judging, and prizes. Overall, it's a hub for developers to engage in coding challenges, build innovative projects, and network with like-minded individuals."
    company_domain = "edtech"
    hiring_needs = "We are looking for a Full Stack Developer with experience in React, Node.js, and MongoDB. The ideal candidate should have a strong understanding of web development and be able to work in a fast-paced startup environment."
    specific_benefits = "We offer flexible working hours, a competitive salary, and the opportunity to work on cutting-edge technologies in the fintech industry."

    # Create Agents
    researcher_agent = agents.research_agent()
    writer_agent = agents.writer_agent()
    review_agent = agents.review_agent()

    # Define Tasks for each agent
    research_company_culture_task = tasks.research_company_culture_task(
        researcher_agent, company_description, company_domain
    )
    industry_analysis_task = tasks.industry_analysis_task(
        researcher_agent, company_domain, company_description
    )
    research_role_requirements_task = tasks.research_role_requirements_task(
        researcher_agent, hiring_needs
    )
    draft_job_posting_task = tasks.draft_job_posting_task(
        writer_agent, company_description, hiring_needs, specific_benefits
    )
    review_and_edit_job_posting_task = tasks.review_and_edit_job_posting_task(
        review_agent, hiring_needs
    )

    # Instantiate the crew with a sequential process
    crew = Crew(
        agents=[researcher_agent, writer_agent, review_agent],
        tasks=[
            research_company_culture_task,
            industry_analysis_task,
            research_role_requirements_task,
            draft_job_posting_task,
            review_and_edit_job_posting_task,
        ],
        output_log_file=True,
    )

    # Kick off the process
    result = crew.kickoff()

    print("Job Posting Creation Process Completed.")
    print("Final Job Posting:")
    print(result)
