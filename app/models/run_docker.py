import subprocess

container_id = "e4801c07ba50"
result = subprocess.check_output(["docker", "exec", container_id, "python", "/workspace/cust_model_flow/class_custom/rand.py"])

result = result.decode("utf-8")
print(result)
