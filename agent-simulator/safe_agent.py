import time
import requests
import uuid

SERVER = "http://localhost:8000/api/v1"

def register():
    r = requests.post(f"{SERVER}/agents/register", json={
        "hostname": "student-lab",
        "platform": "linux",
        "tags": ["simulation"]
    })
    return r.json()["agent_id"]

def get_tasks(agent_id):
    r = requests.get(f"{SERVER}/agents/{agent_id}/tasks")
    return r.json()

def heartbeat(agent_id):
    requests.post(f"{SERVER}/agents/{agent_id}/heartbeat", json={
        "uptime": 1234,
        "load": 0.1,
        "ip": "127.0.0.1"
    })

def complete(agent_id, task):
    requests.post(
        f"{SERVER}/agents/{agent_id}/complete/{task['task_id']}",
        json={"status": "done", "result": {"output": "simulated"}}
    )

def main():
    aid = register()
    print("[*] agent id:", aid)

    while True:
        heartbeat(aid)
        tasks = get_tasks(aid)
        for t in tasks:
            print("[*] executing (simulated):", t)
            time.sleep(1)
            complete(aid, t)

        time.sleep(3)

if __name__ == "__main__":
    main()
