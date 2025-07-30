import argparse
import logging
import sys
import os
from pathlib import Path

from batch_metrics import run_batch_metrics
from experience_metrics import run_experience_metrics

# Update this to the path of your input log file
DEFAULT_LOG_PATH = "/tmp/resim/inputs/logs/output.mcap"
# These shouldn't change
DEFAULT_BATCH_METRICS_CONFIG_PATH = "/tmp/resim/inputs/batch_metrics_config.json"
DEFAULT_METRICS_PATH = "/tmp/resim/outputs/metrics.binproto"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
logger = logging.getLogger(os.path.basename(__file__))


def parse_args() -> argparse.Namespace:
    """Parses arguments."""

    parser = argparse.ArgumentParser()

    # Adding fields with default values
    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_METRICS_PATH,
        help=f"Path to the output file (default: {DEFAULT_METRICS_PATH})",
    )

    parser.add_argument(
        "--log-path",
        type=Path,
        default=DEFAULT_LOG_PATH,
        help=f"Path to the input log file (default: {DEFAULT_LOG_PATH})",
    )

    parser.add_argument(
        "--batch-metrics-config-path",
        type=Path,
        default=DEFAULT_BATCH_METRICS_CONFIG_PATH,
        help=(
            f"Path to the batch metrics configuration file (default: "
            f"{DEFAULT_BATCH_METRICS_CONFIG_PATH})"
        ),
    )

    # Parse and return arguments
    return parser.parse_args()


def main():
    """Script entrypoint."""
    args = parse_args()
    if args.log_path.exists():
        logger.info(f"Running experience metrics for {str(args.log_path)}...")
        run_experience_metrics(args)
    elif args.batch_metrics_config_path.exists():
        logger.info(
            f"Running batch metrics for {str(args.batch_metrics_config_path)}..."
        )
        run_batch_metrics(args)
    else:
        logger.error("Couldn't find input files for experience or batch metrics jobs.")
        exit(1)


if __name__ == "__main__":
    main()
