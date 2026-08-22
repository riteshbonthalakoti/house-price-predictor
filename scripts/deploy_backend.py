from huggingface_hub import HfApi

def deploy():
    api = HfApi()
    username = api.whoami()['name']
    repo_id = f"{username}/house-price-api"
    
    print(f"Creating Space: {repo_id}")
    api.create_repo(repo_id=repo_id, exist_ok=True, repo_type="space", space_sdk="docker")
    
    print("Uploading backend files...")
    api.upload_file(path_or_fileobj="backend/requirements.txt", path_in_repo="requirements.txt", repo_id=repo_id, repo_type="space")
    api.upload_file(path_or_fileobj="backend/Dockerfile", path_in_repo="Dockerfile", repo_id=repo_id, repo_type="space")
    api.upload_file(path_or_fileobj="backend/main.py", path_in_repo="backend/main.py", repo_id=repo_id, repo_type="space")
    api.upload_folder(folder_path="model", repo_id=repo_id, path_in_repo="model", repo_type="space")
    
    print(f"Backend deployed to https://huggingface.co/spaces/{repo_id}")
    print(f"Direct API endpoint: https://{username}-house-price-api.hf.space")

if __name__ == '__main__':
    deploy()
