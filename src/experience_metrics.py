import uuid
import logging
import os
from resim.metrics.python.metrics_writer import ResimMetricsWriter
from utils import write_proto

logger = logging.getLogger(os.path.basename(__file__))


def run_experience_metrics(args):
    """Run the metrics for a single experience."""

    job_id = uuid.UUID(int=0)
    metrics_writer = ResimMetricsWriter(job_id=job_id)

    # add metrics here

    metrics_output = write_proto(metrics_writer, args.output_path)
