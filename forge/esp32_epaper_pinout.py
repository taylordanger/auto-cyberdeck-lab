#!/usr/bin/env python3

def get_esp32_epaper_pinout():
    return {
        'GPIO0': 'Reset',
        'GPIO1': 'Deep Sleep',
        'GPIO2': 'Boot Mode',
        'GPIO4': 'Busy',
        'GPIO5': 'CS',
        'GPIO10': 'DC',
        'GPIO13': 'MOSI',
        'GPIO14': 'CLK',
        'GPIO15': 'RST'
    }
