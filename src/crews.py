from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from datetime import datetime
from langchain_openai import ChatOpenAI
from src.tools.patent_search_tool import PatentSearchTool
from src.tools.new_search_tool import NewsSearchTool
from src.tools.scholar_search_tool import ScholarSearchTool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

# Building Crews
@CrewBase
class PatentCrew:
    """Patent Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    

    @agent
    def strategist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["strategist"],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )

    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )
    
    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["writer"],
            llm = llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )
        
    @task
    def generate_queries_task(self) -> Task:
        return Task(
            config = self.tasks_config["generate_queries_task"],
            agent = self.strategist_agent()
        )
    
    @task 
    def patent_search_task(self) -> Task:
        return Task(
            config = self.tasks_config["patent_search_task"],
            agent = self.researcher_agent(),
            tools = [PatentSearchTool()]
        )
        
    @task
    def select_patents_task(self) -> Task:
        return Task(
            config = self.tasks_config["select_patents_task"],
            agent = self.strategist_agent()
        )
        
    @task
    def summarize_task(self) -> Task:
        return Task(
            config = self.tasks_config["summarize_task"],
            agent = self.writer_agent()
        )
    
    @crew
    def patent_crew(self) -> Crew:
        """Creates the Stock Analysis"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = False
        )
        
@CrewBase
class ScholarCrew:
    """Scholar Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def strategist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["strategist"],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )

    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )
    
    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config = self.agents_config["writer"],
            llm = llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )
        
    @task
    def generate_queries_task(self) -> Task:
        return Task(
            config = self.tasks_config["generate_queries_task"],
            agent = self.strategist_agent()
        )
    
    @task 
    def scholar_search_task(self) -> Task:
        return Task(
            config = self.tasks_config["scholar_search_task"],
            agent = self.researcher_agent(),
            tools = [ScholarSearchTool()]
        )
        
    @task
    def select_papers_task(self) -> Task:
        return Task(
            config = self.tasks_config["select_papers_task"],
            agent = self.strategist_agent()
        )
    
    @task
    def summarize_task(self) -> Task:
        return Task(
            config = self.tasks_config["summarize_task"],
            agent = self.writer_agent()
        )
    
    @crew
    def scholar_crew(self) -> Crew:
        """Creates the Stock Analysis"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = False,
            output_name='scholar_output'
        )
        
@CrewBase
class InsightsCrew:
    """Generate Insights Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def insight_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["insight_agent"],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )
        
    @task
    def insight_task(self) -> Task:
        return Task(
            config = self.tasks_config["insight_task"],
            agent = self.insight_agent(),
            
        )
        
    @crew
    def insights_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = False
        )

@CrewBase
class OpportunitiesCrew:
    """Generate Opportunity Spaces Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def insight_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["insight_agent"],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            memory = True
        )
        
    @task
    def insight_task(self) -> Task:
        return Task(
            config = self.tasks_config["insight_task"],
            agent = self.insight_agent(),
            
        )
        
    @crew
    def insights_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = False
        )