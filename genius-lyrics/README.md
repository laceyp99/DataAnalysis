# What repeated lines do to the numbers

Open [report.html](report.html) in a browser. The [Quarto notebook](report.ipynb) compares repeated-line distributions and recurring word groups from 2 to 64 words across Genius tags using English lyrics of similar length from the 2010s.

## Data and rendering

Download version 1 of [Genius Song Lyrics with Language Information](https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information/data). Save the downloaded ZIP as `data/song_lyrics.zip` in this directory, or extract its CSV to `data/song_lyrics.csv`. If you already have the CSV from the original notebook, move it to `data/song_lyrics.csv`. The notebook uses the CSV when both formats are present. The ZIP is about 3.3 GB and can be read directly, saving about 9 GB of extracted disk space.

The notebook streams the archive and computes metrics on a deterministic sample of song IDs. Expect a few minutes to read the archive and rebuild the charts. Only aggregate measurements appear in the rendered report.

Follow the [repository setup](../README.md#rebuild-the-reports), then run the following in this directory:

~~~powershell
quarto render report.ipynb --execute
Start-Process .\report.html
~~~
