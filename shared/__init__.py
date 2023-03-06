
class AlgoTradingBot:
    def __init__(self, strategy, broker):
        self.strategy = strategy
        self.broker = broker

    def run(self):
        self.broker.connect()
        self.strategy.run()
        self.broker.disconnect()

class BaseBroker:
    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def place_order(self, order):
        raise NotImplementedError

    def cancel_order(self, order):
        raise NotImplementedError

class ZerodhaBroker(BaseBroker):
    def connect(self):
        # code to connect to Zerodha API
        pass

    def disconnect(self):
        # code to disconnect from Zerodha API
        pass

    def place_order(self, order):
        # code to place an order on Zerodha
        pass

    def cancel_order(self, order):
        # code to cancel an order on Zerodha
        pass

class FyersBroker(BaseBroker):
    def connect(self):
        # code to connect to Fyers API
        pass

    def disconnect(self):
        # code to disconnect from Fyers API
        pass

    def place_order(self, order):
        # code to place an order on Fyers
        pass

    def cancel_order(self, order):
        # code to cancel an order on Fyers
        pass

class KotakBroker(BaseBroker):
    def connect(self):
        # code to connect to Kotak API
        pass

    def disconnect(self):
        # code to disconnect from Kotak API
        pass

    def place_order(self, order):
        # code to place an order on Kotak
        pass

    def cancel_order(self, order):
        # code to cancel an order on Kotak
        pass

