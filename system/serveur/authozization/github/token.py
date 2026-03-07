import os;

def get_token_github():

        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("Error: GITHUB_TOKEN not set")
            return None 
        return token