import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self, model_name="llama-3.1-8b-instant"):
        self.client = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=model_name,
            temperature=0.1,
            max_tokens=4000
        )

    def chat_completion(self, system_prompt: str, user_prompt: str) -> str:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.client.invoke(messages)
        return response.content

    def analyze_prompt(self, user_prompt: str) -> str:
        system_prompt = """
You are a Flutter app requirements analyst. Your task is to parse user requests into a structured JSON format.

**CRITICAL INSTRUCTIONS:**

1. Your ENTIRE response MUST be ONLY the JSON object. No markdown or explanations.

2. The `ui_components` array must contain only UNIQUE values and ONLY what is explicitly requested.

**STRICT UI COMPONENT DETECTION RULES:**

- ONLY include "button" if user explicitly asks for buttons, on/off, toggle, turn on, turn off
- DO NOT include "slider" unless user specifically asks for slider, range, level control, brightness
- DO NOT include "color_picker" unless user specifically asks for color selection, RGB, color control
- DO NOT include "text_input" unless user specifically asks for text input, custom commands, terminal input
- DO NOT include "terminal" unless user specifically asks for terminal, log display, console

**For requests like "neopixel on and off buttons":**
- ONLY include: ["button"] in ui_components
- DO NOT add slider, color_picker, text_input, or terminal

**JSON Schema:**
{
  "app_name": "string",
  "description": "string", 
  "features": ["feature1", "feature2"],
  "ui_components": ["button"],
  "color_theme": "blue",
  "complexity": "simple"
}
"""
        return self.chat_completion(system_prompt, user_prompt)

    def design_architecture(self, requirements: dict) -> str:
        system_prompt = """
You are a Flutter architecture expert. Your response MUST be ONLY a valid JSON object.

**CRITICAL INSTRUCTIONS:**

1. Your entire response must be a single, parsable JSON object. No extra text or markdown.

2. The JSON object MUST contain these exact top-level keys: `project_structure`, `dependencies`, `main_features`, `file_templates`.

3. For any Bluetooth app, you MUST include `flutter_blue_plus` and `permission_handler` in the dependencies.

4. ONLY include dependencies that are actually needed based on ui_components.

**JSON OUTPUT STRUCTURE:**
{
  "project_structure": { "lib": { "main.dart": "App entry point", "screens": {}, "services": {}, "widgets": {} } },
  "dependencies": { "dependency_name": "version" },
  "main_features": [ { "name": "Feature Name", "description": "Brief description." } ],
  "file_templates": { "lib/main.dart": { "purpose": "Main UI and app logic." } }
}
"""

        user_prompt = f"""
Design a Flutter app architecture based on these requirements:
{requirements}
"""

        return self.chat_completion(system_prompt, user_prompt)