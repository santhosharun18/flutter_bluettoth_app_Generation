import os
import re
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AnthropicClient:
    def __init__(self, model_name="claude-3-haiku-20240307"):
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.model = model_name

    def chat_completion(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API error: {e}")
            raise Exception(f"Failed to get response from Anthropic: {str(e)}")

    def generate_code(self, prompt: str) -> str:
        '''Generate dynamic Flutter code using AI with proper reference guidelines.'''

        system_prompt = '''
You are an expert Flutter developer. Generate DYNAMIC, CUSTOMIZED Flutter Bluetooth apps based on user requests.

**CRITICAL VARIABLE DECLARATION RULES:**
ALWAYS declare these variables in State class:
```dart
class _BluetoothScreenState extends State<BluetoothScreen> {
  List<ScanResult> scanResults = [];
  BluetoothDevice? connectedDevice;
  BluetoothCharacteristic? writeCharacteristic;
  bool isScanning = false;
  String connectionStatus = "Ready";
  bool permissionsGranted = false;
```

**FLUTTER API REQUIREMENTS:**
- Use backgroundColor: Colors.green (NOT primary:)
- Use foregroundColor: Colors.white (NOT onPrimary:)
- Use command.codeUnits (NOT Uint8List.fromList())
- Use FlutterBluePlus.startScan() (NOT _flutterBlue)
- Use cardTheme: CardThemeData (NOT CardTheme)

**BLUETOOTH REFERENCE PATTERN:**
```dart
// Permission request
var locationStatus = await Permission.locationWhenInUse.request();
await Permission.bluetoothScan.request();

// Scanning
await FlutterBluePlus.startScan(timeout: Duration(seconds: 10));
FlutterBluePlus.scanResults.listen((results) {
  setState(() { scanResults = results; });
});

// Send commands
await writeCharacteristic!.write(command.codeUnits);
```

**DYNAMIC UI GENERATION RULES:**
Analyze the user request and create appropriate UI:

1. **For "neopixel on/off"**: Generate ON/OFF buttons sending "1"/"2"
2. **For "temperature"**: Create temperature display cards with gauges
3. **For "slider control"**: Add sliders with real-time value updates
4. **For "color picker"**: Include color selection interface
5. **For "sensor dashboard"**: Multiple data cards with icons

**REQUIRED IMPORTS:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';
```

**GENERATE COMPLETE APP:** Create full MyApp, BluetoothScreen, and UI based on user's specific request. Make it unique and customized to their needs while following the reference patterns.
'''

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            generated_code = response.content[0].text

            # Apply smart fixes to ensure compatibility
            fixed_code = self._smart_api_fixes(generated_code)

            return fixed_code

        except Exception as e:
            print(f"Code generation error: {e}")
            raise Exception(f"Failed to generate code: {str(e)}")

    def _smart_api_fixes(self, code: str) -> str:
        '''Apply targeted fixes while preserving AI creativity.'''

        # Fix 1: Replace _devices with scanResults
        code = re.sub(r'_devices\s*=.*?results.*?\.toList\(\);', 
                     'setState(() { scanResults = results; });', code)
        code = code.replace('_devices', 'scanResults')

        # Fix 2: Fix deprecated button parameters
        code = re.sub(r'primary:\s*(Colors\.\w+)', r'backgroundColor: \1', code)
        code = re.sub(r'onPrimary:\s*(Colors\.\w+)', r'foregroundColor: \1', code)

        # Fix 3: Fix Uint8List usage
        code = code.replace('Uint8List.fromList([int.parse(command)])', 'command.codeUnits')
        code = code.replace('Uint8List.fromList(command.codeUnits)', 'command.codeUnits')

        # Fix 4: Replace _flutterBlue references
        code = code.replace('_flutterBlue.', 'FlutterBluePlus.')

        # Fix 5: Fix theme API
        code = code.replace('CardTheme(', 'CardThemeData(')
        code = code.replace('ElevatedButtonTheme(', 'ElevatedButtonThemeData(')

        # Fix 6: Add missing imports if needed
        required_imports = [
            "import 'package:flutter/material.dart';",
            "import 'package:flutter_blue_plus/flutter_blue_plus.dart';",
            "import 'package:permission_handler/permission_handler.dart';",
            "import 'dart:io';"
        ]

        for import_stmt in required_imports:
            if import_stmt not in code:
                code = import_stmt + "\n" + code

        return code

    def analyze_prompt(self, user_prompt: str) -> str:
        '''Analyze user prompt dynamically.'''

        system_prompt = '''
Analyze the Bluetooth app request and return JSON with detected features.

Detect from prompt:
- "temperature", "temp" → add "temperature_display" to ui_components
- "humidity" → add "humidity_display" 
- "slider", "brightness" → add "sliders"
- "color", "rgb" → add "color_picker"
- "sensor", "data" → add "sensor_displays"
- "on", "off", "button" → add "control_buttons"

Generate app name based on request (e.g., "Temperature Monitor", "RGB Controller", etc.)

Return ONLY JSON:
{
  "app_name": "Dynamic name based on request",
  "description": "Brief description", 
  "features": ["bluetooth_scanning", "device_connection", "data_transmission"],
  "ui_components": ["detected_components"],
  "control_types": ["buttons", "sliders"],
  "color_theme": "gradient_blue_purple",
  "complexity": "professional"
}
'''

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Prompt analysis error: {e}")
            return '{"app_name": "Bluetooth Controller", "description": "Professional Bluetooth application", "features": ["bluetooth_scanning", "device_connection", "data_transmission"], "ui_components": ["status_card", "control_buttons", "device_list"], "control_types": ["buttons"], "color_theme": "gradient_blue_purple", "complexity": "professional"}'