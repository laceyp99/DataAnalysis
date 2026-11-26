# Data Analysis Projects

This repository explores music through audio, lyrics, and streaming datasets.

## Current Projects

| Study | Offline report | Notebook and data |
| --- | --- | --- |
| **Does MERT match the groove or the drum kit?** compares kit and rhythm similarity across 192 listening trials. | [Open the drum study](drum-kit-vs-rhythm/report.html) | [Drum study guide](drum-kit-vs-rhythm/README.md) |
| **The sound of high energy** explores Spotify’s audio features and genre mix. | [Open the Spotify report](spotify-tracks/report.html) | [Spotify study guide](spotify-tracks/README.md) |
| **What repeated lines do to the numbers** explores distributions of repeated lines and word groups in Genius lyrics. | [Open the Genius report](genius-lyrics/report.html) | [Genius study guide](genius-lyrics/README.md) |

Open the HTML files in a local browser. Each report includes its figures and can be read without Python or the source data.

## Rebuild the reports

Install the [Quarto CLI](https://quarto.org/docs/get-started/) and use the study guides to place any required data. The reports were built with Quarto 1.11.9 and Python 3.12. From the repository root in PowerShell:

~~~powershell
$reportEnv = Join-Path $env:LOCALAPPDATA 'dataanalysis-report-env'
uv venv --python 3.12 $reportEnv
$env:QUARTO_PYTHON = Join-Path $reportEnv 'Scripts/python.exe'
uv pip install --python $env:QUARTO_PYTHON ipykernel==6.31.0 nbclient==0.10.2 nbformat==5.10.4 pyyaml==6.0.3 pandas==2.2.3 matplotlib==3.10.6

quarto render spotify-tracks/report.ipynb --execute
quarto render genius-lyrics/report.ipynb --execute
~~~
