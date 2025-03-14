class Cache:
    def __init__(self):
        self.items = {}

    def check(self, item):
        return item in self.items

    def write(self, item, time, html):
        self.items[item] = time
        f = open(self.get_str(item), 'wb')
        f.write(html)
        f.close()

    def read(self, item):
        f = open(self.get_str(item), 'rb')
        data = f.read()
        f.close()
        return data

    def lastModified(self, item):
        return self.items[item]

    def get_str(self, item):
        forbidden = './\\:;,?='
        for i in forbidden:
            item = item.replace(i, '')
        if len(item) > 30:
            item = item[:30]
        return item