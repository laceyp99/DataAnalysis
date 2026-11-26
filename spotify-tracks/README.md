# The sound of high energy

Open [report.html](report.html) in a browser. The [Quarto notebook](report.ipynb) compares Spotify’s energy and valence scores, including within a narrow energy band, then shows which tracks move the pooled loudness gap and which genre labels qualify for that comparison. It also includes the original key and mode exploration, using distinct track IDs.

## Data and rendering

The checkout includes [data/dataset.csv](data/dataset.csv) from the [Spotify Tracks Dataset on Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/data). The notebook also accepts `dataset.csv` alongside the notebook. The raw table has 114,000 rows, balanced across 114 genre labels. The report counts Spotify track IDs once across the sample or once per label, depending on the comparison.

Follow the [repository setup](../README.md#rebuild-the-reports), then run the following in this directory:

~~~powershell
quarto render report.ipynb --execute
Start-Process .\report.html
~~~
