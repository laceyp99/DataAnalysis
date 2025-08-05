# Genius Lyrics Dataset Analysis

This project analyzes song lyrics from the Genius platform to understand patterns in vocabulary richness and language distribution across different songs.

## Dataset

**Source**: [Genius Song Lyrics with Language Information - Kaggle](https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information/data)

The dataset contains song lyrics from Genius.com along with metadata including:
- Song titles and artists
- Lyrics text
- Language detection information (multiple detection methods)
- Various other metadata fields

## Analysis Overview

### 1. Data Loading and Exploration
- Loaded the dataset using pandas
- Explored the structure and content of the data
- Identified key features for analysis

### 2. Data Cleaning
- **Missing Data Handling**: Identified missing values across all columns
- **Language Processing**: 
  - Consolidated language information from multiple detection sources
  - Filled missing language tags using alternative language detection columns
  - Removed entries with no language information
- **Title Cleaning**: Replaced null titles with 'Unknown' to retain data

### 3. Feature Engineering
Created new metrics to analyze lyrical complexity:
- **Word Count**: Total number of words in each song
- **Unique Word Count**: Number of distinct words used
- **Vocabulary Richness**: Ratio of unique words to total words (unique_words / total_words)

### 4. Vocabulary Richness Analysis
- Generated distribution histogram of vocabulary richness across all songs
- Analyzed how diverse the vocabulary is in different songs
- Used custom formatting for better visualization (thousands format on y-axis)

## Key Findings

The analysis focuses on **vocabulary richness** as a measure of lyrical diversity:
- **Vocabulary Richness Score**: Ranges from 0 to 1, where higher values indicate more diverse vocabulary
- The distribution shows how varied artists are in their word choice and lyrical complexity
- This metric helps identify songs with repetitive vs. diverse language patterns

## Future Analysis Ideas

- Language-specific vocabulary richness comparison
- Artist-based vocabulary analysis
- Temporal trends in lyrical complexity
- Genre-based lyrical pattern analysis
- Sentiment analysis integration