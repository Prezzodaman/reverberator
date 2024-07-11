# Reverberator

A simple reverb library written using the basic principle that reverb's just a ton of slightly different delays!

## Stuff
* **Reverberator**() - Initializes a Reverberator object. The keywords **preset**, **reflections**, **size**, **length**, **dry**, **wet** and **predelay** can all be specified as arguments!
* **set_preset**(preset, sample_rate) - Sets the preset. The sample rate is required to achieve a consistent predelay. The list of available presets is:
    * small_room, medium_room, large_room, small_hall, medium_hall, large_hall, church, arena, dampened
* **get_crunched_wave**(wave_file) - Converts the wave to an "object" that can be used by Reverberator (supports 8-bit, 16-bit and 24-bit). The "object" will be referred to as a sound for convenience, and is actually a dict consisting of:
    * **"bytes"** - The converted bytes from -32768 to 32767, regardless of bit depth
    * **"sample_rate"** - you work it out
* **get_processed_bytes**(sound) - Supplied a sound, this will return one in the same format, but processed through the specified reverb! **clip** and **normalize** can be specified as optional arguments.
* **save**(sound, filename) - This will save the specified sound (ssss) to a wave file.

## Basic usage

```
import reverberator
import wave

reverb = reverberator.Reverberator()

wave_crunched = reverb.get_crunched_wave("input.wav")
reverb.set_preset("small_room", wave_crunched["sample_rate"])
wave_processed = reverb.get_processed_bytes(wave_crunched, normalize=True)
reverb.save(wave_processed, "output.wav")
```

## Plans

I planned to get real-time reverb working (the whole reason I made it into a library), but unfortunately it's extremely slow and basically unusable for that purpose. I'd love to figure it out one day!