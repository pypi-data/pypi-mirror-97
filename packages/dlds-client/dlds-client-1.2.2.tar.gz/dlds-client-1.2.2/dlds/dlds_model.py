#  Copyright 2021 Data Spree GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import importlib
import logging
import signal
from abc import ABC, abstractmethod
from queue import Queue, Full, Empty
from threading import Thread
from typing import Dict, Optional

import click
import requests as rq

from dlds import DLDSClient

logger = logging.getLogger(__name__)


class DLDSModel(ABC):
    def __init__(self, dlds_client: DLDSClient, dataset_dir: str, model: Dict,
                 iterations: int, worker_url: str) -> None:
        super().__init__()
        self.dlds_client: DLDSClient = dlds_client
        self.dataset_dir: str = dataset_dir
        self.dldsdata_model: Dict = model
        self.iterations: int = iterations
        self.worker_url: str = worker_url

        self.run_heartbeat_send_loop = True

        self.heartbeat_queue: Optional[Queue] = None
        self.heartbeat_sender: Optional[Thread] = None
        if self.worker_url != '':
            self.heartbeat_queue = Queue(maxsize=10)
            self.heartbeat_sender: Thread = Thread(target=self.heartbeat_send_loop)
            self.heartbeat_sender.start()

    @abstractmethod
    def run(self) -> None:
        """
        Stub for implementing the training and evaluation loop. Regularly, the send_heartbeat function must be
        called:
        >>> self.send_heartbeat(status)
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """
        Stub for implementing the shutdown. You can use this function for implementing a graceful shutdown of the
        training. For instance, create a last checkpoint.
        """
        pass

    def heartbeat_send_loop(self):
        while self.run_heartbeat_send_loop:
            try:
                status = self.heartbeat_queue.get(timeout=1.0)
                rq.post(f'{self.worker_url}/model_status', json=status)
            except Empty:
                pass

    def send_heartbeat(self, status) -> None:
        """
        Report the status of the model. This callback must be called regularly. Otherwise, the process will be
        terminated.
        :param status: Dictionary containing the current number of iterations, one of the following states:
                       ['init', 'running', 'finished', 'exception'], and optionally the current stage ['train', 'eval']
        Example:
        >>> { 'state': 'running', 'iteration': 350 }
        """
        try:
            status_element = {
                'state': status.get('status', 'running'),
                'iteration': status.get('iteration', 0),
                'epoch': status.get('epoch', 0),
                'end_iteration': status.get('end_iteration', 0),
                'start_iteration': status.get('start_iteration', 0),
                'eta': status.get('eta', 0)
            }

            stage = status.get('stage', None)
            if stage is not None:
                status_element['stage'] = stage

            error = status.get('error', None)
            if error is not None:
                status_element['error'] = error

            self.heartbeat_queue.put_nowait(status_element)
        except Full:
            pass

    @classmethod
    def start(cls, job_id: int, username: Optional[str] = None, password: Optional[str] = None,
              token: Optional[str] = None, server_url: str = '', dataset_dir: str = '',
              worker_url: str = 'http://localhost:6714') -> None:
        """
        Initialize the model and call the run method.
        :param job_id: ID of the DLDS training job that will be processed.
        :param username: Username for DLDS Server.
        :param password: Password for DLDS Server.
        :param token: Authentication token for DLDS Server (use either username/password or a token).
        :param server_url: URL to the DLDS Server.
        :param dataset_dir: Directory where dataset items are cached.
        :param worker_url: URL to the DLDS Training Worker.
        """

        # initialize dlds client
        client = DLDSClient(username, password, token, server_url=server_url, verify_ssl=False, verify_s3_ssl=False)

        # load job information (model_id, #iteration)
        job = client.get_job(job_id)
        if job is None:
            return

        # load model information
        model_id = job.get('model')
        dldsdata_model = client.get_model(model_id)
        dldsdata_model['parameters'] = client.get_model_parameters(model_id)

        # create model and start training
        model = cls(client, dataset_dir, dldsdata_model, job.get('iterations'), worker_url)

        def shutdown():
            model.shutdown()
            model.run_heartbeat_send_loop = False
            if model.heartbeat_sender is not None:
                # join the sender thread
                model.heartbeat_sender.join()

        def shutdown_handler(signum, frame):
            logger.info('Received signal to shutdown the model training.')
            shutdown()

        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, shutdown_handler)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, shutdown_handler)

        shutdown_done = False
        try:
            model.run()
        except KeyboardInterrupt:
            shutdown()
            shutdown_done = True

        if not shutdown_done:
            shutdown()

        logger.info('Model finished.')


@click.command()
@click.option('--job_id', type=int, required=True, help='ID of the training job.',
              envvar='DLDS_JOB_ID')
@click.option('--username', type=str, help='Username for DLDS Server.', default=None,
              envvar='DLDS_USERNAME')
@click.option('--password', type=str, help='Password for DLDS Server.', default=None,
              envvar='DLDS_PASSWORD')
@click.option('--token', type=str, help='Token for data spree vision platform.', default=None,
              envvar='DLDS_TOKEN')
@click.option('--server_url', default='https://api.vision.data-spree.com/api', help='URL to the API of the platform.',
              envvar='DLDS_SERVER_URL')
@click.option('--dataset_dir', type=click.Path(file_okay=False), default=None,
              help='Directory for caching datasets.',
              envvar='DLDS_DATASET_DIR')
@click.option('--worker_url', default='http://localhost:6714', help='URL to the training worker.',
              envvar='DLDS_WORKER_URL')
@click.option('--model_class', 'model_class_abs', type=str, default=None,
              help='Class name of the Model, e.g. "dldstraining.TrainerModel"',
              envvar='DLDS_MODEL_CLASS')
def main(job_id, username, password, token, server_url, dataset_dir, worker_url, model_class_abs) -> None:
    log_level = logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s %(name)s %(levelname)-6s %(message)s')

    parts = model_class_abs.split('.')
    module_name = '.'.join(parts[:-1])
    class_name = parts[-1]
    try:
        model_class = getattr(importlib.import_module(module_name), class_name)
    except Exception as e:
        click.echo(f'Could not import "{class_name}" from "{module_name}"')
        return

    model_class.start(job_id, username, password, token, server_url, dataset_dir, worker_url)


if __name__ == '__main__':
    main()
