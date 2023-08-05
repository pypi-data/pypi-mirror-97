from ast import literal_eval
from ocli import arg, flag, param, Main, Base
from ocli.extra import BasicLog, LogOpt


def parse_keyfile(path):
    with as_source(path, "r") as r:
        return parse_key(r.read())


def parse_key(text):
    return literal_eval(text)


def as_source(path, mode="rb"):
    if path and path != "-":
        return open(path, mode)
    from sys import stdin

    return stdin.buffer if "b" in mode else stdin


def as_sink(path, mode="wb"):
    if path and path != "-":
        return open(path, mode)
    from sys import stdout

    return stdout.buffer if "b" in mode else stdout


# @arg("output", default=None, help="save key to file")
# @arg("which", required=True, choices=["1", "2", "e", "d"], help="which key to output")
# @arg("keyfile", required=True, help="the key file to extract key")
# class Pick(BasicLog, Main):
class Pick(LogOpt, Base):
    app_name = "pick"

    def options(self, opt):
        super().options(
            opt
            # first argument
            .arg("keyfile", required=True, help="the key file to extract key")
            # second argument
            .arg(
                "which",
                required=True,
                choices=["1", "2", "e", "d"],
                help="which key to output",
            )
            # third argument
            .arg("output", default=None, help="save key to file")
        )

    def start(self, *args, **kwargs):
        desc = parse_keyfile(self.keyfile)

        if self.which in ("2", "d"):
            desc.pop("e")
        else:
            desc.pop("d")

        with as_sink(self.output, "w") as out:
            from pprint import pformat

            out.write(pformat(desc))


# @flag("short", "s", help="short message encryption", default=False)
# @param("output", "o", help="output to file", default=None)
class Crypt:
    def options(self, opt):
        super().options(
            opt
            # --short, -s
            .flag(
                "short", "s", help="short message encryption", default=False
            )
            # --output FILE, -o FILE
            .param("output", "o", help="output to file", default=None)
        )


(__name__ == "__main__") and Pick().main()
