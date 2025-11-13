#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from scam_detector import ScamDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

detector = ScamDetector(model_dir='./models')

try:
    detector.load_model()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector.is_trained
    })


@app.route('/api/detect', methods=['POST'])
def detect_scam():
    """Detect scam in message."""
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'Message field is required'
            }), 400

        message = data['message']

        if not message or not message.strip():
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400

        result = detector.predict(message)

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze URL for suspicious characteristics."""
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL field is required'
            }), 400

        url = data['url']

        if not url or not url.strip():
            return jsonify({
                'error': 'URL cannot be empty'
            }), 400

        result = detector.analyze_url(url)

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/batch-detect', methods=['POST'])
def batch_detect():
    """Batch detection for multiple messages."""
    try:
        data = request.get_json()

        if not data or 'messages' not in data:
            return jsonify({
                'error': 'Messages array is required'
            }), 400

        messages = data['messages']

        if not isinstance(messages, list):
            return jsonify({
                'error': 'Messages must be an array'
            }), 400

        results = []
        for message in messages:
            if message and message.strip():
                result = detector.predict(message)
                results.append(result)

        return jsonify({
            'success': True,
            'data': results,
            'total': len(results)
        })

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
