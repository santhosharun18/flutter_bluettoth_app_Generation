import os
import subprocess
import tempfile
import shutil
import re
from models.app_state import AppGenerationState

class BuildAutomatorAgent:
    def __init__(self):
        self.flutter_sdk_path = os.getenv('FLUTTER_SDK_PATH', '/usr/local/flutter')

    def process(self, state: AppGenerationState) -> AppGenerationState:
        if state.get('current_agent') == 'error':
            return state

        try:
            project_path = state.get('project_path')
            if not project_path or not os.path.exists(project_path):
                raise Exception("Project path not found. ProjectCreator must run first.")

            print(f"🏗️ Starting BULLETPROOF Flutter APK build: {project_path}")

            # BULLETPROOF FIXES - ENSURES PERMISSIONS WORK
            self._bulletproof_fixes(state)

            # Pre-build validations and fixes
            self._pre_build_setup(project_path, state)

            # Flutter pub get with retry
            self._flutter_pub_get_with_retry(project_path)

            # Build APK
            apk_path = self._build_apk_with_fixes(project_path, state)

            if apk_path and os.path.exists(apk_path):
                state['apk_path'] = apk_path
                state['build_status'] = 'completed'
                state['current_agent'] = 'completed'
                state['progress'] = 100
                print(f"🎉 APK build successful: {apk_path}")
            else:
                raise Exception("APK was not generated successfully")

        except Exception as e:
            print(f"💥 Build failed: {str(e)}")
            state['error_log'].append(f"Enhanced build failed: {str(e)}")
            state['current_agent'] = 'error'
            state['build_status'] = 'failed'
            state['progress'] = 90

        return state

    def _bulletproof_fixes(self, state: AppGenerationState):
        """Apply bulletproof fixes to ensure permissions and Bluetooth work properly."""

        generated_files = state.get('generated_files', {})
        if 'lib/main.dart' not in generated_files:
            return

        print("🔧 Applying BULLETPROOF fixes...")

        code = generated_files['lib/main.dart']

        # BULLETPROOF FIX 1: Ensure permissions are requested immediately
        # Check if permission request is called in initState
        if 'requestPermissions();' not in code:
            print("⚠️ Adding missing permission request call")
            # Add to initState
            init_state_pattern = r'(void initState\(\).*?\{.*?super\.initState\(\);)'
            replacement = r'\1\n    WidgetsBinding.instance.addPostFrameCallback((_) {\n      requestPermissions();\n    });'
            code = re.sub(init_state_pattern, replacement, code, flags=re.DOTALL)

        # BULLETPROOF FIX 2: Ensure all required variables are declared
        required_vars = [
            'List<ScanResult> scanResults = [];',
            'BluetoothDevice? connectedDevice;',
            'BluetoothCharacteristic? writeCharacteristic;',
            'bool isScanning = false;',
            'bool isConnecting = false;',
            'String connectionStatus = "Ready to scan";',
            'bool permissionsGranted = false;',
            'int dataPackets = 0;',
            'String deviceId = "Unknown";'
        ]

        for var in required_vars:
            if var not in code:
                print(f"⚠️ Adding missing variable: {var}")
                # Find State class and add the variable
                state_class_pattern = r'(class _\w*State extends State<\w+>\s*\{)'
                code = re.sub(state_class_pattern, f'\1\n  {var}', code)

        # BULLETPROOF FIX 3: Fix any API compatibility issues
        code = code.replace('FlutterBluePlus.FlutterBluePlus.', 'FlutterBluePlus.')
        code = code.replace('FlutterBluePlus.instance.', 'FlutterBluePlus.')
        code = code.replace('_devices', 'scanResults')
        code = re.sub(r'primary:\s*(Colors\.\w+)', r'backgroundColor: \1', code)
        code = re.sub(r'onPrimary:\s*(Colors\.\w+)', r'foregroundColor: \1', code)
        code = re.sub(r'Uint8List\.fromList\([^)]+\)', 'command.codeUnits', code)

        # BULLETPROOF FIX 4: Ensure proper imports
        required_imports = [
            "import 'package:flutter/material.dart';",
            "import 'package:flutter_blue_plus/flutter_blue_plus.dart';",
            "import 'package:permission_handler/permission_handler.dart';",
            "import 'dart:io';"
        ]

        for import_stmt in required_imports:
            if import_stmt not in code:
                code = import_stmt + "\n" + code

        # Update state and write file
        state['generated_files']['lib/main.dart'] = code

        project_path = state.get('project_path')
        if project_path:
            main_dart_path = os.path.join(project_path, 'lib/main.dart')
            with open(main_dart_path, 'w', encoding='utf-8') as f:
                f.write(code)

        print("✅ BULLETPROOF fixes applied - permissions will work!")

    def _pre_build_setup(self, project_path: str, state: AppGenerationState):
        print("🔧 Running pre-build setup and validations...")

        self._fix_android_configuration(project_path)
        self._fix_pubspec_yaml(project_path, state)
        self._fix_android_manifest_bulletproof(project_path)
        self._fix_gradle_files(project_path)

        print("✅ Pre-build setup completed")

    def _fix_android_manifest_bulletproof(self, project_path: str):
        """Add ALL required Bluetooth permissions to Android manifest."""

        manifest_path = os.path.join(project_path, 'android/app/src/main/AndroidManifest.xml')
        if not os.path.exists(manifest_path):
            return

        try:
            with open(manifest_path, 'r') as f:
                content = f.read()

            # Complete list of Bluetooth permissions for modern Android
            bluetooth_permissions = [
                '<uses-permission android:name="android.permission.BLUETOOTH" />',
                '<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />',
                '<uses-permission android:name="android.permission.BLUETOOTH_SCAN" android:usesPermissionFlags="neverForLocation" />',
                '<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />',
                '<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />',
                '<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />',
                '<uses-feature android:name="android.hardware.bluetooth" android:required="false" />',
                '<uses-feature android:name="android.hardware.bluetooth_le" android:required="false" />'
            ]

            # Add permissions before <application tag
            if '<application' in content and 'BLUETOOTH_SCAN' not in content:
                permissions_text = '\n    '.join(bluetooth_permissions)
                content = content.replace(
                    '<application',
                    f'    {permissions_text}\n\n    <application'
                )

                with open(manifest_path, 'w') as f:
                    f.write(content)

                print("✅ Fixed AndroidManifest.xml with BULLETPROOF Bluetooth permissions")

        except Exception as e:
            print(f"⚠️ Warning: Could not fix AndroidManifest.xml: {e}")

    def _fix_android_configuration(self, project_path: str):
        app_build_gradle = os.path.join(project_path, 'android/app/build.gradle')
        if os.path.exists(app_build_gradle):
            with open(app_build_gradle, 'r') as f:
                content = f.read()

            content = re.sub(r'compileSdkVersion\s+\d+', 'compileSdkVersion 34', content)
            content = re.sub(r'targetSdkVersion\s+\d+', 'targetSdkVersion 34', content)
            content = re.sub(r'minSdkVersion\s+\d+', 'minSdkVersion 21', content)

            if 'multiDexEnabled true' not in content:
                content = content.replace(
                    'defaultConfig {',
                    'defaultConfig {\n        multiDexEnabled true'
                )

            with open(app_build_gradle, 'w') as f:
                f.write(content)

            print("✅ Fixed app-level build.gradle")

    def _fix_pubspec_yaml(self, project_path: str, state: AppGenerationState):
        pubspec_path = os.path.join(project_path, 'pubspec.yaml')
        if not os.path.exists(pubspec_path):
            return

        try:
            requirements = state.get('structured_requirements', {})

            # Use the most stable versions that work
            dependencies = {
                'flutter_blue_plus': '^1.36.8',
                'permission_handler': '^11.3.1',
            }

            sensor_types = requirements.get('sensor_types', [])
            if sensor_types:
                dependencies['fl_chart'] = '^0.68.0'

            with open(pubspec_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            in_dependencies = False

            for line in lines:
                if line.strip() == 'dependencies:':
                    in_dependencies = True
                    new_lines.append(line)
                    new_lines.append('  flutter:\n')
                    new_lines.append('    sdk: flutter\n')

                    for dep, version in dependencies.items():
                        new_lines.append(f'  {dep}: {version}\n')

                elif in_dependencies and line.startswith('  ') and ':' in line:
                    continue
                elif in_dependencies and not line.startswith('  ') and line.strip():
                    in_dependencies = False
                    new_lines.append(line)
                else:
                    new_lines.append(line)

            with open(pubspec_path, 'w') as f:
                f.writelines(new_lines)

            print("✅ Fixed pubspec.yaml with BULLETPROOF dependencies")

        except Exception as e:
            print(f"⚠️ Warning: Could not fix pubspec.yaml: {e}")

    def _fix_gradle_files(self, project_path: str):
        project_gradle = os.path.join(project_path, 'android/build.gradle')
        if os.path.exists(project_gradle):
            try:
                with open(project_gradle, 'r') as f:
                    content = f.read()

                if 'com.android.tools.build:gradle:' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'com.android.tools.build:gradle:' in line:
                            lines[i] = "        classpath 'com.android.tools.build:gradle:8.1.4'"
                    content = '\n'.join(lines)

                if 'ext.kotlin_version' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'ext.kotlin_version' in line:
                            lines[i] = "    ext.kotlin_version = '1.9.10'"
                    content = '\n'.join(lines)

                with open(project_gradle, 'w') as f:
                    f.write(content)

                print("✅ Fixed project-level build.gradle")

            except Exception as e:
                print(f"⚠️ Warning: Could not fix project build.gradle: {e}")

    def _flutter_pub_get_with_retry(self, project_path: str, max_retries: int = 3):
        for attempt in range(max_retries):
            try:
                print(f"📦 Running flutter pub get (attempt {attempt + 1}/{max_retries})...")

                if attempt > 0:
                    subprocess.run(['flutter', 'pub', 'cache', 'clean'], 
                                 cwd=project_path, 
                                 capture_output=True, 
                                 text=True,
                                 shell=True)

                result = subprocess.run(
                    ['flutter', 'pub', 'get'],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    shell=True
                )

                if result.returncode == 0:
                    print("✅ Dependencies fetched successfully")
                    return
                else:
                    print(f"⚠️ Pub get attempt {attempt + 1} failed:")
                    print(result.stderr)
                    if attempt == max_retries - 1:
                        raise Exception(f"Flutter pub get failed: {result.stderr}")

            except subprocess.TimeoutExpired:
                print(f"⏰ Pub get attempt {attempt + 1} timed out")
                if attempt == max_retries - 1:
                    raise Exception("Flutter pub get timed out")
            except Exception as e:
                print(f"❌ Pub get attempt {attempt + 1} error: {e}")
                if attempt == max_retries - 1:
                    raise e

    def _build_apk_with_fixes(self, project_path: str, state: AppGenerationState) -> str:
        original_cwd = os.getcwd()
        max_build_attempts = 2

        try:
            for attempt in range(max_build_attempts):
                try:
                    print(f"🔨 Building APK (attempt {attempt + 1}/{max_build_attempts})...")

                    os.chdir(project_path)

                    if attempt > 0:
                        print("Running flutter clean for retry...")
                        subprocess.run(['flutter', 'clean'], cwd=project_path, capture_output=True, shell=True)
                        subprocess.run(['flutter', 'pub', 'get'], cwd=project_path, capture_output=True, shell=True)
                    else:
                        print("Running flutter clean...")
                        result = subprocess.run(['flutter', 'clean'], capture_output=True, text=True, timeout=60, shell=True)
                        if result.returncode != 0:
                            print(f"Flutter clean warning: {result.stderr}")

                        print("Running flutter pub get...")
                        result = subprocess.run(['flutter', 'pub', 'get'], capture_output=True, text=True, timeout=120, shell=True)

                        if result.returncode != 0:
                            print(f"Pub get STDOUT: {result.stdout}")
                            print(f"Pub get STDERR: {result.stderr}")
                            raise Exception(f"Flutter pub get failed: {result.stderr}")

                        print("Dependencies fetched successfully")

                    print("Building release APK...")
                    build_result = subprocess.run(
                        ['flutter', 'build', 'apk', '--release'],
                        capture_output=True,
                        text=True,
                        timeout=600,
                        shell=True
                    )

                    if build_result.returncode == 0:
                        temp_apk_path = os.path.join(project_path, 'build', 'app', 'outputs', 'flutter-apk', 'app-release.apk')

                        if not os.path.exists(temp_apk_path):
                            alt_paths = [
                                os.path.join(project_path, 'build', 'app', 'outputs', 'apk', 'release', 'app-release.apk'),
                                os.path.join(project_path, 'build', 'app', 'outputs', 'apk', 'app-release.apk')
                            ]

                            for alt_path in alt_paths:
                                if os.path.exists(alt_path):
                                    temp_apk_path = alt_path
                                    break
                            else:
                                raise Exception(f"APK not found at expected location: {temp_apk_path}")

                        print(f"APK built at temporary location: {temp_apk_path}")

                        session_id = state.get('session_id', 'unknown')
                        # Generate app name from user prompt
                        requirements = state.get('structured_requirements', {})
                        app_name = requirements.get('app_name', 'bluetooth_app')
                        app_name_clean = re.sub(r'[^a-zA-Z0-9_]', '_', app_name.lower())
                        apk_filename = f"{app_name_clean}_{session_id[:8]}.apk"


                        # Save to project output folder (current working directory)
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        project_root = os.path.dirname(current_dir)  # Go up from agents folder
                        permanent_dir = os.path.join(project_root, 'output')
                        os.makedirs(permanent_dir, exist_ok=True)

                        final_apk_path = os.path.join(permanent_dir, apk_filename)
                        shutil.copy2(temp_apk_path, final_apk_path)

                        print(f"✅ PROFESSIONAL APK ready: {final_apk_path}")
                        return final_apk_path

                    else:
                        error_output = build_result.stderr
                        print(f"❌ Build attempt {attempt + 1} failed:")
                        print("STDOUT:", build_result.stdout)
                        print("STDERR:", error_output)

                        if attempt == max_build_attempts - 1:
                            raise Exception(f"Build failed with exit code {build_result.returncode}. Check output above.")

                except subprocess.TimeoutExpired:
                    if attempt == max_build_attempts - 1:
                        raise Exception("Build timeout - operation took longer than expected")
                    print("⏰ Build timed out, retrying...")

                except Exception as e:
                    if attempt == max_build_attempts - 1:
                        raise Exception(f"APK build failed: {str(e)}")
                    print(f"🔄 Build attempt {attempt + 1} failed, retrying: {e}")

            raise Exception("All build attempts failed")

        finally:
             os.chdir(original_cwd)