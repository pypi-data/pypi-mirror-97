from ducts.spi import EventHandler

from datetime import datetime

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('送受信テスト用イベントです。サーバのUNIX時間を返します。')
        handler_spec.set_as_responsive()
        return handler_spec

    def handle(self, event):
        return datetime.now().strftime('%s')


