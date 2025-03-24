import re
import csv
import json
import logging
from collections import Counter

logger = logging.getLogger(__name__)

# Text preprocessing functions
def clean_text(text):
    """
    Clean and preprocess text for analysis
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_text(text):
    """
    Simplified text preprocessing pipeline
    
    Args:
        text (str): Raw input text
        
    Returns:
        str: Preprocessed text
    """
    return clean_text(text)

# Helper function to count keyword occurrences in text
def count_keywords(text, keyword_list):
    """
    Count occurrences of keywords in text
    
    Args:
        text (str): Text to analyze
        keyword_list (list): List of keywords to count
        
    Returns:
        int: Count of keyword occurrences
    """
    text = preprocess_text(text)
    words = text.split()
    count = sum(1 for word in words if word in keyword_list)
    return count

# Helper functions for fake review detection
def extract_text_features(text):
    """
    Extract features from text for fake review detection
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Dictionary of extracted features
    """
    if not isinstance(text, str):
        text = ""
        
    # Preprocess text
    processed_text = preprocess_text(text)
    words = processed_text.split()
    
    # Extract basic features
    features = {
        'review_length': len(text),
        'word_count': len(words),
        'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
        'exclamation_count': text.count('!'),
        'question_count': text.count('?'),
        'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
    }
    
    # Extract word frequency features
    word_counts = Counter(words)
    repeated_words = sum(1 for count in word_counts.values() if count > 3)
    features['repeated_words'] = repeated_words
    
    # Extract superlative features
    superlative_count = sum(1 for word in words if word.endswith('est'))
    features['superlative_count'] = superlative_count
    
    return features

def load_csv_data(file_path):
    """
    Load data from CSV file
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        list: List of dictionaries with CSV data
    """
    try:
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        logger.error(f"Error loading CSV data: {str(e)}")
        return []

def calculate_stats(data):
    """
    Calculate statistics from review data
    
    Args:
        data (list): List of review dictionaries
        
    Returns:
        dict: Dictionary with calculated statistics
    """
    # Sentiment distribution
    sentiment_counts = Counter(item.get('Sentiment', 'Unknown') for item in data)
    
    # Fake vs real distribution
    fake_counts = Counter(int(item.get('Fake Review', 0)) for item in data)
    fake_percentage = (fake_counts.get(1, 0) / len(data)) * 100 if len(data) > 0 else 0
    real_percentage = (fake_counts.get(0, 0) / len(data)) * 100 if len(data) > 0 else 0
    
    # Rating distribution
    rating_counts = Counter(item.get('Rating', 'Unknown') for item in data)
    
    # Airline distribution
    airline_counts = Counter(item.get('Airline Name', 'Unknown') for item in data)
    top_airlines = {k: v for k, v in airline_counts.most_common(5)}
    
    return {
        'sentiment_counts': dict(sentiment_counts),
        'fake_counts': {
            'fake': fake_counts.get(1, 0),
            'real': fake_counts.get(0, 0),
            'fake_percentage': fake_percentage,
            'real_percentage': real_percentage
        },
        'rating_counts': dict(rating_counts),
        'airline_counts': top_airlines
    }

def save_results_to_json(results, file_path):
    """
    Save analysis results to JSON file
    
    Args:
        results (dict): Analysis results to save
        file_path (str): Path to save JSON file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving results to JSON: {str(e)}")
        return False
