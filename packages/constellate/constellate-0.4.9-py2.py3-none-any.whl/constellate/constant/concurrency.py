import psutil

# CPU cores
process = psutil.Process()
LOGICAL_CPUS_COUNT = (
    len(process.cpu_affinity())
    if hasattr(process, "cpu_affinity")
    else psutil.cpu_count(logical=True)
)
