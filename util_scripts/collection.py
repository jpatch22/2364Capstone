import re
import subprocess
import time
import pandas as pd

DEFAULT_BASH_COMMAND = "/opt/xilinx/xrt/bin/xbutil examine --device --report thermal electrical"
DEFAULT_INTERVAL = 1 #s
DEFAULT_ITERATIONS = 20
UNIT_MAPPING = {
    'Temp-PCB': ['C'],
    'Temp-device': ['C'],
    'Temp-vccint': ['C'],
    'Temp-cage_temp_0': ['C'],
    'Temp-cage_temp_1': ['C'],
    'Max Power': ['Watts'],
    'Power': ['Watts'],
    'Power Warning': [],
    '12v_pex': ['V', 'A'],
    '3v3_pex': ['V'],
    '3v3_aux': ['V'],
    '12v_aux_0': ['V', 'A'],
    '12v_aux_1': ['V', 'A'],
    'vccint': ['V', 'A']
}


class Data_Collector:
    def __init__(self, file_name, number_of_iterations = DEFAULT_ITERATIONS, bash_command = DEFAULT_BASH_COMMAND, interval = DEFAULT_INTERVAL):
        self.bash_command = bash_command
        self.interval = interval
        self.file_name = file_name
        self.number_of_iterations = number_of_iterations
        self.data = {}

    def run_collection(self):
        # runs the command to collect data and records the output
        for i in range(self.number_of_iterations):
            output = subprocess.check_output(self.bash_command, shell=True, text=True)
            #output = re.escape(output)
            self.parse_data(i, output)
            time.sleep(self.interval)


    def parse_data(self, iteration, format_str):
        matches = []
        matches.extend(extract_temperature_info(format_str))
        matches.extend(extract_volt_info(format_str))
        matches.extend(extract_power_info(format_str))
        matches.extend(extract_volt_amps_info(format_str))
        for m in matches:
            for unit in UNIT_MAPPING[m[0]]:
                key = f"{m[0]} ({unit})"
                if key not in self.data:
                    self.data[key] = []
            if len(m) == 3:
                key = f"{m[0]} ({UNIT_MAPPING[m[0]][0]})"
                self.data[key].append((iteration, m[1]))
            elif len(m) == 4:
                keyVolts = f"{m[0]} ({UNIT_MAPPING[m[0]][0]})"
                keyAmps = f"{m[0]} ({UNIT_MAPPING[m[0]][1]})"
                self.data[keyVolts].append((iteration, m[1]))
                self.data[keyAmps].append((iteration, m[1]))

    def save_to_csv(self):
        df = pd.DataFrame()
    
        for key, values in self.data.items():
            if not values:
                continue
            _, value_col = zip(*values)

            key_df = pd.DataFrame({
                f'{key}_value': value_col
            })
            
            df = pd.concat([df, key_df], axis=1)
    
        df.to_csv(self.file_name) 

def extract_temperature_info(input_string):
    temperature_pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*(\w*)\s*C')
    
    matches = re.findall(temperature_pattern, input_string)
    res = []
    for match in matches:
        res.append((f"Temp-{match[0]}", match[1], match[2]))

    return res 

def extract_volt_info(input_string):
    voltage_pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*(\w*)\s*V(?!,\s*\d+\.\d+\s*A)')
    
    matches = re.findall(voltage_pattern, input_string)

    return matches

def extract_power_info(input_string):
    power_pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*Watts?\s*')

    matches = re.findall(power_pattern, input_string)

    return matches

def extract_volt_amps_info(input_string):
    pattern = re.compile(r'(\w+)\s*:\s*([\d.]+)\s*(V|A)?,\s*([\d.]+)?\s*A?')

    matches = re.findall(pattern, input_string)
    
    return matches

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

def main():
    dc = Data_Collector('test.csv')
    dc.parse_data(0, format_str)
    dc.parse_data(1, format_str)
    dc.save_to_csv()

if __name__ == "__main__":
    main()
