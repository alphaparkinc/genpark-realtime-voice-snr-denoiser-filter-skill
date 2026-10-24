from client import RealtimeVoiceSnrDenoiserFilterClient
import math, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    denoiser = RealtimeVoiceSnrDenoiserFilterClient()
    print("=== REALTIME VOICE SNR DENOISER FILTER ===")
    
    # 1. High SNR clean audio frame
    clean_audio = [int(12000.0 * math.sin(i * 0.1) + (i % 20 - 10)) for i in range(1600)]
    res_clean = denoiser.process_frame(clean_audio)
    print()
    print(f"1. Clean Audio: SNR={res_clean['estimated_snr_db']} dB | Profile={res_clean['audio_quality_profile']}")
    print(f"   Gain: {res_clean['recommended_wiener_gain_linear']} ({res_clean['recommended_attenuation_db']} dB) -> Action: {res_clean['recommended_dsp_action']}")

    # 2. Noisy audio frame (heavy background ambient)
    noisy_audio = [int(4000.0 * math.sin(i * 0.1) + ((i * 37) % 3500 - 1750)) for i in range(1600)]
    res_noisy = denoiser.process_frame(noisy_audio)
    print()
    print(f"2. Noisy Audio: SNR={res_noisy['estimated_snr_db']} dB | Profile={res_noisy['audio_quality_profile']}")
    print(f"   Gain: {res_noisy['recommended_wiener_gain_linear']} ({res_noisy['recommended_attenuation_db']} dB) -> Action: {res_noisy['recommended_dsp_action']}")

if __name__ == "__main__":
    main()
