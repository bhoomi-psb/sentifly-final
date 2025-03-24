import re
from collections import Counter

class SentimentAnalyzer:
    """
    Advanced rule-based sentiment analyzer for airline reviews.
    """
    def __init__(self):
        self.positive_keywords = [
            "good", "great", "excellent", "amazing", "wonderful", "best", "love",
            "enjoy", "comfortable", "clean", "friendly", "helpful", "professional",
            "recommend", "awesome", "delicious", "pleasant", "smooth", "impressed",
            "fantastic", "perfect", "satisfied", "happy", "efficient", "courteous"
        ]
        
        self.negative_keywords = [
            "bad", "worst", "terrible", "awful", "horrible", "poor", "hate",
            "disappointing", "uncomfortable", "dirty", "rude", "unhelpful", "unprofessional",
            "avoid", "disgusting", "unpleasant", "rough", "unimpressed",
            "lousy", "imperfect", "unsatisfied", "unhappy", "inefficient", "discourteous"
        ]
        
        self.neutral_keywords = [
            "okay", "average", "moderate", "fair", "decent", "standard", "usual",
            "normal", "typical", "common", "regular", "ordinary", "tolerable", "acceptable",
            "satisfactory", "mediocre", "middle", "intermediate", "adequate", "sufficient"
        ]
        
        self.emergency_keywords = [
            "emergency", "danger", "unsafe", "alarming", "crash", "accident", "medical",
            "sick", "ill", "injury", "injured", "turbulence", "cancelled", "stranded",
            "urgent", "emergency landing", "oxygen masks", "panic", "critical", "disaster",
            "fire", "loss of control", "engine failure", "mayday", "severe turbulence",
            "medical assistance", "breathing issue", "unconscious", "technical failure"
        ]
        
        self.labels = ["Negative", "Neutral", "Positive", "Emergency"]
        self.colors = {
            "Negative": "danger",
            "Neutral": "secondary",
            "Positive": "success",
            "Emergency": "warning"
        }

    def preprocess(self, text):
        """Preprocess text: remove special characters, convert to lowercase."""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
        return text

    def count_keywords(self, text, keyword_list):
        """Count occurrences of keywords and key phrases in text."""
        text = self.preprocess(text)
        words = text.split()

        # Count single-word matches
        single_word_count = sum(1 for word in words if word in keyword_list)

        # Count phrase matches
        phrase_count = sum(1 for phrase in keyword_list if len(phrase.split()) > 1 and phrase in text)

        return single_word_count + phrase_count

    def analyze(self, text):
        """Analyze sentiment of the given text."""
        pos_count = self.count_keywords(text, self.positive_keywords)
        neg_count = self.count_keywords(text, self.negative_keywords)
        neu_count = self.count_keywords(text, self.neutral_keywords)
        emg_count = self.count_keywords(text, self.emergency_keywords)
        
        # Adjust weighting to better detect emergency situations
        pos_score = pos_count * 1.2
        neg_score = neg_count * 1.0
        neu_score = neu_count * 0.8
        emg_score = emg_count * 2.0  # Increased weight for emergency terms

        scores = [neg_score, neu_score, pos_score, emg_score]
        max_score_idx = scores.index(max(scores))
        sentiment = self.labels[max_score_idx]

        return {
            "sentiment": sentiment,
            "sentiment_color": self.colors[sentiment]
        }
    
    def detect_fake_review(self, text):
        """
        Detects potential fake reviews based on repetitive patterns, excessive keywords, and generic language.
        """
        text = self.preprocess(text)
        words = text.split()
        word_counts = Counter(words)

        # Simple rule: if too many repeated words, it might be fake
        most_common = word_counts.most_common(3)
        if most_common and most_common[0][1] > 5:
            return "Fake"

        fake_indicators = ["scam", "fake", "fraud", "not real", "bot", "scripted", "paid review"]
        if any(word in text for word in fake_indicators):
            return "Fake"

        return "Genuine"
