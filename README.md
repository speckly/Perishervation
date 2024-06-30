# Perishervation

A Python IoT Project to ensure the quality preservation of perishable goods during transport. This is done by monitoring variables that affect the quality of perishable goods, using sensors connected to a Raspberry Pi.

# Variables

- Temperature (Degrees Celsius)
- Humidity (%)
- Shock (Watts per square meter? Perhaps standardise to %?)
- Light (Lumens? Perhaps standardise to %?)

# Hardware

- Raspberry Pi 3B+, 40 GPIO
- Analog to Digital converter: MCP3008, 10 bits, 8 channels
- Temperature and humidity: DHT22

# Requirements

python>=3.11
installation of all libraries stated in `requirements.txt`

# Setup

It is recommended to use a virtual environment to avoid version conflict with other packages