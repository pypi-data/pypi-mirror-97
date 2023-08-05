import logging
from typing import List, Dict
from xialib import Service
from xialib import BasicStorer
from xialib import BasicDecoder, ZipDecoder
from xialib import BasicFormatter, CSVFormatter
from xialib import BasicTranslator, SapTranslator
from xialib.storer import Storer
from xialib.decoder import Decoder
from xialib.formatter import Formatter
from xialib.publisher import Publisher
from xialib.translator import Translator

__all__ = ['Xeed']


class Xeed(Service):
    """Xeed Application

    """
    log_level = logging.WARNING
    api_url = 'api.x-i-a.com'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger("Xeed")
        self.log_context = {'context': ''}
        self.logger.setLevel(self.log_level)

        default_storer = {"basic": BasicStorer()}
        if 'storer' in kwargs:
            if isinstance(kwargs['storer'], dict):
                default_storer.update(kwargs['storer'])
            else:
                default_storer.update({"custom": kwargs['storer']})
        self.storer_dict = self.get_storer_register_dict(default_storer)

        default_decoder = {"basic": BasicDecoder(), "zip": ZipDecoder()}
        if 'decoder' in kwargs:
            if isinstance(kwargs['decoder'], dict):
                default_decoder.update(kwargs['decoder'])
            else:
                default_decoder.update({"custom": kwargs['decoder']})
        self.decoder_dict = self.get_decoder_register_dict(default_decoder)

        default_formatter = {"basic": BasicFormatter(), "csv": CSVFormatter()}
        if 'formatter' in kwargs:
            if isinstance(kwargs['formatter'], dict):
                default_formatter.update(kwargs['formatter'])
            else:
                default_formatter.update({"custom": kwargs['formatter']})
        self.formatter = self.get_formatter_register_dict(default_formatter)

        default_translator = {"basic": BasicTranslator(), "sap": SapTranslator()}
        if 'translator' in kwargs:
            if isinstance(kwargs['translator'], dict):
                default_translator.update(kwargs['translator'])
            else:
                default_translator.update({"custom": kwargs['translator']})
        self.translator = self.get_translator_register_dict(default_translator)

    @classmethod
    def get_storer_register_dict(cls, storer_list: Dict[str, Storer]) -> Dict[str, Storer]:
        register_dict = dict()
        for storer in [v for k,v in storer_list.items()]:
            for store_type in storer.store_types:
                register_dict[store_type] = storer
        return register_dict

    @classmethod
    def get_decoder_register_dict(cls, decoder_list: List[Decoder]) -> Dict[str, Decoder]:
        register_dict = dict()
        for decoder in [v for k,v in decoder_list.items()]:
            for encode in decoder.supported_encodes:
                register_dict[encode] = decoder
        return register_dict

    @classmethod
    def get_formatter_register_dict(cls, formatter_list: List[Decoder]) -> Dict[str, Formatter]:
        register_dict = dict()
        for formatter in [v for k,v in formatter_list.items()]:
            for format in formatter.support_formats:
                register_dict[format] = formatter
        return register_dict

    @classmethod
    def get_translator_register_dict(cls, translator_list: List[Decoder]) -> Dict[str, Translator]:
        register_dict = dict()
        for translator in [v for k,v in translator_list.items()]:
            for spec in translator.spec_list:
                register_dict[spec] = translator
        return register_dict