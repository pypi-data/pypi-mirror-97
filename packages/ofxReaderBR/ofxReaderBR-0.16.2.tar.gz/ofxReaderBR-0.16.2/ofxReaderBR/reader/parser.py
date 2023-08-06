import abc
import logging
import re
from datetime import datetime

from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError

logger = logging.getLogger(__name__)


class BasePdfParser(abc.ABC):
    """ Parse pdf file data for controllers. """

    def __init__(self, file):
        self.file = file

    @abc.abstractmethod
    def run(self):
        pass

    def _read_file(self):
        file = self.file
        input1 = PdfFileReader(file)
        try:
            num_pages = input1.getNumPages()
        except PdfReadError as err:
            raise PdfReadError(f"O arquivo {file} está protegido com senha. \n {err}")

        pages = ''
        for i in range(0, num_pages):
            page = input1.getPage(i)
            page_text = page.extractText()
            pages += page_text

        return pages


class PDFParser(BasePdfParser):

    def run(self):
        pdf_string = self._read_file()

        print('run string')
        logger.info(pdf_string)

        regex = r'[0-9][0-9]\/[0-9][0-9].{1,23}[0-9]+,[0-9][0-9]'
        matches = re.findall(regex, pdf_string)

        emission_start = pdf_string.find('Emissão: ')
        emission_date = pdf_string[emission_start + 9:emission_start + 19]

        results = []

        for m in matches:
            r = self.__parse_match(m, emission_date)
            logger.info(r)
            results.append(r)
        return results

    @staticmethod
    def __parse_match(match, emission_date):
        regex = r'[-]?[\s]*[0-9\.]+,'
        start_value = re.search(regex, match).start()
        end_date = 5

        date = match[0:end_date].replace(' ', '')
        desc = match[end_date:start_value]
        if str(desc).endswith('/'):
            start_value += 2
        desc = match[end_date:start_value]
        value = match[start_value:].replace(' ', '')

        emission_month = emission_date[3:5]
        emission_year = emission_date[6:]

        date_month = date[3:]

        year = int(emission_year)
        if int(date_month) > int(emission_month):
            year -= 1

        date += '/' + str(year)

        return [date, desc, value]


class PDFParserSantander(BasePdfParser):

    def __init__(self, file):
        super().__init__(file)

        self.cards = []
        self.results = []

        self._text = None
        self._type = None

    def run(self):
        self.results.clear()

        self._text = self._read_file()
        if 'Santander' not in self._text:
            raise ValueError(f'Parser does not know how to handle this file: {self.file}')

        pdf_type = self._get_type()

        if pdf_type == 'internet':
            self._run_internet_banking()
        elif pdf_type in ['standard', 'unique']:
            self._run()
        else:
            raise ValueError(f'Unexpected value for type: {pdf_type}')

        return self.results

    @staticmethod
    def __change_sign(value_str):
        if '-' in value_str:
            return value_str.strip('-')
        else:
            return f'-{value_str}'

    @staticmethod
    def __replace_separator(value_str_brl):
        # Remove thousands separator and then replace decimal separator
        return value_str_brl.replace('.', '').replace(',', '.')

    def _get_type(self):
        if self._type is None:
            if self._text is None:
                raise ValueError(
                    'Run parser before calling this method or check if text is being improperly assigned'
                )
            if self._text.startswith('Internet Banking'):
                self._type = 'internet'
            elif self.__check_card_type(['ELITE PLATINUM', 'UNIQUE']):
                self._type = 'unique'
            else:
                self._type = 'standard'

        return self._type

    def _run_internet_banking(self):
        cash_flows_delimiter = 'Resumo das despesas'
        if cash_flows_delimiter in self._text:
            tables_and_footers, _ = self._text.split(cash_flows_delimiter)
            cash_date = self.__find_cash_date()
        else:
            tables_and_footers = self._text
            cash_date = None

        header_delimiter = 'Data\nDescrição\nValor (US$)\nValor (R$)'
        tables_and_footers_list = tables_and_footers.split(header_delimiter)

        footer_delimiter = ' Central de Atendimento Santander'
        table_list = [t.split(footer_delimiter)[0].strip() for t in tables_and_footers_list]
        tables = '\n'.join(table_list)

        cards_raw = tables.split('NªCartao')[1:]
        for raw in cards_raw:
            card = {}
            tokens = raw.strip().split('\n')
            card['last_digits'] = tokens[0].strip('Final:')
            card['owner'] = tokens[1].strip('Titular:')
            card['cash_flows'] = []
            for i in range(2, len(tokens), 4):
                cash_flow = {
                    'date': datetime.strptime(tokens[i], '%d/%m/%Y'),
                    'description': tokens[i + 1],
                    'value_usd': self.__change_sign(self.__replace_separator(tokens[i + 2].strip('US$ '))),
                    'value_brl': self.__change_sign(self.__replace_separator(tokens[i + 3].strip('R$ '))),
                }

                self.results.append([
                    cash_flow['date'],
                    cash_flow['description'],
                    cash_flow['value_brl'],
                    card['last_digits'],
                    cash_date,
                ])

                card['cash_flows'].append(cash_flow)

            self.cards.append(card)

    def _run(self):
        cash_date = self.__find_cash_date()
        origin = self.__find_card_number()

        pages = self._text.split('Nº DO CARTÃO ')

        if self._type == 'unique':
            expense_pages = pages[2:]
        elif self._type == 'standard':
            expense_pages = pages[3:]
        else:
            raise ValueError(f'Could not run type={self._type}')

        expense_pages[0] = expense_pages[0].split('IOF e CET')[0]

        expense_history = ''.join(expense_pages)
        tokens = expense_history.split()
        start = False
        card_tokens = []
        for token in tokens:
            if token in ['Histórico', 'TransaçõesNacionais', 'TransaçõesInternacionais']:
                start = True
            elif token in ['DataDescrição', '(+)Despesas/DébitosnoBrasil']:
                start = False
            elif start is True:
                card_tokens.append(token)

        for i in range(len(card_tokens)):
            token = card_tokens[i]
            if re.match(r"\d{2}/\d{2}", token[:5]):
                date_str = f"{token[:5]}/{cash_date.year}"
                date = datetime.strptime(date_str, '%d/%m/%Y')

                if date > cash_date:
                    date = date.replace(year=date.year - 1)

                description = token[5:]

                next_token = card_tokens[i + 1]
                if next_token.startswith('PARC'):
                    description = f"{description} {next_token}"
                    next_token = card_tokens[i + 2]

                value_without_separator = self.__replace_separator(next_token)
                value = self.__change_sign(value_without_separator)

                self.results.append([date, description, value, origin, cash_date])

    def __check_card_type(self, card_type_list):
        return any(f'SANTANDER {card_type}' in self._text for card_type in card_type_list)

    def __find_card_number(self):
        pos = self._text.find('Nº DO CARTÃO ')
        # format: Nº DO CARTÃO 1234 XXXX XXXX 4321
        return self._text[pos + 13:pos + 32]

    def __find_cash_date(self):
        if self._type == 'internet':
            delimiter = 'Data de vencimento:\n'
            pos = self._text.find(delimiter) + len(delimiter)
        elif self._type in ['unique', 'standard']:
            delimiter = '!Vencimento\n'
            pos = self._text.find(delimiter) + len(delimiter)
        else:
            raise ValueError('Could not find cash date.')

        # format dd/mm/YYYY (len=10)
        date_str = self._text[pos:pos + 10]
        return datetime.strptime(date_str, '%d/%m/%Y')
