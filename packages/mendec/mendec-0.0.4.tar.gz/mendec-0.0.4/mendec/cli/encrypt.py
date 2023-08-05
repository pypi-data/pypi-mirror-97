from ocli import arg, Main, Base
from ocli.extra import BasicLog, LogOpt

from .pick import Crypt


# @arg("message", default=None, help="the message file")
# @arg("key", required=True, help="the key file")
# class Encrypt(Crypt, BasicLog, Main):
class Encrypt(Crypt, LogOpt, Base):
    def options(self, opt):
        super().options(
            opt
            # 1st argument
            .arg("key", required=True, help="the key file")
            # 2nd argument
            .arg("message", default=None, help="the message file")
        )

    def start(self, *args, **kwargs):
        from .pick import parse_keyfile, as_source, as_sink

        # parse the key file
        desc = parse_keyfile(self.key)
        # get n, e, d
        e = desc["e"] if "e" in desc else desc["d"]
        if self.short:
            from ..message import encrypt

            with as_source(self.message) as r, as_sink(self.output) as w:
                w.write(encrypt(r.read(), desc["n"], e))
        else:
            from ..message import vencrypt

            with as_source(self.message) as r, as_sink(self.output) as w:
                vencrypt(desc["n"], e, r, w)


(__name__ == "__main__") and Encrypt().main()
