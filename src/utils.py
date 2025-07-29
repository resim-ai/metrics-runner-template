from resim.metrics.python.metrics_utils import ResimMetricsOutput
from resim.metrics.proto.validate_metrics_proto import validate_job_metrics
from resim.metrics.python.metrics import SeriesMetricsData
from typing import cast
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))


def write_proto(writer, path: str) -> ResimMetricsOutput:
    """Write out the binproto for our metrics."""
    metrics_proto = writer.write()
    validate_job_metrics(metrics_proto.metrics_msg)
    # Known location where the runner looks for metrics
    with open(path, "wb") as f:
        f.write(metrics_proto.metrics_msg.SerializeToString())

    return metrics_proto


def extract_metric_series(job_to_metrics: dict, metric_name: str) -> dict:
    """Extract a metric series from job_to_metrics for all jobs."""
    return {
        str(pair[0]): cast(SeriesMetricsData, data).series
        for pair in job_to_metrics.items()
        if (
            data := next(
                (data for data in pair[1].metrics_data if data.name == metric_name),
                None,
            )
        )
        is not None
    }
