# 🚀 Flutter Bluetooth App Generator

<div align="center">

![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?logo=flutter)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.34-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**AI-Powered Low-Code Platform for IoT Application Development**

Transform natural language descriptions into production-ready Flutter Bluetooth Android applications in minutes using LangGraph multi-agent workflows and advanced AI models.

[Features](#-key-features) • [Installation](#-installation) • [Usage](#-usage-guide) • [Documentation](#-project-structure) • [Examples](#-examples) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [QR Code Download](#-qr-code-download-feature)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Multi-Agent Pipeline](#-multi-agent-pipeline)
- [Supported Hardware](#-supported-hardware)
- [API Reference](#-api-reference)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Advanced Configuration](#-advanced-configuration)
- [Contributing](#-contributing)
- [License](#-license)
- [Roadmap](#-roadmap)

---

## 🎯 Overview

The **Flutter Bluetooth App Generator** is a sophisticated code generation platform designed for rapid IoT application development. It eliminates the complexity of Bluetooth integration, Android permissions, and Flutter configuration by using a multi-agent AI system that handles the entire development lifecycle.

### **What Makes This Special?**

**Traditional Bluetooth App Development** requires:
- ❌ Deep understanding of Flutter and Dart
- ❌ BLE protocol knowledge (GATT, services, characteristics)
- ❌ Android permission handling (especially Android 12+)
- ❌ Gradle configuration and dependency management
- ❌ UI/UX design for device controls
- ❌ Hours or days of development time

**This Platform** reduces that to:
- ✅ A simple text description of what you want
- ✅ Optional hardware command specifications
- ✅ 2-5 minutes of automated generation
- ✅ A working APK ready for installation via QR code scan

---

## ✨ Key Features

### 🤖 **AI-Powered Generation**
- **Natural Language Processing**: Describe your app in plain English
- **Intelligent Feature Detection**: Automatically identifies sensors (temperature, humidity, light, distance, motion), control types (buttons, sliders, RGB), and device types (relay, LED, servo, motor)
- **Context-Aware Code Generation**: Produces Flutter code tailored to your specific hardware

### 📱 **Complete Bluetooth Integration**
- **BLE Central Role**: Full implementation using `flutter_blue_plus` for device scanning, connection management, and data exchange
- **Multi-Device Support**: Connect to and control multiple Bluetooth devices simultaneously
- **Real-Time Communication**: Asynchronous data streaming with BLE notifications
- **Modern Permission Handling**: Automatic Android 12+ permission requests (BLUETOOTH_SCAN, BLUETOOTH_CONNECT, BLUETOOTH_ADVERTISE, ACCESS_FINE_LOCATION)

### 🔌 **Extensive Hardware Support**
- **Actuators**: Relays, servos, motors, buzzers, lasers, neopixels, LED strips
- **Sensors**: DHT11/DHT22 (temp/humidity), LDR (light), ultrasonic (distance), IMU/accelerometer/gyroscope (motion), moisture
- **Input Devices**: Joysticks, buttons, potentiometers
- **Display Components**: Real-time sensor data visualization

### 🎨 **Dynamic UI Generation**
- **Smart Layout Creation**: Context-aware UI components based on detected hardware
- **Sensor Display Cards**: Real-time data visualization with units
- **Control Widgets**: Buttons, sliders, RGB color pickers
- **Connection Management**: Device list, status, scan/disconnect controls
- **Professional Theming**: Material Design 3 with gradient backgrounds

### 📦 **Production-Ready APK Build**
- **Automated Compilation**: Complete Flutter build pipeline with retry logic
- **Bulletproof Fixes**: Automatic corrections for deprecated APIs, permissions, and Gradle conflicts
- **QR Code Download**: Instant sharing via local network - **scan and install on your phone in seconds!**
- **Release Optimization**: Minified APKs with ProGuard (targetSdk 35, minSdk 21)

---

## 📸 Screenshots

### Web Interface

<table>
  <tr>
    <td align="center">
      <img src="screenshots/01_home_page.png" alt="Home Page" width="400"/><br/>
      <b>Home Page</b><br/>
      <sub>Enter app description and hardware commands</sub>
    </td>
    <td align="center">
      <img src="screenshots/02_progress.png" alt="Progress" width="400"/><br/>
      <b>Generation Progress</b><br/>
      <sub>Real-time multi-agent pipeline tracking</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/04_result_page.png" alt="Result Page" width="400"/><br/>
      <b>Result Page with QR Code</b><br/>
      <sub>Download via QR scan or direct button</sub>
    </td>
    <td align="center">
      <img src="screenshots/05_qr_code_scan_2.png" alt="Result Page" width="400"/><br/>
      <b>Result Page with  Code</b><br/>
      <sub>Gnerated code show </sub>
    </td>
    <td align="center">
      <img src="screenshots/05_qr_code_scan.png" alt="QR Scan" width="400"/><br/>
      <b>Mobile QR Code Scan</b><br/>
      <sub>Instant APK download to phone</sub>
    </td>
  </tr>
</table>

### Generated Mobile App

<table>
  <tr>
    <td align="center">
      <img src="screenshots/06_app_device_scanner.jpg" alt="Scanner" width="250"/><br/>
      <b>Device Scanner</b><br/>
      <sub>mobile qr scan </sub>
    </td>
    <td align="center">
      <img src="screenshots/06_app_device_scanner_2.jpg" alt="Scanner" width="250"/><br/>
      <b>Device Scanner</b><br/>
      <sub>BLE device discovery</sub>
    </td>
    <td align="center">
      <img src="screenshots/07_app_connected.jpg" alt="Connected" width="250"/><br/>
      <b>Connected View</b><br/>
      <sub>Real-time sensor data</sub>
    </td>
    <td align="center">
      <img src="screenshots/08_app_controls.jpg" alt="Controls" width="250"/><br/>
      <b>Control Interface</b><br/>
      <sub>Buttons, sliders, toggles</sub>
    </td>
  </tr>
  
</table>

### Installation Process

<table>
  <tr>
    <td align="center">
      <img src="screenshots/10_android_install.jpg" alt="Install" width="400"/><br/>
      <b>Android Installation</b><br/>
      <sub>APK install flow with permissions</sub>
    </td>
  </tr>
</table>

> 📝 **Note**: Screenshots show actual generated apps controlling real ESP32 Bluetooth devices with sensors and actuators.

---

## 📱 QR Code Download Feature

### **How It Works**

One of the **most powerful features** is the instant QR code download system:

1. **After APK generation completes**, the system automatically:
   - Gets your computer's local network IP address (e.g., `192.168.1.100`)
   - Creates a download URL: `http://192.168.1.100:5000/download/<session_id>`
   - Generates a QR code containing this URL
   - Displays it on the result page

2. **On your mobile device**:
   - Open any QR code scanner app (or your phone's camera)
   - Scan the QR code displayed on your computer screen
   - Your phone opens the download URL automatically
   - The APK starts downloading directly to your phone
   - Install and test immediately!

### **Network Requirements**

Both devices must be on the **same local network**:

Computer (Flask Server) Mobile Phone
192.168.1.100:5000 ←→ 192.168.1.50
Same WiFi Network

text

### **Technical Implementation**

The QR code generation is handled in `app.py`:

Get local IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()
s.close()

Create download URL
download_url = f"http://{ip_address}:5000/download/{session_id}"

Generate QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(download_url)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")

Convert to base64 for HTML display
img_buffer = io.BytesIO()
qr_img.save(img_buffer, format='PNG')
img_buffer.seek(0)
qrcode_data = base64.b64encode(img_buffer.getvalue()).decode()

text

### **Alternative Download Methods**

If QR code doesn't work:

| Method | Steps |
|--------|-------|
| **Direct Download** | Click "Download APK" button on computer, transfer via USB/cloud |
| **ADB Push** | `adb push app-release.apk /sdcard/Download/` |
| **Cloud Storage** | Upload to Google Drive/Dropbox, download on phone |

### **Troubleshooting QR Download**

| Issue | Solution |
|-------|----------|
| QR code doesn't appear | Check if APK was built successfully |
| Phone can't access URL | Ensure same WiFi network |
| "Connection refused" | Verify Flask server is running |
| Firewall blocking | Allow port 5000 in firewall settings |

---

## 🏗️ Architecture

The system implements a **stateful multi-agent workflow** using LangGraph, where specialized agents collaborate through a shared state object.

### **Agent Pipeline Flow**

User Input → Prompt Analyzer → Architecture Designer → Project Creator
→ Code Generator → Build Automator → APK Download (QR Code)

text

Each agent is an independent, specialized unit that:
- Receives the current application state
- Performs its specific task
- Updates the state with results
- Passes control to the next agent

### **State Management**

The `AppGenerationState` TypedDict maintains workflow continuity:

{
"messages": [], # Communication log
"user_prompt": str, # Original description
"hardware_commands": str, # Optional JSON commands
"structured_requirements": dict, # Parsed requirements
"flutter_structure": dict, # Project architecture
"generated_files": dict, # Code artifacts
"build_status": str, # pending/in_progress/completed/failed
"apk_path": str, # Final APK location
"current_agent": str, # Active agent name
"progress": int, # 0-100%
"error_log": list, # Error tracking
"session_id": str, # Unique identifier
"project_path": str, # Flutter project directory
"temp_dir": str # Temporary build location
}

text

---

## 🛠️ Technology Stack

### **Backend Framework**
- **Flask 3.0.0**: Web server with RESTful API endpoints
- **LangGraph 0.2.34**: Stateful workflow orchestration with conditional routing

### **AI Services**
- **Anthropic Claude Haiku**: Advanced code generation with 4000 token context
- **Groq**: Fast inference for prompt analysis and architecture design

### **Mobile Development**
- **Flutter SDK**: Cross-platform framework (tested with 3.x)
- **flutter_blue_plus 1.32.2**: BLE Central role implementation
- **permission_handler 11.3.0**: Runtime permission requests

### **Supporting Libraries**
- **LangChain Core 0.3.15**: Message handling and agent abstractions
- **python-dotenv 1.0.0**: Environment variable management
- **qrcode**: QR code generation for APK distribution

---

## 📦 Prerequisites

### **System Requirements**

1. **Python 3.8 or higher**
python --version # Should show 3.8+

text

2. **Flutter SDK (3.x recommended)**
- Download from [flutter.dev](https://flutter.dev)
- Add Flutter to your PATH
- Verify installation:
  ```
  flutter --version
  flutter doctor
  ```

3. **Android SDK**
- Install Android Studio or standalone Android SDK
- Required API levels: 21 (minimum) to 35 (target)
- Accept Android licenses:
  ```
  flutter doctor --android-licenses
  ```

4. **AI API Keys**
- **Anthropic API Key**: Get from [console.anthropic.com](https://console.anthropic.com)
- **Groq API Key**: Get from [console.groq.com](https://console.groq.com)
- At least one is required, both recommended for flexibility

### **Optional Tools**
- Git for version control
- VS Code or Android Studio for development
- Physical Android device for testing (recommended over emulator for Bluetooth)

---

## 🚀 Installation

### **Step 1: Clone the Repository**
git clone https://github.com/yourusername/flutter-bluetooth-app-generator.git
cd flutter-bluetooth-app-generator

text

### **Step 2: Create Virtual Environment**
Create virtual environment
python -m venv venv

Activate it
On Linux/Mac:
source venv/bin/activate

On Windows:
venv\Scripts\activate

text

### **Step 3: Install Python Dependencies**
pip install -r requirements.txt

text

This installs:
- Flask 3.0.0
- langchain-groq 0.1.9
- langchain-core 0.3.15
- langgraph 0.2.34
- anthropic 0.39.0
- python-dotenv 1.0.0
- typing-extensions 4.12.2

### **Step 4: Configure Environment Variables**
Copy example configuration
cp .env.example .env

Edit .env with your API keys
nano .env # or use any text editor

text

**Required `.env` content**:
AI Service API Keys
GROQ_API_KEY=gsk_your_groq_key_here
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here

Agent Configuration (groq or anthropic)
PROMPT_ANALYZER_SERVICE=groq
ARCHITECTURE_DESIGNER_SERVICE=groq
CODE_GENERATOR_SERVICE=anthropic

Flutter SDK Path (optional)
FLUTTER_SDK_PATH=/usr/local/flutter

text

### **Step 5: Verify Flutter Setup**
flutter doctor -v

text

Ensure you see:
- ✅ Flutter SDK installed
- ✅ Android toolchain ready
- ✅ Android licenses accepted

### **Step 6: Start the Application**
python app.py

text

You should see:
🧹 Performing startup cleanup of old temporary build directories...

Serving Flask app 'app'

Running on http://127.0.0.1:5000

text

### **Step 7: Access Web Interface**
Open your browser and navigate to:
http://localhost:5000

text

---

## ⚙️ Configuration

### **AI Service Selection**

Each agent can use a different AI provider:

| Agent | Recommended Service | Reason |
|-------|-------------------|---------|
| Prompt Analyzer | Groq | Fast inference for JSON extraction |
| Architecture Designer | Groq | Quick dependency resolution |
| Code Generator | Anthropic | Superior code quality and long context |

**To change configuration**, edit `.env`:
Use Anthropic for all agents
PROMPT_ANALYZER_SERVICE=anthropic
ARCHITECTURE_DESIGNER_SERVICE=anthropic
CODE_GENERATOR_SERVICE=anthropic

text

### **Flutter SDK Path**

If Flutter is not in your system PATH, specify the location:
FLUTTER_SDK_PATH=/custom/path/to/flutter

text

---

## 📖 Usage Guide

### **Basic Workflow**

1. **Start the Server**
python app.py

text

2. **Open Web Interface**
Navigate to `http://localhost:5000`

3. **Describe Your App**
Enter a natural language description. Examples:

- *"Create a Bluetooth app to control an RGB LED strip and display temperature from a DHT11 sensor"*
- *"Build an app to control 4 relays and monitor light levels with an LDR sensor"*
- *"I need an app to control a servo motor with a slider and turn on/off a buzzer"*

4. **Add Hardware Commands (Optional)**
Specify custom device commands in JSON format:
{
"relay": {"on": "R1", "off": "R0"},
"led": {"on": "L1", "off": "L0"},
"neopixel": {"command": "N{r},{g},{b}"},
"servo": {"command": "S{angle}"}
}

text

5. **Generate**
Click "Generate App" and watch the progress bar

6. **Download APK**
- **Method 1 (Recommended)**: Scan QR code with your phone for instant download
- **Method 2**: Click "Download APK" button
- Install and test!

### **Advanced Usage**

**Multi-Sensor Apps**:
Create an environmental monitoring app with:

Temperature sensor (DHT11)

Humidity sensor

Light sensor (LDR)

Display all readings in real-time

text

**Complex Control Systems**:
Build a smart home control app:

8 relays for lights/appliances

RGB LED strip with color picker

2 servo motors for curtain control

Motion sensor alerts

text

---

## 📁 Project Structure

flutter-bluetooth-app-generator/
│
├── app.py # Flask application & LangGraph workflow
├── config.py # AI service configuration & validation
├── requirements.txt # Python dependencies
├── .env # Environment variables (not in Git)
├── .env.example # Environment template
├── .gitignore # Git ignore rules
├── README.md # This file
│
├── services/ # AI client implementations
│ ├── init.py
│ ├── anthropic_client.py # Anthropic Claude API wrapper
│ └── groq_client.py # Groq API wrapper
│
├── agents/ # LangGraph multi-agent pipeline
│ ├── init.py
│ ├── prompt_analyzer.py # Feature detection & requirement parsing
│ ├── architecture_designer.py # Flutter project structure design
│ ├── project_creator.py # Flutter CLI project scaffolding
│ ├── code_generator.py # Dart/Flutter code generation
│ └── build_automator.py # APK compilation & fixes
│
├── models/ # Data models
│ ├── init.py
│ └── app_state.py # AppGenerationState TypedDict
│
├── templates/ # Flask HTML templates
│ ├── index.html # Main generation interface
│ └── result.html # APK download page with QR code
│
├── static/ # CSS/JS assets (optional)
│ └── style.css
│
└── screenshots/ # Project screenshots
├── 01_home_page.png
├── 02_progress.png
├── 04_result_page.png
├── 05_qr_code_scan.png
├── 06_app_device_scanner.png
├── 07_app_connected.png
├── 08_app_controls.png
├── 09_rgb_control.png
└── 10_android_install.png

text

---

## 🤝 Multi-Agent Pipeline

### **Agent 1: Prompt Analyzer**

**Purpose**: Analyzes user input to extract structured requirements

**Process**:
1. Receives raw user prompt and hardware commands
2. Enhances prompt with Bluetooth-specific context
3. Calls AI (Groq/Anthropic) to extract:
   - App name and description
   - Detected sensors (temperature, humidity, light, distance, motion, moisture)
   - Detected controls (buttons, sliders, RGB, joystick)
   - Device types (relay, neopixel, servo, buzzer, LED, motor)
   - UI preferences
4. Parses AI response (handles both JSON and markdown-wrapped JSON)
5. Updates state with `structured_requirements`

**Example Output**:
{
"app_name": "SmartHome Controller",
"description": "Control RGB LED and monitor temperature",
"sensors": ["temperature"],
"controls": ["rgb", "button"],
"devices": ["neopixel"],
"ui_preferences": {"theme": "modern", "layout": "cards"}
}

text

### **Agent 2: Architecture Designer**

**Purpose**: Designs Flutter project structure and dependencies

**Process**:
1. Receives structured requirements
2. Determines required Flutter packages:
   - Always includes: `flutter_blue_plus`, `permission_handler`
   - Conditional: `sensors_plus` (for motion), `geolocator` (for location)
3. Creates project architecture with package structure, dependencies, and widget structure
4. Updates state with `flutter_structure`

### **Agent 3: Project Creator**

**Purpose**: Scaffolds Flutter project using CLI

**Process**:
1. Sanitizes app name (lowercase, underscores, valid Dart identifier)
2. Creates temporary directory
3. Runs `flutter create` command
4. Updates `pubspec.yaml` with dependencies
5. Configures Android-specific settings:
   - **AndroidManifest.xml**: Adds all Bluetooth permissions
   - **build.gradle**: Sets `minSdkVersion 21`, `compileSdkVersion 35`, `targetSdkVersion 35`
6. Runs `flutter pub get` to fetch dependencies
7. Updates state with `project_path`

### **Agent 4: Code Generator**

**Purpose**: Generates complete Flutter Dart code

**Process**:
1. Analyzes requirements to determine code template
2. Generates complete `main.dart` with:
   - **Imports**: flutter_blue_plus, permission_handler, material
   - **State Variables**: device connections, sensor data, UI state
   - **Permission Handler**: Requests all necessary Bluetooth permissions
   - **Bluetooth Scanner**: Device discovery with filtering
   - **Connection Manager**: Connect/disconnect with error handling
   - **Data Parser**: GRASP JSON format and simple string format
   - **Device Controllers**: Send commands based on hardware_commands
   - **Dynamic UI**: Sensor cards, control buttons, sliders, color pickers
3. Applies AI post-processing for code quality
4. Writes code to `lib/main.dart`
5. Updates state with `generated_files`

### **Agent 5: Build Automator**

**Purpose**: Compiles Flutter project into release APK

**Process**:
1. **Bulletproof Fixes**: Validates variables, fixes deprecated APIs, injects permissions, updates Gradle
2. **Pre-build Setup**: Runs `flutter clean` and `flutter pub get` with retry
3. **APK Build**: Executes `flutter build apk --release` with error monitoring
4. **APK Collection**: Locates and copies built APK
5. **QR Code Generation**: Creates download URL and QR code image
6. Updates build status to `completed`

---

## 🔌 Supported Hardware

### **Actuators & Output Devices**

| Device | Default Commands | Customizable |
|--------|-----------------|--------------|
| Relay | `R1` (ON), `R0` (OFF) | ✅ |
| LED | `L1` (ON), `L0` (OFF) | ✅ |
| RGB LED / Neopixel | `N{r},{g},{b}` | ✅ |
| Servo Motor | `S{angle}` (0-180) | ✅ |
| DC Motor | `M{speed}` (0-255) | ✅ |
| Buzzer | `B1` (ON), `B0` (OFF) | ✅ |
| Laser | `Z1` (ON), `Z0` (OFF) | ✅ |

### **Sensors & Input Devices**

| Sensor | Data Format | UI Display |
|--------|------------|-----------|
| Temperature (DHT11/DHT22) | `TEMP:25.4` or JSON | Card with °C |
| Humidity | `HUMID:60` or JSON | Card with % |
| Light (LDR) | `LIGHT:450` or JSON | Card with lux |
| Distance (Ultrasonic) | `DIST:25.5` or JSON | Card with cm |
| Motion (IMU/Gyro) | `MOTION:x,y,z` or JSON | Card with axes |
| Moisture | `MOIST:35` or JSON | Card with % |
| Joystick | `JOY:x,y,button` | X/Y display |

### **Data Formats**

**GRASP JSON** (Recommended):
{
"type": "temperature",
"value": 25.4,
"unit": "C"
}

text

**Simple String** (Also supported):
TEMP:25.4
HUMID:60
LIGHT:450

text

---

## 🔗 API Reference

### **POST /generate**

Initiates app generation workflow

**Request**:
POST /generate HTTP/1.1
Content-Type: multipart/form-data

prompt: Create a Bluetooth app to control RGB LED
hardware_commands: {"led": {"on": "L1", "off": "L0"}}

text

**Response**:
{
"session_id": "uuid-here",
"message": "Generation started"
}

text

### **GET /api/progress/<session_id>**

Checks generation progress (poll every 2 seconds)

**Response**:
{
"current_agent": "code_generator",
"progress": 60,
"build_status": "in_progress",
"error_log": []
}

text

### **GET /result/<session_id>**

Displays result page with download link and QR code

**Response**: HTML page with APK download button and QR code

### **GET /download/<session_id>**

Downloads generated APK

**Response**: Binary APK file

### **GET /qrcode/<session_id>**

Returns QR code image

**Response**: PNG image (Base64 in JSON)

---

## 💡 Examples

### **Example 1: Simple LED Controller**

**Prompt**:
Create an app to turn on and off an LED via Bluetooth

text

**Hardware Commands** (optional):
{
"led": {"on": "L1", "off": "L0"}
}

text

**Generated Features**:
- Device scanner
- Connect/disconnect buttons
- ON/OFF toggle for LED
- Connection status indicator

---

### **Example 2: Temperature Monitor**

**Prompt**:
Build an app to display temperature readings from a DHT11 sensor

text

**Generated Features**:
- Temperature display card
- Real-time updates
- Unit display (°C)
- Connection management

---

### **Example 3: RGB LED Strip Controller**

**Prompt**:
Create an app to control an RGB LED strip with color picker and brightness slider

text

**Hardware Commands**:
{
"neopixel": {"command": "N{r},{g},{b}"}
}

text

**Generated Features**:
- Color picker widget
- Brightness slider (0-255)
- Preset color buttons
- Real-time preview

---

### **Example 4: Smart Home Controller**

**Prompt**:
Build a comprehensive smart home app with:

4 relays for lights and fans

Temperature and humidity monitoring

Motion detection alerts

RGB mood lighting control

text

**Hardware Commands**:
{
"relay1": {"on": "R1_ON", "off": "R1_OFF"},
"relay2": {"on": "R2_ON", "off": "R2_OFF"},
"relay3": {"on": "R3_ON", "off": "R3_OFF"},
"relay4": {"on": "R4_ON", "off": "R4_OFF"},
"rgb": {"command": "RGB_{r},{g},{b}"}
}

text

**Generated Features**:
- 4 relay control cards
- Temperature/humidity display
- Motion sensor alerts
- RGB color picker
- All real-time via BLE

---

## 🐛 Troubleshooting

### **Build Failures**

**Problem**: APK build fails with Gradle errors

**Solutions**:
1. Accept Android SDK licenses: `flutter doctor --android-licenses`
2. Update Flutter: `flutter upgrade`
3. Check `minSdkVersion` compatibility (should be 21)
4. Clear cache: `flutter clean && flutter pub get`

---

### **Permission Errors**

**Problem**: App crashes with permission denial

**Solutions**:
1. Verify AndroidManifest.xml contains all permissions
2. Android 12+ requires BLUETOOTH_SCAN, BLUETOOTH_CONNECT
3. Enable location services (required for BLE scanning)

---

### **API Errors**

**Problem**: "Failed to get response from Anthropic/Groq"

**Solutions**:
1. Verify API keys in `.env` are correct
2. Check API key permissions and billing
3. Test API connectivity
4. Switch to alternative AI provider in config

---

### **QR Code Download Issues**

**Problem**: QR code doesn't work

**Solutions**:
1. Ensure both devices on same WiFi network
2. Check Flask server is running on port 5000
3. Verify firewall allows port 5000
4. Try direct download button as alternative

---

### **Bluetooth Connection Issues**

**Problem**: App can't find or connect to devices

**Solutions**:
1. Ensure device is advertising BLE services
2. Check device not already connected elsewhere
3. Verify Bluetooth enabled on phone
4. Try scanning with nRF Connect app (troubleshooting tool)

---

## 🔧 Advanced Configuration

### **Custom AI Models**

Modify agent clients to use different models:

**anthropic_client.py**:
def init(self, model_name="claude-3-5-sonnet-20240620"): # Upgrade to Sonnet
self.model = model_name

text

**groq_client.py**:
self.model_name = "mixtral-8x7b-32768" # Use Mixtral instead of Llama

text

---

### **Build Optimization**

Enable more aggressive optimizations in `build_automator.py`:

build_command = [
'flutter', 'build', 'apk',
'--release',
'--obfuscate', # Code obfuscation
'--split-debug-info=debug', # Separate debug symbols
'--tree-shake-icons' # Remove unused icons
]

text

---

### **Timeout Configuration**

Adjust build timeout for slower machines:

In build_automator.py
result = subprocess.run(
build_command,
cwd=project_path,
timeout=600, # Increase from 300 to 600 seconds
...
)

text

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**: Generate apps with different features
5. **Commit with descriptive messages**: `git commit -m "Add stepper motor support"`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### **Areas for Contribution**

- Additional sensor support (GPS, compass, barometer)
- iOS app generation (currently Android-only)
- Advanced UI templates
- Custom widget library
- Performance optimizations
- Multi-language support
- Database integration (SQLite, Firebase)
- Cloud connectivity features
- Testing automation

---

## 📄 License

**MIT License**

Copyright (c) 2025 Santhosh D

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🙏 Acknowledgments

This project builds upon amazing open-source technologies:

- **LangGraph** by LangChain for multi-agent orchestration
- **Anthropic Claude** for intelligent code generation
- **Groq** for fast AI inference
- **Flutter** and **flutter_blue_plus** for cross-platform BLE
- The open-source community for countless tools and libraries

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/santhosharun18/flutter_bluettoth_app_Generation/issues)
- **Discussions**: [GitHub Discussions](https://github.com/santhosharun18/flutter_bluettoth_app_Generation/discussions)
- **Email**: santhosharun31@gmail.com

---

## 🗺️ Roadmap

### **Version 2.0 (Planned)**
- [ ] iOS app generation support
- [ ] Web app generation (Flutter Web)
- [ ] Custom UI theme editor
- [ ] Database integration (SQLite/Firebase)
- [ ] Cloud sync capabilities
- [ ] Advanced sensor fusion
- [ ] Machine learning on-device inference
- [ ] Wi-Fi configuration alongside Bluetooth

### **Version 1.1 (In Progress)**
- [x] QR code download feature
- [ ] Enhanced error messages
- [ ] Build caching for faster regeneration
- [ ] Template library for common IoT patterns
- [ ] Video tutorials

---

<div align="center">

**Built with ❤️ for the IoT and Flutter community**

If this project helps you, please give it a ⭐ on GitHub!

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/flutter-bluetooth-app-generator?style=social)](https://github.com/santhosharun18/flutter_bluettoth_app_Generation)

</div>
