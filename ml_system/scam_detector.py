#!/usr/bin/env python3
import re
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScamDetector:
    """ML-based scam message detector with URL analysis."""

    def __init__(self, model_dir: str = './models', stop_words_path: Optional[str] = None):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95,
            stop_words='english'
        )

        self.classifier = RandomForestClassifier(
            n_estimators=200,
            max_depth=50,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        self.is_trained = False

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        url_pattern_simple = r'(?:www\.|[a-zA-Z0-9-]+\.(?:com|org|net|in|co|io|ai|app|xyz|info|biz|tk|ml|ga|cf|gq))[^\s]*'

        urls = re.findall(url_pattern, text)
        urls += re.findall(url_pattern_simple, text)

        shortened_pattern = r'(?:bit\.ly|tinyurl\.com|goo\.gl|ow\.ly|t\.co|cutt\.ly)/[a-zA-Z0-9]+'
        urls += re.findall(shortened_pattern, text)

        return list(set(urls))

    def analyze_url(self, url: str) -> Dict[str, any]:
        """Analyze URL for suspicious characteristics."""
        suspicion_score = 0
        reasons = []

        url_lower = url.lower()

        phishing_keywords = [
            'verify', 'login', 'account', 'secure', 'update', 'confirm',
            'bank', 'paypal', 'amazon', 'suspended', 'urgent', 'click',
            'prize', 'winner', 'free', 'claim', 'limited', 'offer'
        ]

        for keyword in phishing_keywords:
            if keyword in url_lower:
                suspicion_score += 15
                reasons.append(f"Contains keyword: {keyword}")

        if any(shortener in url_lower for shortener in ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'cutt.ly']):
            suspicion_score += 20
            reasons.append("Shortened URL")

        if '@' in url:
            suspicion_score += 25
            reasons.append("Contains @ symbol")

        if url.count('//') > 1:
            suspicion_score += 20
            reasons.append("Multiple slashes")

        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
        if any(tld in url_lower for tld in suspicious_tlds):
            suspicion_score += 15
            reasons.append("Suspicious TLD")

        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            suspicion_score += 20
            reasons.append("IP address in URL")

        if len(url) > 100:
            suspicion_score += 10
            reasons.append("Unusually long URL")

        if url_lower.count('-') > 3:
            suspicion_score += 10
            reasons.append("Multiple hyphens")

        suspicion_score = min(suspicion_score, 100)

        return {
            'url': url,
            'suspicion_score': suspicion_score,
            'is_suspicious': suspicion_score >= 40,
            'reasons': reasons
        }

    def train(self, texts: List[str], labels: List[int],
              test_size: float = 0.2, save: bool = True) -> Dict[str, float]:
        """Train the model."""
        processed_texts = [self.preprocess_text(text) for text in texts]

        X_train, X_test, y_train, y_test = train_test_split(
            processed_texts, labels,
            test_size=test_size,
            random_state=42,
            stratify=labels
        )

        logger.info(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)

        self.classifier.fit(X_train_vec, y_train)

        y_pred = self.classifier.predict(X_test_vec)

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0)
        }

        logger.info(f"Model Performance:")
        logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall:    {metrics['recall']:.4f}")
        logger.info(f"  F1-Score:  {metrics['f1_score']:.4f}")

        self.is_trained = True

        if save:
            self.save_model()

        return metrics

    def predict(self, text: str) -> Dict[str, any]:
        """Predict if message is scam."""
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load a trained model.")

        processed_text = self.preprocess_text(text)
        X = self.vectorizer.transform([processed_text])

        prediction = self.classifier.predict(X)[0]
        probability = self.classifier.predict_proba(X)[0]

        urls = self.extract_urls(text)
        url_analyses = [self.analyze_url(url) for url in urls]

        max_url_score = max([ua['suspicion_score'] for ua in url_analyses], default=0)
        has_suspicious_urls = any([ua['is_suspicious'] for ua in url_analyses])

        text_scam_prob = probability[1]
        url_risk_factor = max_url_score / 100.0

        combined_score = (text_scam_prob * 0.6) + (url_risk_factor * 0.4)

        final_prediction = 1 if combined_score >= 0.5 else 0

        if has_suspicious_urls and final_prediction == 0:
            final_prediction = 1
            combined_score = max(combined_score, 0.6)

        reasons = []
        if text_scam_prob > 0.6:
            reasons.append(f"High scam probability in text ({text_scam_prob:.2%})")
        if has_suspicious_urls:
            reasons.append("Contains suspicious URLs")
        if final_prediction == 0:
            reasons.append("Message appears safe")

        return {
            'text': text,
            'is_scam': bool(final_prediction),
            'confidence': float(combined_score),
            'text_scam_probability': float(text_scam_prob),
            'text_safe_probability': float(probability[0]),
            'urls_found': len(urls),
            'url_analyses': url_analyses,
            'has_suspicious_urls': has_suspicious_urls,
            'max_url_suspicion_score': max_url_score,
            'reasons': reasons,
            'verdict': 'SCAM' if final_prediction == 1 else 'SAFE'
        }

    def save_model(self):
        """Save trained model."""
        vectorizer_path = self.model_dir / 'vectorizer.pkl'
        classifier_path = self.model_dir / 'classifier.pkl'

        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)

        with open(classifier_path, 'wb') as f:
            pickle.dump(self.classifier, f)

        logger.info(f"Model saved to {self.model_dir}")

    def load_model(self):
        """Load trained model."""
        vectorizer_path = self.model_dir / 'vectorizer.pkl'
        classifier_path = self.model_dir / 'classifier.pkl'

        if not vectorizer_path.exists() or not classifier_path.exists():
            raise FileNotFoundError(f"Model files not found in {self.model_dir}")

        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)

        with open(classifier_path, 'rb') as f:
            self.classifier = pickle.load(f)

        self.is_trained = True
        logger.info(f"Model loaded from {self.model_dir}")
