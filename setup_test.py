#!/usr/bin/env python3
"""
Setup verification script for OLED display project
Checks dependencies, hardware configuration, and SPI interface
"""

import sys
import os
import subprocess
import importlib
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        logger.error(f"Python 3.7+ required, found {version.major}.{version.minor}")
        return False
    logger.info(f"Python version OK: {version.major}.{version.minor}.{version.micro}")
    return True

def check_spi_enabled():
    """Check if SPI interface is enabled"""
    try:
        # Check if SPI device exists
        spi_devices = ['/dev/spidev0.0', '/dev/spidev0.1']
        spi_found = any(os.path.exists(dev) for dev in spi_devices)
        
        if spi_found:
            logger.info("SPI interface is enabled")
            return True
        else:
            logger.error("SPI interface not found")
            logger.error("Enable SPI with: sudo raspi-config -> Interface Options -> SPI -> Enable")
            return False
    except Exception as e:
        logger.error(f"Error checking SPI: {e}")
        return False

def check_required_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        'luma.oled',
        'PIL',  # Pillow
        'spidev'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            logger.info(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"✗ {package} is missing")
    
    if missing_packages:
        logger.error("Install missing packages with:")
        logger.error("pip install -r requirements.txt")
        return False
    
    return True

def check_gpio_permissions():
    """Check if user has GPIO permissions"""
    try:
        # Check if user is in gpio group
        groups = subprocess.check_output(['groups'], text=True)
        if 'gpio' in groups:
            logger.info("User has GPIO permissions")
            return True
        else:
            logger.warning("User not in gpio group")
            logger.warning("Add with: sudo usermod -a -G gpio $USER")
            logger.warning("Then logout and login again")
            return True  # Not critical, might still work
    except Exception as e:
        logger.warning(f"Could not check GPIO permissions: {e}")
        return True  # Not critical

def check_hardware_connections():
    """Provide hardware connection checklist"""
    logger.info("Hardware Connection Checklist:")
    connections = [
        "VCC     -> Pin 2 (5V)",
        "GND     -> Pin 6 (Ground)",
        "DIN     -> Pin 19 (GPIO 10/MOSI)",
        "CLK     -> Pin 23 (GPIO 11/SCLK)",
        "CS      -> Pin 24 (GPIO 8/CE0)",
        "DC      -> Pin 18 (GPIO 24)",
        "RST     -> Pin 22 (GPIO 25)"
    ]
    
    for connection in connections:
        logger.info(f"  {connection}")
    
    return True

def main():
    """Run all setup checks"""
    logger.info("=== OLED Display Setup Verification ===")
    
    checks = [
        ("Python Version", check_python_version),
        ("SPI Interface", check_spi_enabled),
        ("Required Packages", check_required_packages),
        ("GPIO Permissions", check_gpio_permissions),
        ("Hardware Connections", check_hardware_connections)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        logger.info(f"\n--- Checking {check_name} ---")
        if not check_func():
            all_passed = False
    
    logger.info("\n=== Setup Verification Summary ===")
    if all_passed:
        logger.info("✓ All checks passed! Ready to run display test.")
        logger.info("Run the test with: python3 test_display_layout.py")
    else:
        logger.error("✗ Some checks failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 