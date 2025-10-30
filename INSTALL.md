# Installation Guide

This guide will help you install and configure the STT Audio Chain on your PipeWire-based Linux system.

## Prerequisites

### 1. Verify PipeWire is Running

```bash
systemctl --user status pipewire pipewire-pulse
```

If PipeWire is not running:

```bash
systemctl --user enable --now pipewire pipewire-pulse
```

### 2. Install Required LADSPA Plugins

The audio chain uses LADSPA plugins for compression, gating, and noise suppression.

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ladspa-sdk swh-plugins calf-plugins
```

**Arch Linux:**
```bash
sudo pacman -S ladspa swh-plugins calf
```

**Fedora:**
```bash
sudo dnf install ladspa ladspa-swh-plugins calf
```

### 3. Verify LADSPA Plugins are Installed

```bash
listplugins 2>/dev/null | grep -E "(gate_1410|sc4_1882)"
```

You should see output showing these plugins. If not, the required packages may not be installed correctly.

## Installation Methods

### Method 1: Using the CLI Script (Recommended)

1. Clone or download this repository
2. Navigate to the repository directory
3. Run the installation command:

```bash
./stt-chain install
```

This will:
- Copy the configuration to `~/.config/pipewire/pipewire.conf.d/`
- Restart PipeWire to load the filter chain
- Verify the chain loaded successfully

### Method 2: Manual Installation

1. Create the PipeWire configuration directory if it doesn't exist:

```bash
mkdir -p ~/.config/pipewire/pipewire.conf.d
```

2. Copy the configuration file:

```bash
cp stt-audio-chain.conf ~/.config/pipewire/pipewire.conf.d/
```

3. Restart PipeWire:

```bash
systemctl --user restart pipewire
```

4. Verify the chain loaded:

```bash
pw-cli ls Node | grep "STT"
```

You should see output mentioning "STT Microphone Audio Chain".

## Post-Installation

### 1. Verify the Audio Chain is Running

```bash
./stt-chain status
```

Expected output:
```
==========================================
STT Audio Chain Status
==========================================

[OK] PipeWire: running
[OK] Configuration: installed
[OK] Audio chain: loaded

Chain Node ID: [some number]

Available nodes:
[List of STT-related nodes]
==========================================
```

### 2. Connect Your Microphone

Use a PipeWire graph tool to route your microphone through the filter chain:

**Using qpwgraph (GUI - Recommended for first-time setup):**

1. Install qpwgraph:
   ```bash
   sudo apt install qpwgraph  # Ubuntu/Debian
   ```

2. Launch qpwgraph:
   ```bash
   qpwgraph &
   ```

3. In the graph view:
   - Find your microphone on the left (Audio → Sources)
   - Find "STT Microphone Audio Chain" on the right (Audio → Sinks)
   - Drag a connection from your microphone to the audio chain input

4. On the right side:
   - Find "STT Microphone Audio Chain" in Sources
   - Connect it to your desired destination (e.g., your STT application input)

**Using pw-link (CLI):**

First, find your microphone name:
```bash
pw-link --links | grep -i input
```

Then link it to the audio chain (replace `Your_Mic_Name` with actual name):
```bash
pw-link "Your_Mic_Name:capture_FL" "stt_audio_chain_playback:playback_FL"
pw-link "Your_Mic_Name:capture_FR" "stt_audio_chain_playback:playback_FR"
```

### 3. Test the Audio Chain

Record a short audio sample to test the processing:

```bash
# Record 10 seconds through the processed chain
pw-record --target stt_audio_chain_capture test-processed.wav &
sleep 1
arecord -d 10 -f cd test-raw.wav

# Compare the files in Audacity or your audio player
```

## Optional: Enable Auto-Start on Boot

If you want the audio chain to start automatically when you log in:

### Using systemd User Service

1. Copy the service file:

```bash
cp stt-audio-chain.service ~/.config/systemd/user/
```

2. Reload systemd and enable the service:

```bash
systemctl --user daemon-reload
systemctl --user enable stt-audio-chain.service
```

3. The service will now start automatically when you log in.

**Note:** The systemd service simply ensures the configuration stays enabled. PipeWire automatically loads the filter chain when it finds the config file.

## Optional: Install CLI Script System-Wide

To use the `stt-chain` command from anywhere:

```bash
sudo cp stt-chain /usr/local/bin/
sudo chmod +x /usr/local/bin/stt-chain
```

Now you can run commands like:
```bash
stt-chain status
stt-chain restart
```

## Troubleshooting Installation

### Issue: "Configuration: installed" but "Audio chain: not loaded"

**Cause:** LADSPA plugins may not be installed or PipeWire can't find them.

**Solution:**
1. Verify LADSPA plugins are installed (see Prerequisites)
2. Check PipeWire logs for errors:
   ```bash
   journalctl --user -u pipewire -n 50
   ```
3. Look for errors mentioning "ladspa", "plugin", or "filter-chain"

### Issue: PipeWire keeps crashing after installation

**Cause:** Syntax error in configuration or incompatible plugin.

**Solution:**
1. Temporarily disable the configuration:
   ```bash
   mv ~/.config/pipewire/pipewire.conf.d/stt-audio-chain.conf{,.disabled}
   systemctl --user restart pipewire
   ```

2. Check PipeWire logs:
   ```bash
   journalctl --user -u pipewire -n 100
   ```

3. If you find the error, fix the configuration and re-enable:
   ```bash
   mv ~/.config/pipewire/pipewire.conf.d/stt-audio-chain.conf{.disabled,}
   systemctl --user restart pipewire
   ```

### Issue: Audio sounds distorted or strange

**Cause:** Filter settings may be too aggressive for your voice/environment.

**Solution:**
1. Edit the configuration:
   ```bash
   nano ~/.config/pipewire/pipewire.conf.d/stt-audio-chain.conf
   ```

2. Try these adjustments:
   - **Reduce compression:** Lower the `"Ratio (1:n)"` in the compressor (try 2.0-2.5)
   - **Lighter noise gate:** Increase the threshold from -45 to -40 or -35 dB
   - **Less de-essing:** Increase the de-esser threshold from -18 to -12 dB

3. Restart to apply changes:
   ```bash
   systemctl --user restart pipewire
   ```

### Issue: Can't find my microphone to connect

**Solution:**
List all available audio sources:
```bash
pw-link --links
```

Or use `pw-cli`:
```bash
pw-cli ls Node | grep -A 3 "Audio/Source"
```

## Next Steps

After installation:

1. Read [VOICE_ANALYSIS.md](VOICE_ANALYSIS.md) to understand how the filter chain was tuned
2. Test the chain with your STT application
3. Adjust settings if needed (see README.md → Customization section)
4. Optionally record your own voice sample and run `analyze_audio.py` to see if you need custom tuning

## Uninstallation

To remove the STT audio chain:

```bash
# Stop and disable the service (if enabled)
systemctl --user disable --now stt-audio-chain.service
rm ~/.config/systemd/user/stt-audio-chain.service

# Remove the configuration
rm ~/.config/pipewire/pipewire.conf.d/stt-audio-chain.conf

# Restart PipeWire
systemctl --user restart pipewire

# Optionally remove system-wide CLI script
sudo rm /usr/local/bin/stt-chain
```

## Getting Help

If you encounter issues:

1. Check [README.md](README.md) Troubleshooting section
2. Review PipeWire logs: `journalctl --user -u pipewire -n 100`
3. Open an issue on GitHub with:
   - Your distro and PipeWire version (`pw-cli --version`)
   - Output of `./stt-chain status`
   - Relevant log excerpts
