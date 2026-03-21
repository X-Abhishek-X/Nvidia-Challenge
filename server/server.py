import grpc
from concurrent import futures
import time
from proto import gpu_metrics_pb2, gpu_metrics_pb2_grpc
from rich.console import Console

console = Console()

class GPUOrchestratorService(gpu_metrics_pb2_grpc.GPUOrchestratorServicer):
    def StreamMetrics(self, request_iterator, context):
        """Receive a stream of GPU metrics from worker nodes."""
        console.print("📡 [bold cyan]New Telemetry Stream Established[/bold cyan]")
        
        for metric in request_iterator:
            # High Performance Orchestration Logic (Simulation)
            # This is where a real cluster drain would happen
            if metric.temperature > 88:
                console.print(f"🚨 [bold red]CRITICAL EVENT:[/bold red] Node {metric.node_id} GPU {metric.gpu_uuid} overheating ({metric.temperature:.1f}C)!")
                console.print(f"🔄 [yellow]ACTION:[/yellow] Initiating Kubernetes Node Drain for {metric.node_id}...")
            elif metric.vram_used > (metric.vram_total * 0.9):
                console.print(f"💡 [yellow]ADVISORY:[/yellow] Node {metric.node_id} is running low on VRAM.")

            # Return a simple health ACK
            yield gpu_metrics_pb2.GPUMetricsResponse(
                status="OK",
                message=f"Metrics for {metric.gpu_uuid} logged."
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gpu_metrics_pb2_grpc.add_GPUOrchestratorServicer_to_server(GPUOrchestratorService(), server)
    server.add_insecure_port('[::]:50051')
    console.print("🏢 [bold green]Nvidia Challenges Central Orchestrator[/bold green] live on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
