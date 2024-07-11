import random
import wave
import time

class Reverberator:
	def __init__(self, preset=None, reflections=None, size=None, length=None, dry=None, wet=None, predelay=None):
		self.presets = {
			"small_room":  {"reflections": 20,  "size": 1000, "length": 0.6,  "dry": 0.8, "wet": 1.8, "predelay": 0},
			"medium_room": {"reflections": 35,  "size": 2000, "length": 0.6,  "dry": 0.8, "wet": 1.5, "predelay": 0.01},
			"large_room":  {"reflections": 40,  "size": 3000, "length": 0.6,  "dry": 0.6, "wet": 1,   "predelay": 0.02},
			"small_hall":  {"reflections": 40,  "size": 2000, "length": 0.7,  "dry": 0.8, "wet": 2,   "predelay": 0},
			"medium_hall": {"reflections": 50,  "size": 3000, "length": 0.75, "dry": 0.8, "wet": 1.8, "predelay": 0.01},
			"large_hall":  {"reflections": 60,  "size": 4000, "length": 0.8,  "dry": 0.6, "wet": 1.5, "predelay": 0.02},
			"church":      {"reflections": 70,  "size": 5000, "length": 0.85, "dry": 1,   "wet": 1,   "predelay": 0.06},
			"arena":       {"reflections": 100, "size": 6000, "length": 0.8,  "dry": 0.8, "wet": 2.4, "predelay": 0.1},
			"dampened":    {"reflections": 20,  "size": 500,  "length": 0.5,  "dry": 1,   "wet": 6,   "predelay": 0}
		}

		random.seed(120)  # funny number
		if preset is None:
			if reflections is not None:
				self.reflections = reflections
			if size is not None:
				self.size = size
			if length is not None:
				self.length = length
			if dry is not None:
				self.dry_level = dry
			if wet is not None:
				self.wet_level = wet
			if predelay is not None:
				self.predelay = predelay
		else:
			self.set_preset(preset)
			if reflections is None:
				self.reflections = self.presets[preset]["reflections"]
			else:
				self.reflections = reflections
			if size is None:
				self.size = self.presets[preset]["size"]
			else:
				self.size = size
			if length is None:
				self.length = self.presets[preset]["length"]
			else:
				self.length = length
			if dry is None:
				self.dry_level = self.presets[preset]["dry"]
			else:
				self.dry_level = dry
			if wet is None:
				self.wet_level = self.presets[preset]["wet"]
			else:
				self.wet_level = wet
			if predelay is None:
				self.predelay = self.presets[preset]["predelay"]
			else:
				self.predelay = predelay
		self.print_counter_max = 2000

	def set_preset(self, preset, sample_rate):
		self.reflections = self.presets[preset]["reflections"]
		self.size = self.presets[preset]["size"]
		self.length = self.presets[preset]["length"]
		self.dry_level = self.presets[preset]["dry"]
		self.wet_level = self.presets[preset]["wet"]
		self.predelay = self.presets[preset]["predelay"]

		self.buffer_lengths = []
		for a in range(0, self.reflections):  # beep bip boop bep bop
			self.buffer_lengths.append(random.randint((self.size // 100) + 1, self.size))
		self.buffer_positions = [0] * len(self.buffer_lengths)
		self.buffers = []
		for length in self.buffer_lengths:
			self.buffer_temp = [0] * length
			self.buffers.append(self.buffer_temp.copy())
		temp = [0, 0]
		self.predelay_buffer = []
		for a in range(0, int(self.predelay * sample_rate)):
			self.predelay_buffer.append(temp.copy())

	def get_crunched_wave(self, filename, verbose=False):
		with wave.open(filename, "rb") as wave_file:
			print_counter = 0
			sound = {
				"bytes": [],
				"sample_rate": wave_file.getframerate()
			}
			sound_temp = wave_file.readframes(wave_file.getnframes())
			if wave_file.getsampwidth() == 1:
				for byte in range(0, len(sound_temp) - (wave_file.getnchannels() - 1), wave_file.getnchannels()):
					byte_left = ((sound_temp[byte] - 128) / 128) * 32768
					if wave_file.getnchannels() == 1:
						sound["bytes"].append([byte_left])
					elif wave_file.getnchannels() == 2:
						byte_right = ((sound_temp[byte + 1] - 128) / 128) * 32768
						sound["bytes"].append([byte_left, byte_right])
					if verbose:
						percentage = (byte / len(sound_temp)) * 100
						print(f"Crunching wave file... {percentage:.2f}%", end="\r")
			elif wave_file.getsampwidth() == 2:
				for byte in range(0, len(sound_temp) - (wave_file.getnchannels() - 1) * 2, wave_file.getnchannels() * 2):
					byte_left = sound_temp[byte] | (sound_temp[byte + 1] << 8)
					byte_left = ((byte_left + 32768) & 65535) - 32768
					if wave_file.getnchannels() == 1:
						sound["bytes"].append([byte_left])
					elif wave_file.getnchannels() == 2:
						byte_right = sound_temp[byte + 2] | (sound_temp[byte + 3] << 8)
						byte_right = ((byte_right + 32768) & 65535) - 32768
						sound["bytes"].append([byte_left, byte_right])
					if verbose:
						print_counter += 1
						if print_counter > self.print_counter_max:
							percentage = (byte / len(sound_temp)) * 100
							print(f"Crunching wave file... {percentage:.2f}%", end="\r")
							print_counter = 0
			elif wave_file.getsampwidth() == 3:
				for byte in range(0, len(sound_temp) - (wave_file.getnchannels() - 1) * 3, wave_file.getnchannels() * 3):
					byte_left = sound_temp[byte + 1] | (sound_temp[byte + 2] << 8)
					byte_left = ((byte_left + 32768) & 65535) - 32768
					if wave_file.getnchannels() == 1:
						sound["bytes"].append([byte_left])
					elif wave_file.getnchannels() == 2:
						byte_right = sound_temp[byte + 4] | (sound_temp[byte + 5] << 8)
						byte_right = ((byte_right + 32768) & 65535) - 32768
						sound["bytes"].append([byte_left, byte_right])
					if verbose:
						print_counter += 1
						if print_counter > self.print_counter_max:
							percentage = (byte / len(sound_temp)) * 100
							print(f"Crunching wave file... {percentage:.2f}%", end="\r")
							print_counter = 0
			return sound

	def get_processed_bytes(self, sound, clip=False, normalize=False, verbose=False):
		print_counter = 0
		processed_sound = {
			"bytes": [],
			"sample_rate": sound["sample_rate"]
		}
		start_time = time.perf_counter()
		bytes_rendered = 0
		for byte in sound["bytes"]:
			byte_left = 0
			byte_right = 0
			reverb_byte_left = 0
			reverb_byte_right = 0

			if len(byte) == 1:
				byte_left = byte[0] * self.dry_level
				byte_right = byte[0] * self.dry_level
			elif len(byte) == 2:
				byte_left = byte[0] * self.dry_level
				byte_right = byte[1] * self.dry_level

			for buff in range(0, len(self.buffer_lengths)):
				buffer_byte_temp = self.buffers[buff][self.buffer_positions[buff]]
				if len(byte) == 1:
					buffer_byte_temp += byte[0]
				elif len(byte) == 2:
					if buff % 2 == 0:
						buffer_byte_temp += byte[0]
					else:
						buffer_byte_temp += byte[1]
				buffer_byte_temp *= self.length
				self.buffers[buff][self.buffer_positions[buff]] = int(buffer_byte_temp)
				buffer_byte = self.buffers[buff][self.buffer_positions[buff]]  # B-uffer B-yte. B--ufferB--yte. BBBBBBbbbbb
				self.buffer_positions[buff] += 1
				if self.buffer_positions[buff] >= self.buffer_lengths[buff]:
					self.buffer_positions[buff] = 0
				if buff % 2 == 0:
					reverb_byte_left += buffer_byte
				else:
					reverb_byte_right += buffer_byte
			reverb_byte_left /= len(self.buffer_lengths) - 1
			reverb_byte_right /= len(self.buffer_lengths) - 1
			reverb_byte_left += 0 - (byte[0] * (self.length / 2))
			if len(byte) == 1:
				reverb_byte_right += 0 - (byte[0] * (self.length / 2))
			elif len(byte) == 2:
				reverb_byte_right += 0 - (byte[1] * (self.length / 2))

			if self.predelay == 0:
				self.predelay_buffer = [[reverb_byte_left, reverb_byte_right]]
			else:
				self.predelay_buffer.insert(0, [reverb_byte_left, reverb_byte_right])
				self.predelay_buffer.pop()

			byte_left += self.predelay_buffer[-1][0] * self.wet_level
			byte_right += self.predelay_buffer[-1][1] * self.wet_level

			if clip:
				if byte_left > 32767:
					byte_left = 32767
				if byte_left < -32768:
					byte_left = -32768
				if byte_right > 32767:
					byte_right = 32767
				if byte_right < -32768:
					byte_right = -32768
			processed_sound["bytes"].append([byte_left, byte_right])
			bytes_rendered += 1
			if verbose:
				print_counter += 1
				if print_counter > self.print_counter_max:
					time_elapsed = time.perf_counter() - start_time
					kbps = (bytes_rendered / time_elapsed) / 1000
					percentage = (bytes_rendered / len(sound["bytes"])) * 100
					time_left = ((time_elapsed / bytes_rendered) * len(sound["bytes"])) - time_elapsed
					print(f"Render speed: {kbps:.2f}kbps, {percentage:.2f}% done (approx. {time_left:.0f} seconds left) ", end="\r")
					print_counter = 0
		if normalize:
			processed_sound["bytes"] = self.get_normalized_bytes(processed_sound["bytes"])
		if verbose:
			print()
		return processed_sound

	def get_normalized_bytes(self, bytes):
		max_peak = 0
		for byte in bytes:
			byte_average = (byte[0] + byte[1]) / 2
			if byte_average > max_peak:
				max_peak = byte_average
		if max_peak == 0:
			normalize_ratio = 0
		else:
			normalize_ratio = 32768 / max_peak

		normalized_bytes = []
		for byte in bytes:
			byte_left = int(byte[0] * normalize_ratio)
			byte_right = int(byte[1] * normalize_ratio)
			if byte_left > 32767:
				byte_left = 32767
			if byte_left < -32768:
				byte_left = -32768
			if byte_right > 32767:
				byte_right = 32767
			if byte_right < -32768:
				byte_right = -32768
			normalized_bytes.append([byte_left, byte_right])
		return normalized_bytes

	def get_decrunched_bytes(self, bytes):
		raw_bytes = bytearray()
		for byte in bytes:
			byte_left = int(byte[0]) & 65535
			byte_right = int(byte[1]) & 65535

			raw_bytes.append(byte_left & 255)
			raw_bytes.append(byte_left >> 8)
			raw_bytes.append(byte_right & 255)
			raw_bytes.append(byte_right >> 8)
		return raw_bytes

	def save(self, sound, output_file):
		raw_bytes = self.get_decrunched_bytes(sound["bytes"])
		with wave.open(output_file, "wb") as wave_file:
			wave_file.setnchannels(2)
			wave_file.setsampwidth(2)
			wave_file.setframerate(sound["sample_rate"])
			wave_file.writeframesraw(raw_bytes)