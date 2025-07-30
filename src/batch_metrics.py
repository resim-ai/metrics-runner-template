import os
import logging
import argparse
import json
import uuid
from resim.metrics.python.metrics_writer import ResimMetricsWriter
from resim.metrics.fetch_job_metrics import fetch_job_metrics_by_batch
from resim.metrics.fetch_all_pages import fetch_all_pages
from resim_python_client.client import AuthenticatedClient
from resim_python_client.api.batches import list_jobs
from utils import write_proto

logger = logging.getLogger(os.path.basename(__file__))


def run_batch_metrics(args: argparse.Namespace) -> None:
    """Run metrics for a batch."""
    with open(
        args.batch_metrics_config_path, "r", encoding="utf-8"
    ) as metrics_config_file:
        metrics_config = json.load(metrics_config_file)

    token = metrics_config["authToken"]
    api_url = metrics_config["apiURL"]
    batch_id = metrics_config["batchID"]
    project_id = metrics_config["projectID"]
    job_to_metrics = fetch_job_metrics_by_batch(
        token=token,
        api_url=api_url,
        project_id=project_id,
        batch_id=uuid.UUID(batch_id),
    )

    client = AuthenticatedClient(
        base_url=metrics_config["apiURL"], token=metrics_config["authToken"]
    )

    batch_jobs_response = fetch_all_pages(
        list_jobs.sync,
        project_id=project_id,
        batch_id=batch_id,
        client=client,
        page_size=100,
    )
    job_id_to_experience_name = {
        job.job_id: job.experience_name
        for page in batch_jobs_response
        if page.jobs
        for job in page.jobs
    }

    writer = ResimMetricsWriter(uuid.uuid4())

    # add batch metrics here

    write_proto(writer, args.output_path)
