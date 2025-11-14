import os
import subprocess
import json
import tempfile
import re
from xml.etree import ElementTree as ET
from models.app_state import AppGenerationState

class ProjectCreatorAgent:
    def __init__(self):
        pass
    
    def process(self, state: AppGenerationState) -> AppGenerationState:
        """Create Flutter project structure with all fixes applied."""
        try:
            print("Creating Flutter project structure with all fixes...")
            
            architecture = state['flutter_structure']
            requirements = state['structured_requirements']
            app_name = requirements.get('app_name', 'flutter_app').lower().replace(' ', '_')
            
            app_name = self._sanitize_app_name(app_name)
            
            temp_dir = tempfile.mkdtemp(prefix=f'flutter_app_{state["session_id"]}_')
            project_path = os.path.join(temp_dir, app_name)
            
            print(f"Project will be created at: {project_path}")
            
            self._create_flutter_project(app_name, project_path, temp_dir)
            
            self._update_pubspec(project_path, architecture.get('dependencies', {}), 
                        architecture.get('dev_dependencies', {}), app_name, requirements)
            
            self._run_pub_get(project_path)
            
            self._create_project_structure(project_path, architecture.get('project_structure', {}))
            
            # --- MODIFICATION ---
            # The logic for adding permissions has been removed from this agent.
            # It will now be handled correctly and automatically by the build agent and plugins.
            self._fix_gradle_files(project_path)
            print("Android configuration fixed.")
            # --- END MODIFICATION ---

            state['project_path'] = project_path
            state['temp_dir'] = temp_dir
            state['current_agent'] = 'code_generator'
            state['progress'] = 60
            
            total_files = self._count_created_files(project_path)
            print(f"Project structure created with {total_files} files")
            print(f"Project location: {project_path}")
            
        except Exception as e:
            print(f"Critical error during project creation: {str(e)}")
            state['error_log'].append(f"Project creation failed: {str(e)}")
            state['current_agent'] = 'error'
            state['build_status'] = 'failed'
            
        return state
    
    def _sanitize_app_name(self, name: str) -> str:
        sanitized = re.sub(r'[^a-z0-9_]', '_', name.lower())
        if sanitized and sanitized[0].isdigit():
            sanitized = 'app_' + sanitized
        if not sanitized:
            sanitized = 'flutter_app'
        return sanitized
    
    def _create_flutter_project(self, app_name: str, project_path: str, temp_dir: str):
        command = [
            'flutter', 'create', 
            '--project-name', app_name,
            '--platforms', 'android',
            '--android-language', 'kotlin',
            project_path
        ]
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, cwd=temp_dir, timeout=120, shell=True)
        if result.returncode != 0:
            raise Exception(f"Flutter create failed: {result.stderr}")
        print("Base Flutter project created successfully")
    
    def _update_pubspec(self, project_path: str, dependencies: dict, dev_dependencies: dict, app_name: str, requirements: dict):
        """
        Update pubspec.yaml and FORCE the use of modern, stable packages
        to prevent all build failures.
        """
        pubspec_path = os.path.join(project_path, 'pubspec.yaml')
        
        try:
            print("\n--- Updating pubspec.yaml with definitive package fixes ---")
            
            app_requirements_text = str(requirements).lower()
            ui_components = requirements.get('ui_components', [])

            # --- Definitive Bluetooth Fix ---
            if 'flutter_bluetooth_serial' in dependencies:
                print("Found and removed problematic 'flutter_bluetooth_serial' package.")
                del dependencies['flutter_bluetooth_serial']
            
            is_bluetooth_app = any(keyword in app_requirements_text for keyword in ['bluetooth', 'ble', 'hc-05', 'sensor'])
            if is_bluetooth_app:
                print("Bluetooth app detected. Forcing essential dependencies.")
                dependencies['flutter_blue_plus'] = '^1.32.2'
                dependencies['permission_handler'] = '^11.3.0'

            # --- Dynamic Dependency for UI Components ---
            if 'color_picker' in ui_components:
                 print("Color picker UI detected. Adding `flutter_colorpicker` dependency.")
                 dependencies['flutter_colorpicker'] = '^1.1.0'

            # --- Remove known bad packages ---
            bad_packages = ['line_graph', 'charts_flutter', 'graph_view', 'color_picker', 'slider']
            for pkg in bad_packages:
                if pkg in dependencies:
                    print(f"Found and removed problematic package: {pkg}")
                    del dependencies[pkg]

            dependencies = self._filter_problematic_dependencies(dependencies, requirements)

            # Build the final dependency list
            final_deps = {
                'flutter': {'sdk': 'flutter'},
                'cupertino_icons': '^1.0.2',
            }
            final_deps.update(dependencies)

            yaml_safe_name = self._sanitize_app_name(app_name)
            lines = [
                f"name: {yaml_safe_name}", "description: A Flutter application.",
                "publish_to: 'none'", "version: 1.0.0+1", "",
                "environment:", '  sdk: ">=3.2.0 <4.0.0"', "", "dependencies:"
            ]
            
            for dep, version in final_deps.items():
                if dep == 'flutter': continue
                lines.append(f"  {dep}: {version}")
            
            lines.extend([
                "", "dev_dependencies:", "  flutter_test:", "    sdk: flutter",
                "  flutter_lints: ^3.0.0", "", "flutter:", "  uses-material-design: true"
            ])
            
            with open(pubspec_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print(f"SUCCESS: pubspec.yaml updated with {len(final_deps)} stable dependencies.\n")
            
        except Exception as e:
            raise Exception(f"Could not update pubspec.yaml: {e}")

    def _is_bluetooth_app(self, dependencies: dict) -> bool:
        ble_deps = ['flutter_blue_plus', 'flutter_bluetooth_serial', 'bluetooth']
        for dep in dependencies.keys():
            if any(ble_dep in dep.lower() for ble_dep in ble_deps):
                return True
        return False

    def _run_pub_get(self, project_path: str):
        try:
            print("Running flutter pub get...")
            result = subprocess.run(['flutter', 'pub', 'get'], cwd=project_path, capture_output=True, text=True, timeout=120, shell=True)
            if result.returncode != 0:
                raise Exception(f"Flutter pub get failed:\n{result.stderr}")
            print("Dependencies downloaded successfully")
        except Exception as e:
            raise e

    def _create_project_structure(self, project_path: str, project_structure: dict):
        if 'lib' in project_structure:
            lib_path = os.path.join(project_path, 'lib')
            self._create_recursive_structure(project_path, {'lib': project_structure['lib']})
        print("Project structure and empty files created")

    def _create_recursive_structure(self, base_path: str, structure: dict):
        for name, content in structure.items():
            current_path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(current_path, exist_ok=True)
                self._create_recursive_structure(current_path, content)
            elif '/lib/' in current_path.replace('\\', '/'):
                os.makedirs(os.path.dirname(current_path), exist_ok=True)
                if current_path.endswith('.dart') and (name != 'main.dart' or not os.path.exists(current_path)):
                    with open(current_path, 'w', encoding='utf-8') as f:
                        f.write(f"// {content}\n// TODO: Implement {name}\n\n")
    
    def _fix_gradle_files(self, project_path: str):
        app_gradle_path = os.path.join(project_path, 'android/app/build.gradle')
        if os.path.exists(app_gradle_path):
            with open(app_gradle_path, 'r', encoding='utf-8') as f: content = f.read()
            content = re.sub(r'compileSdk .*', 'compileSdk 35', content)
            content = re.sub(r'minSdkVersion .*', 'minSdkVersion 21', content)
            content = re.sub(r'targetSdkVersion .*', 'targetSdkVersion 35', content)
            with open(app_gradle_path, 'w', encoding='utf-8') as f: f.write(content)
    
    def _count_created_files(self, project_path: str) -> int:
        return sum(len(files) for root, dirs, files in os.walk(project_path))
    
    def _filter_problematic_dependencies(self, dependencies: dict, requirements: dict) -> dict:
        """Remove dependencies that cause build conflicts."""
        
        app_requirements_text = str(requirements).lower()
        is_bluetooth_app = any(keyword in app_requirements_text for keyword in ['bluetooth', 'ble', 'terminal', 'data'])
        
        problematic_packages = [
            'connectivity_plus', 'network_info_plus', 'device_info_plus', 
            'package_info_plus', 'shared_preferences_plus'
        ]
        
        cleaned_deps = {}
        for dep, version in dependencies.items():
            if dep not in problematic_packages:
                cleaned_deps[dep] = version
            else:
                print(f"Removed problematic dependency: {dep}")
        
        if is_bluetooth_app:
            bluetooth_essentials = {
                'flutter_blue_plus': '^1.32.2',
                'permission_handler': '^11.3.0'
            }
            cleaned_deps.update(bluetooth_essentials)
        
        return cleaned_deps

