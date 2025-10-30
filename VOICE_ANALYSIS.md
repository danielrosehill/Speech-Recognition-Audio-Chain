# Voice Sample Analysis - Samson Q2U

## Sample Information
- **File**: voice-samples/raw-q2u.wav
- **Microphone**: Samson Q2U (untreated, direct USB recording)
- **Date Analyzed**: 2025-10-30
- **Format**: 16-bit Stereo, 44.1 kHz
- **Duration**: 130.96 seconds (2 minutes 11 seconds)
- **Recording**: Full profile reading from texts/full-profile.txt

## Audio Characteristics

### Level Metrics
- **RMS Level**: -22.06 dB
- **Peak Level**: 0.00 dB (normalized)
- **Crest Factor**: 12.68 (moderate dynamic variation)
- **Noise Floor**: -56.68 dB (10th percentile)
- **Dynamic Range**: 56.68 dB
- **Estimated SNR**: 42.29 dB (moderate background noise present)

### Speech Dynamics (2-second segment analysis)
- **Loudest segment**: -14.11 dB
- **Quietest segment**: -25.71 dB
- **Average speech level**: -22.65 dB
- **Level variation**: 2.04 dB std dev (very consistent!)
- **Dynamic range of speech**: 11.59 dB

**Observation**: Daniel maintains remarkably consistent levels - only 2 dB standard deviation across 65 segments. This indicates good microphone technique and minimal need for aggressive AGC.

### Frequency Distribution

**Frequency Band Energy:**
| Band | Energy | Peak Frequency | Peak Level |
|------|--------|----------------|------------|
| Sub-bass (20-60 Hz) | 1.82% | 32 Hz | -52.45 dB |
| Bass/Rumble (60-120 Hz) | 4.62% | 118 Hz | -49.68 dB |
| **Low-mids/Body (120-500 Hz)** | **58.88%** | **188 Hz** | **-45.60 dB** |
| Mids/Presence (500-2000 Hz) | 25.43% | 501 Hz | -51.13 dB |
| Upper-mids/Clarity (2-4 kHz) | 5.32% | 2719 Hz | -63.06 dB |
| Presence/Sibilance (4-8 kHz) | 2.60% | 4183 Hz | -67.57 dB |
| Air/Brilliance (8-12 kHz) | 0.71% | 8199 Hz | -74.27 dB |
| Ultra-high (12-20 kHz) | 0.12% | 12037 Hz | -81.31 dB |

**Key Observations:**
- Nearly 60% of energy concentrated in 120-500 Hz range (fundamental voice frequencies)
- Low sibilance content (2.6%) - very gentle de-essing needed
- Minimal ultra-low rumble (1.82% below 60 Hz)
- Natural voice with good frequency balance

### Sibilance Analysis

| Band | Energy | Avg Level | Peak Frequency |
|------|--------|-----------|----------------|
| Lower sibilance (3-5 kHz) | 3.63% | -70.20 dB | 3677 Hz |
| **Primary sibilance (5-7 kHz)** | **1.15%** | **-75.13 dB** | **5168 Hz** |
| Upper sibilance (7-10 kHz) | 0.69% | -78.67 dB | 8199 Hz |

**Primary Sibilance Frequency**: 4183 Hz

**Observation**: Very low sibilance content overall. This is a warm, smooth voice that requires only gentle de-essing. Aggressive sibilance reduction would dull the voice unnecessarily.

### Background Noise Analysis

**Quiet sections analyzed**: 26.2 seconds (20% of recording)

| Noise Type | Avg Noise Level | Peak Frequency | Peak Level |
|------------|-----------------|----------------|------------|
| Low rumble (20-80 Hz) | -86.66 dB | 32 Hz | -86.01 dB |
| AC hum (50-60 Hz) | -86.23 dB | 54 Hz | -86.23 dB |
| HVAC/Room (80-200 Hz) | -86.31 dB | 118 Hz | -84.62 dB |
| Mid-range noise (200-1000 Hz) | -90.18 dB | 226 Hz | -87.27 dB |
| High-freq noise (1-5 kHz) | -92.83 dB | 1766 Hz | -91.02 dB |

**Observations:**
- Very low noise floor during quiet sections (avg -86 to -92 dB)
- Some low-frequency room noise present (HVAC at 118 Hz)
- No significant AC hum or electrical interference
- Clean recording environment overall

## Recommendations Based on Analysis

### 1. **High-Pass Filter**
**Priority**: MEDIUM
- **Current state**: 2.48% energy below 80 Hz
- **Assessment**: Minimal low-frequency content, gentle filtering sufficient
- **Recommendation**: 60-80 Hz cutoff, 12 dB/octave slope
- **Purpose**: Remove subsonic rumble without affecting voice body

