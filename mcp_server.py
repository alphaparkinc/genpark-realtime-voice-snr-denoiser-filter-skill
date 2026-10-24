import sys, json
from client import RealtimeVoiceSnrDenoiserFilterClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    denoiser = RealtimeVoiceSnrDenoiserFilterClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-realtime-voice-snr-denoiser-filter-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    samples = req.get("samples", [0] * 640)
    res = denoiser.process_frame(samples)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
