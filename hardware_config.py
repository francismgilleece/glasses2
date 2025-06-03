"""
Hardware configuration for Raspberry Pi Zero 2 W with 128x64 OLED display
Based on project specifications with SPI connection
"""

# OLED Display Configuration
OLED_CONFIG = {
    # Display dimensions
    'width': 128,
    'height': 64,
    'orientation': 'landscape',
    
    # SPI Pin Configuration (based on project specs)
    'spi_config': {
        'port': 0,  # SPI port
        'device': 0,  # CE0
        'gpio_dc': 24,  # Data/Command pin (Pin 18)
        'gpio_rst': 25,  # Reset pin (Pin 22)
        'gpio_cs': 8,   # Chip Select (CE0) (Pin 24)
    },
    
    # Display settings
    'contrast': 255,  # Max contrast
    'rotate': 0,      # 0 = landscape, 2 = landscape flipped
}

# Pin Reference (for documentation)
PIN_REFERENCE = {
    'VCC': 'Pin 2 (5V)',
    'GND': 'Pin 6 (Ground)', 
    'DIN_MOSI': 'Pin 19 (GPIO 10)',
    'CLK_SCLK': 'Pin 23 (GPIO 11)',
    'CS': 'Pin 24 (GPIO 8/CE0)',
    'DC': 'Pin 18 (GPIO 24)',
    'RST': 'Pin 22 (GPIO 25)'
} 