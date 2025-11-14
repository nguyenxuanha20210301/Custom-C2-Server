# tools/agent_sim.py
"""
Benign agent simulator cho C2 Simulation Lab.

Chức năng:
  - Đăng ký agent mới với server.
  - Poll /agents/{id}/next để lấy nhiệm vụ.
  - Với các task loại sim.exec / sim.persist / sim.delivery:
      -> sinh kết quả mô phỏng (không thực thi gì trên OS)
      -> POST /agents/{id}/complete/{task_id} với status + result.

Dùng để demo các khái niệm:
  - Command execution / reverse shell queue
  - Persistence
  - Payload delivery / staging

Nhưng toàn bộ đều ở mức giả lập, không thực hiện hoạt động tấn công.
"""

import argparse
import json
import time
from typing import Any, Dict

import httpx

from server.src.app.sim_catalog import (
    SIM_EXEC_CATALOG,
    SIM_PERSISTENCE_CATALOG,
    SIM_DELIVERY_CATALOG,
)

DEFAULT_BASE_URL = "http://localhost:8000/api/v1"


def register_agent(
    base_url: str,
    hostname: str = "lab-agent",
    platform: str = "linux",
) -> str:
    resp = httpx.post(
        f"{base_url}/agents/register",
        json={"hostname": hostname, "platform": platform},
        timeout=5.0,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["agent_id"]


def simulate_exec_task(meta: Dict[str, Any]) -> Dict[str, Any]:
    spec = meta.get("spec") or {}
    name = spec.get("name", "whoami")
    args = spec.get("args", [])

    stdout = SIM_EXEC_CATALOG.get(name, f"Simulated output for '{name}'\n")
    if args:
        stdout += f"(args: {', '.join(args)})\n"

    return {
        "kind": "exec",
        "success": True,
        "stdout": stdout,
        "stderr": "",
        "exit_code": 0,
    }


def simulate_persist_task(meta: Dict[str, Any]) -> Dict[str, Any]:
    spec = meta.get("spec") or {}
    mech = spec.get("mechanism", "startup_folder")
    label = spec.get("label", "demo-agent")

    desc = SIM_PERSISTENCE_CATALOG.get(mech, "Simulated persistence mechanism.")
    stdout = f"{desc}\nLabel: {label}\n"

    return {
        "kind": "persist",
        "success": True,
        "persistence_mechanism": mech,
        "installed": True,
        "stdout": stdout,
    }


def simulate_delivery_task(meta: Dict[str, Any]) -> Dict[str, Any]:
    spec = meta.get("spec") or {}
    artifact_name = spec.get("artifact_name", "benign-tool.zip")
    stage = spec.get("stage", "staging")
    size_kb = spec.get("size_kb", 1024)

    desc = SIM_DELIVERY_CATALOG.get(
        artifact_name,
        "Simulated payload artifact.",
    )

    stdout = (
        f"Artifact: {artifact_name} ({size_kb}KB)\n"
        f"Stage: {stage}\n"
        f"Desc: {desc}\n"
    )

    return {
        "kind": "delivery",
        "success": True,
        "artifact_name": artifact_name,
        "stage": stage,
        "stdout": stdout,
    }


def handle_task(base_url: str, agent_id: str, task: Dict[str, Any]) -> None:
    task_id = task["task_id"]
    t_type = task["type"]
    meta = task.get("payload") or task.get("meta") or {}

    if t_type == "sim.exec":
        result = simulate_exec_task(meta)
    elif t_type == "sim.persist":
        result = simulate_persist_task(meta)
    elif t_type == "sim.delivery":
        result = simulate_delivery_task(meta)
    else:
        # Các loại khác (vd collect-metrics) chỉ ack cho đơn giản
        result = {
            "kind": "noop",
            "success": True,
            "stdout": f"Task type {t_type} handled as noop in simulator.\n",
        }

    body = {
        "status": "done",
        "error": None,
        "result": result,
    }

    resp = httpx.post(
        f"{base_url}/agents/{agent_id}/complete/{task_id}",
        json=body,
        timeout=10.0,
    )
    resp.raise_for_status()
    print(f"[+] Completed task {task_id} ({t_type})")


def poll_loop(
    base_url: str,
    agent_id: str,
    interval: int = 5,
) -> None:
    print(f"[+] Starting poll loop for agent {agent_id} (interval={interval}s)")
    while True:
        try:
            resp = httpx.get(
                f"{base_url}/agents/{agent_id}/next",
                params={"limit": 5},
                timeout=5.0,
            )
            resp.raise_for_status()
            tasks = resp.json()
            if tasks:
                print(f"[+] Received {len(tasks)} task(s)")
                for t in tasks:
                    print("    Task:", json.dumps(t, indent=2))
                    handle_task(base_url, agent_id, t)
            else:
                print("[.] No tasks, sleeping...")
        except Exception as exc:  # noqa: BLE001
            print(f"[!] Error during poll: {exc}")

        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benign C2 agent simulator")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--hostname", default="lab-agent")
    parser.add_argument("--platform", default="linux")
    parser.add_argument("--poll-interval", type=int, default=5)

    args = parser.parse_args()

    agent_id = register_agent(
        args.base_url,
        hostname=args.hostname,
        platform=args.platform,
    )
    print(f"[+] Registered agent_id={agent_id}")

    poll_loop(args.base_url, agent_id, interval=args.poll_interval)


if __name__ == "__main__":
    main()
