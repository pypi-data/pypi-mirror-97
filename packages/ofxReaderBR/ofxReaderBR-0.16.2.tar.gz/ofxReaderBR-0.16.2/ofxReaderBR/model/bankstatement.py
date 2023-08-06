class BankStatement:
    WAITING = 'waiting'
    COMPLETE = 'complete'
    INCOMPLETE = 'incomplete'
    ERROR = 'error'

    def __init__(self, file):
        self.file = file
        self.read_status = BankStatement.WAITING
        self.transactions = []

    def __repr__(self):
        formatted_transactions = '\n'.join([str(t) for t in self.transactions])
        return f'status: {self.read_status}\n' \
               f'transactions: [\n{formatted_transactions}\n]'

    def __add__(self, other):
        if self.file != other.file:
            raise ValueError('Can only add bank statements with same file.')

        self.transactions.extend(other.transactions)

        if self.read_status == BankStatement.WAITING or other.read_status in (
                BankStatement.INCOMPLETE, BankStatement.ERROR):
            self.read_status = other.read_status

        return self
