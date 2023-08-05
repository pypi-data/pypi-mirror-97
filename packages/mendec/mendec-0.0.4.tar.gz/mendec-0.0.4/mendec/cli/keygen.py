from ocli import Base, Main, flag, param
from ocli.extra import BasicLog, LogOpt


def x8(v):
    return int(v) * 8


# @param("bits", "b", default=2048, type=int, help="How many bits")
# @param("bytes", "B", type=x8, dest="bits", help="How many bits in bytes")
# @param("pool", "p", default=1, type=int, help="How many process to generate primes")
# @param("output", "o", help="output to file", default=None)
# @flag("test", "t", default=True, help="Test the generated key")
# @flag("near", "n", default=True, dest="accurate", help="Not exact bits is ok")
# class KeyGen(BasicLog, Main):
class KeyGen(LogOpt, Base):
    app_name = "keygen"
    log_format = "%(asctime)s %(levelname)s: %(message)s"

    def options(self, opt):
        super().options(
            opt
            # --bits 256, -b 256
            .param("bits", "b", default=2048, type=int, help="How many bits")
            # --bytes 96, -B 96
            .param("bytes", "B", type=x8, dest="bits", help="How many bits in bytes")
            # --pool 4, -p 4
            .param(
                "pool",
                "p",
                default=1,
                type=int,
                help="How many process to generate primes",
            )
            # --output FILE, -p FILE
            .param("output", "o", help="output to file", default=None)
            # --test, -t
            .flag("test", "t", default=True, help="Test the generated key")
            # --near, -n
            .flag(
                "near", "n", default=True, dest="accurate", help="Not exact bits is ok"
            )
        )

    def start(self, *args, **kwargs):
        from datetime import datetime
        from logging import info
        from sys import platform
        from time import time

        from ..key import newkeys
        from ..message import decrypt, encrypt
        from .pick import as_sink

        t = time()
        n, e, d = newkeys(self.bits, accurate=self.accurate, poolsize=self.pool)
        info("Duration %ss", time() - t)

        import pprint

        k = dict(n=n, e=e, d=d)
        max_bits = max(v.bit_length() for n, v in k.items())
        k[""] = "{} bits, {} bytes, {}".format(
            max_bits, max_bits // 8, (datetime.utcnow()).strftime("%Y%b%d_%H%M%S")
        )

        with as_sink(self.output, "w") as out:
            out.write("#")
            for x, v in k.items():
                if x:
                    out.write(
                        " {}:{}@{}".format(x, v.bit_length() // 8, v.bit_length())
                    )
            out.write("\n")

            pprint.pprint(k, stream=out)

        if self.test:
            data = dict(message=platform.encode())
            data["encrypted"] = encrypt(data["message"], n, e)
            data["decrypted"] = decrypt(data["encrypted"], n, d)

            if data["decrypted"] == data["message"]:
                info("test: passed")
            else:
                raise RuntimeError(
                    "Test failed message={message!r}, encrypted={encrypted!r}, decrypted={decrypted!r}".format(
                        **data
                    )
                )


(__name__ == "__main__") and KeyGen().main()
