import requests

url = "https://api.novita.ai/v3/async/txt2video"

payload = {
    "extra": {
        "response_video_type": "<string>",
        "webhook": {
            "url": "<string>",
            "test_mode": {"enabled": True, "return_task_status": "<string>"},
        },
        "enterprise_plan": {"enabled": True},
    },
    "model_name": "<string>",
    "height": 123,
    "width": 123,
    "steps": 123,
    "prompts": [{"frames": 123, "prompt": "<string>"}],
    "negative_prompt": "<string>",
    "guidance_scale": 123,
    "seed": 123,
    "loras": [{"model_name": "<string>", "strength": {}}],
    "embeddings": [{"model_name": "<string>"}],
    "closed_loop": True,
    "clip_skip": 123,
}
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer <sk_VRh3m-IvWjjbkLxpH7DZ75CymCOFkBXJkSMCBA-fksI>",
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
