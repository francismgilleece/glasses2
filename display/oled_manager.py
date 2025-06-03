"""
OLED Display Manager for SPI-connected 128x64 display
Handles hardware initialization and display operations
"""

import logging
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.hardware_config import OLED_CONFIG

logger = logging.getLogger(__name__)

class OLEDManager:
    """Manages OLED display hardware and rendering operations"""
    
    def __init__(self):
        self.device = None
        self.width = OLED_CONFIG['width']
        self.height = OLED_CONFIG['height']
        self.initialized = False
        
    def initialize(self):
        """Initialize the OLED display with SPI interface"""
        try:
            # Create SPI interface
            serial = spi(
                port=OLED_CONFIG['spi_config']['port'],
                device=OLED_CONFIG['spi_config']['device'],
                gpio_DC=OLED_CONFIG['spi_config']['gpio_dc'],
                gpio_RST=OLED_CONFIG['spi_config']['gpio_rst'],
                gpio_CS=OLED_CONFIG['spi_config']['gpio_cs']
            )
            
            # Initialize SSD1306 device
            self.device = ssd1306(
                serial,
                width=self.width,
                height=self.height,
                rotate=OLED_CONFIG['rotate']
            )
            
            # Set contrast
            self.device.contrast(OLED_CONFIG['contrast'])
            
            self.initialized = True
            logger.info(f"OLED display initialized: {self.width}x{self.height}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize OLED display: {e}")
            self.initialized = False
            return False
    
    def clear(self):
        """Clear the display"""
        if not self.initialized:
            return False
        try:
            self.device.clear()
            return True
        except Exception as e:
            logger.error(f"Failed to clear display: {e}")
            return False
    
    def display_image(self, image):
        """Display a PIL Image on the OLED"""
        if not self.initialized:
            logger.error("Display not initialized")
            return False
        
        try:
            # Ensure image is the right size and mode
            if image.size != (self.width, self.height):
                image = image.resize((self.width, self.height))
            
            if image.mode != '1':  # Convert to 1-bit (monochrome)
                image = image.convert('1')
            
            self.device.display(image)
            return True
            
        except Exception as e:
            logger.error(f"Failed to display image: {e}")
            return False
    
    def create_canvas(self):
        """Create a drawing canvas for the display"""
        return Image.new('1', (self.width, self.height), 0)  # Black background
    
    def get_font(self, size=10):
        """Get a font for text rendering"""
        try:
            # Try to load a nice font, fall back to default
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            try:
                return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", size)
            except:
                return ImageFont.load_default()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.device:
            try:
                self.device.clear()
                logger.info("OLED display cleaned up")
            except:
                pass
        self.initialized = False 