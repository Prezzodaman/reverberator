import reverberator
import wave
import argparse

reverb = reverberator.Reverberator()

parser = argparse.ArgumentParser(description="Adds reverb to a wave file")
parser.add_argument("input_file", type=argparse.FileType("r"), help="The name of the original file")
parser.add_argument("output_file", type=argparse.FileType("w"), help="The name of the reverbed file")
parser.add_argument("preset", type=str, choices=reverb.presets.keys(), help="The reverb preset to use")
parser.add_argument("-r", "--reflections", type=int, help="The reflectivity of the virtual room")
parser.add_argument("-s", "--size", type=int, help="The size of the virtual room")
parser.add_argument("-l", "--length", type=int, choices=range(0, 101), metavar="(0-100)", help="The length of the reverb (higher values result in a longer reverb)")
parser.add_argument("-d", "--dry", type=int, choices=range(0, 101), metavar="volume (0-100)", help="The volume of the dry (unprocessed) signal")
parser.add_argument("-w", "--wet", type=int, choices=range(0, 101), metavar="volume (0-100)", help="The volume of the wet (processed) signal")
parser.add_argument("-p", "--predelay", type=int, choices=range(0, 2001), metavar="(0-2000)", help="How long to delay the reverb (in milliseconds)")
parser.add_argument("-v", "--verbose", action="store_true", help="Display detailed information while rendering")

args = parser.parse_args()
input_file = args.input_file.name
output_file = args.output_file.name
preset = args.preset
verbose = args.verbose

print("ReVeRbErAtOr!!! (v0.1)")
print("by Presley Peters, 2024")
print()

if not verbose:
	print("Crunching wave file...")
wave_crunched = reverb.get_crunched_wave(input_file, verbose=verbose)
reverb.set_preset(preset, wave_crunched["sample_rate"])
reflections = args.reflections
size = args.size
length = args.length
dry = args.dry
wet = args.wet
predelay = args.predelay
if reflections is not None:
	reverb.reflections = reflections / 100
if size is not None:
	reverb.size = size / 100
if length is not None:
	reverb.length = length / 100
if dry is not None:
	reverb.dry_level = dry / 100
if wet is not None:
	reverb.wet_level = wet / 100
if predelay is not None:
	reverb.predelay = predelay / 100

if reflections is not None or size is not None or length is not None or wet is not None or dry is not None:
	print(f"Rendering using preset: {preset}... (with overrides)")
else:
	print(f"Rendering using preset: {preset}...")
if verbose:
	print(f" - Reflections: {reverb.reflections}")
	print(f" - Size: {reverb.size}")
	print(f" - Length: {reverb.length}")
	print(f" - Dry level: {reverb.dry_level}")
	print(f" - Wet level: {reverb.wet_level}")
	print(f" - Predelay: {reverb.predelay}")
	print()

reverb.save(reverb.get_processed_bytes(wave_crunched, normalize=True, verbose=verbose), output_file)

print("Done!")