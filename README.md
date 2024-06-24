# Microsnake
Micropython Snake Game for ESP32 using SSD1306 OLED Screen ([Original C++ Version](https://wokwi.com/projects/296135008348799496))

## Hardware Setup

### 1. Connect Screen
- Connect `VCC` from Screen with `3V3` on ESP32
  - Connect `SCL` from Screen with `G22`
  - Connect `SDA` from Screen with `G23`
- Connect Ground (`GND`)

### 2. Connect Buttons

1. Connect one Button side with ESP32
   - LEFT with Pin `G25`
   - UP with Pin `G26`
   - RIGHT with Pin `G27`
   - DOWN with Pin `G14`


2. Connect second Pin on each Button witch Ground (`GND`)


### 3. Connect Buzzer (optional)

- Connect `+` from Buzzer with `G19`
- Connect `-` from Buzzer with Ground (`GND`)

<img src="https://raw.githubusercontent.com/FreakMediaLP/Microsnake/main/circuit%20sketch.png" alt="Circuit Sketch" width="500">

## Software Setup

### 1. Flash Python Interpreter on EPS32

Use a tool f.E. [Thonny](https://thonny.org/) to flash the Micropython Interpreter to the ESP32

### 2. Push Game Files on EPS32

Save following files on the ESP32:
- `boot.py`
- `snake.py`
- `ssd1306.py`
- `settings.json`
