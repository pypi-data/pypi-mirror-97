import io
import json
import gzip
import logging
import hashlib
import uuid
import time
import http.client
from datetime import datetime
from typing import Union, Dict, List
from xialib.publisher import Publisher
from xialib.storer import Storer, RWStorer, IOStorer
from pyxeed.xeed import Xeed

__all__ = ['Seeder']


class Seeder(Xeed):
    """Relay and publish message to Insight Module or even Directly to Agent Module

    Move the data from depositor to archiver. Design to store huge amount of data on column usage

    Attributes:
        storers (:obj:`list` of :obj:`Storer`): Read the data which is not in a message body
        decoders (:obj:`list` of :obj:`Decoder`): Decode message of different type
        formatters (:obj:`list` of :obj:`Formatter`): Format message of different format
        translators (:obj:`list` of :obj:`Translator`): Translate message of different specification
        publisher (:obj:`dict` of :obj:`Publisher`): Publish the message of standard format
    """
    def __init__(self, publisher, **kwargs):
        super().__init__(publisher=publisher, **kwargs)
        self.logger = logging.getLogger("Xeed.Seeder")
        if len(self.logger.handlers) == 0:
            log_format = logging.Formatter('%(asctime)s-%(process)d-%(thread)d-%(module)s-%(funcName)s-%(levelname)s-'
                                          '%(context)s:%(message)s')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_format)
            self.logger.addHandler(console_handler)

        # Unique publisher support
        if isinstance(self.publisher, dict):
            self.publisher = [v for k, v in self.publisher.items()][0]

    def _get_active_units(self, header: dict, data_store: str):
        if not all(key in header for key in ['start_seq', 'data_encode', 'data_format', 'data_store']):
            self.logger.error("Header doesn't contain all needed fields", extra=self.log_context)
            raise ValueError("XED-000016")

        active_decoder = self.decoder_dict.get(header['data_encode'])
        if not active_decoder:
            self.logger.error("No decoder for encode {}".format(header['data_encode']), extra=self.log_context)
            raise ValueError("XED-000012")

        active_formatter = self.formatter.get(header['data_format'])
        if not active_formatter:
            self.logger.error("No formatter for format {}".format(header['data_format']), extra=self.log_context)
            raise ValueError("XED-000015")

        if 'data_spec' in header:
            active_translator = self.translator.get(header['data_spec'], None)
        else:
            active_translator = self.translator.get('x-i-a')
        if not active_translator:
            self.logger.error("No translator for data_spec {}".format(header['data_spec']), extra=self.log_context)
            raise ValueError("XED-000004")

        publish_storer = None
        if data_store is not None:
            publish_storer = self.storer_dict.get(data_store, None)
            if publish_storer is None or not isinstance(publish_storer, RWStorer):
                self.logger.error("No rw storer for store type {}".format(data_store), extra=self.log_context)
                raise ValueError("XED-000005")

        if header['data_store'] != 'body':
            reader_storer = self.storer_dict.get(header['data_store'], None)
            if reader_storer is None:
                self.logger.error("No storer for store type {}".format(header['data_store']), extra=self.log_context)
                raise ValueError("XED-000005")
            reader_io_support = True if isinstance(reader_storer, IOStorer) else False
        else:
            reader_storer, reader_io_support = None, None
        return active_decoder, \
               active_formatter, \
               active_translator, \
               publish_storer, \
               reader_storer, \
               reader_io_support

    def _get_age_start_seq(self, header):
        age, end_age, start_seq = 0, 0, ''
        if 'age' in header and int(header.get('age', 0)) > 1:
            age = int(header['age'])
            end_age = int(header.get('end_age', header['age']))
        else:
            start_seq = header['start_seq']
        return age, end_age, start_seq

    def _get_next_age_start_seq(self, header, age, end_age, start_seq):
        if age > end_age:
            self.logger.error("Age range overflow", extra=self.log_context)
            raise ValueError("XED-000020")
        if 'age' in header:
            header.pop('end_age', None)
            header['age'] = age
            age += 1
        else:
            header['start_seq'] = start_seq
            start_seq = str(int(start_seq) + 1)
        return header, age, end_age, start_seq

    def check_destination(self, destination: str, topic_id: str):
        """Check Push Destination
        """
        return self.publisher.check_destination(destination, topic_id)

    def push_data(self, header: dict, data_or_io: Union[str, bytes, io.BufferedIOBase],
                  destination: str, topic_id: str, table_id: str, size_limit: int = 2 * 20,
                  data_store: str = None, store_path: str = None):
        """Push data to a single destination
        """
        self.log_context['context'] = '-'.join([destination, topic_id, table_id])
        active_decoder, \
        active_formatter, \
        active_translator, \
        publish_storer, \
        reader_storer, \
        reader_io_support \
            = self._get_active_units(header, data_store)

        age, end_age, start_seq = self._get_age_start_seq(header)

        # Case 1: flow pass-through
        if header['data_store'] == 'body' \
                and header['data_encode'] in ['blob', 'flat', 'gzip', 'b64g'] \
                and header['data_format'] == 'record' and header.get('data_spec', '') == 'x-i-a':
            data_body = active_decoder.decoder(data_or_io, header['data_encode'], 'gzip')
            header['data_encode'] = 'gzip'
            self._publish_data(header, data_or_io, self.publisher,
                                   destination, topic_id, table_id,
                                   publish_storer, data_store, store_path)
        # Case 2: full-data send mode
        elif header['data_store'] == 'body' or \
                (header['data_store'] != 'body' and not reader_io_support) or \
                int(header.get('age', 0)) == 1 or \
                size_limit == 0:
            active_translator.compile(header, data_or_io)
            if header['data_store'] == 'body':
                raw_data = data_or_io
            else:
                raw_data = reader_storer.read(data_or_io)
            data_body = list()
            for decoded_blob in active_decoder.decoder(raw_data, header['data_encode'], 'blob'):
                data_body.extend([active_translator.get_translated_line(raw_line, age=age, start_seq=start_seq)
                                  for raw_line in active_formatter.formatter(decoded_blob, header['data_format'])])
                header['data_spec'] = 'x-i-a'
            header['data_format'] = 'record'
            header['data_encode'] = 'gzip'
            self._publish_data(header, gzip.compress(json.dumps(data_body, ensure_ascii=False).encode()),
                               self.publisher, destination, topic_id, table_id,
                               publish_storer, data_store, store_path)
        # Case 3: IO Send mode with chunk support
        else:
            chunk_size = size_limit // 8
            active_translator.compile(header, data_or_io)
            for data_io in reader_storer.get_io_stream(data_or_io):
                for decoded_blob in active_decoder.decoder(data_io, header['data_encode'], 'blob'):
                    chunk_number, raw_size, data_io, zipped_size, zipped_io = 0, 0, None, 0, None
                    for raw_line in active_formatter.formatter(decoded_blob, header['data_format']):
                        result_line = active_translator.get_translated_line(raw_line, age=age, start_seq=start_seq)
                        json_line = json.dumps(result_line)
                        if not data_io:
                            data_io = io.BytesIO()
                            zipped_io = gzip.GzipFile(mode='wb', fileobj=data_io)
                            zipped_io.write(('[' + json_line).encode())
                        else:
                            zipped_io.write((',' + json_line).encode())
                        raw_size += (len(json_line) + 1)
                        cur_chunk_number = raw_size // chunk_size
                        if cur_chunk_number != chunk_number:
                            chunk_number = cur_chunk_number
                            zipped_io.flush()
                            zipped_size = data_io.getbuffer().nbytes
                            if zipped_size + chunk_size > size_limit:
                                zipped_io.write(']'.encode())
                                zipped_io.close()
                                header['data_spec'] = 'x-i-a'
                                header['data_format'] = 'record'
                                header['data_encode'] = 'gzip'
                                header, age, end_age, start_seq = \
                                    self._get_next_age_start_seq(header, age, end_age, start_seq)
                                self._publish_data(header, data_io.getvalue(),
                                                   self.publisher, destination, topic_id, table_id,
                                                   publish_storer, data_store, store_path)
                                chunk_number, raw_size, data_io, zipped_size, zipped_io = 0, 0, None, 0, None
                    if raw_size > 0:
                        zipped_io.write(']'.encode())
                        zipped_io.close()
                        header['data_spec'] = 'x-i-a'
                        header['data_format'] = 'record'
                        header['data_encode'] = 'gzip'
                        header, age, end_age, start_seq = \
                            self._get_next_age_start_seq(header, age, end_age, start_seq)
                        self._publish_data(header, data_io.getvalue(),
                                           self.publisher, destination, topic_id, table_id,
                                           publish_storer, data_store, store_path)
                # Need to add an empty message add the end to fill the age gap
                if age < end_age:
                    header['data_spec'] = 'x-i-a'
                    header['data_format'] = 'record'
                    header['data_encode'] = 'gzip'
                    header, age, end_age, start_seq = \
                        self._get_next_age_start_seq(header, age, end_age, start_seq)
                    header['end_age'] = end_age
                    self._publish_data(header, gzip.compress(b'[]'),
                                       self.publisher, destination, topic_id, table_id,
                                       publish_storer, data_store, store_path)

    def _publish_data(self, header: dict, data: bytes,
                      publisher: Publisher, destination: str, topic_id: str, table_id: str,
                      storer: RWStorer = None, data_store: str = None, store_path: str = None):
        header['topic_id'] = topic_id
        header['table_id'] = table_id
        """
        if int(header.get('age', 0)) == 1:
            header['event_type'] = 'source_table_init'
            header['event_token'] = datetime.now().strftime('%Y%m%d%H%M%S') + '-' + str(uuid.uuid4())
        """

        if storer is None:
            header['data_store'] = 'body'
            publisher.publish(destination, topic_id, header, data)
        else:
            merge_key = str(int(header['start_seq']) + int(header.get('age', 0)))
            location = store_path + hashlib.md5(merge_key.encode()).hexdigest()[:4] + '-' + merge_key
            storer.write(data, location)
            header['data_store'] = data_store
            publisher.publish(destination, table_id, header, location)

        """
        # Heade post-check: Target tables must have been initialized
        if int(header.get('age', 0)) == 1:
            for i in range(6):
                time.sleep(2 ** i)
                conn = http.client.HTTPSConnection(self.api_url)
                conn.request("GET", "/events/source-table-init/" + header['event_token'])
                resp = conn.getresponse()
                if resp.status == 200:
                    break  # pragma: no cover
        """
