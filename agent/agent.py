import random
import time
import os
import grpc
from typing import Dict
from proto import gpu_metrics_pb2, gpu_metrics_pb2_grpc
from rich.console import Console

console = Console()

class GPUSimulator:
    """Mock for nvidia-smi data for local laptop development"""
    def __init__(self, node_id: str):
        self.node_id = node_id or "local-node-01"
        self.gpu_uuid = f"GPU-{random.randint(1000, 9999)}"
        self.temp = 45.0
        self.power = 30.0
        self.vram_used = 1024

    def sample(self) -> Dict:
        # Simulate load/fluctuations
        self.temp += random.uniform(-2, 5)
        self.power += random.uniform(-5, 15)
        self.vram_used += random.randint(-100, 500)
        
        # Keep within realistic ranges
        self.temp = max(35, min(95, self.temp))
        self.power = max(20, min(350, self.power))
        self.vram_used = max(512, min(16384, self.vram_used))
        
        return {
            "node_id": self.node_id,
            "gpu_uuid": self.gpu_uuid,
            "temperature": self.temp,
            "power_draw": self.power,
            "vram_used": self.vram_used,
            "vram_total": 16384.0
        }

def run_agent():
    simulator = GPUSimulator(node_id="worker-mac-01")
    console.print(f"🚀 [cyan]GPU Telemetry Agent[/cyan] starting (Targetting: localhost:50051)")
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = gpu_metrics_pb2_grpc.GPUOrchestratorStub(channel)
        
        def metric_generator():
            while True:
                data = simulator.sample()
                if data["temperature"] > 85:
                    console.print(f"🔥 [bold red]THERMAL WARNING:[/bold red] GPU at {data['temperature']:.1f}C")
                
                request = gpu_metrics_pb2.GPUMetricsRequest(**data)
                yield request
                time.sleep(1) # High frequency (1Hz)

        try:
            responses = stub.StreamMetrics(metric_generator())
            for response in responses:
                console.print(f"✅ Server Ack: {response.status}")
        except grpc.RpcError as e:
            console.print(f"❌ [red]Telemetry Stream Error:[/red] {e.details()}")

if __name__ == "__main__":
    run_agent()
