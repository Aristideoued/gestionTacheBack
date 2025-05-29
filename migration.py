import subprocess


commands = [
    'flask db init',
    'flask db migrate -m "Initial migration."',
    'flask db upgrade'
]
    
for command in commands:
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e)


