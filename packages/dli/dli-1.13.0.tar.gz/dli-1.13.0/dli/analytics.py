#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import threading
import queue

from urllib.parse import urljoin

import dli
from dli.client.components.urls import consumption_urls


class AnalyticsSender(threading.Thread):

    BUFFER_THREASHOLD = 10

    def __init__(self, client):
        super().__init__()
        self.daemon = True
        self._client = client
        self.queue = queue.Queue()
        self._buffer = []

    def run(self):
        while True:
            # Send buffer every 5 seconds
            try:
                event = self.queue.get(block=True, timeout=5)
                if event is None:
                    # end thread
                    break

                self._buffer.append(event)

                if len(self._buffer) > self.BUFFER_THREASHOLD:
                    self._send_buffer()
            except queue.Empty:
                # Means we've timed out.
                # send what's in the buffer
                self._send_buffer()
                continue

    def _send_buffer(self):
        try:
            if len(self._buffer):
                url = urljoin(
                    self._client._environment.consumption,
                    consumption_urls.consumption_analytics
                )
                session = self._client.session
                session.post(url, json={
                    'data': self._buffer
                })

                self._buffer = []

        except Exception as e:
            # Data scientists do not want to see stack dumps by default,
            # especially when we have a root cause that triggers secondary
            # exceptions.
            if self._client.strict:
                self._client.logger.exception(
                    'Error while sending analytics: ', e
                )

class AnalyticsHandler:
    __acceptable_properties = [
        'package_id', 'dataset_id', 'name', 'dataset_name', 'datafile_id',
        'dictionary_id', 'api_key'
    ]

    def __init__(self, dli_client):
        self._app_name = 'SDK'
        self._app_version = dli.__version__
        self._client = dli_client
        self._analytics_sender = AnalyticsSender(dli_client)
        self._analytics_sender.start()

    def create_event(
        self, user_id, organisation_id,
        entity=None, action=None, properties=None, result_status_code=None
    ):
        body = self._prepare_body_to_send(
            user_id, organisation_id, entity, action, properties,
            result_status_code,
        )
        self._send_event_to_analytics(body)

    def _prepare_body_to_send(
        self, user_id, organisation_id, entity, action, properties, result
    ):
        properties_to_send = self._filter_out_properties(properties)
        properties_to_send = self._override_properties_for_dataset_functions(
            action, entity, properties, properties_to_send)
        if 'api_key' in properties:
            properties['api_key'] = properties['api_key'][:6]
        event = {
            'application_name': self._app_name,
            'application_version': self._app_version,
            'user_id': user_id,
            'entity': entity,
            'action': action,
            'organisation_id': organisation_id,
            'result': result,
            'properties': properties_to_send
        }
        return {'attributes': event}

    def _filter_out_properties(self, properties):
        return {
            k: v
            for k, v in properties.items() if k in self.__acceptable_properties
        }

    # This is ugly, but 1) register_dataset accepts builder,
    # so we need to extract data from it 2) some functions accept 'id'
    # instead of dataset_id. We either ovveride it like this or not make it
    # generic at all.
    def _override_properties_for_dataset_functions(
            self, action, entity, properties, props
    ):
        if entity == 'Dataset':
            if action == 'register_dataset':
                props = self._filter_out_properties(properties['builder']._data)
            elif 'id' in properties:
                props['dataset_id'] = properties['id']
        return props

    def __del__(self):
        # tell the queue it's over
        self._analytics_sender.queue.put(None)

    def _send_event_to_analytics(self, body):
        self._analytics_sender.queue.put(body)
