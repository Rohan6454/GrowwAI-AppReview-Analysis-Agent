import subprocess
import sys
import os
import time
import logging
from pathlib import Path

from dotenv import load_dotenv

# Load env vars from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def run_step_with_retry(name, command, max_retries=3, delay=60):
    logger.info(f"========== RUNNING STEP: {name} ==========")
    
    # Ensure current process environment is passed to subprocess
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    
    for attempt in range(1, max_retries + 1):
        try:
            # We use shell=True for Windows/Linux compatibility with environments
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, env=env)
            logger.info(f"[{name}] SUCCESS on attempt {attempt}")
            logger.info(f"Output:\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.warning(f"[{name}] FAILED on attempt {attempt}")
            error_output = e.stderr or e.stdout
            logger.error(f"Error Output:\n{error_output}")
            
            if attempt < max_retries:
                # If it's a rate limit error, wait longer
                wait = delay
                if "429" in error_output or "RESOURCE_EXHAUSTED" in error_output or "quota" in error_output.lower():
                    wait = 90  # Wait 90s for rate limit errors
                    logger.info(f"Rate limit detected. Waiting {wait} seconds before retry...")
                else:
                    logger.info(f"Retrying in {wait} seconds...")
                time.sleep(wait)
            else:
                logger.error(f"[{name}] Exhausted all {max_retries} retries. Aborting pipeline.")
                return False

def main():
    logger.info("=" * 80)
    logger.info("APP REVIEW INSIGHTS ANALYZER - END-TO-END PIPELINE (PHASE 1-7)")
    logger.info("=" * 80)

    steps = [
        ("Phase 1a: Scrape App Reviews", "python phase1/src/agent/scraper.py"),
        ("Phase 1b: Data Ingestion", "python test_phase1_ingestion.py"),
        ("Phase 2: Data Cleaning", "python phase2/src/agent/process_data.py"),
        ("Phase 3: Theme Analysis", "python phase3/src/agent/analyze_themes.py"),
        ("Phase 4: Quote Extraction", "python phase4/src/agent/run_extraction.py"),
        ("Phase 5: Recommendation Generation", "python phase5/src/agent/run_recommendations.py"),
        ("Phase 6: Note Generation (Docs)", "python phase6/src/run_note_generation.py"),
        ("Phase 7: Email Draft (Gmail)", "python phase7/src/run_email_draft.py")
    ]

    for name, command in steps:
        if not run_step_with_retry(name, command):
            logger.error("Pipeline halted due to failure in step: " + name)
            sys.exit(1)

    logger.info("=" * 80)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 80)

if __name__ == "__main__":
    main()
