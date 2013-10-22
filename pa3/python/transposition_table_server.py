import asyncore, socket
from struct import unpack


cache = {}


class TranspositionTableServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(1)

    def handle_accept(self):
        socket, address = self.accept()
        print 'Connection by', address
        TranspositionTableHandler(socket, address, self)


class TranspositionTableHandler(asyncore.dispatcher):
    def __init__(self, conn_sock, client_address, server):
        self.server = server
        self.client_address = client_address
        self.read_buffer = ""
        self.write_buffer = ""
        self.is_writable = False
        asyncore.dispatcher.__init__(self, sock=conn_sock)

    def readable(self):
        return True

    def writable(self):
        return self.is_writable

    def handle_read(self):
        data = self.recv(64)
        if data:
            self.write_buffer = unpack('!16i', data)
            self.is_writable = True

    def handle_write(self):
        if self.write_buffer:
            data = (self.write_buffer[14], self.write_buffer[15])
            key = str(self.write_buffer[:14])
            cacheData = cache.get(key)

            if data[1] > 0:
                if cacheData is None:
                    cache[key] = [data[0], str(data[1]), 0]
                elif data[0] >= cacheData[0]:
                    cacheData[0] = data[0]
                    cacheData[1] = str(data[1])
                    cacheData[2] += 1
            elif cacheData is not None and cacheData[0] >= data[0]:
                cacheData[2] += 1
                self.send(cacheData[1])
            else:
                self.send('000')

            self.write_buffer = ''
            self.is_writable = False

    def handle_close(self):
        print 'Connection closed:', self.client_address
        self.close()


s = TranspositionTableServer('', 5007)
asyncore.loop()