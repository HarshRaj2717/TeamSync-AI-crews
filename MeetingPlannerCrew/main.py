from dotenv import load_dotenv

import asyncio

from crewai import Crew

from MeetingPlannerCrew.tasks import MeetingPreparationTasks
from MeetingPlannerCrew.agents import MeetingPreparationAgents

async def run():
	load_dotenv()
	tasks = MeetingPreparationTasks()
	agents = MeetingPreparationAgents()

	print("## Welcome to the Meeting Prep Crew")
	print('-------------------------------')
	# TODO hardcoded values
	context = "We are preparing for a meeting with a potential client in the tech industry. We are looking to understand the industry trends and the client's needs to prepare for the meeting."
	objective = "Understand the industry trends and the client's needs to prepare for the meeting."

	# Create Agents
	industry_analyst_agent = agents.industry_analysis_agent()
	meeting_strategy_agent = agents.meeting_strategy_agent()
	summary_and_briefing_agent = agents.summary_and_briefing_agent()

	# Create Tasks
	industry_analysis = tasks.industry_analysis_task(industry_analyst_agent, context)
	meeting_strategy = tasks.meeting_strategy_task(meeting_strategy_agent, context, objective)
	summary_and_briefing = tasks.summary_and_briefing_task(summary_and_briefing_agent, context, objective)

	meeting_strategy.context = [industry_analysis]
	summary_and_briefing.context = [industry_analysis, meeting_strategy]

	# Create Crew responsible for Copy
	crew = Crew(
		agents=[
			industry_analyst_agent,
			meeting_strategy_agent,
			summary_and_briefing_agent
		],
		tasks=[
			industry_analysis,
			meeting_strategy,
			summary_and_briefing
		],
		output_log_file = True 
	)

	game = crew.kickoff()


	# Print results
	print("\n\n################################################")
	print("## Here is the result")
	print("################################################\n")
	print(game)
