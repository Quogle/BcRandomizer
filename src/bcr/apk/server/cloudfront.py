import base64
import json
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


CF_KEY_PAIR_ID = "APKAJO6MLYTURWB2NOWQ"

CF_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCORX64nic2atwz
1VsqbI/jqHwrdrSktgjoBrFWqgziJXrVvHVZ+shhUfRxa4BKvdRigbZuNjrmFfUE
Scxdfj72QAe0SRxgMhaloPikbSUlvrfOacFOiQD7dMtwv8DAAjvshKU/qmzdkp1j
DC3QcIX5gsuNqUuM6SxPBZviuvxD/IsbLlxxUCh30hZNUb/3aTf00SzI1/rAL2jB
faQfR6FY2qt0yICoXaVwCu6GObJDPdMjX8ssCmTxRb81aAnfUy6A9x/ywutYjjaY
W2RA9hzWCxk6nONpuRQsZkEbNULoKzgyfxMc/xNfFYH+0T2ui59zsRVTNsCHYVEb
iz9an3HXAgMBAAECggEAGMPgGyLskHxpeFxbUjczlN1vP+GZ8FH/muQPWpafR35e
s3Xqt47/8nDhrByaaGhC4CLULrsh5YtM60ItYNjo/NSIgsl3NweBCbPLlFOrc7aP
KE8gZxtSIHNkNmwqkUHSTImKelqgOLGc0/D6yJ3NtHEgHbiqfgzYuaiwSfdikjLR
T5sRs7T5k0Gy67FSOOa43s4WHj77ywdcvYbzBdSM/uu8R2Syng4RijKCvKLIEIE0
3lPDI9/KNG8ofSyaqjLa09xfooQ7S8La21El3iu/icOowR0WM+hXLcEilCkuMFY1
IrheIsx2Pyb6N3qwE/jRMIqQwH5uzM8OThmU+17tgQKBgQDCwrR33GXg5SNvSg4N
iBsuV1p2sXeuJxZrSCyNUVaT7lg01dUnk9MbAflqNsD43mHdXWYLd8FqKZ4Fc3K/
t3sdYJPeOmMIKmBexhOnohoAwg4FZhuUvzhx6DPuBG2gSCzzGNjU9SXCr9TQlwkc
XTRIEjBe5JuFFhHGe+xMVEu+rQKBgQC7AasNilpc7lhXuNi/fXdJwqX+s3Jiolys
8BQJ83i1Xy7pzfa2usOjYLFcebcXv9lTfrDUW4ju1ip8zVVWkdF9xE9uRFDbSBJo
MvQNa9bGgFlLu/V5XsbCFbFrYqI94OHIT4/2dHJsyeJpoXpoFHZ2aGt/98fFEGqU
YbAdR/HXEwKBgQCPMEUshm6knPKjZKfWTQXm2TRaZXmfIX+7GlIfB/kGQ8q39aqE
MYuYpKfx7hWMIzuCW6OltMMPwU87pLhtuYEbhSDR1s1ueHFn3Gsg6O4DNqjGUV7f
yoK+REDBsqHCoK3jgJYSY7YCX/Gv9gstvlyszCqh6aNpgmNJMVz2dVdG9QKBgQCK
G2FITrUNjLiRkGICiZZfUvFkeQIw9deboHIsJzMuP21WHlXl/WgecHqL4Rfm4jiO
ATJ2omMuf9xA7yPnGymryB8hQDK2vzNY4Mh8YPftATzxQY64Y9ZF3993fxBywnH8
jUW0rasTzMT5XdgYpYQXTmaVy1gtoUIU81AtT8S7IQKBgQC2F7xdWSv7Pw+MimN2
Tx8VMiCUkL+5uNJwvWw2rrEHvt2jphD016pgdutlgI28qoXwcleLxAz1Ey1njCTO
19bsOA9bhuwbIrIb93nGHyRrQe1L7PdBjwlIqEj8R08Z/oGQsXhqzgF9KfO2V46i
oPSxLzYw2sBjmwVooXMVr6GxEw==
-----END PRIVATE KEY-----"""


def generate_signed_cookie() -> str:
    url = "https://nyanko-assets.ponosgames.com/*"

    policy = {
        "Statement": [
            {
                "Resource": url,
                "Condition": {
                    "DateLessThan": {
                        "AWS:EpochTime": int(time.time()) + 3600,
                    },
                    "DateGreaterThan": {
                        "AWS:EpochTime": int(time.time()) - 3600,
                    },
                },
            }
        ]
    }

    policy_string = json.dumps(
        policy,
        separators=(",", ":"),
    )

    private_key = serialization.load_pem_private_key(
        CF_PRIVATE_KEY.encode(),
        password=None,
    )

    signature = private_key.sign(
        policy_string.encode(),
        padding.PKCS1v15(),
        hashes.SHA1(),
    )

    encoded_policy = base64.b64encode(
        policy_string.encode()
    ).decode()

    encoded_signature = base64.b64encode(
        signature
    ).decode()

    return (
        f"CloudFront-Key-Pair-Id={CF_KEY_PAIR_ID};"
        f"CloudFront-Policy={encoded_policy};"
        f"CloudFront-Signature={encoded_signature}"
    )