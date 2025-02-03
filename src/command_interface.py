class Command:
    def execute(self, connection, bank, client_message):
        raise NotImplementedError