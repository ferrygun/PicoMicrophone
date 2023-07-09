import machine
import uio

# Configure the MAX9814 microphone module
mic_pin = machine.ADC(26)

# Set the audio parameters
sample_rate = 16000  # Sample rate in Hz
bits_per_sample = 16  # Bits per sample
recording_time = 5  # Duration of recording in seconds
conversion_factor =3.3/(4096)

# Calculate the number of samples to record
num_samples = sample_rate * recording_time

# Create a byte array to store the audio samples
audio_data = bytearray(num_samples * 2)  # 2 bytes per sample (16 bits)

# Start recording audio
for i in range(num_samples):
    sample = mic_pin.read_u16()*conversion_factor   
    audio_data[i * 2] = int(sample) & 0xFF  # Least significant byte
    audio_data[i * 2 + 1] = (int(sample) >> 8) & 0xFF  # Most significant byte

# Create a WAV file
with uio.open("recording.wav", "wb") as wav_file:
    wav_file.write(b"RIFF")
    wav_file.write((36 + len(audio_data)).to_bytes(4, "little"))  # Chunk size
    wav_file.write(b"WAVE")
    wav_file.write(b"fmt ")
    wav_file.write((16).to_bytes(4, "little"))  # Subchunk1 size
    wav_file.write((1).to_bytes(2, "little"))  # Audio format (PCM)
    wav_file.write((1).to_bytes(2, "little"))  # Number of channels (mono)
    wav_file.write(sample_rate.to_bytes(4, "little"))  # Sample rate
    wav_file.write((sample_rate * bits_per_sample // 8).to_bytes(4, "little"))  # Byte rate
    wav_file.write((bits_per_sample // 8).to_bytes(2, "little"))  # Block align
    wav_file.write(bits_per_sample.to_bytes(2, "little"))  # Bits per sample
    wav_file.write(b"data")
    wav_file.write(len(audio_data).to_bytes(4, "little"))  # Subchunk2 size
    wav_file.write(audio_data)

print("Recording saved as 'recording.wav'")

