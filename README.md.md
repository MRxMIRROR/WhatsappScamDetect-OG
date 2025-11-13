# WhatsApp Scam Detection System - Setup Instructions

Complete ML-based system for detecting scam messages with URL analysis.

## System Architecture

- **Frontend**: React + TypeScript + Tailwind CSS (Vite)
- **Backend**: Python Flask REST API
- **ML Model**: TF-IDF + Random Forest Classifier
- **URL Analysis**: Heuristic-based scoring system

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- pip (Python package manager)

## Setup Steps

### 1. Install Python Dependencies

```bash
cd ml_system
pip install -r requirements.txt
```

### 2. Train the ML Model

Create sample dataset and train the model:

```bash
python train.py --create-sample
```

This will:
- Create a sample dataset with multilingual examples
- Train the Random Forest model
- Save model artifacts to `./models/` directory
- Display training metrics (accuracy, precision, recall, F1-score)

Expected output:
```
Training completed successfully!
Accuracy: 0.95+
Model saved to ./models
```

### 3. Test the Model (Optional)

Test with example messages:

```bash
python predict.py --test
```

Or test a specific message:

```bash
python predict.py --message "Congratulations! You won $5000. Click here to claim."
```

### 4. Start the Python API Server

```bash
python api.py
```

The API will start on `http://localhost:5000`

Endpoints:
- `GET /health` - Check API status
- `POST /api/detect` - Analyze a message
- `POST /api/analyze-url` - Analyze a URL
- `POST /api/batch-detect` - Batch analysis

### 5. Install Frontend Dependencies

Open a new terminal and navigate to the project root:

```bash
npm install
```

### 6. Start the Frontend Development Server

```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Enter a message in the text area or click an example message
3. Click "Analyze Message"
4. View the detailed results including:
   - Scam/Safe verdict with confidence score
   - Text analysis probabilities
   - URL analysis with suspicion scores
   - Detailed reasons for the verdict

## API Usage Examples

### Detect Scam

```bash
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"message": "URGENT! Bank account suspended. Verify now: bit.ly/verify123"}'
```

### Analyze URL

```bash
curl -X POST http://localhost:5000/api/analyze-url \
  -H "Content-Type: application/json" \
  -d '{"url": "http://suspicious-site.tk/login"}'
```

### Batch Detection

```bash
curl -X POST http://localhost:5000/api/batch-detect \
  -H "Content-Type: application/json" \
  -d '{"messages": ["Hi there!", "You won $5000!", "Meeting at 3pm"]}'
```

## Training with Custom Dataset

Create a CSV file with two columns:
- `message`: The text message
- `label`: 0 for safe, 1 for scam

Example CSV:
```csv
message,label
"Hi how are you",0
"You won $5000! Click here",1
"Let's meet tomorrow",0
"Urgent! Verify your account",1
```

Train with your dataset:

```bash
python train.py --data /path/to/your/dataset.csv --test-size 0.2
```

## Supported Languages

The system supports multilingual detection:
- English
- Tamil-English (Tanglish)
- Hindi
- Mixed language messages

Example multilingual messages:
- "Panam jeyikum! Investment guarantee 100%"
- "Aap jeet gaye! Prize claim karo"

## URL Detection Features

The system analyzes URLs for:
- Phishing keywords (verify, login, bank, secure, etc.)
- Shortened URLs (bit.ly, tinyurl, goo.gl, etc.)
- Suspicious TLDs (.tk, .ml, .ga, .cf, .gq, .xyz)
- IP addresses in URLs
- Special characters (@, multiple //)
- Abnormal URL length
- Multiple hyphens in domain

## Suspicion Score Ranges

- **0-20**: Low risk
- **21-40**: Medium risk
- **41-60**: High risk
- **61-100**: Critical risk

## Troubleshooting

### API Connection Error

If frontend shows "Failed to connect to ML API":
1. Ensure Python API is running on port 5000
2. Check that `python api.py` is running without errors
3. Verify no firewall blocking port 5000

### Model Not Found Error

If you see "Model not found":
1. Run `python train.py --create-sample` first
2. Check that `./models/` directory exists
3. Verify `vectorizer.pkl` and `classifier.pkl` are in models directory

### Import Errors

If Python imports fail:
```bash
pip install --upgrade -r requirements.txt
```

## Model Performance

Expected metrics with sample dataset:
- Accuracy: >90%
- Precision: >88%
- Recall: >85%
- F1-Score: >87%

With larger, diverse datasets, performance improves significantly.

## Production Deployment

For production use:

1. Train with a large, diverse dataset (10,000+ samples)
2. Use environment variables for API configuration
3. Add authentication to API endpoints
4. Implement rate limiting
5. Use HTTPS for all connections
6. Consider using GPU for larger models
7. Implement logging and monitoring

## Advanced Usage

### Using XLM-RoBERTa (Optional)

For better multilingual support, you can integrate transformers:

```bash
pip install transformers torch
```

Modify `scam_detector.py` to use transformer models instead of Random Forest.

### Integrating with Supabase

Store detection results in Supabase for analytics:

1. Create a table for detection logs
2. Add Supabase client to API
3. Save each detection result
4. Build analytics dashboard

## System Requirements

- RAM: 2GB minimum (4GB recommended)
- Storage: 500MB for models and dependencies
- CPU: 2+ cores recommended
- Network: Required for initial package installation

## Support

For issues or questions:
1. Check the README.md in ml_system directory
2. Verify all dependencies are installed
3. Ensure correct Python version (3.8+)
4. Check API logs for error messages
