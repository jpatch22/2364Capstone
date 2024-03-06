import re

format_str = r"""
---------------------------------------------------
[0000:01:00.1] : xilinx_vck5000_gen4x8_qdma_base_2
---------------------------------------------------
Thermals
  Temperature            : Celcius
  PCB                    :     (\d+) C
  device                 :     39 C
  vccint                 :     36 C
  cage_temp_0            :      0 C
  cage_temp_1            :      0 C

Electrical
  Max Power              : NA Watts
  Power                  : 42 Watts
  Power Warning          : NA

  Power Rails            : Voltage   Current
  12v_pex                : 11.999 V,  1.072 A
  3v3_pex                :  3.270 V
  3v3_aux                :  3.310 V
  12v_aux_0              : 12.077 V,  1.569 A
  12v_aux_1              : 12.127 V,  0.840 A
  vccint                 :  0.800 V, 31.100 A
"""

def extract_temperature_info(input_string):
    temperature_pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*(\w*)\s*C')
    
    matches = re.findall(temperature_pattern, input_string)

    for match in matches:
        label, number, unit = match
        print(f"{label}: {number} {unit}")

def extract_volt_info(input_string):
    #temperature_pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*(\w*)\s*V')
    voltage_pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*(\w*)\s*V(?!,\s*\d+\.\d+\s*A)')
    
    matches = re.findall(voltage_pattern, input_string)

    for match in matches:
        label, number, unit = match
        print(f"{label}: {number} {unit}")

def extract_power_info(input_string):
    power_pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*Watts?\s*')

    matches = re.findall(power_pattern, input_string)

    for match in matches:
        label, number = match
        print(f"{label}: {number} Watts")

def extract_volt_amps_info(input_string):
    pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*(V|A)?,\s*([\d.]+)?\s*A?')

    matches = re.findall(pattern, input_string)

    for match in matches:
        label, voltage, voltage_unit, current = match
        if voltage_unit:
            print(f"{label}: {voltage} {voltage_unit}, {current} A")
        else:
            print(f"{label}: {voltage} {current} A")

def main():
    extract_temperature_info(format_str)
    extract_power_info(format_str)
    extract_volt_amps_info(format_str)
    extract_volt_info(format_str)

if __name__ == "__main__":
    main()

