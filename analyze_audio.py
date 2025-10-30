#!/usr/bin/env python3
"""
Analyze audio characteristics of voice sample to inform PipeWire filter design
"""

import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import sys

def analyze_audio(filename):
    # Read the audio file
    sample_rate, audio_data = wavfile.read(filename)

    # Convert stereo to mono if needed
    if len(audio_data.shape) == 2:
        audio_mono = np.mean(audio_data, axis=1)
    else:
        audio_mono = audio_data

    # Normalize to float
    audio_float = audio_mono.astype(float) / np.iinfo(audio_data.dtype).max

    print(f"Audio Analysis for: {filename}")
    print("=" * 60)
    print(f"Sample Rate: {sample_rate} Hz")
    print(f"Duration: {len(audio_mono) / sample_rate:.2f} seconds")
    print(f"Channels: {'Stereo' if len(audio_data.shape) == 2 else 'Mono'}")
    print()

    # Level analysis
    rms = np.sqrt(np.mean(audio_float**2))
    peak = np.max(np.abs(audio_float))
    print(f"RMS Level: {rms:.4f} ({20 * np.log10(rms + 1e-10):.2f} dB)")
    print(f"Peak Level: {peak:.4f} ({20 * np.log10(peak + 1e-10):.2f} dB)")
    print(f"Crest Factor: {peak/rms:.2f}")
    print()

    # Dynamic range
    noise_floor = np.percentile(np.abs(audio_float), 10)
    dynamic_range = 20 * np.log10(peak / (noise_floor + 1e-10))
    print(f"Noise Floor (10th percentile): {20 * np.log10(noise_floor + 1e-10):.2f} dB")
    print(f"Dynamic Range: {dynamic_range:.2f} dB")
    print()

    # Frequency analysis
    freqs, psd = signal.welch(audio_float, sample_rate, nperseg=4096)

    # Find dominant frequencies
    peak_indices = signal.find_peaks(psd, height=np.percentile(psd, 95))[0]
    if len(peak_indices) > 0:
        print("Dominant Frequencies:")
        for idx in peak_indices[:5]:  # Top 5
            print(f"  {freqs[idx]:.1f} Hz")
    print()

    # Low frequency energy (potential rumble/room noise)
    low_freq_energy = np.sum(psd[freqs < 120]) / np.sum(psd)
    print(f"Low Frequency Energy (<120 Hz): {low_freq_energy*100:.2f}%")

    # High frequency energy (potential sibilance)
    high_freq_energy = np.sum(psd[freqs > 5000]) / np.sum(psd)
    print(f"High Frequency Energy (>5 kHz): {high_freq_energy*100:.2f}%")
    print()

    # Estimate SNR
    signal_power = np.mean(audio_float[np.abs(audio_float) > noise_floor]**2)
    noise_power = np.mean(audio_float[np.abs(audio_float) <= noise_floor]**2)
    if noise_power > 0:
        snr = 10 * np.log10(signal_power / noise_power)
        print(f"Estimated SNR: {snr:.2f} dB")

    print()
    print("Recommendations:")
    print("-" * 60)

    if low_freq_energy > 0.15:
        print("- High-pass filter recommended (>80 Hz) for rumble reduction")

    if high_freq_energy > 0.05:
        print("- De-esser recommended for sibilance control")

    if dynamic_range > 40:
        print("- Compression/AGC recommended for dynamic range control")

    if noise_floor > 0.01:
        print("- Noise gate recommended to reduce background noise")

if __name__ == "__main__":
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else "voice-sample.wav"
    analyze_audio(filename)
