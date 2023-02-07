import os

# Get the directory path of the script file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Path to the .env file
env_file = os.path.join(dir_path, '..', '.env')

# Read the .env file
with open(env_file) as f:
    content = f.readlines()

# Store the key-value pairs in a dictionary
config = {}
for line in content:
    line = line.strip()
    if line.startswith("#") or line == '':
        continue
    key, value = line.split("=")
    key = key.strip()
    value = value.strip()

    # Mulitiple Options List 
    multiple_options = ["WS_USERS", "WS_NUMBERS", "WEBHOOK_ALLOWED_EVENTS"]

    # Process the values based on the key
    if key in multiple_options:
        config[key] = [v.strip() for v in value.replace("'", "").split(",") if v.strip()]
    elif value == "true":
        config[key] = True
    elif value == "false":
        config[key] = False
    else:
        config[key] = value

# Create the WS_USERS_MAP dictionary
WS_USERS_MAP = {}
for i in range(len(config['WS_USERS'])):
    WS_USERS_MAP[config['WS_USERS'][i]] = config['WS_NUMBERS'][i]

config['WS_USERS_MAP'] = WS_USERS_MAP