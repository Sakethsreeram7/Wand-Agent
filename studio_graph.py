from dotenv import load_dotenv
from app.agent.agentic_workflow import GraphBuilder

# Load environment variables from .env
load_dotenv()

graph = GraphBuilder()()
