from huggingface_hub import snapshot_download
model_name = "XDawned/minecraft-en-zh"
model_path = snapshot_download(model_name, endpoint="https://hf-mirror.com", local_dir="minecraft-en-zh")