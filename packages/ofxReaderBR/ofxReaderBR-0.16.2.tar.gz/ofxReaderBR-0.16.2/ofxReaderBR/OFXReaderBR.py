import logging
from pathlib import Path

from .reader.factory import ReaderFactory

logger = logging.getLogger(__name__)


class OFXReaderBR:

    @staticmethod
    def run(file_list):
        if not file_list:
            logger.info('No files specified.')
            return

        files = {}
        for file in file_list:
            if hasattr(file, 'filename'):
                path = Path(file.filename)
            elif hasattr(file, 'name'):
                path = Path(file.name)
            else:
                raise ValueError(f'Unable to handle file: {file}')
            suffix = path.suffix
            files[suffix] = files.get(suffix, [])
            files[suffix].append(file)

        logger.info(files)

        bank_statements = []
        for factory_type in ReaderFactory.types:
            factory = ReaderFactory(factory_type)
            reader_controller = factory.create_reader_controller()
            _files = files.get(f'.{factory_type}')
            if _files:
                bank_stmts = reader_controller.read(_files)
                bank_statements.extend(bank_stmts)

        logger.info(bank_statements)

        return bank_statements
