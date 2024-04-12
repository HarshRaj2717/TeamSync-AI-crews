from crewai import Task
from textwrap import dedent

class EmailFilterTasks:
	def filter_emails_task(self, agent, emails):
		return Task(
			description=dedent(f"""\
				Analyze a batch of emails and filter out
				non-essential ones such as newsletters, promotional content and notifications.

			    Use your expertise in email content analysis to distinguish
				important emails from the rest, pay attention to the sender and avoind invalid emails.

				Make sure to filter for the messages actually directed at the user and avoid notifications.

				EMAILS
				-------
				{emails}

				Your final answer MUST be a the relevant thread_ids and the sender, use bullet points.
				"""),
			agent=agent,
			expected_output = "relevant thread_ids and the sender",
			output_file = "filterEmails.txt"
		)

	def action_required_emails_task(self, agent):
		return Task(
			description=dedent("""\
				For each email thread, pull and analyze the complete threads using only the actual Thread ID.
				understand the context, key points, and the overall sentiment
				of the conversation.

				Identify the main query or concerns that needs to be
				addressed in the response for each

				Your final answer MUST be a list for all emails with:
				- the thread_id
				- a summary of the email thread
				- a highlighting with the main points
				- identify the user and who he will be answering to
				- communication style in the thread
				- the sender's email address
				"""),
			agent=agent,
			expected_output = """
				Your final answer MUST be a list for all emails with:
				- the thread_id
				- a summary of the email thread
				- a highlighting with the main points
				- identify the user and who he will be answering to
				- communication style in the thread
				- the sender's email address
				""",
			output_file = "actionRequiredEmails.json"
		)

	def draft_responses_task(self, agent):
		return Task(
			description=dedent(f"""\
				Based on the action-required emails identified, draft responses for each.
				Ensure that each response is tailored to address the specific needs
				and context outlined in the email.

				- Assume the persona of the user and mimic the communication style in the thread.
				- Feel free to do research on the topic to provide a more detailed response, IF NECESSARY.
				- IF a research is necessary do it BEFORE drafting the response.
				- If you need to pull the thread again do it using only the actual Thread ID.

				Use the tool provided to draft each of the responses in JSON with all relevant fields (sender, to, subject, message).
				When using the tool pass the following input:
				- to (sender to be responded)
				- subject
				- message

				You MUST create draft response with relevant fields in JSON then final response with same fields in JSON.
				Your final answer MUST be a confirmation that all responses have been drafted and return the output JSON containing the above created draft and final created JSON.
				"""),
			agent=agent,
			expected_output = """for each mail input, there MUST be a JSON containing 2 draft JSON and 1 final JSON response in a single list from the given information. 
			For eg: Total Mails are 2, then for all the mails, 2 draft response JSON and 1 final response JSON in a single list. A list of list containing 2 drafts and 1 last response JSON for single receiver, i.e each list will have 3 JSON for single receiver. OUTPUT FORMAT: Please provide valid JSON data. Input only the JSON array containing email information.
			Consider the following layout:
			[
				[
					{"type": "Draft1",
					"to": "email1",
					"from": "email"
					"message": "body"
					},
					{"type": "Draft2",
					"to": "email1",
					"from": "email"
					"message": "body"
					},
					{"type": "Final",
					"to": "email1",
					"from": "email"
					"message": "body"
					},
				],
				[
					{"type": "Draft1",
					"to": "email2",
					"from": "email"
					"message": "body"
					},
					{"type": "Draft2",
					"to": "email2",
					"from": "email"
					"message": "body"
					},
					{"type": "Final",
					"to": "email2",
					"from": "email"
					"message": "body"
					},
				],
				....
				[
					{},
					{},
					{}
				]
			]
			""",
			output_file = "draftResponses.json"
		)