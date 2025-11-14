import os
import re
from models.app_state import AppGenerationState
from services.anthropic_client import AnthropicClient

class CodeGeneratorAgent:
    def __init__(self):
        self.anthropic_client = AnthropicClient()
        self.max_retry_attempts = 3

    def process(self, state: AppGenerationState) -> AppGenerationState:
        """Generate complete enhanced Bluetooth code with multi-device support."""

        try:
            print("🚀 Starting COMPLETE ENHANCED MULTI-DEVICE generation...")

            project_path = state.get('project_path')
            if not project_path:
                raise Exception("Project path not found.")

            # Generate code using complete enhanced template
            generated_code = self._generate_complete_enhanced_template(state)

            # Write the generated code
            main_dart_path = os.path.join(project_path, 'lib/main.dart')
            self._write_code_to_file(main_dart_path, generated_code)

            state['generated_files'] = {'lib/main.dart': generated_code}
            state['current_agent'] = 'build_automator'
            state['progress'] = 80

            print("🎉 COMPLETE ENHANCED MULTI-DEVICE generation completed successfully")

        except Exception as e:
            print(f"💥 Critical error during code generation: {str(e)}")
            state['error_log'].append(f"Template generation failed: {str(e)}")
            state['current_agent'] = 'error'
            state['build_status'] = 'failed'

        return state

    def _generate_complete_enhanced_template(self, state: AppGenerationState) -> str:
        """Generate complete enhanced template with all board sensor support."""

        requirements = state.get('structured_requirements', {})
        user_prompt = state.get('user_prompt', '').lower()
        hardware_commands = state.get('hardware_commands', '')

        print(f"🔍 Analyzing prompt for COMPLETE ENHANCED features: {user_prompt[:100]}...")

        # COMPLETE FEATURE DETECTION with hardware commands support
        multi_devices = self._detect_multi_devices(user_prompt, requirements, hardware_commands)
        has_buttons = len(multi_devices) > 0 or self._detect_buttons(user_prompt, requirements)
        has_brightness = self._detect_brightness(user_prompt, requirements)
        has_speed = self._detect_speed(user_prompt, requirements)
        has_rgb = self._detect_rgb(user_prompt, requirements)
        has_temperature = self._detect_temperature(user_prompt, requirements)
        has_humidity = self._detect_humidity(user_prompt, requirements)
        has_light = self._detect_light_sensor(user_prompt, requirements)
        has_distance = self._detect_distance_sensor(user_prompt, requirements)
        has_motion = self._detect_motion_sensor(user_prompt, requirements)
        has_moisture = self._detect_moisture_sensor(user_prompt, requirements)
        has_joystick = self._detect_joystick(user_prompt, requirements)
        has_servo = self._detect_servo_controls(user_prompt, requirements)

        # Generate components
        sensor_cards = self._generate_complete_sensor_cards(has_temperature, has_humidity, has_light, has_distance, has_motion, has_moisture)
        control_buttons = self._generate_multi_device_controls(multi_devices, has_buttons)
        slider_controls = self._generate_complete_slider_controls(has_brightness, has_speed, has_rgb, has_servo)
        input_controls = self._generate_input_controls(has_joystick)

        app_name = requirements.get('app_name', 'Professional Bluetooth Controller')

        print(f"✅ COMPLETE Features: Devices={len(multi_devices)}, Buttons={has_buttons}, Sensors={has_temperature or has_humidity or has_light}")

        # COMPLETE ENHANCED TEMPLATE WITH GRASP JSON SUPPORT
        template_code = f"""import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{app_name}',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: BluetoothScreen(),
      debugShowCheckedModeBanner: false,
    );
  }}
}}

class BluetoothScreen extends StatefulWidget {{
  @override
  _BluetoothScreenState createState() => _BluetoothScreenState();
}}

class _BluetoothScreenState extends State<BluetoothScreen> {{
  // Professional Bluetooth variables
  List<ScanResult> scanResults = [];
  BluetoothDevice? connectedDevice;
  BluetoothCharacteristic? writeCharacteristic;
  BluetoothCharacteristic? readCharacteristic;
  bool isScanning = false;
  bool isConnecting = false;
  String connectionStatus = "Ready to scan";
  bool permissionsGranted = false;
  int dataPackets = 0;
  int receivedPackets = 0;
  String deviceId = "Unknown";
  Timer? dataTimer;

  // GRASP board support
  String currentDeviceId = "Unknown";
  Map<String, DateTime> deviceLastSeen = {{}};
  Set<String> connectedDevices = {{}};

  // Complete sensor data variables
  String temperatureValue = "--";
  String humidityValue = "--";
  String lightValue = "--";
  String distanceValue = "--";
  String motionValue = "Still";
  String moistureValue = "--";
  String joystickX = "0";
  String joystickY = "0";

  // Complete control variables
  double brightnessValue = 50.0;
  double speedValue = 50.0;
  double redValue = 255.0;
  double greenValue = 255.0;
  double blueValue = 255.0;
  double servoPosition = 90.0;

  @override
  void initState() {{
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {{
      requestPermissions();
    }});
  }}

  @override
  void dispose() {{
    dataTimer?.cancel();
    super.dispose();
  }}

  Future<void> requestPermissions() async {{
    try {{
      setState(() => connectionStatus = "Requesting permissions...");

      var locationStatus = await Permission.locationWhenInUse.request();

      if (locationStatus == PermissionStatus.granted) {{
        if (Platform.isAndroid) {{
          await Permission.bluetoothScan.request();
          await Permission.bluetoothConnect.request();
        }}

        setState(() {{
          permissionsGranted = true;
          connectionStatus = "Permissions granted - Ready to scan";
        }});
      }} else {{
        setState(() {{
          permissionsGranted = false;
          connectionStatus = "Location permission required";
        }});

        if (mounted) {{
          showDialog(
            context: context,
            builder: (context) => AlertDialog(
              title: Text('Permission Required'),
              content: Text('Location permission is needed for Bluetooth scanning.'),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: Text('OK'),
                ),
              ],
            ),
          );
        }}
      }}
    }} catch (e) {{
      setState(() {{
        permissionsGranted = false;
        connectionStatus = "Permission error: $e";
      }});
    }}
  }}

  Future<void> startScan() async {{
    if (!permissionsGranted || isScanning) return;

    setState(() {{
      isScanning = true;
      scanResults.clear();
      connectionStatus = "Scanning...";
    }});

    try {{
      await FlutterBluePlus.startScan(timeout: Duration(seconds: 10));

      FlutterBluePlus.scanResults.listen((results) {{
        if (mounted) {{
          setState(() {{
            scanResults = results;
            connectionStatus = "Found ${{results.length}} devices";
          }});
        }}
      }});

      await Future.delayed(Duration(seconds: 10));
      await FlutterBluePlus.stopScan();

      if (mounted) {{
        setState(() {{
          connectionStatus = scanResults.isEmpty ? "No devices found" : "Scan complete";
        }});
      }}
    }} catch (e) {{
      if (mounted) {{
        setState(() {{
          connectionStatus = "Scan failed: $e";
        }});
      }}
    }} finally {{
      if (mounted) {{
        setState(() => isScanning = false);
      }}
    }}
  }}

  Future<void> connectToDevice(BluetoothDevice device) async {{
    if (isConnecting) return;

    setState(() {{
      isConnecting = true;
      connectionStatus = "Connecting...";
    }});

    try {{
      await device.connect();

      List<BluetoothService> services = await device.discoverServices();

      // Find write and read characteristics
      for (BluetoothService service in services) {{
        for (BluetoothCharacteristic char in service.characteristics) {{
          if (char.properties.write) {{
            writeCharacteristic = char;
          }}
          if (char.properties.read || char.properties.notify) {{
            readCharacteristic = char;

            // Enable notifications for real-time data
            if (char.properties.notify) {{
              await char.setNotifyValue(true);
              char.onValueReceived.listen((value) {{
                String data = String.fromCharCodes(value);
                _parseReceivedData(data);
              }});
            }}
          }}
        }}
      }}

      setState(() {{
        connectedDevice = device;
        deviceId = device.platformName.isNotEmpty ? device.platformName : "Unknown Device";
        connectionStatus = "Connected to $deviceId";
      }});

      // Start periodic data reading
      _startDataReading();

    }} catch (e) {{
      setState(() {{
        connectionStatus = "Connection failed: $e";
      }});
    }} finally {{
      setState(() => isConnecting = false);
    }}
  }}

  Future<void> disconnectDevice() async {{
    if (connectedDevice != null) {{
      try {{
        dataTimer?.cancel();
        await connectedDevice!.disconnect();
        setState(() {{
          connectedDevice = null;
          writeCharacteristic = null;
          readCharacteristic = null;
          deviceId = "Unknown";
          currentDeviceId = "Unknown";
          connectionStatus = "Disconnected - Ready to scan";
        }});

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Device disconnected"),
            backgroundColor: Colors.orange,
          ),
        );
      }} catch (e) {{
        setState(() {{
          connectionStatus = "Disconnect failed: $e";
        }});
      }}
    }}
  }}

  void _startDataReading() {{
    dataTimer = Timer.periodic(Duration(seconds: 2), (timer) {{
      if (connectedDevice == null) {{
        timer.cancel();
        return;
      }}
      _requestSensorData();
    }});
  }}

  void _requestSensorData() async {{
    if (readCharacteristic != null) {{
      try {{
        List<int> value = await readCharacteristic!.read();
        String data = String.fromCharCodes(value);
        _parseReceivedData(data);
      }} catch (e) {{
        // Silent fail for read attempts
      }}
    }}
  }}

  void _parseReceivedData(String data) {{
    setState(() {{
      receivedPackets++;

      try {{
        // First try to parse as JSON (GRASP format)
        if (data.trim().startsWith('{{')) {{
          _parseGraspJsonData(data);
        }} else {{
          // Fall back to simple string parsing
          _parseSimpleStringData(data);
        }}
      }} catch (e) {{
        print("Error parsing data: $e");
        // Try simple parsing as fallback
        _parseSimpleStringData(data);
      }}
    }});
  }}

  void _parseGraspJsonData(String jsonData) {{
    
    try {{
      Map<String, dynamic> json = jsonDecode(jsonData);

      // Extract device ID
      if (json.containsKey('Device_id')) {{
        String newDeviceId = json['Device_id'];
        currentDeviceId = newDeviceId;
        deviceId = newDeviceId;

        // Track multiple devices
        connectedDevices.add(newDeviceId);
        deviceLastSeen[newDeviceId] = DateTime.now();

        print("📱 Updated Device ID: $newDeviceId");
      }}

      // Parse parameters
      if (json.containsKey('Parameters')) {{
        Map<String, dynamic> parameters = json['Parameters'];

        parameters.forEach((paramKey, paramValue) {{
          if (paramValue is Map<String, dynamic> && paramValue.containsKey('Data')) {{
            Map<String, dynamic> data = paramValue['Data'];

            // Extract sensor values
            data.forEach((sensorType, value) {{
              switch (sensorType.toLowerCase()) {{
                case 'temperature':
                  temperatureValue = value.toString();
                  break;
                case 'humidity':
                  humidityValue = value.toString();
                  break;
                case 'light':
                case 'ldr':
                  lightValue = value.toString();
                  break;
                case 'distance':
                case 'ultrasonic':
                  distanceValue = value.toString();
                  break;
                case 'motion':
                case 'accelerometer':
                case 'gyroscope':
                  motionValue = value.toString();
                  break;
                case 'moisture':
                case 'soil':
                  moistureValue = value.toString();
                  break;
                case 'joystick_x':
                case 'joy_x':
                  joystickX = value.toString();
                  break;
                case 'joystick_y':
                case 'joy_y':
                  joystickY = value.toString();
                  break;
              }}
            }});
          }}
        }});
      }}
    }} catch (e) {{
      print("JSON parsing failed: $e");
    }}
  }}

  void _parseSimpleStringData(String data) {{
    
    // Simple string parsing
    if (data.contains('TEMP:')) {{
      temperatureValue = data.split('TEMP:')[1].split(',')[0];
    }}
    if (data.contains('HUMID:')) {{
      humidityValue = data.split('HUMID:')[1].split(',')[0];
    }}
    if (data.contains('LIGHT:')) {{
      lightValue = data.split('LIGHT:')[1].split(',')[0];
    }}
    if (data.contains('DIST:')) {{
      distanceValue = data.split('DIST:')[1].split(',')[0];
    }}
    if (data.contains('MOTION:')) {{
      motionValue = data.split('MOTION:')[1].split(',')[0];
    }}
    if (data.contains('MOISTURE:')) {{
      moistureValue = data.split('MOISTURE:')[1].split(',')[0];
    }}
    if (data.contains('JOY_X:')) {{
      joystickX = data.split('JOY_X:')[1].split(',')[0];
    }}
    if (data.contains('JOY_Y:')) {{
      joystickY = data.split('JOY_Y:')[1].split(',')[0];
    }}
    if (data.contains('BRIGHT:')) {{
      try {{
        brightnessValue = double.parse(data.split('BRIGHT:')[1].split(',')[0]);
      }} catch (e) {{}}
    }}
  }}

  Future<void> sendCommand(String command) async {{
    if (writeCharacteristic == null) {{
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("No device connected")),
      );
      return;
    }}

    try {{
      await writeCharacteristic!.write(command.codeUnits);
      setState(() {{ dataPackets++; }});

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Sent: $command"),
          backgroundColor: Colors.green,
          duration: Duration(seconds: 1),
        ),
      );
    }} catch (e) {{
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Send failed: $e")),
      );
    }}
  }}

  Future<void> sendSliderValue(String type, double value) async {{
    String command = "$type:${{value.round()}}";
    await sendCommand(command);
  }}

  // Smart font sizing based on Device ID length
  double _getDeviceIdFontSize(String value, String title) {{
    if (title != "Device ID") return 14;

    if (value.length <= 8) return 14;      // Short IDs: normal size
    if (value.length <= 12) return 12;     // Medium IDs: smaller
    return 10;                             // Long IDs: smallest
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('{app_name}'),
        backgroundColor: Colors.blue[600],
        elevation: 0,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.blue[600]!, Colors.blue[400]!],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: EdgeInsets.all(16),
            child: SingleChildScrollView(
              child: Column(
                children: [
                  // Status Row (ALWAYS PRESENT)
                  Row(
                    children: [
                      Expanded(
                        child: _buildStatusCard(
                          "Device ID",
                          deviceId,
                          Icons.settings,
                          Colors.blue[700]!,
                        ),
                      ),
                      SizedBox(width: 8),
                      Expanded(
                        child: _buildStatusCard(
                          "Sent",
                          dataPackets.toString(),
                          Icons.upload,
                          Colors.green[700]!,
                        ),
                      ),
                      SizedBox(width: 8),
                      Expanded(
                        child: _buildStatusCard(
                          "Received",
                          receivedPackets.toString(),
                          Icons.download,
                          Colors.orange[700]!,
                        ),
                      ),
                    ],
                  ),

                  SizedBox(height: 16),

                  // Complete Sensor Cards
{sensor_cards}

                  SizedBox(height: 16),

                  // Connection Status Card (ALWAYS PRESENT)
                  Card(
                    elevation: 8,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                    child: Container(
                      padding: EdgeInsets.all(20),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              Icon(
                                Icons.bluetooth,
                                color: Colors.amber[700],
                                size: 24,
                              ),
                              SizedBox(width: 10),
                              Text(
                                "Connection Status",
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 10),
                          Text(
                            connectionStatus,
                            style: TextStyle(fontSize: 14),
                            textAlign: TextAlign.center,
                          ),
                          SizedBox(height: 15),

                          // Scan Button
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton(
                              onPressed: (permissionsGranted && !isScanning) ? startScan : null,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.grey[300],
                                foregroundColor: Colors.black87,
                                padding: EdgeInsets.symmetric(vertical: 12),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                              ),
                              child: Text(
                                isScanning ? "Scanning devices..." : "Scan for devices",
                                style: TextStyle(fontSize: 14),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  // Multi-Device Controls
{control_buttons}

                  // Complete Slider Controls
{slider_controls}

                  // Input Controls
{input_controls}

                  SizedBox(height: 16),

                  // Available Devices List (ALWAYS PRESENT)
                  Container(
                    height: 350,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  "Available Devices",
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Container(
                                  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                  decoration: BoxDecoration(
                                    color: Colors.blue[600],
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Text(
                                    '${{scanResults.length}}',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 15),
                            Expanded(
                              child: scanResults.isEmpty
                                  ? Center(
                                      child: Column(
                                        mainAxisAlignment: MainAxisAlignment.center,
                                        children: [
                                          Icon(
                                            Icons.bluetooth_disabled,
                                            size: 50,
                                            color: Colors.grey[400],
                                          ),
                                          SizedBox(height: 10),
                                          Text(
                                            "No devices found",
                                            style: TextStyle(
                                              color: Colors.grey[600],
                                              fontSize: 16,
                                            ),
                                          ),
                                          Text(
                                            permissionsGranted 
                                                ? 'Tap "Scan for devices" to search'
                                                : 'Grant permissions first',
                                            style: TextStyle(
                                              color: Colors.grey[500],
                                              fontSize: 12,
                                            ),
                                          ),
                                        ],
                                      ),
                                    )
                                  : ListView.builder(
                                      itemCount: scanResults.length,
                                      itemBuilder: (context, index) {{
                                        final result = scanResults[index];
                                        final device = result.device;
                                        final isConnected = connectedDevice?.remoteId == device.remoteId;

                                        return Card(
                                          margin: EdgeInsets.only(bottom: 8),
                                          child: ListTile(
                                            leading: Container(
                                              padding: EdgeInsets.all(8),
                                              decoration: BoxDecoration(
                                                color: isConnected ? Colors.green[600] : Colors.blue[600],
                                                shape: BoxShape.circle,
                                              ),
                                              child: Icon(
                                                isConnected ? Icons.bluetooth_connected : Icons.bluetooth,
                                                color: Colors.white,
                                                size: 20,
                                              ),
                                            ),
                                            title: Text(
                                              device.platformName.isNotEmpty 
                                                  ? device.platformName 
                                                  : "Unknown Device",
                                              style: TextStyle(
                                                fontWeight: FontWeight.bold,
                                                fontSize: 14,
                                              ),
                                            ),
                                            subtitle: Column(
                                              crossAxisAlignment: CrossAxisAlignment.start,
                                              children: [
                                                Text(
                                                  device.remoteId.toString(),
                                                  style: TextStyle(fontSize: 12),
                                                ),
                                                if (isConnected)
                                                  Text(
                                                    "Connected",
                                                    style: TextStyle(
                                                      fontSize: 11,
                                                      color: Colors.green[700],
                                                      fontWeight: FontWeight.bold,
                                                    ),
                                                  ),
                                              ],
                                            ),
                                            trailing: ElevatedButton(
                                              onPressed: isConnected 
                                                  ? () => disconnectDevice()
                                                  : (isConnecting ? null : () => connectToDevice(device)),
                                              style: ElevatedButton.styleFrom(
                                                backgroundColor: isConnected 
                                                    ? Colors.red[600] 
                                                    : Colors.green[600],
                                                foregroundColor: Colors.white,
                                                padding: EdgeInsets.symmetric(
                                                  horizontal: 16,
                                                  vertical: 8,
                                                ),
                                              ),
                                              child: Text(
                                                isConnected 
                                                    ? "Disconnect" 
                                                    : "Connect",
                                                style: TextStyle(fontSize: 12),
                                              ),
                                            ),
                                          ),
                                        );
                                      }},
                                    ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),

                  SizedBox(height: 20), // Bottom padding
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }}

  Widget _buildStatusCard(String title, String value, IconData icon, Color color) {{
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        padding: EdgeInsets.all(12),
        child: Column(
          children: [
            Icon(icon, color: color, size: 20),
            SizedBox(height: 4),
            Text(
              title,
              style: TextStyle(
                fontSize: 10,
                color: Colors.grey[600],
              ),
            ),
            SizedBox(height: 2),
            // Dynamic sizing based on Device ID length
            Flexible(
              child: Text(
                value,
                style: TextStyle(
                  fontSize: _getDeviceIdFontSize(value, title),
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
                overflow: TextOverflow.ellipsis,
                maxLines: title == "Device ID" ? 2 : 1, // Allow 2 lines for long IDs
              ),
            ),
          ],
        ),
      ),
    );
  }}
}}
"""

        return template_code

    def _detect_multi_devices(self, user_prompt: str, requirements: dict, hardware_commands: str = '') -> dict:
        """Detect devices with custom or default commands."""

        devices = {}

        # PRIORITY 1: Parse hardware commands box if provided
        if hardware_commands.strip():
            print(f"🎯 Hardware commands found: {hardware_commands[:100]}...")
            devices = self._parse_hardware_commands_box(hardware_commands, user_prompt)
            if devices:
                print(f"✅ Custom commands parsed: {devices}")
                return devices

        # PRIORITY 2: Auto-detect from main prompt
        print("🔍 Using auto-detection from main prompt...")

        # Device detection patterns - ENHANCED
        device_patterns = {
            'relay': ['relay', 'switch relay', 'relay control'],
            'neopixel': ['neopixel', 'neo pixel', 'neopixels', 'rgb led', 'led strip'],
            'servo': ['servo', 'servo motor', 'motor servo'],
            'buzzer': ['buzzer', 'beeper', 'alarm sound', 'sound'],
            'laser': ['laser', 'laser pointer', 'light beam'],
            'motor': ['motor', 'dc motor', 'stepper motor'],
            'led': ['led', 'light', 'lamp']
        }

        command_counter = 1

        for device_type, keywords in device_patterns.items():
            if any(keyword in user_prompt.lower() for keyword in keywords):
                # Check if ON/OFF control is mentioned
                if any(word in user_prompt.lower() for word in ['on', 'off', 'control', 'switch', 'toggle']):
                    devices[device_type] = {
                        'on_command': str(command_counter),
                        'off_command': str(command_counter + 1),
                        'display_name': device_type.title()
                    }
                    command_counter += 2

        print(f"🔢 Default commands assigned: {devices}")
        return devices

    def _parse_hardware_commands_box(self, hardware_commands: str, user_prompt: str) -> dict:
        """Parse structured hardware commands from the second input box."""

        devices = {}
        lines = hardware_commands.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Parse: button "Turn On": sends "RELAY_START"
            if 'button' in line.lower() and 'sends' in line.lower():
                try:
                    # Extract button name and command
                    button_part = line.split(':')[0]  # button "Turn On"
                    command_part = line.split('sends')[1].strip()  # "RELAY_START"

                    # Get button name
                    button_name = ""
                    if '"' in button_part:
                        button_name = button_part.split('"')[1].lower()

                    # Get command
                    command = command_part.strip('"<>\'').strip()

                    # Determine device from user prompt or button context
                    device_type = self._guess_device_from_context(user_prompt, line)

                    if device_type not in devices:
                        devices[device_type] = {
                            'display_name': device_type.title()
                        }

                    # Assign command based on button name
                    if any(word in button_name for word in ['on', 'start', 'enable']):
                        devices[device_type]['on_command'] = command
                    elif any(word in button_name for word in ['off', 'stop', 'disable']):
                        devices[device_type]['off_command'] = command

                except Exception as e:
                    print(f"⚠️ Failed to parse line: {line} - {e}")
                    continue

        return devices

    def _guess_device_from_context(self, user_prompt: str, command_line: str) -> str:
        """Guess device type from context."""

        combined_text = (user_prompt + " " + command_line).lower()

        device_keywords = {
            'relay': ['relay', 'switch'],
            'neopixel': ['neopixel', 'led', 'rgb'],
            'servo': ['servo', 'motor'],
            'buzzer': ['buzzer', 'beep'],
            'laser': ['laser', 'light']
        }

        for device_type, keywords in device_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                return device_type

        return 'device'  # fallback

    # ENHANCED DETECTION FUNCTIONS
    def _detect_buttons(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if buttons are needed - ENHANCED."""
        button_keywords = ['button', 'on off', 'turn on', 'turn off', 'switch', 'toggle', 'control']
        exclude_keywords = ['monitor', 'station', 'sensor', 'data', 'read', 'receive', 'logging']

        if any(word in user_prompt for word in exclude_keywords):
            return False

        return any(word in user_prompt for word in button_keywords)

    def _detect_brightness(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if brightness control slider is needed - STRICT detection."""
        # Must explicitly mention brightness CONTROL, not just sensing
        brightness_keywords = ['brightness control', 'brightness slider', 'dimmer', 'light control', 'intensity control']

        # EXCLUDE sensor monitoring keywords
        exclude_keywords = ['sensor', 'monitoring', 'station', 'environmental', 'light sensor', 'monitor']

        # Don't trigger if it's clearly about monitoring/sensing
        if any(word in user_prompt.lower() for word in exclude_keywords):
            return False

        return any(word in user_prompt.lower() for word in brightness_keywords)

    def _detect_speed(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if speed slider is needed."""
        speed_keywords = ['speed', 'fast', 'slow', 'rate', 'velocity']
        return any(word in user_prompt for word in speed_keywords)

    def _detect_rgb(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if RGB sliders are needed - STRICT detection."""
        rgb_keywords = ['rgb control', 'color control', 'colour control', 'red green blue control']

        # EXCLUDE sensor monitoring
        exclude_keywords = ['monitor', 'station', 'sensor', 'environmental']

        if any(word in user_prompt.lower() for word in exclude_keywords):
            return False

        return any(word in user_prompt.lower() for word in rgb_keywords)

    def _detect_temperature(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if temperature card is needed."""
        temp_keywords = ['temperature', 'temp', 'dht11', 'thermal']
        return any(word in user_prompt for word in temp_keywords)

    def _detect_humidity(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if humidity card is needed."""
        humid_keywords = ['humidity', 'humid', 'dht11', 'moisture']
        return any(word in user_prompt for word in humid_keywords)

    # NEW ENHANCED SENSOR DETECTION FUNCTIONS
    def _detect_light_sensor(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if light sensor card is needed."""
        light_keywords = ['light sensor', 'ldr', 'brightness sensor', 'ambient light']
        return any(word in user_prompt for word in light_keywords)

    def _detect_distance_sensor(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if distance sensor card is needed."""
        distance_keywords = ['distance', 'ultrasonic', 'range', 'proximity']
        return any(word in user_prompt for word in distance_keywords)

    def _detect_motion_sensor(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if motion sensor card is needed."""
        motion_keywords = ['motion', 'accelerometer', 'gyroscope', 'imu', 'movement']
        return any(word in user_prompt for word in motion_keywords)

    def _detect_moisture_sensor(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if moisture sensor card is needed."""
        moisture_keywords = ['moisture', 'soil', 'water level', 'wet', 'dry']
        return any(word in user_prompt for word in moisture_keywords)

    def _detect_joystick(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if joystick control is needed - STRICT detection."""
        # Must explicitly mention joystick
        joystick_keywords = ['joystick', 'analog stick', 'game pad', 'joystick control']

        # Don't trigger on generic "controller" word
        return any(word in user_prompt.lower() for word in joystick_keywords)

    def _detect_servo_controls(self, user_prompt: str, requirements: dict) -> bool:
        """Detect if servo position slider is needed - STRICT detection."""
        # Must explicitly mention position/angle control
        servo_control_keywords = ['servo position', 'servo angle', 'position control', 'angle control', 'servo slider']

        # Exclude if only basic on/off control mentioned
        exclude_keywords = ['on off', 'on and off', 'turn on', 'turn off']

        if any(word in user_prompt.lower() for word in exclude_keywords):
            return False

        return any(word in user_prompt.lower() for word in servo_control_keywords)

    def _generate_complete_sensor_cards(self, has_temperature: bool, has_humidity: bool, has_light: bool, has_distance: bool, has_motion: bool, has_moisture: bool) -> str:
        """Generate all available sensor cards."""

        cards = []

        # Temperature card
        if has_temperature:
            cards.append("""                  // Temperature Sensor Card
                  Container(
                    height: 140,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.red[600]!, Colors.red[400]!],
                          ),
                        ),
                        child: Column(
                          children: [
                            Icon(Icons.thermostat, color: Colors.white, size: 30),
                            SizedBox(height: 8),
                            Text(
                              'Temperature',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.baseline,
                              textBaseline: TextBaseline.alphabetic,
                              children: [
                                Text(
                                  temperatureValue,
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 28,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Text(
                                  '°C',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 18,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),""")

        # Humidity card
        if has_humidity:
            cards.append("""                  
                  SizedBox(height: 16),

                  // Humidity Sensor Card
                  Container(
                    height: 140,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.teal[600]!, Colors.teal[400]!],
                          ),
                        ),
                        child: Column(
                          children: [
                            Icon(Icons.water_drop, color: Colors.white, size: 30),
                            SizedBox(height: 8),
                            Text(
                              'Humidity',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.baseline,
                              textBaseline: TextBaseline.alphabetic,
                              children: [
                                Text(
                                  humidityValue,
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 28,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Text(
                                  '%',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 18,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),""")

        # Light sensor card
        if has_light:
            cards.append("""                  
                  SizedBox(height: 16),

                  // Light Sensor Card
                  Container(
                    height: 140,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.amber[600]!, Colors.amber[400]!],
                          ),
                        ),
                        child: Column(
                          children: [
                            Icon(Icons.wb_sunny, color: Colors.white, size: 30),
                            SizedBox(height: 8),
                            Text(
                              'Light Level',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Text(
                              lightValue,
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 28,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),""")

        # Distance sensor card
        if has_distance:
            cards.append("""                  
                  SizedBox(height: 16),

                  // Distance Sensor Card
                  Container(
                    height: 140,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.purple[600]!, Colors.purple[400]!],
                          ),
                        ),
                        child: Column(
                          children: [
                            Icon(Icons.straighten, color: Colors.white, size: 30),
                            SizedBox(height: 8),
                            Text(
                              'Distance',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.baseline,
                              textBaseline: TextBaseline.alphabetic,
                              children: [
                                Text(
                                  distanceValue,
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 28,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Text(
                                  ' cm',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 18,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),""")

        # Motion sensor card
        if has_motion:
            cards.append("""                  
                  SizedBox(height: 16),

                  // Motion Sensor Card
                  Container(
                    height: 140,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.indigo[600]!, Colors.indigo[400]!],
                          ),
                        ),
                        child: Column(
                          children: [
                            Icon(Icons.directions_run, color: Colors.white, size: 30),
                            SizedBox(height: 8),
                            Text(
                              'Motion',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Text(
                              motionValue,
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 28,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),""")

        # Moisture sensor card
        if has_moisture:
            cards.append("""                  
                  SizedBox(height: 16),

                  // Moisture Sensor Card
                  Container(
                    height: 140,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.brown[600]!, Colors.brown[400]!],
                          ),
                        ),
                        child: Column(
                          children: [
                            Icon(Icons.opacity, color: Colors.white, size: 30),
                            SizedBox(height: 8),
                            Text(
                              'Soil Moisture',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.baseline,
                              textBaseline: TextBaseline.alphabetic,
                              children: [
                                Text(
                                  moistureValue,
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 28,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Text(
                                  '%',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 18,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),""")

        if not any([has_temperature, has_humidity, has_light, has_distance, has_motion, has_moisture]):
            # Default device status card
            cards.append("""                  // Default Device Status Card
                  Container(
                    height: 120,
                    child: Card(
                      elevation: 8,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      child: Container(
                        padding: EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.blue[600]!, Colors.blue[400]!],
                          ),
                        ),
                        child: Row(
                          children: [
                            Icon(Icons.devices, color: Colors.white, size: 40),
                            SizedBox(width: 20),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    'Device Status',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  SizedBox(height: 5),
                                  Text(
                                    connectedDevice != null 
                                        ? 'Connected: $currentDeviceId'
                                        : 'Disconnected',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 14,
                                    ),
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                  if (connectedDevices.length > 1)
                                    Text(
                                      '${connectedDevices.length} devices seen',
                                      style: TextStyle(
                                        color: Colors.white70,
                                        fontSize: 12,
                                      ),
                                    ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),""")

        return '\n'.join(cards)

    def _generate_multi_device_controls(self, multi_devices: dict, has_buttons: bool) -> str:
        """Generate multi-device specific controls."""

        if not has_buttons or not multi_devices:
            return ""

        device_sections = []

        for device_type, config in multi_devices.items():
            device_name = config['display_name']
            on_cmd = config['on_command']
            off_cmd = config['off_command']

            # Device-specific icons
            icon_map = {
                'relay': 'Icons.electrical_services',
                'neopixel': 'Icons.lightbulb',
                'servo': 'Icons.precision_manufacturing', 
                'buzzer': 'Icons.volume_up',
                'laser': 'Icons.flashlight_on',
                'motor': 'Icons.settings',
                'led': 'Icons.light'
            }

            icon = icon_map.get(device_type, 'Icons.power')

            device_sections.append(f"""
                        // {device_name} Control Section
                        Card(
                          margin: EdgeInsets.only(bottom: 12),
                          child: Padding(
                            padding: EdgeInsets.all(16),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    Icon({icon}, color: Colors.blue[700], size: 24),
                                    SizedBox(width: 10),
                                    Text(
                                      '{device_name} Control',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                                SizedBox(height: 15),
                                Row(
                                  children: [
                                    Expanded(
                                      child: ElevatedButton(
                                        onPressed: connectedDevice != null ? () => sendCommand("{on_cmd}") : null,
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.green[600],
                                          foregroundColor: Colors.white,
                                          padding: EdgeInsets.symmetric(vertical: 12),
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                        ),
                                        child: Row(
                                          mainAxisAlignment: MainAxisAlignment.center,
                                          children: [
                                            Icon(Icons.power_settings_new, size: 18),
                                            SizedBox(width: 6),
                                            Text('{device_name} ON'),
                                          ],
                                        ),
                                      ),
                                    ),
                                    SizedBox(width: 12),
                                    Expanded(
                                      child: ElevatedButton(
                                        onPressed: connectedDevice != null ? () => sendCommand("{off_cmd}") : null,
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.red[600],
                                          foregroundColor: Colors.white,
                                          padding: EdgeInsets.symmetric(vertical: 12),
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                        ),
                                        child: Row(
                                          mainAxisAlignment: MainAxisAlignment.center,
                                          children: [
                                            Icon(Icons.power_off, size: 18),
                                            SizedBox(width: 6),
                                            Text('{device_name} OFF'),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),""")

        return f"""
                  SizedBox(height: 16),

                  // Multi-Device Controls
                  Card(
                    elevation: 8,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                    child: Container(
                      padding: EdgeInsets.all(20),
                      child: Column(
                        children: [
                          Text(
                            'Device Controls',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 15),
{''.join(device_sections)}
                        ],
                      ),
                    ),
                  ),"""

    def _generate_complete_slider_controls(self, has_brightness: bool, has_speed: bool, has_rgb: bool, has_servo: bool) -> str:
        """Generate complete slider controls."""

        sliders = []

        # Brightness slider
        if has_brightness:
            sliders.append("""                        // Brightness Control
                        Card(
                          child: Padding(
                            padding: EdgeInsets.all(16),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    Icon(Icons.brightness_6, color: Colors.amber[700]),
                                    SizedBox(width: 10),
                                    Text(
                                      'Brightness',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    Spacer(),
                                    Text(
                                      '${brightnessValue.round()}%',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.amber[700],
                                      ),
                                    ),
                                  ],
                                ),
                                SizedBox(height: 10),
                                Slider(
                                  value: brightnessValue,
                                  min: 0,
                                  max: 100,
                                  divisions: 100,
                                  activeColor: Colors.amber[700],
                                  onChanged: (value) {
                                    setState(() {
                                      brightnessValue = value;
                                    });
                                  },
                                  onChangeEnd: (value) {
                                    sendSliderValue("BRIGHT", value);
                                  },
                                ),
                              ],
                            ),
                          ),
                        ),""")

        # Speed slider
        if has_speed:
            sliders.append("""                        
                        SizedBox(height: 10),

                        // Speed Control
                        Card(
                          child: Padding(
                            padding: EdgeInsets.all(16),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    Icon(Icons.speed, color: Colors.indigo[700]),
                                    SizedBox(width: 10),
                                    Text(
                                      'Speed',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    Spacer(),
                                    Text(
                                      '${speedValue.round()}%',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.indigo[700],
                                      ),
                                    ),
                                  ],
                                ),
                                SizedBox(height: 10),
                                Slider(
                                  value: speedValue,
                                  min: 0,
                                  max: 100,
                                  divisions: 100,
                                  activeColor: Colors.indigo[700],
                                  onChanged: (value) {
                                    setState(() {
                                      speedValue = value;
                                    });
                                  },
                                  onChangeEnd: (value) {
                                    sendSliderValue("SPEED", value);
                                  },
                                ),
                              ],
                            ),
                          ),
                        ),""")

        # Servo position slider
        if has_servo:
            sliders.append("""                        
                        SizedBox(height: 10),

                        // Servo Position Control
                        Card(
                          child: Padding(
                            padding: EdgeInsets.all(16),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    Icon(Icons.precision_manufacturing, color: Colors.green[700]),
                                    SizedBox(width: 10),
                                    Text(
                                      'Servo Position',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    Spacer(),
                                    Text(
                                      '${servoPosition.round()}°',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.green[700],
                                      ),
                                    ),
                                  ],
                                ),
                                SizedBox(height: 10),
                                Slider(
                                  value: servoPosition,
                                  min: 0,
                                  max: 180,
                                  divisions: 180,
                                  activeColor: Colors.green[700],
                                  onChanged: (value) {
                                    setState(() {
                                      servoPosition = value;
                                    });
                                  },
                                  onChangeEnd: (value) {
                                    sendSliderValue("SERVO", value);
                                  },
                                ),
                              ],
                            ),
                          ),
                        ),""")

        # RGB color sliders
        if has_rgb:
            sliders.append("""                        
                        SizedBox(height: 10),

                        // RGB Color Controls
                        Card(
                          child: Padding(
                            padding: EdgeInsets.all(16),
                            child: Column(
                              children: [
                                Text(
                                  'RGB Color Control',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                SizedBox(height: 15),

                                // Red Slider
                                Row(
                                  children: [
                                    Icon(Icons.circle, color: Colors.red),
                                    SizedBox(width: 10),
                                    Text('Red'),
                                    Spacer(),
                                    Text('${redValue.round()}'),
                                  ],
                                ),
                                Slider(
                                  value: redValue,
                                  min: 0,
                                  max: 255,
                                  divisions: 255,
                                  activeColor: Colors.red,
                                  onChanged: (value) {
                                    setState(() {
                                      redValue = value;
                                    });
                                  },
                                  onChangeEnd: (value) {
                                    sendSliderValue("RED", value);
                                  },
                                ),

                                // Green Slider
                                Row(
                                  children: [
                                    Icon(Icons.circle, color: Colors.green),
                                    SizedBox(width: 10),
                                    Text('Green'),
                                    Spacer(),
                                    Text('${greenValue.round()}'),
                                  ],
                                ),
                                Slider(
                                  value: greenValue,
                                  min: 0,
                                  max: 255,
                                  divisions: 255,
                                  activeColor: Colors.green,
                                  onChanged: (value) {
                                    setState(() {
                                      greenValue = value;
                                    });
                                  },
                                  onChangeEnd: (value) {
                                    sendSliderValue("GREEN", value);
                                  },
                                ),

                                // Blue Slider
                                Row(
                                  children: [
                                    Icon(Icons.circle, color: Colors.blue),
                                    SizedBox(width: 10),
                                    Text('Blue'),
                                    Spacer(),
                                    Text('${blueValue.round()}'),
                                  ],
                                ),
                                Slider(
                                  value: blueValue,
                                  min: 0,
                                  max: 255,
                                  divisions: 255,
                                  activeColor: Colors.blue,
                                  onChanged: (value) {
                                    setState(() {
                                      blueValue = value;
                                    });
                                  },
                                  onChangeEnd: (value) {
                                    sendSliderValue("BLUE", value);
                                  },
                                ),
                              ],
                            ),
                          ),
                        ),""")

        if not sliders:
            return ""

        return f"""
                  SizedBox(height: 16),

                  // Advanced Controls
                  Card(
                    elevation: 8,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                    child: Container(
                      padding: EdgeInsets.all(20),
                      child: Column(
                        children: [
                          Text(
                            'Advanced Controls',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 15),
{''.join(sliders)}
                        ],
                      ),
                    ),
                  ),"""

    def _generate_input_controls(self, has_joystick: bool) -> str:
        """Generate input control interfaces."""

        if not has_joystick:
            return ""

        return """
                  SizedBox(height: 16),

                  // Input Controls
                  Card(
                    elevation: 8,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                    child: Container(
                      padding: EdgeInsets.all(20),
                      child: Column(
                        children: [
                          Text(
                            'Joystick Input',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 15),
                          Row(
                            children: [
                              Expanded(
                                child: Card(
                                  child: Padding(
                                    padding: EdgeInsets.all(16),
                                    child: Column(
                                      children: [
                                        Icon(Icons.gamepad, color: Colors.purple[700]),
                                        SizedBox(height: 8),
                                        Text('X-Axis'),
                                        Text(
                                          joystickX,
                                          style: TextStyle(
                                            fontSize: 24,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(width: 16),
                              Expanded(
                                child: Card(
                                  child: Padding(
                                    padding: EdgeInsets.all(16),
                                    child: Column(
                                      children: [
                                        Icon(Icons.gamepad, color: Colors.purple[700]),
                                        SizedBox(height: 8),
                                        Text('Y-Axis'),
                                        Text(
                                          joystickY,
                                          style: TextStyle(
                                            fontSize: 24,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),"""

    def _write_code_to_file(self, file_path: str, code: str):
        """Write code to file with proper encoding and validation."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)

            if not os.path.exists(file_path):
                raise Exception(f"File was not created: {file_path}")

            file_size = os.path.getsize(file_path)
            if file_size < 1000:
                raise Exception(f"Generated file is too small ({file_size} bytes)")

            print(f"✅ COMPLETE ENHANCED TEMPLATE written: {file_path} ({file_size} bytes)")

        except Exception as e:
            raise Exception(f"Failed to write code to {file_path}: {str(e)}")
