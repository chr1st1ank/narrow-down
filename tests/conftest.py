"""Common fixtures for the test modules."""
import pytest


@pytest.fixture
def sample_byte_strings():
    """Return a list of byte arbitrary byte strings."""
    return [
        b"QHtbc3lzdGVtICJ0b3VjaCAvdG1wL2JsbnMuZmFpbCJdfQ==",
        b"ZXZhbCgicHV0cyAnaGVsbG8gd29ybGQnIik=",
        b"U3lzdGVtKCJscyAtYWwgLyIp",
        b"YGxzIC1hbCAvYA==",
        b"S2VybmVsLmV4ZWMoImxzIC1hbCAvIik=",
        b"S2VybmVsLmV4aXQoMSk=",
        b"JXgoJ2xzIC1hbCAvJyk=",
        b"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iSVNPLTg4NTktMSI/PjwhRE9DVFlQRSBmb28g",
        b"WyA8IUVMRU1FTlQgZm9vIEFOWSA+PCFFTlRJVFkgeHhlIFNZU1RFTSAiZmlsZTovLy9ldGMvcGFz",
        b"c3dkIiA+XT48Zm9vPiZ4eGU7PC9mb28+",
        b"JEhPTUU=",
        b"JEVOVnsnSE9NRSd9",
        b"true",
        b"false",
        b"-1.00",
        b"-$1.00",
        b"-1/2",
        b"-1E2",
        b"0/0",
        b"-2147483648/-1",
        b"-9223372036854775808/-1",
        b"-0",
        b"-0.0",
        b"+0",
        b"+0.0",
    ]
