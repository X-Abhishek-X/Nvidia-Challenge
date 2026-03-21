# GPU Metric Orchestrator (Nvidia Challenge) 🏢🚀

A high-performance telemetry and auto-healing engine for GPU clusters. Built to simulate real-time monitoring and orchestration of Nvidia GPU nodes using **gRPC streams** and asynchronous Python.

## The Architecture
1. **The Telemetry Agent (`/agent`):** Sits on worker nodes and streams GPU metrics (Temp, Power, VRAM) via a persistent gRPC connection at 1Hz frequency.
2. **The Proto Definition (`/proto`):** Language-neutral interface using Protocol Buffers.
3. **The Orchestrator Server (`/server`):** A high-throughput central controller that receives streams, analyzes them for hardware-critical events (like 85°C+ thermal warnings), and simulates "Kubernetes Node Drains" to prevent hardware failure.

## Getting Started
### 1. Requirements
- Python 3.9+
- gRPC
- Protobuf

### 2. Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Generate gRPC Code
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/gpu_metrics.proto
```

### 4. Run the Orchestrator (Terminal 1)
```bash
python server/server.py
```

### 5. Start the GPU Agent (Terminal 2)
```bash
python agent/agent.py
```

## Why this project?
This project demonstrates key competencies for high-level infrastructure engineering at Tier-1 tech companies:
- **Low-Latency Streaming:** Using gRPC instead of standard REST.
- **Hardware Telemetry:** Working with metrics at a systems-level (Nvidia GPU specifics).
- **Asynchronous Fault Tolerance:** Decoupling worker stats from centralized decision-making.

---
**Maintained by [X-Abhishek-X](https://github.com/X-Abhishek-X)**
