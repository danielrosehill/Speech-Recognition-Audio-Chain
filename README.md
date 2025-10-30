# Speech Recognition Audio Chain for PipeWire

Automated audio processing chain optimized for speech-to-text (STT) applications on PipeWire-based Linux systems.

## Overview

This project provides a **lightweight, auto-starting audio processing pipeline** designed specifically for speech recognition microphones. It applies professional-grade audio processing without the complexity of GUI tools like Easy Effects.

### Features

- ✅ **Automatic Gain Control (AGC)** - Normalizes speech levels for consistent STT accuracy
- ✅ **De-essing** - Reduces harsh sibilance (s/sh sounds)
- ✅ **Background Noise Suppression** - Lightweight noise gating for home office environments
- ✅ **De-reverb** - Reduces room reflections for clearer speech
- ✅ **High-pass Filtering** - Removes rumble and low-frequency noise
- ✅ **Auto-start on Boot** - Systemd service integration
- ✅ **CLI Control** - Simple command-line start/stop/status interface
- ✅ **Multi-microphone Support** - Works with any PipeWire input device

### Tested Hardware

- **Samson Q2U** (USB dynamic microphone) - primary test device
- Compatible with any PipeWire-recognized microphone

## Installation

### Prerequisites

```bash
# Ensure PipeWire is installed and running
systemctl --user status pipewire pipewire-pulse

# Install required LADSPA plugins
sudo apt install ladspa-sdk swh-plugins calf-plugins tap-plugins
```

### Setup

1. Clone this repository:
```bash
cd ~/repos/github
git clone <this-repo> Speech-Recognition-Audio-Chain
cd Speech-Recognition-Audio-Chain
```

2. Copy the filter chain configuration:
```bash
mkdir -p ~/.config/pipewire/pipewire.conf.d
cp stt-audio-chain.conf ~/.config/pipewire/pipewire.conf.d/
```

3. Install the control script:
```bash
sudo cp stt-chain /usr/local/bin/
sudo chmod +x /usr/local/bin/stt-chain
```

4. Enable auto-start (optional):
```bash
cp stt-audio-chain.service ~/.config/systemd/user/
systemctl --user enable --now stt-audio-chain.service
```

## Usage

### Manual Control

```bash
# Start the audio chain
stt-chain start

# Stop the audio chain
stt-chain stop

# Check status
stt-chain status

# Restart (reload configuration)
stt-chain restart
```

### Systemd Service Control

```bash
# Start service
systemctl --user start stt-audio-chain

# Stop service
systemctl --user stop stt-audio-chain

# Check status
systemctl --user status stt-audio-chain

# Enable auto-start on boot
systemctl --user enable stt-audio-chain

# Disable auto-start
systemctl --user disable stt-audio-chain
```

### Connecting Your Microphone

After starting the audio chain, use any PipeWire-compatible tool to route your microphone through it:

```bash
# Using pw-link (example)
pw-link "Your_Microphone" "STT Microphone Audio Chain:capture_FL"
```

Or use **qpwgraph** (GUI) to visually connect your microphone to the filter chain input.

## Configuration

The filter chain is defined in [stt-audio-chain.conf](stt-audio-chain.conf). The configuration is tuned based on actual voice analysis of the Samson Q2U microphone.

### Processing Chain Order

1. **High-Pass Filter** (80 Hz) - Removes rumble
2. **Noise Gate** (-45 dB threshold) - Suppresses background noise
3. **De-reverb** (Low-pass at 8 kHz) - Reduces room reflections
4. **Compressor** (-22 dB threshold, 4:1 ratio) - AGC for consistent levels
5. **De-esser** (4.2 kHz center, gentle ratio) - Tames sibilance
6. **Noise Suppressor** (RNNoise-style VAD) - Adaptive noise reduction
7. **Limiter** (0.95 ceiling) - Prevents clipping

### Customization

Edit `~/.config/pipewire/pipewire.conf.d/stt-audio-chain.conf` and adjust control parameters. Common adjustments:

- **More/Less AGC**: Adjust compressor `"Ratio (1:n)"` (higher = more compression)
- **Noise Gate Sensitivity**: Adjust `"Threshold (dB)"` (lower = more aggressive)
- **De-essing Amount**: Adjust de-esser `"Ratio (1:n)"` or threshold

After editing, restart: `stt-chain restart`

## Voice Analysis

This project includes a Python-based audio analysis tool to help optimize filter settings for your specific microphone and environment.

See [VOICE_ANALYSIS.md](VOICE_ANALYSIS.md) for detailed analysis of the reference recordings and recommended settings.

### Running Your Own Analysis

```bash
# Record a test sample (30-60 seconds of natural speech)
pw-record --target <your_mic> test-sample.wav

# Analyze it
python3 analyze_audio.py test-sample.wav
```

The analysis will provide recommendations for filter adjustments.

## Testing in Audacity

Before committing to the PipeWire configuration, you can test filter settings in Audacity:

1. Record a voice sample: `pw-record --target <your_mic> test.wav`
2. Open in Audacity
3. Apply effects in this order:
   - Effect > High-Pass Filter (80 Hz, 24 dB/octave)
   - Effect > Noise Gate (-45 dB threshold)
   - Effect > Compressor (-22 dB, 4:1, 10ms/150ms, +6 dB makeup)
   - Effect > Equalization (-4 dB at 4183 Hz, Q=2.0)
   - Effect > Limiter (-1 dB)
4. Export and compare with original

## Project Structure

```
.
├── stt-audio-chain.conf       # PipeWire filter chain config
├── stt-chain                  # CLI control script
├── stt-audio-chain.service    # Systemd user service
├── analyze_audio.py           # Audio analysis tool
├── voice-samples/             # Reference recordings
│   └── raw-q2u.wav           # Untreated Samson Q2U sample
├── texts/                     # Text samples for recording
│   └── full-profile.txt      # Comprehensive test script
├── VOICE_ANALYSIS.md         # Detailed analysis documentation
└── README.md                 # This file
```

## Troubleshooting

### Audio chain not appearing

```bash
# Check if PipeWire loaded the config
journalctl --user -u pipewire -n 50

# Verify filter chain module
pw-cli ls Module | grep filter-chain
```

### No audio passing through

```bash
# List all PipeWire nodes
pw-cli ls Node

# Check connections
pw-link -l
```

### High latency

The default configuration prioritizes quality over latency. For lower latency:

1. Reduce compressor/gate attack/release times
2. Reduce FFT sizes in spectral processors
3. Consider disabling the noise suppressor

## Performance

- **CPU Usage**: ~2-5% on modern systems (tested on i7-12700F)
- **Latency**: ~20-50ms (acceptable for STT, not suitable for real-time monitoring)
- **Memory**: ~50MB additional PipeWire memory usage

## Contributing

Contributions welcome! Areas of interest:

- Additional microphone profiles
- Alternative LADSPA/LV2 plugin recommendations
- Performance optimizations
- Better de-reverb algorithms

## License

MIT License - See LICENSE file for details

## References

- Voice sample analysis based on raw-q2u.wav (Samson Q2U, 131 seconds)
- Optimized for home office environment with periodic background noise
- Tuned for STT accuracy rather than broadcast quality

## Author

Daniel Rosehill
- Website: [danielrosehill.com](https://danielrosehill.com)
- Email: public@danielrosehill.com
