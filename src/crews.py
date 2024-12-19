from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from langchain_openai import ChatOpenAI
from src.tools.patent_search_tool import PatentSearchTool
from src.tools.scholar_search_tool import ScholarSearchTool
from crewai_tools import DallETool
from crewai_tools import CSVSearchTool, DOCXSearchTool, TXTSearchTool

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")
llm_2 = ChatOpenAI(temperature=0.7, model="o1-preview")
llm_3 = ChatOpenAI(temperature=0.7, model_name="gpt-4-1106-preview")

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
    def opportunities_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["opportunities_strategist"],
            llm=llm_2,
            verbose=True,
            allow_delegation=False,
            memory = True
        )
        
    @task
    def opportunities_task(self) -> Task:
        return Task(
            config = self.tasks_config["opportunities_task"],
            agent = self.opportunities_strategist(),
            
        )
        
    @crew
    def opp_spaces_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = False
        )

@CrewBase
class OpportunitiesImagesCrew:
    """Generate Opportunity Spaces Images Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def opp_images(self) -> Agent:
        return Agent(
            config=self.agents_config["opp_images"],
            llm=llm_3,
            tools = [DallETool()],
            verbose=True,
            allow_delegation=False,
            memory = True
        )
        
    @task
    def opportunities_task(self) -> Task:
        return Task(
            config = self.tasks_config["opp_image_task"],
            agent = self.opp_images(),
            
        )
        
    @crew
    def opp_images_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = False
        )

@CrewBase
class DocAnalystCrew:
    """Generate Opportunity Spaces Images Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def doc_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["doc_analyst"],
            llm=llm_3,
            tools = [CSVSearchTool(),DOCXSearchTool(),TXTSearchTool()],
            verbose=True,
            allow_delegation=False,
            memory = True
        )
        
    @task
    def doc_analyst_task(self) -> Task:
        return Task(
            config = self.tasks_config["doc_analyst_task"],
            agent = self.doc_analyst(),
            
        )
        
    @crew
    def doc_analyst_crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            memory = False
        )