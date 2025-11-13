#!/usr/bin/env python3
import argparse
import logging
from scam_detector import ScamDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def predict_message(message: str, model_dir: str = './models'):
    """Predict if a message is scam."""
    detector = ScamDetector(model_dir=model_dir)

    try:
        detector.load_model()
    except FileNotFoundError:
        logger.error("Model not found. Please train the model first using train.py")
        return

    result = detector.predict(message)

    print("\n" + "="*70)
    print("SCAM DETECTION ANALYSIS")
    print("="*70)
    print(f"\nMessage: {result['text']}")
    print(f"\n{'🚨 VERDICT: SCAM' if result['is_scam'] else '✅ VERDICT: SAFE'}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"\nText Analysis:")
    print(f"  Scam Probability: {result['text_scam_probability']:.2%}")
    print(f"  Safe Probability: {result['text_safe_probability']:.2%}")

    if result['urls_found'] > 0:
        print(f"\nURL Analysis:")
        print(f"  URLs Found: {result['urls_found']}")
        print(f"  Suspicious URLs: {'YES' if result['has_suspicious_urls'] else 'NO'}")
        print(f"  Max Suspicion Score: {result['max_url_suspicion_score']}/100")

        for i, url_data in enumerate(result['url_analyses'], 1):
            print(f"\n  URL {i}: {url_data['url']}")
            print(f"    Suspicion Score: {url_data['suspicion_score']}/100")
            print(f"    Status: {'⚠️  SUSPICIOUS' if url_data['is_suspicious'] else '✓ OK'}")
            if url_data['reasons']:
                print(f"    Reasons:")
                for reason in url_data['reasons']:
                    print(f"      - {reason}")

    print(f"\nReasons:")
    for reason in result['reasons']:
        print(f"  • {reason}")

    print("="*70 + "\n")

    return result


def test_examples(model_dir: str = './models'):
    """Test with example messages."""
    test_messages = [
        "Hi, how are you? Let's catch up tomorrow.",
        "URGENT! Your bank account has been suspended. Click http://secure-bank-verify.tk/login to restore access immediately!",
        "Congratulations! You've won 10 lakhs. Pay 5000 processing fee to bit.ly/claim123",
        "Enaku solla irukku, call me when free",
        "FREE iPhone 15! Limited offer! Click www.free-iphone-claim.xyz/winner",
        "Meeting at 3 PM today in conference room",
        "Panam jeyikum! Investment guarantee 100%. Contact: http://192.168.1.1/invest"
    ]

    detector = ScamDetector(model_dir=model_dir)

    try:
        detector.load_model()
    except FileNotFoundError:
        logger.error("Model not found. Please train the model first using train.py")
        return

    for message in test_messages:
        predict_message(message, model_dir)
        print("\n")


def main():
    parser = argparse.ArgumentParser(description="Predict scam messages")
    parser.add_argument('--message', type=str, help='Message to analyze')
    parser.add_argument('--model-dir', type=str, default='./models',
                       help='Directory containing trained model')
    parser.add_argument('--test', action='store_true',
                       help='Run test examples')

    args = parser.parse_args()

    if args.test:
        test_examples(args.model_dir)
    elif args.message:
        predict_message(args.message, args.model_dir)
    else:
        print("Error: Provide --message or use --test")
        parser.print_help()


if __name__ == '__main__':
    main()
