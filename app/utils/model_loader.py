import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from .config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["google", "groq", "openai"] = "google"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model with fallback support.
        Google Generative AI is the default, with Groq as fallback.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        
        # Try Google Generative AI first (default)
        if self.model_provider == "google":
            try:
                print("Loading LLM from Google Generative AI..............")
                google_api_key = os.getenv("GOOGLE_API_KEY")
                if not google_api_key:
                    raise ValueError("GOOGLE_API_KEY not found in environment variables")
                
                model_name = self.config["llm"]["google"]["model_name"]
                llm = ChatGoogleGenerativeAI(
                    model=model_name, 
                    google_api_key=google_api_key,
                    temperature=0.7
                )
                print("✅ Google Generative AI loaded successfully")
                return llm
                
            except Exception as e:
                print(f"❌ Failed to load Google Generative AI: {str(e)}")
                print("🔄 Falling back to Groq...")
                return self._load_fallback_groq()
        
        # Groq provider
        elif self.model_provider == "groq":
            return self._load_groq()
        
        # OpenAI provider
        elif self.model_provider == "openai":
            return self._load_openai()
        
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
    
    def _load_groq(self):
        """Load Groq LLM"""
        try:
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(model=model_name, api_key=groq_api_key)
            print("✅ Groq LLM loaded successfully")
            return llm
        except Exception as e:
            print(f"❌ Failed to load Groq: {str(e)}")
            raise
    
    def _load_fallback_groq(self):
        """Load Groq as fallback when Google fails"""
        try:
            return self._load_groq()
        except Exception as e:
            print(f"❌ Fallback to Groq also failed: {str(e)}")
            print("💡 Please ensure either GOOGLE_API_KEY or GROQ_API_KEY is set in your environment")
            raise ValueError("Both Google Generative AI and Groq fallback failed to load")
    
    def _load_openai(self):
        """Load OpenAI LLM"""
        try:
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model=model_name, api_key=openai_api_key)
            print("✅ OpenAI LLM loaded successfully")
            return llm
        except Exception as e:
            print(f"❌ Failed to load OpenAI: {str(e)}")
            raise
