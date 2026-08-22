from huggingface_hub import HfApi
import os

def push_to_hub():
    api = HfApi()
    
    user_info = api.whoami()
    username = user_info['name']
    
    repo_id = f"{username}/house-price-predictor"
    print(f"Creating or retrieving repository: {repo_id}")
    api.create_repo(repo_id=repo_id, exist_ok=True, repo_type="model")
    
    print("Uploading model files...")
    api.upload_folder(
        folder_path="model",
        repo_id=repo_id,
        repo_type="model",
        commit_message="Add Linear Regression model and feature names"
    )
    print(f"Model successfully pushed to https://huggingface.co/{repo_id}")

if __name__ == "__main__":
    push_to_hub()
