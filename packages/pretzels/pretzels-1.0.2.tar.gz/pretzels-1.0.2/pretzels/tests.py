from pretzels.functions import *

def testSourceDataDerivation():
    """Tests year, month, and day derivation"""
    print('Enter filename')
    filename = str(input())
    _, mth, dt, _ = deriveFeedNameAndSourceData(filename)

    # assert mth properly derived
    year = int(mth[:4])
    assert 2018 < year < 2030, f"Invalid {mth}"

    month = int(mth[-2:])
    assert 0 < month < 13

    day = int(dt[-2:])
    assert 0 < day < 32

if __name__ == "__main__":
    testSourceDataDerivation()