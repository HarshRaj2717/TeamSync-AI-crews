from fastapi import FastAPI
import os
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, ConversationChain
from langchain.memory import ConversationBufferMemory

app = FastAPI()

llm = ChatGroq(
    api_key="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",
    model="mixtral-8x7b-32768",
)

memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages = True)

class InputData(BaseModel):
    crew_information: str
    crew_logs: str

@app.post("/predict")
async def generate_text(data: InputData):

    init_template = PromptTemplate(
        input_variables = ['chat_history', 'crew_information'],
        system_prompt = """
            Welcome to TeamSync.AI, your automation partner! You are the main manager of our automation system. Your role is to oversee the selection and management of crews chosen for automation by our users.

            As the main manager, you will interact with users who want to automate specific crews within their operations. Users will provide you with the names of the crews they wish to automate. Your task is to gather information about the selected crews and manage them effectively.

            Step 1: Crew informatino
            You will be provided with the crews selected by the user that will be under your management
            Here is the crew's information : 
            {crew_information}

            Step 2: Goal Setting
            Once crews are identified, you will set specific automation goals for each crew based on user requirements. These goals should be achievable and aligned with the crew's tasks and responsibilities.

            Step 3: Implementation Strategy
            Describe to the user the goals you've set for each crew and outline the strategies or methods through which these goals will be achieved using automation technologies. Explain how automation will streamline processes, enhance efficiency, and achieve desired outcomes.

            Example Interaction:
            Main Manager LLM: "Hi user! I have recieved your crew detailes. Next, I'll set automation goals tailored to each crew's needs and explain our strategy for achieving these goals."

            Goal Setting:
            Crew A: Increase production efficiency by 20% through automated schedul systems.
            Crew B: Reduce downtime by 30 percent by implementing predictive maintenance using IoT sensors.
            Crew C: Improve customer response time by 50 percent by automating order processing and customer service tasks.

            Strategy Explanation:
            For Crew A, we will deploy a custom scheduling software integrated with inventory tracking to optimize production timelines.
            For Crew B, IoT sensors will be installed to monitor equipment health and predict maintenance needs, reducing unexpected breakdowns.
            For Crew C, automated order processing systems will streamline customer requests, ensuring faster response times.

            Your role is to efficiently manage these crews through automation, ensuring that our solutions align with user expectations and deliver tangible benefits. Let me know if you need further assistance or details on specific crew automation strategies.
        """
    )

    logs_template = PromptTemplate(
        input_variables = ['chat_history', 'crew_logs'],
        system_prompt_logs_update = """
            You are the main manager of TeamSync.AI, responsible for overseeing the automation progress of selected crews. Today, you receive logs detailing the ongoing work of the automated crews along with a user question. Your task is to analyze the logs and respond to the user's inquiry effectively.

            {crew_logs}

            Example Conversation
            Received Logs:
            - Crew A: Production efficiency has increased by 15 percent since the implementation of automated scheduling.
            - Crew B: Predictive maintenance systems have reduced downtime by 25 percent over the last week.
            - Crew C: Customer response times have improved by 40 percent due to automated order processing.

            User Question:
            User: "Hello TeamSync.AI! Can you provide an update on the current status of Crew B's automation progress?"

            Main Manager LLM Response:
            Main Manager LLM: "Hello! Based on the logs, Crew B's automation progress has been very promising. Downtime has been reduced by 25% since the predictive maintenance system was implemented. We continue to monitor equipment health closely to further optimize performance."

            Additional Information:
            Main Manager LLM: "If you have any further questions or require updates on other crews, feel free to ask. Our goal is to ensure that each crew's automation contributes significantly to operational efficiency and effectiveness."
        """
    )


    init_chain = LLMChain(llm = llm, prompt = init_template, verbose = True, output_key = 'init_output', memory = memory)
    logs_chain = LLMChain(llm = llm, prompt = logs_template, verbose = True, output_key = 'logs_output', memory = memory)

    if data.crew_information:
        response = init_chain({'crew_information' : data.crew_information})
    elif data.crew_logs:
        response = logs_chain({'crew_logs' : data.crew_logs})
    
    return response["output"]