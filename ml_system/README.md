# WhatsApp Scam Message Detection System

Complete ML-based system for detecting scam, spam, and phishing messages in multiple languages with URL analysis.

## Features

- Multilingual text classification (English, Tamil-English, Hindi, etc.)
- Advanced URL phishing detection
- Heuristic-based URL suspicion scoring
- Real-time message analysis
- REST API for integration
- Batch processing support

## Algorithms Used

### 1. Text Classification
- **TF-IDF Vectorization**: Converts text to numerical features
- **Random Forest Classifier**: Ensemble learning with 200 decision trees
- **N-gram Analysis**: Captures patterns (unigrams, bigrams, trigrams)

### 2. URL Detection & Analysis
- **Regex-based URL Extraction**: Identifies all URL formats
- **Heuristic Scoring System**: Analyzes 8+ suspicious characteristics
  - Phishing keywords (verify, login, bank, etc.)
  - Shortened URLs (bit.ly, tinyurl, etc.)
  - Special characters (@, multiple //)
  - Suspicious TLDs (.tk, .ml, .ga, etc.)
  - IP addresses in URLs
  - URL length and structure anomalies

### 3. Combined Decision Algorithm
- Weighted scoring: Text (60%) + URL (40%)
- Dynamic threshold adjustment
- Multi-factor risk assessment

## Installation

```bash
cd ml_system
pip install -r requirements.txt
```

## Quick Start

### 1. Train the Model

```bash
python train.py --create-sample
```

This creates a sample dataset and trains the model.

### 2. Test Predictions

```bash
python predict.py --test
```

Or analyze a specific message:

```bash
python predict.py --message "Congratulations! You won $5000. Click here to claim."
```

### 3. Start API Server

```bash
python api.py
```

API runs on `http://localhost:5000`

## API Endpoints

### 1. Health Check
```bash
GET /health
```

### 2. Detect Scam
```bash
POST /api/detect
Content-Type: application/json

{
  "message": "Your message here"
}
```

### 3. Analyze URL
```bash
POST /api/analyze-url
Content-Type: application/json

{
  "url": "http://suspicious-site.tk/login"
}
```

### 4. Batch Detection
```bash
POST /api/batch-detect
Content-Type: application/json

{
  "messages": ["message1", "message2", "message3"]
}
```

## Response Format

```json
{
  "success": true,
  "data": {
    "is_scam": true,
    "confidence": 0.85,
    "verdict": "SCAM",
    "text_scam_probability": 0.92,
    "urls_found": 1,
    "has_suspicious_urls": true,
    "max_url_suspicion_score": 75,
    "url_analyses": [{
      "url": "http://example.tk/verify",
      "suspicion_score": 75,
      "is_suspicious": true,
      "reasons": ["Contains keyword: verify", "Suspicious TLD"]
    }],
    "reasons": [
      "High scam probability in text (92%)",
      "Contains suspicious URLs"
    ]
  }
}
```

## Training with Custom Dataset

Create a CSV file with columns: `message`, `label`
- label: 0 = safe, 1 = scam

```bash
python train.py --data /path/to/dataset.csv --test-size 0.2
```

## URL Suspicion Scoring

| Score Range | Risk Level |
|-------------|-----------|
| 0-20        | Low       |
| 21-40       | Medium    |
| 41-60       | High      |
| 61-100      | Critical  |

## Supported Languages

- English
- Tamil-English (Tanglish)
- Hindi
- Mixed multilingual texts

## Model Performance

Expected metrics:
- Accuracy: >90%
- Precision: >88%
- Recall: >85%
- F1-Score: >87%

## Architecture

```
ml_system/
├── scam_detector.py    # Core ML model and URL analyzer
├── train.py            # Training script
├── predict.py          # CLI prediction tool
├── api.py              # Flask REST API
├── requirements.txt    # Python dependencies
├── models/             # Trained model artifacts (generated)
└── data/              # Training datasets (generated)
```

## Example Results

### Example 1: Safe Message
```
Message: "Hi, how are you? Let's meet tomorrow."
Verdict: SAFE
Confidence: 95%
```

### Example 2: Scam with URL
```
Message: "URGENT! Bank suspended. Verify: bit.ly/verify123"
Verdict: SCAM
Confidence: 89%
- High scam probability (87%)
- Suspicious shortened URL detected
- URL suspicion score: 65/100
```

### Example 3: Multilingual Scam
```
Message: "Panam jeyikum! 100% guarantee investment."
Verdict: SCAM
Confidence: 91%
- High scam probability (91%)
```

## Technical Details

### Text Preprocessing
1. Lowercase conversion
2. Special character removal
3. Whitespace normalization
4. TF-IDF vectorization (5000 features)

### URL Analysis Features
- Domain analysis
- TLD reputation checking
- Keyword detection
- Structural anomaly detection
- Length analysis
- Character distribution

### Classification Process
1. Extract and preprocess text
2. Extract URLs from message
3. Vectorize text using TF-IDF
4. Predict text-based scam probability
5. Analyze each URL independently
6. Combine scores (weighted)
7. Apply decision threshold
8. Return detailed results

## Notes

- Model retrains automatically when new data is provided
- URL detection uses multiple regex patterns
- Shortened URLs flagged automatically
- System supports real-time and batch processing
- All predictions include confidence scores and reasons
