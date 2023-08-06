import uuid

EOL = b"\r\n"


def _convert_bytes_to_dict(data: bytes) -> dict:
    respons = dict()
    list_values = list()
    for _ in data.decode("utf-8").split(EOL.decode()):
        if _ != "":
            if _.split(": ", 1)[0] in respons.keys():
                list_values.append(_.split(": ", 1)[1])
                respons[_.split(": ", 1)[0]] = list_values
                continue
            respons[_.split(": ", 1)[0]] = _.split(": ", 1)[1]
    return respons


def _convert_dict_to_bytes(data: dict) -> bytes:
    string = ""
    for _, __ in data.items():
        string += _ + ": " + __ + EOL.decode()
    string += EOL.decode()
    return string.encode()


class IdGenerator:
    """Generate some uuid for actions:"""
    instances = []

    def __init__(self, prefix):
        self.instances.append(self)
        self.prefix = prefix
        self.uid = str(uuid.uuid4())
        self.generator = self.get_generator()

    def get_generator(self):
        i = 0
        max_val = 10000
        while True:
            yield "%s/%s/%d/%d" % (self.prefix, self.uid, (i // max_val) + 1, (i % max_val) + 1)
            i += 1

    def __call__(self):
        return next(self.generator)

    def __repr__(self):
        return "<%s prefix:%s (uid:%s)>" % (self.__class__.__name__, self.prefix, self.uid)
