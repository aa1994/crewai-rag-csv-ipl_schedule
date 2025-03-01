from crewai import Agent, LLM, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from pydantic import BaseModel

import os
import dotenv

#JSON Response as a Pydantic model
class CrewResponse(BaseModel):
    answer_response: str


@CrewBase
class IPLCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    #load .env values
    dotenv.load_dotenv()

    GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")

    llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=GOOGLE_API_KEY
    )

    csv_search_tool = CSVSearchTool(
        csv="IPL_Schedule.csv",
        name="IPL Scheduler search tool",
        verbose=True,
        description="A tool that takes input from the user and looks at the IPL_Schedule.csv to answer questions",
        config=dict(
            llm=dict(
                provider="google",
                config=dict(
                    model="gemini-1.5-flash"
                ),
            ),
            embedder=dict(
                provider="google",
                config=dict(
                   model="models/text-embedding-004",
                   task_type="retrieval_document",
                   title="2025 IPL Schedule"
                ),
            ),
        )
    )


    @agent
    def schedule_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['schedule_expert'],
            llm = self.llm,
            tools=[self.csv_search_tool],
            memory=True
        )
    
    @task
    def schedule_read(self) -> Task:
        return Task(
            config=self.tasks_config['schedule_read'],
            tools=[self.csv_search_tool],
            output_json=CrewResponse
        )
    
    @crew
    def iplCrew(self) -> Crew:
        return Crew(
            tasks=self.tasks,
            agents=self.agents,
            verbose=True
)

