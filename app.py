import os
import uuid
import glob
import shutil
import tempfile
import re
from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for
from langgraph.graph import StateGraph, START, END
from models.app_state import AppGenerationState
from agents.prompt_analyzer import PromptAnalyzerAgent
from agents.architecture_designer import ArchitectureDesignerAgent
from agents.project_creator import ProjectCreatorAgent
from agents.code_generator import CodeGeneratorAgent
from agents.build_automator import BuildAutomatorAgent
import qrcode
import io
import base64
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
session_states = {}

def cleanup_old_builds():
    """Finds and removes leftover temporary build directories from previous runs."""
    print("🧹 Performing startup cleanup of old temporary build directories...")
    # --- MODIFICATION FOR WINDOWS ---
    # Use tempfile.gettempdir() to get the correct temporary directory on any OS
    temp_dir_path = tempfile.gettempdir()
    search_pattern = os.path.join(temp_dir_path, 'flutter_app_*')
    temp_dirs = glob.glob(search_pattern)
    # --- END OF MODIFICATION ---
    
    deleted_count = 0
    for directory in temp_dirs:
        try:
            shutil.rmtree(directory)
            deleted_count += 1
        except OSError as e:
            print(f"Error removing directory {directory}: {e}")
    if deleted_count > 0:
        print(f"✅ Cleaned up {deleted_count} old build directories.")
# Initialize agents
prompt_analyzer = PromptAnalyzerAgent()
architecture_designer = ArchitectureDesignerAgent()
project_creator = ProjectCreatorAgent()
code_generator = CodeGeneratorAgent()
build_automator = BuildAutomatorAgent()

def create_workflow():
    """Create a LangGraph workflow with robust conditional error handling."""
    workflow = StateGraph(AppGenerationState)
    workflow.add_node("prompt_analyzer", prompt_analyzer.process)
    workflow.add_node("architecture_designer", architecture_designer.process)
    workflow.add_node("project_creator", project_creator.process)
    workflow.add_node("code_generator", code_generator.process)
    workflow.add_node("build_automator", build_automator.process)
    workflow.add_edge(START, "prompt_analyzer")
    workflow.add_conditional_edges("prompt_analyzer", lambda state: "architecture_designer" if state.get('current_agent') != 'error' else END)
    workflow.add_conditional_edges("architecture_designer", lambda state: "project_creator" if state.get('current_agent') != 'error' else END)
    workflow.add_conditional_edges("project_creator", lambda state: "code_generator" if state.get('current_agent') != 'error' else END)
    workflow.add_conditional_edges("code_generator", lambda state: "build_automator" if state.get('current_agent') != 'error' else END)
    workflow.add_edge("build_automator", END)
    return workflow.compile()

workflow_app = create_workflow()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_app():
    user_prompt = request.form.get('prompt', '').strip()
    hardware_commands = request.form.get('hardware_commands', '').strip() # NEW: Get hardware commands

    if not user_prompt:
        return jsonify({'error': 'Please provide a prompt'}), 400
    
    session_id = str(uuid.uuid4())
    initial_state = AppGenerationState(
        messages=[],
        user_prompt=user_prompt,
        hardware_commands=hardware_commands, # NEW: Add to state
        structured_requirements={},
        flutter_structure={},
        generated_files={},
        build_status='pending',
        apk_path=None,
        current_agent='prompt_analyzer',
        progress=0,
        error_log=[],
        session_id=session_id,
        project_path=None,
        temp_dir=None
    )
    session_states[session_id] = initial_state
    return redirect(url_for('progress', session_id=session_id))

@app.route('/progress/<session_id>')
def progress(session_id):
    if session_id not in session_states:
        return redirect(url_for('index'))
    return render_template('progress.html', session_id=session_id)

@app.route('/api/progress/<session_id>')
def api_progress(session_id):
    state = session_states.get(session_id)
    if not state:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify({
        'progress': state.get('progress'),
        'current_agent': state.get('current_agent'),
        'build_status': state.get('build_status'),
        'errors': state.get('error_log'),
        'apk_ready': state.get('apk_path') is not None,
    })

@app.route('/api/start-generation/<session_id>', methods=['POST'])
def start_generation(session_id):
    if session_id not in session_states:
        return jsonify({'error': 'Session not found'}), 404
    try:
        final_state = workflow_app.invoke(session_states[session_id])
        session_states[session_id] = final_state
        return jsonify({'success': True, 'message': 'Generation completed'})
    except Exception as e:
        session_states[session_id]['error_log'].append(f"Workflow error: {str(e)}")
        session_states[session_id]['build_status'] = 'failed'
        return jsonify({'error': str(e)}), 500

@app.route('/download/<session_id>')
def download_apk(session_id):
    state = session_states.get(session_id, {})
    apk_path = state.get('apk_path')
    
    if not apk_path or not os.path.exists(apk_path):
        return "APK not found.", 404
    
    # Get dynamic filename
    requirements = state.get('structured_requirements', {})
    app_name = requirements.get('app_name', 'bluetooth_app')
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', app_name.lower())
    download_name = f"{clean_name}.apk"
        
    return send_file(apk_path, as_attachment=True, download_name=download_name)


@app.route('/results/<session_id>')
def results(session_id):
    if session_id not in session_states:
        return redirect(url_for('index'))
    
    state = session_states[session_id]
    qr_code_data = None
    download_url = None

    # Generate download URL and QR code if APK exists
    if state.get('apk_path') and os.path.exists(state['apk_path']):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            download_url = f"http://{ip_address}:5000/download/{session_id}"
            
            # GENERATE QR CODE
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(download_url)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            img_buffer = io.BytesIO()
            qr_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            qr_code_data = base64.b64encode(img_buffer.getvalue()).decode()
            
        except Exception as e:
            print(f"QR code generation error: {e}")
            download_url = f"http://localhost:5000/download/{session_id}"

    print(f"🔍 DEBUG - APK Path: {state.get('apk_path')}")
    print(f"🔍 DEBUG - APK Exists: {os.path.exists(state.get('apk_path', ''))}")
    print(f"🔍 DEBUG - Build Status: {state.get('build_status')}")
    print(f"🔍 DEBUG - QR Code Data: {qr_code_data is not None}")
    print(f"🔍 DEBUG - Download URL: {download_url}")

    return render_template('results.html',
                         session_id=session_id,
                         state=state,
                         qr_code_data=qr_code_data,
                         download_url=download_url)


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    cleanup_old_builds()
    app.run(debug=True, host='0.0.0.0', port=5000)
