import subprocess

bash_command = "/opt/xilinx/xrt/bin/xbutil examine --device --report thermal electrical"
output = subprocess.check_output(bash_command, shell=True, text=True)
print(type(output))
output_file_path = "output.txt"

with open(output_file_path, "w") as output_file:
    output_file.write(output)

print(f"Output saved to file: {output_file_path}")
