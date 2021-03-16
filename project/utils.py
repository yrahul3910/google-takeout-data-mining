def get_key():
    # Get the API key from the .env file
    with open('.env', 'r') as f:
        line = f.readline()
        return line.split('=')[1]
