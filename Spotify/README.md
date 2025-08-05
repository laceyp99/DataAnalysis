# Spotify Track Analysis

This project analyzes Spotify track data to understand patterns in audio features, musical characteristics, and content classification across different songs.

## Dataset

The dataset contains Spotify track information with various audio features and metadata including:
- Track names and artists
- Audio features (danceability, energy, loudness, valence, etc.)
- Musical characteristics (key, mode, tempo)
- Content classification (explicit/non-explicit)
- Genre information

## Analysis Overview

### 1. Data Loading and Exploration
- Loaded the dataset using pandas
- Explored dataset structure and basic statistics
- Identified key features for analysis

### 2. Data Cleaning
- **Missing Data Handling**: Identified and removed rows with missing values
- **Data Quality**: Verified data integrity after cleaning operations
- Maintained dataset completeness while ensuring data quality

### 3. Audio Features Analysis
- **Correlation Analysis**: Generated heatmap showing relationships between audio features
- **Feature Relationships**: Analyzed how different audio characteristics correlate with each other
- Key features analyzed: danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence

### 4. Musical Key and Mode Analysis
- **Key Distribution**: Analyzed distribution of songs across all 12 musical keys (C, C♯, D, etc.)
- **Major vs Minor**: Compared popularity of major and minor modes
- **Visual Representation**: Created bar charts showing song counts by key and mode

### 5. Explicit Content Analysis
- **Genre Distribution**: Identified which genres have the most explicit content
- **Audio Feature Comparison**: Compared audio characteristics between explicit and non-explicit tracks
- **Loudness Analysis**: Special focus on loudness differences with color-coded visualization

## Key Findings

### Audio Features
- Correlation patterns reveal relationships between different musical characteristics
- Some features show strong correlations while others are more independent

### Musical Keys and Modes
- Distribution shows preferences for certain keys in popular music
- Clear differences between major and minor mode usage across different keys

### Explicit vs Non-Explicit Content
- **Genre Patterns**: Certain genres show higher concentrations of explicit content
- **Audio Characteristics**: 
  - Explicit tracks tend to have different energy and danceability profiles
  - Loudness differences between explicit and non-explicit content
  - Valence (musical positivity) varies between content types

## Visualizations

The analysis includes several key visualizations:
1. **Correlation Heatmap**: Shows relationships between audio features
2. **Key Distribution Chart**: Bar chart of song counts by musical key and mode
3. **Genre Analysis**: Horizontal bar chart of explicit content by genre
4. **Feature Comparison**: Side-by-side comparison of audio features
5. **Loudness Visualization**: Color-coded loudness comparison with dB ranges

## Technical Implementation

- **Libraries Used**: pandas, matplotlib, numpy, seaborn
- **Data Processing**: Missing value handling, categorical mapping
- **Visualization**: Custom color schemes and formatting for better readability
- **Statistical Analysis**: Mean calculations and comparative statistics

## Future Analysis Ideas

- Temporal trends in audio features over time
- Artist-specific audio signature analysis
- Genre classification using audio features
- Popularity prediction based on audio characteristics
- Regional differences in musical preferences