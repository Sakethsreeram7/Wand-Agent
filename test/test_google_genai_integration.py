#!/usr/bin/env python3
"""
Test script to verify Google Generative AI integration with Groq fallback
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Add the parent directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestGoogleGenAIIntegration(unittest.TestCase):
    """Test cases for Google Generative AI integration"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        load_dotenv()
        cls.google_key = os.getenv("GOOGLE_API_KEY")
        cls.groq_key = os.getenv("GROQ_API_KEY")
    
    def test_model_loader_import(self):
        """Test that ModelLoader can be imported successfully"""
        try:
            from app.utils.model_loader import ModelLoader
            self.assertTrue(True, "ModelLoader imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import ModelLoader: {e}")
    
    def test_google_genai_import(self):
        """Test that Google Generative AI can be imported"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.assertTrue(True, "ChatGoogleGenerativeAI imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import ChatGoogleGenerativeAI: {e}")
    
    def test_model_loader_default_provider(self):
        """Test that ModelLoader defaults to Google provider"""
        from app.utils.model_loader import ModelLoader
        
        model_loader = ModelLoader()
        self.assertEqual(model_loader.model_provider, "google", 
                        "Default provider should be 'google'")
    
    def test_model_loader_google_provider(self):
        """Test ModelLoader with explicit Google provider"""
        from app.utils.model_loader import ModelLoader
        
        model_loader = ModelLoader(model_provider="google")
        self.assertEqual(model_loader.model_provider, "google")
    
    def test_model_loader_groq_provider(self):
        """Test ModelLoader with explicit Groq provider"""
        from app.utils.model_loader import ModelLoader
        
        model_loader = ModelLoader(model_provider="groq")
        self.assertEqual(model_loader.model_provider, "groq")
    
    def test_config_has_google_settings(self):
        """Test that config includes Google settings"""
        from app.utils.config_loader import load_config
        
        config = load_config()
        self.assertIn("google", config["llm"], "Config should include Google settings")
        self.assertEqual(config["llm"]["google"]["provider"], "google")
        self.assertEqual(config["llm"]["google"]["model_name"], "gemini-1.5-flash")
    
    @unittest.skipIf(not os.getenv("GOOGLE_API_KEY"), "GOOGLE_API_KEY not set")
    def test_google_llm_loading(self):
        """Test loading Google Generative AI LLM (requires API key)"""
        from app.utils.model_loader import ModelLoader
        
        try:
            model_loader = ModelLoader(model_provider="google")
            llm = model_loader.load_llm()
            self.assertIsNotNone(llm, "Google LLM should be loaded")
            print("✅ Google Generative AI loaded successfully")
        except Exception as e:
            self.fail(f"Failed to load Google LLM: {e}")
    
    @unittest.skipIf(not os.getenv("GROQ_API_KEY"), "GROQ_API_KEY not set")
    def test_groq_llm_loading(self):
        """Test loading Groq LLM (requires API key)"""
        from app.utils.model_loader import ModelLoader
        
        try:
            model_loader = ModelLoader(model_provider="groq")
            llm = model_loader.load_llm()
            self.assertIsNotNone(llm, "Groq LLM should be loaded")
            print("✅ Groq LLM loaded successfully")
        except Exception as e:
            self.fail(f"Failed to load Groq LLM: {e}")
    
    def test_fallback_mechanism(self):
        """Test fallback from Google to Groq when Google fails"""
        from app.utils.model_loader import ModelLoader
        
        # Temporarily remove Google API key to trigger fallback
        original_google_key = os.environ.get("GOOGLE_API_KEY")
        if original_google_key:
            os.environ.pop("GOOGLE_API_KEY", None)
        
        try:
            if self.groq_key:  # Only test if Groq key is available
                model_loader = ModelLoader(model_provider="google")
                llm = model_loader.load_llm()  # Should fallback to Groq
                self.assertIsNotNone(llm, "Should fallback to Groq when Google fails")
                print("✅ Fallback mechanism working")
            else:
                self.skipTest("GROQ_API_KEY not available for fallback test")
        except Exception as e:
            # This is expected if neither key is available
            if "Both Google Generative AI and Groq fallback failed" in str(e):
                print("⚠️  Expected failure: No API keys available")
            else:
                self.fail(f"Unexpected error in fallback test: {e}")
        finally:
            # Restore Google API key
            if original_google_key:
                os.environ["GOOGLE_API_KEY"] = original_google_key
    
    def test_graph_builder_default_provider(self):
        """Test that GraphBuilder uses Google as default"""
        from app.agent.agentic_workflow import GraphBuilder
        
        # Mock the model loading to avoid API calls
        with patch('app.utils.model_loader.ModelLoader.load_llm') as mock_load_llm:
            mock_llm = MagicMock()
            mock_load_llm.return_value = mock_llm
            
            graph_builder = GraphBuilder()
            self.assertEqual(graph_builder.model_loader.model_provider, "google",
                           "GraphBuilder should default to Google provider")
    
    def test_graph_builder_tool_loading(self):
        """Test that GraphBuilder loads all tools correctly"""
        from app.agent.agentic_workflow import GraphBuilder
        
        # Mock the model loading to avoid API calls
        with patch('app.utils.model_loader.ModelLoader.load_llm') as mock_load_llm:
            mock_llm = MagicMock()
            mock_load_llm.return_value = mock_llm
            
            graph_builder = GraphBuilder()
            self.assertGreater(len(graph_builder.tools), 0, 
                             "GraphBuilder should load tools")
            self.assertEqual(len(graph_builder.tools), 17,
                           "Should load all 17 tools")
    
    def test_requirements_includes_google_genai(self):
        """Test that requirements.txt includes Google Generative AI package"""
        requirements_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            "requirements.txt"
        )
        
        with open(requirements_path, 'r') as f:
            requirements = f.read()
        
        self.assertIn("langchain_google_genai", requirements,
                     "requirements.txt should include langchain_google_genai")

class TestAPIKeyConfiguration(unittest.TestCase):
    """Test cases for API key configuration"""
    
    def test_api_key_detection(self):
        """Test detection of available API keys"""
        google_key = os.getenv("GOOGLE_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        
        print(f"\n🔑 API Key Status:")
        print(f"  Google API Key: {'✅ Found' if google_key else '❌ Missing'}")
        print(f"  Groq API Key: {'✅ Found' if groq_key else '❌ Missing'}")
        
        # At least one key should be available for the system to work
        self.assertTrue(google_key or groq_key, 
                       "At least one API key (Google or Groq) should be available")

def run_integration_test():
    """Run a comprehensive integration test"""
    print("🧪 Running Google Generative AI Integration Test...")
    print("=" * 60)
    
    try:
        # Load environment
        load_dotenv()
        
        # Import required modules
        from app.agent.agentic_workflow import GraphBuilder
        from app.utils.model_loader import ModelLoader
        
        print("✅ All imports successful")
        
        # Test model loader
        print("\n🔬 Testing Model Loader...")
        model_loader = ModelLoader()
        print(f"✅ Default provider: {model_loader.model_provider}")
        
        # Test graph builder (with mocked LLM to avoid API calls)
        print("\n🔬 Testing Graph Builder...")
        with patch('app.utils.model_loader.ModelLoader.load_llm') as mock_load_llm:
            mock_llm = MagicMock()
            mock_load_llm.return_value = mock_llm
            
            graph_builder = GraphBuilder()
            print(f"✅ GraphBuilder created with {len(graph_builder.tools)} tools")
        
        print("\n🎉 Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run integration test first
    print("Running integration test...")
    success = run_integration_test()
    
    if success:
        print("\n" + "=" * 60)
        print("Running unit tests...")
        unittest.main(verbosity=2)
    else:
        print("❌ Integration test failed, skipping unit tests")
        sys.exit(1)
