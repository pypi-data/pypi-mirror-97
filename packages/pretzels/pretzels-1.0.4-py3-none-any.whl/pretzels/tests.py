from pretzels.functions import *

def testSourceDataDerivation(file_name):

    """Tests year, month, and day derivation"""
    
    _, mth, dt, _ = deriveFeedNameAndSourceData(file_name)

    # assert mth properly derived
    year = int(mth[:4])
    assert 2018 < year < 2030, "Invalid year"

    month = int(mth[-2:])
    assert 0 < month < 13, "Invalid month"

    day = int(dt[-2:])
    assert 0 < day < 32, "Invalid day"

    return "All tests pass!"

if __name__ == "__main__":
    # if testing locally, here are some examples of what should pass or fail
    # run with command "python tests.py"
    good_file_name = 'exit_survey_export_20210202111111.csv'
    print("TEST SHOULD PASS:", testSourceDataDerivation(good_file_name))

    bad_file_name = "exit_survey_export_20211325.csv"
    print(testSourceDataDerivation(bad_file_name))
