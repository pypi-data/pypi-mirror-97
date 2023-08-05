from ocli import sub, Main, Base
from .cli import decrypt, encrypt, keygen, pick


# @sub(
#     {
#         "decrypt": decrypt.Decrypt,
#         "encrypt": encrypt.Encrypt,
#         "keygen": keygen.KeyGen,
#         "pick": pick.Pick,
#     },
#     help="select sub command",
#     required=True,
# )
# class Top(Main):
class Top(Base):
    def options(self, opt):
        super().options(
            opt.sub(
                {
                    "decrypt": decrypt.Decrypt,
                    "encrypt": encrypt.Encrypt,
                    "keygen": keygen.KeyGen,
                    "pick": pick.Pick,
                },
                help="select sub command",
                required=True,
            )
        )


def main():
    return Top().main()


(__name__ == "__main__") and Top().main()
