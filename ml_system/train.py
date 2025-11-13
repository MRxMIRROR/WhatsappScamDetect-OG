#!/usr/bin/env python3
import argparse
import logging
import pandas as pd
from pathlib import Path
from scam_detector import ScamDetector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_dataset(output_path: str = './data/sample_dataset.csv'):
    """Create sample training dataset with diverse examples."""
    samples = [
        ("Congratulations! You've won $5000 in our lottery. Click here to claim your prize.", 1),
        ("Hi, how are you today?", 0),
        ("URGENT: Your bank account has been suspended. Verify your details immediately.", 1),
        ("Let's meet tomorrow for coffee", 0),
        ("You are eligible for a free cash transfer. Update your bank account details here.", 1),
        ("Working from home? Earn $500 daily! NO EXPERIENCE NEEDED. Limited offer!", 1),
        ("What time is the meeting?", 0),
        ("Your Amazon account has expired. Click verify account to reactivate.", 1),
        ("Thanks for the birthday wishes!", 0),
        ("FREE iPhone 15! Claim yours now. Limited stock. Act fast!", 1),
        ("Can you send me the document?", 0),
        ("Investment opportunity: Guaranteed 50% returns. Invest now!", 1),
        ("Have you seen the new movie?", 0),
        ("ALERT: Unauthorized login detected. Confirm your password immediately.", 1),
        ("See you at the office tomorrow", 0),
        ("You've been selected for our exclusive program. Apply now!", 1),
        ("How's your family doing?", 0),
        ("Be your own boss! MLM opportunity. Earn unlimited commissions!", 1),
        ("Let me know your availability", 0),
        ("Processing fee pending. Pay $50 to receive $50000 transfer.", 1),

        ("Selected for winning lottery! Prize amount 5 lakhs! Contact immediately!", 1),
        ("Your account verified and confirmed ok", 0),
        ("Panam jeyikum! Vetkalam invest pannu. 100% guarantee.", 1),
        ("Enaku solla irukku, yarkai message pannuven", 0),
        ("Congratulations selected for job! Advance fee required.", 1),
        ("Ok will send the files soon", 0),
    ]

    df = pd.DataFrame(samples, columns=['message', 'label'])
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Sample dataset created at {output_path}")
    return output_path


def train_model(dataset_path: str, model_dir: str = './models',
               stop_words_path: str = None, test_size: float = 0.2):
    """Train scam detector model."""
    logger.info(f"Loading dataset from {dataset_path}")

    df = pd.read_csv(dataset_path)

    if 'message' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must contain 'message' and 'label' columns")

    texts = df['message'].astype(str).tolist()
    labels = df['label'].astype(int).tolist()

    logger.info(f"Dataset loaded: {len(texts)} samples")
    logger.info(f"Class distribution: {pd.Series(labels).value_counts().to_dict()}")

    detector = ScamDetector(
        model_dir=model_dir,
        stop_words_path=stop_words_path
    )

    logger.info("Starting training...")
    metrics = detector.train(
        texts=texts,
        labels=labels,
        test_size=test_size,
        save=True
    )

    logger.info("\n" + "="*50)
    logger.info("Training completed successfully!")
    logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
    logger.info(f"Model saved to {model_dir}")
    logger.info("="*50)

    return detector


def main():
    parser = argparse.ArgumentParser(description="Train scam detection model")
    parser.add_argument('--data', type=str, help='Path to training dataset CSV')
    parser.add_argument('--model-dir', type=str, default='./models',
                       help='Directory to save model artifacts')
    parser.add_argument('--stop-words', type=str, help='Path to stop words file')
    parser.add_argument('--test-size', type=float, default=0.2,
                       help='Test set size (0-1)')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create sample dataset and train')

    args = parser.parse_args()

    if args.create_sample:
        dataset_path = create_sample_dataset()
    elif args.data:
        dataset_path = args.data
    else:
        print("Error: Provide --data or use --create-sample")
        parser.print_help()
        return

    train_model(
        dataset_path=dataset_path,
        model_dir=args.model_dir,
        stop_words_path=args.stop_words,
        test_size=args.test_size
    )


if __name__ == '__main__':
    main()
