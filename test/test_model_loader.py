#!/usr/bin/env python3
"""
Test cases for the ModelLoader class with Google Generative AI and fallback functionality
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
from dotenv import load_dotenv

# Add the parent directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestModelLoader(unittest.TestCase):
    """Test cases for ModelLoader class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        load_dotenv()
    
    def setUp(self):
        """Set up each test"""
        # Store original environment variables
        self.original_google_key = os.environ.get("GOOGLE_API_KEY")
        self.original_groq_key = os.environ.get("GROQ_API_KEY")
        self.original_openai_key = os.environ.get("OPENAI_API_KEY")
    
    def tearDown(self):
        """Clean up after each test"""
        # Restore original environment variables
        if self.original_google_key:
            os.environ["GOOGLE_API_KEY"] = self.original_google_key
        elif "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
            
        if self.original_groq_key:
            os.environ["GROQ_API_KEY"] = self.original_groq_key
        elif "GROQ_API_KEY" in os.environ:
            del os.environ["GROQ_API_KEY"]
            
        if self.original_openai_key:
            os.environ["OPENAI_API_KEY"] = self.original_openai_key
        elif "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
    
    def test_model_loader_initialization(self):
        """Test ModelLoader initialization"""
        from app.utils.model_loader import ModelLoader
        
        # Test default initialization
        loader = ModelLoader()
        self.assertEqual(loader.model_provider, "google")
        
        # Test with explicit provider
        loader_groq = ModelLoader(model_provider="groq")
        self.assertEqual(loader_groq.model_provider, "groq")
        
        loader_openai = ModelLoader(model_provider="openai")
        self.assertEqual(loader_openai.model_provider, "openai")
    
    def test_config_loader_initialization(self):
        """Test that ConfigLoader is properly initialized"""
        from app.utils.model_loader import ModelLoader
        
        loader = ModelLoader()
        self.assertIsNotNone(loader.config)
        self.assertIn("llm", loader.config.config)
    
    @patch('app.utils.model_loader.ChatGoogleGenerativeAI')
    def test_google_llm_loading_success(self, mock_google_chat):
        """Test successful Google LLM loading"""
        from app.utils.model_loader import ModelLoader
        
        # Set up mock
        mock_llm = MagicMock()
        mock_google_chat.return_value = mock_llm
        
        # Set environment variable
        os.environ["GOOGLE_API_KEY"] = "test_google_key"
        
        loader = ModelLoader(model_provider="google")
        llm = loader.load_llm()
        
        # Verify Google LLM was created
        mock_google_chat.assert_called_once()
        self.assertEqual(llm, mock_llm)
    
    @patch('app.utils.model_loader.ChatGroq')
    def test_groq_llm_loading_success(self, mock_groq_chat):
        """Test successful Groq LLM loading"""
        from app.utils.model_loader import ModelLoader
        
        # Set up mock
        mock_llm = MagicMock()
        mock_groq_chat.return_value = mock_llm
        
        # Set environment variable
        os.environ["GROQ_API_KEY"] = "test_groq_key"
        
        loader = ModelLoader(model_provider="groq")
        llm = loader.load_llm()
        
        # Verify Groq LLM was created
        mock_groq_chat.assert_called_once()
        self.assertEqual(llm, mock_llm)
    
    @patch('app.utils.model_loader.ChatOpenAI')
    def test_openai_llm_loading_success(self, mock_openai_chat):
        """Test successful OpenAI LLM loading"""
        from app.utils.model_loader import ModelLoader
        
        # Set up mock
        mock_llm = MagicMock()
        mock_openai_chat.return_value = mock_llm
        
        # Set environment variable
        os.environ["OPENAI_API_KEY"] = "test_openai_key"
        
        loader = ModelLoader(model_provider="openai")
        llm = loader.load_llm()
        
        # Verify OpenAI LLM was created
        mock_openai_chat.assert_called_once()
        self.assertEqual(llm, mock_llm)
    
    def test_google_llm_loading_no_api_key(self):
        """Test Google LLM loading without API key"""
        from app.utils.model_loader import ModelLoader
        
        # Remove Google API key
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        
        # Remove Groq API key to prevent fallback
        if "GROQ_API_KEY" in os.environ:
            del os.environ["GROQ_API_KEY"]
        
        loader = ModelLoader(model_provider="google")
        
        with self.assertRaises(ValueError) as context:
            loader.load_llm()
        
        self.assertIn("Both Google Generative AI and Groq fallback failed", str(context.exception))
    
    @patch('app.utils.model_loader.ChatGroq')
    @patch('app.utils.model_loader.ChatGoogleGenerativeAI')
    def test_fallback_mechanism(self, mock_google_chat, mock_groq_chat):
        """Test fallback from Google to Groq"""
        from app.utils.model_loader import ModelLoader
        
        # Set up mocks - Google fails, Groq succeeds
        mock_google_chat.side_effect = Exception("Google API failed")
        mock_groq_llm = MagicMock()
        mock_groq_chat.return_value = mock_groq_llm
        
        # Set environment variables
        os.environ["GOOGLE_API_KEY"] = "test_google_key"
        os.environ["GROQ_API_KEY"] = "test_groq_key"
        
        loader = ModelLoader(model_provider="google")
        llm = loader.load_llm()
        
        # Verify Google was tried first, then Groq
        mock_google_chat.assert_called_once()
        mock_groq_chat.assert_called_once()
        self.assertEqual(llm, mock_groq_llm)
    
    @patch('app.utils.model_loader.ChatGroq')
    @patch('app.utils.model_loader.ChatGoogleGenerativeAI')
    def test_fallback_both_fail(self, mock_google_chat, mock_groq_chat):
        """Test when both Google and Groq fail"""
        from app.utils.model_loader import ModelLoader
        
        # Set up mocks - both fail
        mock_google_chat.side_effect = Exception("Google API failed")
        mock_groq_chat.side_effect = Exception("Groq API failed")
        
        # Set environment variables
        os.environ["GOOGLE_API_KEY"] = "test_google_key"
        os.environ["GROQ_API_KEY"] = "test_groq_key"
        
        loader = ModelLoader(model_provider="google")
        
        with self.assertRaises(ValueError) as context:
            loader.load_llm()
        
        self.assertIn("Both Google Generative AI and Groq fallback failed", str(context.exception))
    
    def test_unsupported_provider(self):
        """Test loading with unsupported provider"""
        from app.utils.model_loader import ModelLoader
        
        with self.assertRaises(ValueError) as context:
            loader = ModelLoader(model_provider="unsupported")
        
        # This should fail during Pydantic validation
        self.assertIn("Input should be", str(context.exception))
    
    def test_google_llm_parameters(self):
        """Test that Google LLM is created with correct parameters"""
        from app.utils.model_loader import ModelLoader
        
        with patch('app.utils.model_loader.ChatGoogleGenerativeAI') as mock_google_chat:
            mock_llm = MagicMock()
            mock_google_chat.return_value = mock_llm
            
            os.environ["GOOGLE_API_KEY"] = "test_google_key"
            
            loader = ModelLoader(model_provider="google")
            loader.load_llm()
            
            # Verify Google LLM was called with correct parameters
            mock_google_chat.assert_called_once_with(
                model="gemini-1.5-flash",
                google_api_key="test_google_key",
                temperature=0.7
            )
    
    def test_groq_llm_parameters(self):
        """Test that Groq LLM is created with correct parameters"""
        from app.utils.model_loader import ModelLoader
        
        with patch('app.utils.model_loader.ChatGroq') as mock_groq_chat:
            mock_llm = MagicMock()
            mock_groq_chat.return_value = mock_llm
            
            os.environ["GROQ_API_KEY"] = "test_groq_key"
            
            loader = ModelLoader(model_provider="groq")
            loader.load_llm()
            
            # Verify Groq LLM was called with correct parameters
            mock_groq_chat.assert_called_once_with(
                model="llama3-8b-8192",
                api_key="test_groq_key"
            )
    
    def test_openai_llm_parameters(self):
        """Test that OpenAI LLM is created with correct parameters"""
        from app.utils.model_loader import ModelLoader
        
        with patch('app.utils.model_loader.ChatOpenAI') as mock_openai_chat:
            mock_llm = MagicMock()
            mock_openai_chat.return_value = mock_llm
            
            os.environ["OPENAI_API_KEY"] = "test_openai_key"
            
            loader = ModelLoader(model_provider="openai")
            loader.load_llm()
            
            # Verify OpenAI LLM was called with correct parameters
            mock_openai_chat.assert_called_once_with(
                model="gpt-4o-mini",
                api_key="test_openai_key"
            )

class TestModelLoaderIntegration(unittest.TestCase):
    """Integration tests for ModelLoader"""
    
    def test_model_loader_with_real_config(self):
        """Test ModelLoader with real configuration"""
        from app.utils.model_loader import ModelLoader
        from app.utils.config_loader import load_config
        
        # Load real config
        config = load_config()
        
        # Verify config structure
        self.assertIn("llm", config)
        self.assertIn("google", config["llm"])
        self.assertIn("groq", config["llm"])
        self.assertIn("openai", config["llm"])
        
        # Test ModelLoader can access config
        loader = ModelLoader()
        self.assertEqual(loader.config["llm"]["google"]["model_name"], "gemini-1.5-flash")
        self.assertEqual(loader.config["llm"]["groq"]["model_name"], "llama3-8b-8192")
        self.assertEqual(loader.config["llm"]["openai"]["model_name"], "gpt-4o-mini")

if __name__ == "__main__":
    unittest.main(verbosity=2)
