from dotenv import load_dotenv
import os
import argparse

from utils.logging import get_basic_stdout_logger

if __name__ == '__main__':
    logger = get_basic_stdout_logger()

    parser = argparse.ArgumentParser(description='Convert source CSV based on template and save to target CSV.')
    parser.add_argument('--source', type=str, required=True, help='Path to the source CSV file.')
    parser.add_argument('--template', type=str, required=True, help='Path to the template CSV file.')
    parser.add_argument('--target', type=str, default='output.csv',
                        help='Path to the target CSV file where results will be saved.')

    args = parser.parse_args()

    if not os.getenv('OPENAI_API_KEY'):
        logger.info("OPENAI_API_KEY not found in environment variables. Loading from .env file")
        load_dotenv()

    pass

