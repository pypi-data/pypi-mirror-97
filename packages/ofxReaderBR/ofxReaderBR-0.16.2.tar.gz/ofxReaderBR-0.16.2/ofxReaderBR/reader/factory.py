from ofxReaderBR.reader.readerbankstatement import (PDFReaderBankStatement,
                                                    XLSReaderBankStatement,
                                                    XMLReaderBankStatement,
                                                    OFXReaderBankStatement)
from ofxReaderBR.reader.readercashflow import (PDFReaderCashFlow,
                                               XLSXReaderCashFlow,
                                               XMLReaderCashFlow,
                                               OFXReaderCashFlow)
from ofxReaderBR.reader.readercontroller import (PDFReaderController,
                                                 XLSReaderController,
                                                 OFXReaderController)


class ReaderFactory:
    types = ('ofx', 'pdf', 'xls', 'xlsx')

    def __init__(self, factory_type):
        if factory_type not in ReaderFactory.types:
            raise ValueError(f'Unknown type: {factory_type}')
        self._type = factory_type

    def create_reader_controller(self):
        if self._type == 'ofx':
            return OFXReaderController(self)
        elif self._type == 'pdf':
            return PDFReaderController(self)
        elif self._type in ('xls', 'xlsx'):
            return XLSReaderController(self)
        else:
            raise NotImplementedError(f'Not implemented type: {self._type}')

    def create_reader_bank_statement(self, file, data, options=None):
        if self._type == 'ofx':
            return OFXReaderBankStatement(self, file, data, options)
        elif self._type == 'pdf':
            return PDFReaderBankStatement(self, file, data, options)
        elif self._type in ('xls', 'xlsx'):
            return XLSReaderBankStatement(self, file, data, options)
        else:
            raise NotImplementedError(f'Not implemented type: {self._type}')

    def create_reader_cash_flow(self):
        if self._type == 'ofx':
            return OFXReaderCashFlow()
        elif self._type == 'pdf':
            return PDFReaderCashFlow()
        elif self._type in ('xls', 'xlsx'):
            return XLSXReaderCashFlow()
        else:
            raise NotImplementedError(f'Not implemented type: {self._type}')

    class XMLReaderFactory:
        """ Special case for OFX files """

        def create_reader_bank_statement(self, file, data, options=None):
            return XMLReaderBankStatement(self, file, data, options)

        @staticmethod
        def create_reader_cash_flow():
            return XMLReaderCashFlow()

    @classmethod
    def create_xml_factory(cls):
        return cls.XMLReaderFactory()