### 2. **Noise Gate**
**Priority**: MEDIUM-HIGH
- **Current state**: SNR 42 dB (moderate background noise)
- **Assessment**: Noise gate needed to handle room noise and periodic disturbances
- **Recommendation**:
  - Threshold: -45 to -40 dB
  - Fast attack (5 ms) to catch speech onset
  - Moderate hold (100-200 ms) to avoid chopping
  - Gentle release (150 ms)
- **Purpose**: Suppress background noise during pauses without cutting off speech

### 3. **Compression/AGC**
**Priority**: LOW-MEDIUM
- **Current state**: Very consistent speech (2.04 dB variation)
- **Assessment**: Minimal compression needed due to excellent natural consistency
- **Recommendation**:
  - Threshold: -22 dB (just above average speech level)
  - Ratio: 3:1 to 4:1 (gentle compression)
  - Attack: 10 ms
  - Release: 150 ms
  - Makeup gain: +4 to +6 dB
- **Purpose**: Gentle peak limiting and slight loudness normalization for STT

### 4. **De-essing**
**Priority**: LOW
- **Current state**: Only 2.60% sibilance energy (very low)
- **Assessment**: Minimal sibilance - gentle de-essing sufficient
- **Recommendation**:
  - Center frequency: 4183 Hz
  - EQ cut: -2 to -4 dB, Q=2.0
  - Alternative: Dynamic de-esser with 3:1 ratio, -15 dB threshold
- **Purpose**: Subtle sibilance control without dulling voice

### 5. **De-reverb**
**Priority**: LOW-MEDIUM
- **Assessment**: Room acoustics present but not severe
- **Recommendation**: Gentle low-pass filter at 8 kHz
- **Purpose**: Reduce room reflections slightly

### 6. **Noise Suppression**
**Priority**: MEDIUM
- **Current state**: Moderate background noise (SNR 42 dB)
- **Recommendation**: RNNoise-style adaptive suppressor with VAD
- **Purpose**: Handle periodic background noise (mentioned: "screaming baby")

## Optimized Processing Chain

Based on the comprehensive analysis, the recommended signal flow is:

```
Input Mic →
HPF (80Hz, 12dB/oct) →
Noise Gate (-45dB, 5ms attack, 150ms hold/release) →
Dereverb (LPF 8kHz) →
Compressor (3:1, -22dB, 10ms/150ms, +5dB makeup) →
De-esser (gentle, 4.2kHz, -3dB or 3:1 dynamic) →
Adaptive Noise Suppressor (VAD-based) →
Limiter (0.95 ceiling) →
Output
```

## Audacity Test Settings

For testing this processing chain in Audacity before implementing in PipeWire:

1. **Effect > High-Pass Filter**
   - Frequency: 80 Hz
   - Rolloff: 24 dB/octave

2. **Effect > Noise Gate**
   - Gate threshold: -45 dB
   - Gate knee: 3 dB
   - Attack/Decay: 10 ms / 100 ms

3. **Effect > Compressor**
   - Threshold: -22 dB
   - Ratio: 4:1
   - Attack time: 10 ms
   - Release time: 150 ms
   - Makeup gain: +6 dB
   - Compress based on: RMS

4. **Effect > Equalization (Graphic EQ)**
   - 4183 Hz: -4 dB (bandwidth ~2 octaves, Q=2.0)

5. **Effect > Limiter**
   - Type: Hard Limit
   - Limit to: -1 dB
   - Hold: 10 ms

## Comparison: Initial vs. Comprehensive Sample

| Metric | Initial Sample (45s) | Comprehensive Sample (131s) |
|--------|---------------------|------------------------------|
| Dynamic Range | 76.33 dB | 56.68 dB |
| Speech Variation | Not analyzed | 2.04 dB (excellent!) |
| SNR | 69.78 dB | 42.29 dB |
| Sibilance Energy | 5.87% | 2.60% |
| Low-freq Energy | 9.95% | 7.34% |

**Conclusion**: The comprehensive sample better represents real-world usage and shows Daniel has excellent microphone technique with very consistent levels. Processing can be gentler than initially anticipated.

## Filter Settings Summary

**For lightweight STT optimization:**

- ✅ Gentle HPF (80 Hz) - minimal rumble
- ✅ Moderate noise gate (-45 dB) - handle room/background noise
- ✅ Light compression (3-4:1) - speaker is already very consistent
- ✅ Minimal de-essing - very low sibilance content
- ✅ Adaptive noise suppression - for periodic disturbances
- ✅ Safety limiter - prevent any clipping

**Overall philosophy**: Preserve the natural, warm character of the voice while providing clean input for STT engines.
