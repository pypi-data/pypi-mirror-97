from pretzels.functions import *

def testSourceDataDerivation(file_name):
    """Tests year, month, and day derivation"""
    print('Enter filename')
    _, mth, dt, _ = deriveFeedNameAndSourceData(file_name)

    # assert mth properly derived
    year = int(mth[:4])
    assert 2018 < year < 2030, f"Invalid {mth}"

    month = int(mth[-2:])
    assert 0 < month < 13

    day = int(dt[-2:])
    assert 0 < day < 32

if __name__ == "__main__":
    testSourceDataDerivation()