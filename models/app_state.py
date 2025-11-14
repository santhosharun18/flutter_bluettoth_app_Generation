from typing import TypedDict, Annotated, List, Dict, Optional, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class AppGenerationState(TypedDict):
    """State object for Flutter app generation workflow."""
    messages: List[Dict[str, Any]]
    user_prompt: str
    hardware_commands: str
    structured_requirements: Dict[str, Any]
    flutter_structure: Dict[str, Any]
    generated_files: Dict[str, str]
    build_status: str  # 'pending', 'in_progress', 'completed', 'failed'
    apk_path: Optional[str]
    current_agent: str
    progress: int  # 0-100
    error_log: List[str]
    session_id: str
    project_path: Optional[str]  # NEW: Path to the created Flutter project
    temp_dir: Optional[str] 
