from ducts.spi import EventHandler

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('サーバに文字列を送信し、ログとして記録します。')
        return handler_spec

    def handle(self, event):
        pass
    


