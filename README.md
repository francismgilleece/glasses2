# OLED Information Display

A Raspberry Pi project that fetches information from various APIs and displays it on a 128x64 OLED screen.

## Hardware Specifications

- **Raspberry Pi Zero 2 W**
- **128x64 px OLED Display** (SSD1306 compatible)
- **SPI Connection**

### Wiring Diagram

| OLED Pin | Pi Pin | GPIO | Function |
|----------|--------|------|----------|
| VCC      | Pin 2  | 5V   | Power    |
| GND      | Pin 6  | GND  | Ground   |
| DIN      | Pin 19 | GPIO 10 | MOSI (Data) |
| CLK      | Pin 23 | GPIO 11 | SCLK (Clock) |
| CS       | Pin 24 | GPIO 8  | CE0 (Chip Select) |
| DC       | Pin 18 | GPIO 24 | Data/Command |
| RST      | Pin 22 | GPIO 25 | Reset |

## Quick Start

### 1. Enable SPI Interface
```bash
sudo raspi-config
# Navigate to: Interface Options -> SPI -> Enable
sudo reboot
```

### 2. Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Run Setup Verification
```bash
python3 setup_test.py
```

### 4. Test Display
```bash
python3 test_display_layout.py
```

## What the Test Shows

The display test creates a preview of the information layout:

```
┌──────────────────────┐
│ Date/Time Area       │
├──────────────────────┤
│ Weather Info         │
├──────────────────────┤
│ Additional Info      │
│ (Expandable)         │
│ Test: HH:MM:SS       │
└──────────────────────┘
```

### Test Sequence
1. **Layout Preview** - Shows labeled sections (5 seconds)
2. **Realistic Preview** - Shows actual data format (5 seconds)  
3. **Time Update Test** - Live time updates (10 seconds)

## APIs Configured

- **Weather**: OpenMeteo API (temperature, precipitation, sunrise/sunset)
- **Date/Time**: Always displayed (local time)

## Project Structure

```
glasses-simple/
├── requirements.txt           # Python dependencies
├── setup_test.py             # Setup verification
├── test_display_layout.py    # Display layout test
├── config/
│   └── hardware_config.py    # Hardware pin configuration
└── display/
    └── oled_manager.py       # OLED hardware management
```

## Troubleshooting

### Display Not Working
1. Check SPI is enabled: `ls /dev/spi*`
2. Verify wiring connections
3. Check power (5V) and ground connections
4. Ensure GPIO permissions: `sudo usermod -a -G gpio $USER`

### Package Installation Issues
```bash
# Update system packages first
sudo apt-get update
sudo apt-get install python3-pip python3-venv python3-dev

# For luma.oled dependencies
sudo apt-get install libfreetype6-dev libjpeg-dev
```

### Permission Errors
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
# Logout and login again
```

## Next Steps

After successful display test:
1. Implement weather API integration
2. Add configuration management
3. Create main application loop
4. Set up systemd service for auto-start

## Hardware Notes

- **Raspberry Pi Zero 2 W**: More powerful than original Zero, good for API calls
- **5V Power**: OLED requires 5V, not 3.3V
- **SPI Speed**: Default SPI speed should work fine for 128x64 display
- **Orientation**: Configured for landscape mode

## API Information

**Weather API**: Open-Meteo (no API key required)
- Endpoint: `https://api.open-meteo.com/v1/forecast`
- Data: Temperature, precipitation probability, sunrise/sunset
- Update frequency: Configurable (default: every 15 minutes) 