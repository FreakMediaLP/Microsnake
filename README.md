# Microsnake
Micropython Snake Game for ESP32 using SSD1306 OLED Screen ([Original C++ Version](https://wokwi.com/projects/296135008348799496))

## Hardware Setup

### 1. Connect Screen
- Connect `VCC` from Screen with `3V3` on ESP32
  - Connect `SCL` from Screen with `G32`
  - Connect `SDA` from Screen with `G33`
- Connect Ground (`GND`)

### 2. Connect Buttons

1. Connect one Button side with ESP32
   - LEFT with Pin `G25`
   - UP with Pin `G26`
   - RIGHT with Pin `G27`
   - DOWN with Pin `G13`


2. Connect second Pin on each Button witch Ground (`GND`)


### 3. Connect Buzzer (optional)

- Connect `+` from Buzzer with `G14`
- Connect `-` from Buzzer with Ground (`GND`)

## Software Setup

### 1. Flash Python Interpreter on EPS32

Use a tool f.E. Thonny to flash the Micropython Interpreter to the ESP32

### 2. Push Game Files on EPS32

Save following files on the ESP32:
- `boot.py`
- `snake.py`
- `ssd1306.py`
- `settings.json`