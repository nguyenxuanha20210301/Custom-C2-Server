# server/src/app/sim_catalog.py
"""
Catalog cho các "command / persistence / delivery" mô phỏng.

Agent simulator sẽ dùng các dict này để sinh kết quả giả lập.
Không có lệnh hệ điều hành hay payload thực nào ở đây.
"""

SIM_EXEC_CATALOG = {
    "whoami": "labuser (simulated)\n",
    "hostname": "lab-agent-01\n",
    "ps": (
        "PID   CMD\n"
        "101   /usr/bin/python agent_sim.py\n"
        "202   /usr/bin/metrics-collector\n"
    ),
    "netstat": (
        "Proto  Local Address    Foreign Address    State\n"
        "tcp    10.0.0.5:443     10.0.0.10:51820    ESTABLISHED\n"
    ),
}

SIM_PERSISTENCE_CATALOG = {
    "startup_folder": "Simulated: copy shortcut to Startup folder.",
    "systemd_service": "Simulated: create systemd unit and enable at boot.",
    "run_key": "Simulated: create HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run entry.",
}

SIM_DELIVERY_CATALOG = {
    "benign-tool.zip": "Simulated toolkit archive with diagnostics scripts.",
    "update-agent.bin": "Simulated agent update blob.",
    "config-package.tar.gz": "Simulated configuration bundle.",
}
