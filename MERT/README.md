# Does MERT match the groove or the drum kit?

## Listen

Open [report.html](report.html) in a browser. On Windows, from the repository root:

~~~powershell
Start-Process .\MERT\report.html
~~~

Keep the report next to its audio folder and score table when copying it. The rendered study plays locally without Python. [Read the notebook](report.ipynb) or [inspect the trial scores](trials.csv).

## Experiment

Four backing patterns, three snare parts and four kits produce 48 four-second clips. Every clip starts on beat one at 120 BPM. In each trial, one alternative keeps the snare rhythm while changing the kit. The other keeps the kit while changing the snare rhythm. Both preserve the backing pattern.

The opening rhythm comparison changes a snare on beat 3 to snares on beats 2 and 4. The companion comparison moves beats 1 and 3 to beats 2 and 4, holding the number of hits constant. Each kit pair and rhythm comparison contributes four reference positions. The 192 trials reuse the same clips and describe this particular collection of drum sounds.

## Reproduce the scores

Use Python 3.11. The following PowerShell commands run from the MERT directory. Supply your own environment path if preferred.

~~~powershell
$studyEnv = Join-Path $env:LOCALAPPDATA 'mert-study-env'
uv venv --python 3.11 $studyEnv
$studyPython = Join-Path $studyEnv 'Scripts/python.exe'
uv pip install --python $studyPython torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
uv pip install --python $studyPython transformers==4.46.3 numpy==1.26.4
& $studyPython score.py
~~~

The first scoring run needs the pinned MERT checkpoint from Hugging Face. The published model weights have their own CC BY-NC 4.0 license. This repository includes the measured scores. [Model card and license](https://huggingface.co/m-a-p/MERT-v1-95M).

The primary score compares the mean final-layer vectors using cosine similarity. The timing check averages cosine similarity across aligned frames. The signed margin is same-rhythm similarity minus same-kit similarity. Outcomes use full precision and exact equality for ties.

## Rebuild the audio and report

To regenerate the source audio before scoring, run these commands in the same study environment:

~~~powershell
uv pip install --python $studyPython scipy==1.16.1 soundfile==0.13.1
& $studyPython render.py
~~~

The one-shots, their upstream licenses, and the instrument choices are documented in [sample credits](samples/README.md). The render writes 48 WAV files and [their manifest](manifest.csv). The AVL kits use the same closed-hat recording. Keep that shared sound in mind when interpreting their kit-to-kit comparison.

To rebuild the HTML, install the [Quarto CLI](https://quarto.org/docs/get-started/) and run the following from the MERT directory. The report was rendered with Quarto 1.11.9. It reads the existing CSV and WAVs, so this step can run independently of the model.

~~~powershell
$reportEnv = Join-Path $env:LOCALAPPDATA 'mert-report-env'
uv venv --python 3.12 $reportEnv
$env:QUARTO_PYTHON = Join-Path $reportEnv 'Scripts/python.exe'
uv pip install --python $env:QUARTO_PYTHON jupyter==1.1.1 plotly==6.5.2
quarto render report.ipynb --execute
Start-Process .\report.html
~~~
