import abc
import logging
from zipfile import BadZipFile

import pandas as pd
from lxml import etree
from ofxtools import OFXTree
from openpyxl import load_workbook

from ofxReaderBR.model import BankStatement
from ofxReaderBR.reader.exceptions import OFXVersionError
from ofxReaderBR.reader.parser import PDFParserSantander, PDFParser

logger = logging.getLogger(__name__)


class BaseReaderController(abc.ABC):

    def __init__(self, factory):
        self.factory = factory

    def read(self, files):
        logger.debug(files)

        bank_stmts = []
        for file in files:
            options = {}

            try:
                data = self._get_data(file, options)
                bs_reader = self.factory.create_reader_bank_statement(file, data, options)
            except OFXVersionError:
                # ofx nao consegue ler versão 220. Ler como XML
                data = OFXReaderController.get_xml_data(file, options)
                factory = self.factory.create_xml_factory()
                bs_reader = factory.create_reader_bank_statement(file, data, options)
            except (IndexError, ValueError) as err:
                logger.error(f'Error getting data from file {file}: {err}')
                bs = self.__create_bank_statement_with_read_error(file)
                bank_stmts.append(bs)
                continue

            try:
                bs = bs_reader.read()
            except (RuntimeError, ValueError) as err:
                logger.error(f'Error reading file {file}: {err}')
                bs = self.__create_bank_statement_with_read_error(file)

            bank_stmts.append(bs)

        return bank_stmts

    @abc.abstractmethod
    def _get_data(self, file, options):
        pass

    @staticmethod
    def __create_bank_statement_with_read_error(file):
        bs = BankStatement(file)
        bs.read_status = BankStatement.ERROR
        return bs


class PDFReaderController(BaseReaderController):

    def _get_data(self, file, options):
        try:
            result = PDFParserSantander(file).run()
            options['has_header'] = False
        except ValueError as err:
            logger.debug(err)
            result = PDFParser(file).run()
        return result


class XLSReaderController(BaseReaderController):

    def _get_data(self, file, options):
        try:
            wb = load_workbook(file)
            data = wb.active
        except BadZipFile:
            logger.info('Could not read with openpyxl. Trying with pandas...')
            data = pd.read_excel(file, header=None)
            options['pandas'] = True
        return data


class OFXReaderController(BaseReaderController):

    @classmethod
    def get_xml_data(cls, file, options):
        file.seek(0)
        data = file.read().decode("latin-1")
        data = data[data.find('<OFX>'):]
        parser = etree.XMLParser(recover=True)
        tree = etree.fromstring(data, parser=parser)
        options['creditcard'] = cls.__is_credit_card(tree)
        return tree

    def _get_data(self, file, options):
        file.seek(0)
        tree = OFXTree()
        try:
            tree.parse(file)
        except IndexError:
            raise OFXVersionError()

        options['creditcard'] = self.__is_credit_card(tree)

        root = tree.getroot()

        if options['creditcard']:
            if self.__is_nubank_card(root):
                options['nubank'] = True
                self.__fix_acctid(root)
            else:
                options['bradesco'] = self.__is_bradesco_credit_card(root)
        options['bancodobrasil'] = self.__is_banco_do_brasil(root)

        self.__treat_bradesco_exception(root)

        return tree.convert()

    @staticmethod
    def __is_banco_do_brasil(root):
        fi = root.findall("SIGNONMSGSRSV1")[0].findall(
            "SONRS")[0].findall("FI")
        if fi:
            org = fi[0].findall("ORG")
            if org and "Banco do Brasil" in org[0].text:
                return True
        return False

    @staticmethod
    def __is_bradesco_credit_card(root):
        # FT-177 - Check if Bradesco credit card
        creditcardmsgsrsv1_ = root.findall('CREDITCARDMSGSRSV1')
        ccstmttrnrs_ = creditcardmsgsrsv1_[0].findall('CCSTMTTRNRS')
        ccstmtrs_ = ccstmttrnrs_[0].findall('CCSTMTRS')
        banktranlist_ = ccstmtrs_[0].findall('BANKTRANLIST')
        dtstart_ = banktranlist_[0].findall('DTSTART')
        dtend_ = banktranlist_[0].findall('DTEND')
        return dtstart_[0].text == dtend_[0].text

    @staticmethod
    def __is_credit_card(tree):
        return True if tree.findall("CREDITCARDMSGSRSV1") else False

    @staticmethod
    def __is_nubank_card(root):
        # FT-982
        tran_list = root.find('CREDITCARDMSGSRSV1').find('CCSTMTTRNRS').find('CCSTMTRS')
        account_id = tran_list.find('CCACCTFROM').find('ACCTID').text
        return account_id and len(account_id) == 36

    @staticmethod
    def __fix_acctid(root):
        tran_list = root.find('CREDITCARDMSGSRSV1').find('CCSTMTTRNRS').find('CCSTMTRS')
        account_id = tran_list.find('CCACCTFROM').find('ACCTID')
        # acctid max length is 22
        account_id.text = account_id.text[:22]

    # Este tratamento de erro tem que ser melhor descrito
    @staticmethod
    def __treat_bradesco_exception(root):
        unknown_date_in_the_past = '19851021000000[-3:GMT]'

        dt_server = root.findall("SIGNONMSGSRSV1")[0].findall(
            "SONRS")[0].findall("DTSERVER")[0]
        try:
            if int(dt_server.text) == 0:
                dt_server.text = unknown_date_in_the_past
        except ValueError:
            pass
            # se dtServer for um datetime, ele da erro na conversao para int
            # logger.info('Correcting DTServer')

        # se for cartao de credito, a data do balanco vem errada
        try:
            credit_card_trans_rs = root.findall("CREDITCARDMSGSRSV1")[0].findall(
                "CCSTMTTRNRS")

            for c in credit_card_trans_rs:
                dt_balance = c.findall("CCSTMTRS")[0].findall(
                    "LEDGERBAL")[0].findall("DTASOF")[0]

                try:
                    if int(dt_balance.text) == 0:
                        dt_balance.text = unknown_date_in_the_past
                except ValueError:
                    pass
        except IndexError:
            pass
