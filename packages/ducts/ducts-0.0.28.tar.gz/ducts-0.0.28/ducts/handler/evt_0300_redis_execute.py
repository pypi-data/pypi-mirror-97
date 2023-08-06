from ducts.spi import EventHandler

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('Redisサーバへコマンドを送信し、結果を返します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        return await event.session.redis.execute(event.data[0], *event.data[1:])

