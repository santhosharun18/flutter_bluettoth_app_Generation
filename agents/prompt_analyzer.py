from models.app_state import AppGenerationState
from services.groq_client import GroqClient
from services.anthropic_client import AnthropicClient
from config import AgentConfig
import json
import re

class PromptAnalyzerAgent:
    def __init__(self):
        # Initialize the appropriate client based on configuration
        if AgentConfig.PROMPT_ANALYZER_SERVICE == "anthropic":
            self.ai_client = AnthropicClient()
        else:
            self.ai_client = GroqClient()
        self.service_name = AgentConfig.PROMPT_ANALYZER_SERVICE

    def process(self, state: AppGenerationState) -> AppGenerationState:
        """Advanced analysis for Bluetooth apps with comprehensive feature detection."""

        raw_response = ""
        json_str = ""

        try:
            print(f"🔍 Advanced Bluetooth App Analysis using {self.service_name.upper()}: {state['user_prompt'][:100]}...")

            # Enhanced prompt for Bluetooth-specific analysis
            enhanced_prompt = self._enhance_bluetooth_prompt(state['user_prompt'])
            raw_response = self.ai_client.analyze_prompt(enhanced_prompt)

            print("Raw Analysis Response:")
            print(raw_response)

            # Advanced parsing with Bluetooth-specific fallbacks
            parsed_requirements = self._parse_bluetooth_requirements(raw_response, state['user_prompt'])

            state['structured_requirements'] = parsed_requirements
            state['current_agent'] = 'architecture_designer'
            state['progress'] = 20

            print("✅ Advanced Bluetooth analysis completed")
            print("📊 Detected Features:", parsed_requirements.get('features', []))
            print("🎛️ UI Components:", parsed_requirements.get('ui_components', []))
            print("📡 Sensor Types:", parsed_requirements.get('sensor_types', []))

        except Exception as e:
            print(f"⚠️ Analysis error: {str(e)}")
            # Fallback to intelligent Bluetooth app defaults
            state['structured_requirements'] = self._create_bluetooth_fallback(state['user_prompt'])
            state['current_agent'] = 'architecture_designer'
            state['progress'] = 20
            state['error_log'].append(f"Prompt analysis used fallback: {str(e)}")

        return state

    def _enhance_bluetooth_prompt(self, user_prompt: str) -> str:
        """Enhance prompt with Bluetooth-specific context."""

        bluetooth_context = """
        CONTEXT: This is a request for a Bluetooth mobile application. 
        Analyze the following request and identify:
        1. Bluetooth functionality needed
        2. UI components for sensor data display
        3. Control mechanisms (buttons, sliders, etc.)
        4. Data types (temperature, humidity, general sensors)
        5. Professional UI requirements

        USER REQUEST: """

        return bluetooth_context + user_prompt

    def _parse_bluetooth_requirements(self, raw_response: str, original_prompt: str) -> dict:
        """Advanced parsing specifically designed for Bluetooth applications."""

        # Try standard JSON parsing first
        parsed_json = self._extract_json_from_response(raw_response)
        if parsed_json:
            return self._enhance_bluetooth_json(parsed_json, original_prompt)

        # Fallback to intelligent analysis
        return self._intelligent_bluetooth_analysis(original_prompt)

    def _extract_json_from_response(self, response: str) -> dict:
        """Extract JSON using multiple strategies."""

        # Strategy 1: JSON code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            if end != -1:
                json_str = response[start:end].strip()
                try:
                    return json.loads(json_str)
                except:
                    pass

        # Strategy 2: Find JSON object pattern
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, response, re.DOTALL)

        for match in matches:
            try:
                return json.loads(match)
            except:
                continue

        # Strategy 3: Line-by-line extraction
        lines = response.split('\n')
        json_lines = []
        in_json = False

        for line in lines:
            if '{' in line:
                in_json = True
            if in_json:
                json_lines.append(line)
            if '}' in line and in_json:
                break

        if json_lines:
            try:
                return json.loads('\n'.join(json_lines))
            except:
                pass

        return None

    def _enhance_bluetooth_json(self, base_json: dict, prompt: str) -> dict:
        """Enhance JSON with Bluetooth-specific defaults and analysis."""

        enhanced = base_json.copy()

        # Ensure Bluetooth features
        if 'features' not in enhanced:
            enhanced['features'] = []

        bluetooth_features = ['bluetooth_scanning', 'device_connection', 'data_transmission']
        for feature in bluetooth_features:
            if feature not in enhanced['features']:
                enhanced['features'].append(feature)

        # Detect sensor types from prompt
        sensor_types = []
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ['temp', 'temperature', 'thermal']):
            sensor_types.append('temperature')
            if 'sensor_data_parsing' not in enhanced['features']:
                enhanced['features'].append('sensor_data_parsing')

        if any(word in prompt_lower for word in ['humidity', 'humid', 'moisture']):
            sensor_types.append('humidity')
            if 'sensor_data_parsing' not in enhanced['features']:
                enhanced['features'].append('sensor_data_parsing')

        if any(word in prompt_lower for word in ['sensor', 'data', 'reading']):
            sensor_types.append('general_sensor')
            enhanced['features'].extend(['real_time_updates', 'data_monitoring'])

        enhanced['sensor_types'] = sensor_types

        # Enhanced UI components
        if 'ui_components' not in enhanced:
            enhanced['ui_components'] = []

        # Always include professional Bluetooth UI components
        essential_components = ['status_card', 'device_list']
        for component in essential_components:
            if component not in enhanced['ui_components']:
                enhanced['ui_components'].append(component)

        # Add sensor displays if detected
        if sensor_types:
            if 'sensor_displays' not in enhanced['ui_components']:
                enhanced['ui_components'].append('sensor_displays')

        # Detect control types
        control_types = []
        if any(word in prompt_lower for word in ['button', 'on', 'off', 'control', 'switch']):
            control_types.append('buttons')
            if 'control_buttons' not in enhanced['ui_components']:
                enhanced['ui_components'].append('control_buttons')

        if any(word in prompt_lower for word in ['slider', 'brightness', 'level', 'adjust']):
            control_types.append('sliders')
            if 'sliders' not in enhanced['ui_components']:
                enhanced['ui_components'].append('sliders')

        enhanced['control_types'] = control_types

        # Professional defaults
        enhanced['color_theme'] = 'gradient_blue_purple'
        enhanced['complexity'] = 'professional'

        return enhanced

    def _intelligent_bluetooth_analysis(self, prompt: str) -> dict:
        """Create comprehensive Bluetooth app requirements from prompt analysis."""

        prompt_lower = prompt.lower()

        # Base Bluetooth app structure
        requirements = {
            "app_name": "Professional Bluetooth Controller",
            "description": "Advanced Bluetooth application with modern UI",
            "features": [
                "bluetooth_scanning",
                "device_connection", 
                "data_transmission",
                "real_time_updates"
            ],
            "ui_components": [
                "status_card",
                "device_list",
                "control_buttons"
            ],
            "sensor_types": [],
            "control_types": [],
            "color_theme": "gradient_blue_purple",
            "complexity": "professional"
        }

        # Detect specific features from prompt
        if any(word in prompt_lower for word in ['temp', 'temperature']):
            requirements['sensor_types'].append('temperature')
            requirements['features'].append('sensor_data_parsing')
            if 'sensor_displays' not in requirements['ui_components']:
                requirements['ui_components'].append('sensor_displays')

        if any(word in prompt_lower for word in ['humidity', 'humid', 'moisture']):
            requirements['sensor_types'].append('humidity')
            requirements['features'].append('sensor_data_parsing')
            if 'sensor_displays' not in requirements['ui_components']:
                requirements['ui_components'].append('sensor_displays')

        if any(word in prompt_lower for word in ['neopixel', 'led', 'light']):
            requirements['app_name'] = "Neopixel Bluetooth Controller"
            requirements['description'] = "Professional Neopixel control via Bluetooth"
            requirements['control_types'].append('buttons')

        if any(word in prompt_lower for word in ['button', 'on', 'off']):
            requirements['control_types'].append('buttons')

        if any(word in prompt_lower for word in ['slider', 'brightness', 'level']):
            requirements['control_types'].append('sliders')
            if 'sliders' not in requirements['ui_components']:
                requirements['ui_components'].append('sliders')

        return requirements

    def _create_bluetooth_fallback(self, prompt: str) -> dict:
        """Create fallback Bluetooth app structure when analysis fails."""

        return {
            "app_name": "Bluetooth Controller",
            "description": "Professional Bluetooth application",
            "features": [
                "bluetooth_scanning",
                "device_connection",
                "data_transmission",
                "device_control"
            ],
            "ui_components": [
                "status_card",
                "control_buttons", 
                "device_list"
            ],
            "sensor_types": ["general_sensor"],
            "control_types": ["buttons"],
            "color_theme": "gradient_blue_purple",
            "complexity": "professional"
        }