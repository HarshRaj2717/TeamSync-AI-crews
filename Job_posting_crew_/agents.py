import os

from crewai import Agent
from crewai_tools.tools import SerperDevTool, FileReadTool
from langchain_groq import ChatGroq

seper_dev_tool = SerperDevTool()
file_read_tool = FileReadTool(
	file_path='job_description_example.md',
	description='A tool to read the job description example file.'
)

class Agents():
	def __init__(self):
		self.llm = ChatGroq(
			api_key = os.getenv("GROQ_API_KEY"),
			model = "mixtral-8x7b-32768"
		)

	def research_agent(self):
		return Agent(
			role='Research Analyst',
			goal='Analyze the company website and provided description to extract insights on culture, values, and specific needs.',
			tools=[seper_dev_tool],
			backstory='Expert in analyzing company cultures and identifying key values and needs from various sources, including websites and brief descriptions.',
			llm = self.llm,
			max_iter = 2,
			verbose=True
		)

	def writer_agent(self):
			return Agent(
				role='Job Description Writer',
				goal='Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting.',
				tools=[seper_dev_tool, file_read_tool],
				backstory='Skilled in crafting compelling job descriptions that resonate with the company\'s values and attract the right candidates.',
				llm = self.llm,
				max_iter = 2,
				verbose=True
			)

	def review_agent(self):
			return Agent(
				role='Review and Editing Specialist',
				goal='Review the job posting for clarity, engagement, grammatical accuracy, and alignment with company values and refine it to ensure perfection.',
				tools=[seper_dev_tool, file_read_tool],
				backstory='A meticulous editor with an eye for detail, ensuring every piece of content is clear, engaging, and grammatically perfect.',
				llm = self.llm,
				max_iter = 2,
				verbose=True
			)
