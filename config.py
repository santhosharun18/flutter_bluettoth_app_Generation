import os
from dotenv import load_dotenv

load_dotenv()

class AgentConfig:
    """Configuration for different AI agents in the Flutter app generation pipeline."""
    
    # Choose which AI service to use for each agent
    PROMPT_ANALYZER_SERVICE = os.getenv("PROMPT_ANALYZER_SERVICE", "groq")  # "groq" or "anthropic"
    ARCHITECTURE_DESIGNER_SERVICE = os.getenv("ARCHITECTURE_DESIGNER_SERVICE", "groq")  # "groq" or "anthropic"
    CODE_GENERATOR_SERVICE = os.getenv("CODE_GENERATOR_SERVICE", "anthropic")  # "groq" or "anthropic"
    
    # API Keys validation
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    @classmethod
    def validate_config(cls):
        """Validate that required API keys are available for selected services."""
        services_needed = {
            cls.PROMPT_ANALYZER_SERVICE,
            cls.ARCHITECTURE_DESIGNER_SERVICE,
            cls.CODE_GENERATOR_SERVICE
        }
        
        missing_keys = []
        
        if "groq" in services_needed and not cls.GROQ_API_KEY:
            missing_keys.append("GROQ_API_KEY")
            
        if "anthropic" in services_needed and not cls.ANTHROPIC_API_KEY:
            missing_keys.append("ANTHROPIC_API_KEY")
            
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True
    
    @classmethod
    def get_service_info(cls):
        """Get information about which services are configured for each agent."""
        return {
            "prompt_analyzer": cls.PROMPT_ANALYZER_SERVICE,
            "architecture_designer": cls.ARCHITECTURE_DESIGNER_SERVICE,
            "code_generator": cls.CODE_GENERATOR_SERVICE
        }