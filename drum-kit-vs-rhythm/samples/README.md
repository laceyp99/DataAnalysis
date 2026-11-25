# Drum sample sources

The one-shots here are byte-for-byte copies of the upstream FLACs under shorter filenames. The rendered WAVs in `../audio/` use the kick, snare and closed hi-hat from one kit per clip.

## Credits and licenses

- **AVL Drumkits, Black Pearl and Red Zeppelin** by Glen MacArthur (2015), in SFZ, SF2 and Hydrogen drumkit formats. Contact `info@bandshed.net`. The samples are licensed under CC BY-SA 3.0 Unported. The author’s notice applies ShareAlike to modifications of the samples and new sample libraries made with them, and allows separate licensing of produced music and other works outside sample libraries. It asks redistributors to retain the author information and notice, and requires modified libraries to use a different name. Both kits use the same Sabian closed hi-hat recording. [Project website](https://www.bandshed.net/avldrumkits/) · [Author’s license notice](https://github.com/studiorack/avl-drumkits/blob/b06cb2c27359cbc68a830a82bddced05bd73d1a0/AVL-Drumkits%20CC-BY-SA%20License.pdf) · [License text](black-pearl/LICENSE.txt).
- **Virtuosity Drums** by Versilian Studios and Karoryfer Samples, performed by Austin McMahon and recorded at Virtuosity Musical Instruments in Boston. The study uses overhead-mic recordings, under CC0 1.0 Universal. [Pinned source](https://github.com/sfzinstruments/virtuosity_drums/tree/9f04cf9a734527edfbb0a4eee1f674e45bbf71bc) · [License text](virtuosity/LICENSE.txt).
- **Phazite Sounds** by August Byrne, under CC0 1.0 Universal. The three selected electronic hits come from Roberto’s FreePats *Synthesizer Percussion* library. [Pinned source](https://github.com/august-byrne/phazite-sounds/tree/bd71faf5035e8aa278ebfe3f4dc68804ae7bc5ca) · [Upstream provenance](https://github.com/august-byrne/phazite-sounds/blob/bd71faf5035e8aa278ebfe3f4dc68804ae7bc5ca/pack/sources.json) · [License text](phazite/LICENSE.txt).

## Upstream files

Paths are relative to the respective repositories. Each SHA-256 matches both the pinned upstream file and its local copy.

| Local file | Upstream path | SHA-256 |
| --- | --- | --- |
| `black-pearl/kick.flac` | `Samples/36-Pearl22Kick-4.flac` | `83714fe787a09528966a00223614d64d6d5d2f16dbafd73d7fa05048ef38cb19` |
| `black-pearl/snare.flac` | `Samples/38-PearlSnare-4.flac` | `a9d2d70256500920a47d358fdc546ed1a4ca2eb200e51e204eca6ca8691f04b3` |
| `black-pearl/hat.flac` | `Samples/42-SabianRockHatClosed-4.flac` | `e46588123d1f1891c03bed16c595a0a29ec537d6fdaa69f76461149400f7d7d5` |
| `red-zeppelin/kick.flac` | `Samples/36-Ludwig26Kick-4.flac` | `81b21873bae6ac53acfda428c7f16090d4a645f032a9bf0f4c505c8c364c8075` |
| `red-zeppelin/snare.flac` | `Samples/38-PorkpieSnare-4.flac` | `f35cfd3377e84407dd609a24506a03d24933df0c04ae967f8b19bfa4956befe9` |
| `red-zeppelin/hat.flac` | `Samples/42-SabianRockHatClosed-4.flac` | `e46588123d1f1891c03bed16c595a0a29ec537d6fdaa69f76461149400f7d7d5` |
| `virtuosity/kick.flac` | `Samples/oh/kick/oh_kick_snon_vl3_rr1.flac` | `eb415311ae9dd3068e1ee7b06600556fb1f0c6b7a2e795f2ecb57aadb22ef970` |
| `virtuosity/snare.flac` | `Samples/oh/snare/oh_snare_center_vl26.flac` | `0e43265973be2fe792aa3546da5ea2067f52e620b459de71373d165e3c5c3eca` |
| `virtuosity/hat.flac` | `Samples/oh/hh/oh_hh_closed_vl3_rr1.flac` | `328a4d33daf15c72362db234312eba56eda60c1668f5c39a5527d61279793fef` |
| `phazite/kick.flac` | `pack/Drums/Kicks/Kick Electronic.flac` | `3a601daabca1c91289f8b45a4520252b09f15b8a392ce9b7a3a437fab3574c6a` |
| `phazite/snare.flac` | `pack/Drums/Snares/Snare Electronic.flac` | `d1fa4121a6d9bd1e38c1c1f49e30cdd567df08504982804e8b29737dae5b63f1` |
| `phazite/hat.flac` | `pack/Drums/Hats/Hat Closed Electronic.flac` | `51be1962919d4da5a4e80ff0060c7ac2d1ee2b74d98853a90500519694b834a3` |

[Pinned AVL Drumkits source](https://github.com/studiorack/avl-drumkits/tree/b06cb2c27359cbc68a830a82bddced05bd73d1a0).

## Rendering and balance

[`render.py`](../render.py) averages channels, resamples to 24 kHz, and trims each attack to its first sample at or above 2% of that hit’s absolute peak. It places the trimmed attacks on the 120 BPM grid, caps hits longer than 750 ms with a 25 ms fade, and fades the final 10 ms of each clip.

The linear gains below are fixed for every clip using a given kit. The resulting unweighted RMS over each hit’s first 100 ms, before the common mix gain, spans −13.2 to −12.5 dBFS for kick, −16.0 to −15.7 dBFS for snare, and −24.8 to −23.0 dBFS for closed hi-hat.

| Kit | Kick | Snare | Closed hi-hat |
| --- | ---: | ---: | ---: |
| Virtuosity | 24.0 | 3.0 | 16.0 |
| Black Pearl | 0.55 | 0.50 | 1.2 |
| Red Zeppelin | 0.55 | 0.73 | 1.2 |
| Phazite | 0.85 | 0.90 | 0.80 |

A single gain of approximately 0.671307 scales the loudest mix peak to 0.85 before 16-bit PCM encoding. The finished clip RMS levels span −24.26 to −20.96 dBFS.

The 48 WAVs and manifest were reproduced byte-for-byte with Python 3.11.9, NumPy 1.26.4, SciPy 1.16.1, SoundFile 0.13.1, and libsndfile 1.2.2. An independent onset grid accounted for all 1,072 hit placements, reproducing the stored waveforms to within one PCM quantization step.
