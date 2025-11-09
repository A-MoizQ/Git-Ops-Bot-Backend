import os
# ensure main uses a reachable webhook during the TestClient run
os.environ["N8N_WEBHOOK_URL"] = "https://httpbin.org/post"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

resp = client.post("/webhook", json={"branch":"main","commit_message":"auto test","author":"ci"})
print(resp.status_code, resp.json())

commit_id = resp.json().get("commit_id")
if commit_id:
    s = client.get(f"/state/{commit_id}")
    print(s.status_code, s.json())