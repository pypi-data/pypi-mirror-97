import os
import time
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Dict, List, Union

import boto3


class MetricsClient:
    def __init__(self, namespace: str, environment: str = None, dimensions: List[Dict] = None):
        self.cloudwatch = boto3.client("cloudwatch")
        self.namespace = namespace
        self.environment = environment or os.environ.get('PROPERLY_STAGE', 'local')

        self.timers = {}

        additional_dimensions = dimensions or []
        environment_dimensions = [
            {
                "Name": "Environment",
                "Value": self.environment,
            },
        ]

        self.dimensions = environment_dimensions + additional_dimensions

    def record_metric(self, metric_name: str, value: Union[float, int], metric_unit: str = "None", dimensions: List[Dict] = None):
        """
        Records a metric count in CloudWatch

        :param metric_name: The name of the metric
        :param value: The value of the metric. The default unit for this value is to count something.
        :param metric_unit: (Optional) The unit of the metric. Defaults to "None" for count types.
        :param dimensions: (Optional) Any additional dimensions to add to the metric.
        """
        additional_dimensions = dimensions or []
        merged_dimensions = self.dimensions + additional_dimensions

        self.cloudwatch.put_metric_data(
            MetricData=[{
                "MetricName": metric_name,
                "Dimensions": merged_dimensions,
                "Unit": metric_unit,
                "Value": value,
            }],
            Namespace=self.namespace,
        )

    @contextmanager
    def timer(self, metric_name: str):
        """
        A context manager timer that records the time to execute the yielded code.
        The duration of the executed context code will be sent to CloudWatch on exit.

        :param metric_name: The name of the metric
        """
        start_time = time.time()

        # The hand-off to timed code
        yield

        stop_time = time.time()
        duration = stop_time - start_time

        # CloudWatch expects "Duration" (a CloudWatch enum value) to be in seconds.
        self.record_metric(
            metric_name=metric_name,
            value=int(duration),
            metric_unit="Duration",
        )

    def function_timer(self, func: Callable) -> Callable:
        """
        A function wrapper timer that records the time to execute the wrapped function.

        The duration of the executed context code will be sent to CloudWatch on function execution exit.
        The name of the metric will be the function name with "-timing" appended.

        :param func: The function to be timed.
        :return: The wrapped function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            metric_name = f"{func.__name__}-timing"
            with self.timer(metric_name=metric_name):
                # Call the wrapped timed function.
                return func(*args, **kwargs)

        return wrapper
