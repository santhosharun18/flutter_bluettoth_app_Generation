from models.app_state import AppGenerationState
from services.groq_client import GroqClient
from services.anthropic_client import AnthropicClient
from config import AgentConfig
import json

class ArchitectureDesignerAgent:
    def __init__(self):
        # Initialize the appropriate client based on configuration
        if AgentConfig.ARCHITECTURE_DESIGNER_SERVICE == "anthropic":
            self.ai_client = AnthropicClient()
        else:
            self.ai_client = GroqClient()
            
        self.service_name = AgentConfig.ARCHITECTURE_DESIGNER_SERVICE
        
    def process(self, state: AppGenerationState) -> AppGenerationState:
        """Design Flutter app architecture based on structured requirements."""
        raw_response = ""
        json_str = ""
        
        try:
            print(f"🏗️ Designing architecture using {self.service_name.upper()} for: {state['structured_requirements'].get('app_name', 'Unknown App')}")
            
            # Get structured requirements from previous step
            requirements = state['structured_requirements']
            
            # Call AI service to design architecture
            raw_response = self.ai_client.design_architecture(requirements)
            print(raw_response)
            
            # Parse the response using the same robust parsing logic
            if "```json" in raw_response:
                print("Found a JSON markdown block, extracting architecture...")
                json_block_start = raw_response.find("```json") + len("```json")
                json_block_end = raw_response.find("```", json_block_start)
                if json_block_end != -1:
                    json_str = raw_response[json_block_start:json_block_end].strip()
            
            # Fallback to curly braces if no markdown block
            if not json_str:
                print("No JSON markdown block found, searching for curly braces...")
                json_start = raw_response.find('{')
                json_end = raw_response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = raw_response[json_start:json_end]

            if not json_str:
                raise ValueError("Could not extract any JSON from the architecture response.")

            # Parse JSON with fallback for quote fixing
            try:
                architecture = json.loads(json_str)
            except json.JSONDecodeError:
                print("⚠️ Initial JSON parse failed, attempting to auto-fix quotes...")
                fixed_json_str = json_str.replace("'", '"')
                architecture = json.loads(fixed_json_str)

            # Validate architecture structure
            required_keys = ['project_structure', 'dependencies', 'main_features', 'file_templates']
            for key in required_keys:
                if key not in architecture:
                    raise ValueError(f"Missing required architecture key: {key}")

            # Update state on success
            state['flutter_structure'] = architecture
            state['current_agent'] = 'project_creator'
            state['progress'] = 50
            
            # Log architecture summary
            total_files = len(architecture.get('file_templates', {}))
            print(f"✅ Architecture designed with {total_files} files using {self.service_name.upper()}")
            print(f"📁 Main directories: {list(architecture.get('project_structure', {}).keys())}")
            
        except Exception as e:
            print(f"❌ Critical error during architecture design with {self.service_name.upper()}.")
            state['error_log'].append(f"Architecture design failed ({self.service_name}): {str(e)}")
            state['current_agent'] = 'error'
            state['build_status'] = 'failed'
            
            print("--- DEBUG: Failed to parse JSON from Architecture Designer ---")
            print(f"Service used: {self.service_name}")
            print(f"Original AI Response:\n{raw_response}")
            print(f"String we tried to parse:\n{json_str}")
            print("--- END DEBUG ---")
            
        return state