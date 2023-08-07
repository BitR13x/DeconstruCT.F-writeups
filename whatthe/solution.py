import os

def get_command_output(command):
    try:
        with os.popen(command) as stream:
            output = stream.read().strip()
            return output
    except Exception as e:
        print(f"Error executing the command: {e}")
        return None

command_to_run = "python whatthe.py"
output = get_command_output(command_to_run)


while "whySoEagerToSolve" in output: 
    output = output.replace("whySoEagerToSolve", "")

    with open("whatthe.py", "w") as f:
        f.write(output)

    output = get_command_output(command_to_run)



with open("out_w", "w") as f:
    f.write(output)
print(output.split("\n")[0])
 
