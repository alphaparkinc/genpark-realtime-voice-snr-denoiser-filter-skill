import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class RealtimeVoiceSnrDenoiserFilterClient:
    """
    Subband audio noise suppression estimator. Evaluates speech Signal-to-Noise Ratio (SNR)
    using minimum-statistics tracking and computes optimal Wiener filter attenuation gains.
    """
    def __init__(self, min_gain_db=-18.0):
        self.min_gain_db = min_gain_db
        self.min_gain_linear = 10.0 ** (min_gain_db / 20.0)

    def estimate_noise_and_snr(self, samples):
        n = len(samples)
        if n == 0:
            return 0.0, 0.0, 0.0

        # Subdivide into 40ms sub-blocks (640 samples @ 16kHz)
        block_size = min(320, n)
        energies = []
        for i in range(0, n, block_size):
            block = samples[i:i + block_size]
            rms = math.sqrt(sum(x * x for x in block) / float(len(block)))
            energies.append(rms)

        # Minimum statistics noise floor estimate
        noise_floor = min(energies) if energies else 1.0
        peak_signal = max(energies) if energies else 1.0
        mean_signal = sum(energies) / float(len(energies)) if energies else 1.0

        # Compute SNR in dB: 20 * log10(mean_signal / noise_floor)
        snr_db = 20.0 * math.log10(max(1.0, mean_signal) / max(0.1, noise_floor))
        
        # Optimal Wiener filter gain calculation: G = SNR / (1 + SNR)
        snr_linear = 10.0 ** (snr_db / 10.0)
        wiener_gain = snr_linear / (1.0 + snr_linear)
        wiener_gain = max(self.min_gain_linear, min(1.0, wiener_gain))
        wiener_gain_db = 20.0 * math.log10(max(1e-4, wiener_gain))

        return round(snr_db, 2), round(wiener_gain, 3), round(wiener_gain_db, 2), round(noise_floor, 2)

    def process_frame(self, pcm_samples):
        snr_db, gain, gain_db, noise_floor = self.estimate_noise_and_snr(pcm_samples)
        
        if snr_db < 6.0:
            quality = "POOR_HEAVY_NOISE"
            action = "APPLY_AGGRESSIVE_SUPPRESSION"
        elif snr_db < 15.0:
            quality = "MODERATE_AMBIENT_NOISE"
            action = "APPLY_STANDARD_WIENER_ATTENUATION"
        else:
            quality = "PRISTINE_STUDIO_QUALITY"
            action = "PASS_THROUGH_MINIMAL_FILTER"

        return {
            "status": "success",
            "samples_analyzed": len(pcm_samples),
            "estimated_snr_db": snr_db,
            "estimated_noise_floor": noise_floor,
            "recommended_wiener_gain_linear": gain,
            "recommended_attenuation_db": gain_db,
            "audio_quality_profile": quality,
            "recommended_dsp_action": action
        }
