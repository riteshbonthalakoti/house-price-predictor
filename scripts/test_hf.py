from huggingface_hub import HfApi
try:
    api = HfApi()
    api.create_repo(repo_id="ritesh1918/test-gradio-space", exist_ok=True, repo_type="space", space_sdk="gradio")
    print("Gradio space creation succeeded!")
    api.delete_repo(repo_id="ritesh1918/test-gradio-space", repo_type="space")
except Exception as e:
    print(f"Error: {e}")
