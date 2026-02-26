import pandas as pd

"""
In case you're not running the tests from the christian folder, add christian to sys.path,
enabling you to find the clean_materials_utils module.
"""
import os, sys
christian_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(christian_dir) if christian_dir not in sys.path else None

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(project_root)

def test_dates_change_after_tz_conversion():
    """
    Show that some of the receival dates change when converting all dates to GMT +2.
    After writing this test, I realized that we only really care about the date part,
    so there's actually no need to convert the timezones at all.
    """
    main_file = pd.read_csv("data/kernel/receivals.csv", parse_dates=['date_arrival'])
    original_dates = main_file['date_arrival'].apply(lambda x: x.date()).tolist()
    
    processed_utc2 = main_file.copy()
    processed_utc1 = main_file.copy()
    processed_utc = main_file.copy()
    processed_utc2['date_arrival'] = pd.to_datetime(processed_utc2['date_arrival'], utc=True).dt.tz_convert('Etc/GMT+2')
    processed_utc1['date_arrival'] = pd.to_datetime(processed_utc1['date_arrival'], utc=True).dt.tz_convert('Etc/GMT+1')
    processed_utc['date_arrival'] = pd.to_datetime(processed_utc['date_arrival'], utc=True)

    assert original_dates != processed_utc2['date_arrival'].apply(lambda x: x.date()).tolist(), "Receival dates did not change after converting to GMT+2."
    assert original_dates != processed_utc1['date_arrival'].apply(lambda x: x.date()).tolist(), "Receival dates did not change after converting to GMT+1."
    assert original_dates != processed_utc['date_arrival'].apply(lambda x: x.date()).tolist(), "Receival dates did not change after converting to UTC."
