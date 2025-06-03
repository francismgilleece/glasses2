#!/usr/bin/env python3
"""
OLED Display Layout Test
Displays a preview of the layout showing what will be displayed in each position
Based on project specifications: 128x64 px OLED with SPI connection
"""

import time
import logging
import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Import our display manager
from display.oled_manager import OLEDManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_layout_preview():
    """Create a layout preview image showing what will be displayed where"""
    
    # Create image canvas (128x64, monochrome)
    image = Image.new('1', (128, 64), 0)  # Black background
    draw = ImageDraw.Draw(image)
    
    # Get fonts
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw border (matching the example layout)
    draw.rectangle([(0, 0), (127, 63)], outline=1, fill=0)
    
    # Layout areas based on example:
    # __________________
    # | Date/Time     |
    # | Weather       |
    # |               |
    # |               |
    # |________________
    
    # Date/Time area (top section)
    draw.line([(1, 15), (126, 15)], fill=1)  # Horizontal line under date/time
    draw.text((3, 2), "Date/Time Area", font=font_medium, fill=1)
    
    # Weather area (second section)
    draw.line([(1, 30), (126, 30)], fill=1)  # Horizontal line under weather
    draw.text((3, 17), "Weather Info", font=font_medium, fill=1)
    
    # Additional info areas (remaining space)
    draw.text((3, 32), "Additional Info", font=font_small, fill=1)
    draw.text((3, 42), "(Expandable)", font=font_small, fill=1)
    
    # Add current timestamp to show it's working
    current_time = datetime.now().strftime("%H:%M:%S")
    draw.text((3, 52), f"Test: {current_time}", font=font_small, fill=1)
    
    return image

def create_actual_preview():
    """Create a more realistic preview with actual data placeholders"""
    
    image = Image.new('1', (128, 64), 0)
    draw = ImageDraw.Draw(image)
    
    # Get fonts
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Current date and time (always displayed)
    current_time = datetime.now()
    date_str = current_time.strftime("%b %d, %Y")
    time_str = current_time.strftime("%I:%M %p")
    
    # Date/Time section (top)
    draw.text((2, 1), date_str, font=font_medium, fill=1)
    draw.text((2, 12), time_str, font=font_large, fill=1)
    
    # Separator line
    draw.line([(0, 25), (128, 25)], fill=1)
    
    # Weather section
    draw.text((2, 28), "Weather:", font=font_small, fill=1)
    draw.text((2, 37), "Temp: 72°F", font=font_medium, fill=1)
    draw.text((2, 47), "Precip: 20%", font=font_small, fill=1)
    draw.text((70, 37), "Hi:75° Lo:65°", font=font_small, fill=1)
    
    # Status indicator
    draw.text((2, 56), "API: Ready", font=font_small, fill=1)
    
    return image

def main():
    """Main test function"""
    logger.info("Starting OLED Display Layout Test")
    
    # Initialize display manager
    oled = OLEDManager()
    
    if not oled.initialize():
        logger.error("Failed to initialize OLED display")
        logger.error("Make sure:")
        logger.error("1. SPI is enabled (sudo raspi-config)")
        logger.error("2. Connections are correct per specifications")
        logger.error("3. Required packages are installed")
        return False
    
    try:
        logger.info("Display initialized successfully")
        
        # Test 1: Show layout preview
        logger.info("Displaying layout preview...")
        layout_image = create_layout_preview()
        oled.display_image(layout_image)
        
        time.sleep(5)  # Show for 5 seconds
        
        # Test 2: Show realistic preview
        logger.info("Displaying realistic preview...")
        realistic_image = create_actual_preview()
        oled.display_image(realistic_image)
        
        time.sleep(5)  # Show for 5 seconds
        
        # Test 3: Animation test - update time every second for 10 seconds
        logger.info("Running time update test...")
        for i in range(10):
            current_image = create_actual_preview()
            oled.display_image(current_image)
            time.sleep(1)
        
        logger.info("Display test completed successfully!")
        return True
        
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False
        
    finally:
        # Cleanup
        oled.clear()
        oled.cleanup()
        logger.info("Test completed and cleaned up")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 