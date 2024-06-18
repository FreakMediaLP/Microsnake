# Microsnake
Micropython Snake Game for ESP32 using SSD1306 OLED Screen ([Original C++ Version](https://wokwi.com/projects/296135008348799496))

## Hardware Setup

### 1. Connect Screen
- Connect `VCC` from Screen with `3V3` on ESP32
  - Connect `SCL` from Screen with `G22`
  - Connect `SDA` from Screen with `G21`
- Connect Ground (`GND`)

### 2. Connect Buttons

1. Connect one Button side with ESP32
   - UP with Pin `G32`
   - RIGHT with Pin `G25`
   - DOWN with Pin `G26`
   - LEFT with Pin `G27`


2. Connect second Pin on each Button witch Ground (`GND`)


### 3. Connect Buzzer (optional)

- Connect `+` from Buzzer with `G19`
- Connect `-` from Buzzer with Ground (`GND`)

## Software Setup

### 1. Flash Python Interpreter on EPS32


### 2. Push Game Files on EPS32
