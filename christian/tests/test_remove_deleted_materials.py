import pandas as pd

"""
In case you're not running the tests from the christian folder, add christian to sys.path,
enabling you to find the clean_materials_utils module.
"""
import os, sys
christian_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(christian_dir) if christian_dir not in sys.path else None
from clean_materials_utils import extract_unique_rm_pairs, reduce_to_latest_product_versions

def test_number_of_rm_ids():
    """Ensure that the number of unique rm_ids matches the expected count (203)."""
    materials_file = pd.read_csv("data/extended/materials.csv").dropna()
    unique_rm_ids = materials_file["rm_id"].nunique()
    expected_rmid_count = 203
    assert unique_rm_ids == expected_rmid_count, f"Expected {expected_rmid_count} unique rm_ids, found {unique_rm_ids}"

def test_extracts_unique_rm_pairs():
    """Extracts unique (rm_id, product_id) pairs from the given CSV data."""
    test_data = pd.read_csv("christian/tests/material_csv/extract_unique_rm_pairs.csv")

    unique_pairs = extract_unique_rm_pairs(test_data)
    records = unique_pairs[["rm_id", "product_id"]].values.tolist()
    expected = [
        [342, 91900170.0],
        [357, 91900152.0],
    ]
    assert records == expected

def test_reduce_to_latest_product_versions():
    """In-place reduces the materials DataFrame to only the latest product version per rm_id"""
    test_data = pd.read_csv("christian/tests/material_csv/six_entries.csv")
    reduce_to_latest_product_versions(test_data)
    records = test_data.values.tolist()
    expected = [
        [358,91900170.0,2,"SA12 Trader",3.0,"DELETED_28.02:2011_SB05 anodiz"],
        [360,91900160.0,1,"SA16 608250",24.0,"DELETED_28.02:2011_SA16 6082"],
        [362,91900143.0,13,"606035 IS",32.0,"SB 04"],
        [364,91900182.0,4,"99.5 Grannalla",24.0,"DELETED_10.09:2015_SA 99.5"],  
    ]
    assert records == expected

def test_reduce_to_latest_product_versions_same_product_id():
    """
    In this test scenario we have two different rm_ids (3122 and 3123),
    and they both have the same product_id (91901460.0).
    After calling reduce_to_latest_product_versions, we expect to keep one entry
    for each rm_id, specifically the one with the highest product_version.
    """

    test_data = pd.read_csv("christian/tests/material_csv/many_product_versions.csv")
    reduce_to_latest_product_versions(test_data)
    records = test_data.values.tolist()
    expected = [
        [3122,91901460.0,39,"Shredded 95% PC - Alumisel",47.0,"SC 03"],
        [3123,91901460.0,38,"Shredded 95% PC - Hernández",47.0,"SC 05"]
    ]
    assert records == expected

def test_materials_only_one_na_row():
    """The first row in the materials file is ',,,,,' and thus we expect exactly one NA row."""
    materials_file = pd.read_csv("data/extended/materials.csv")
    materials_dropna = materials_file.dropna()
    assert len(materials_file) == len(materials_dropna) + 1, "Expected exactly one NA row in materials file"

def test_rm_id_implies_unique_product_id():
    """
    We want to prove that each rm_id is associated with only one product_id.
    This assumption is often true, but there is one known exception: rm_id 3362.0
    which is associated with two different product_id values.
    """
    materials_file = pd.read_csv("data/extended/materials.csv").dropna()
    rmid_productid_counts = materials_file.groupby("rm_id")["product_id"].nunique()

    assert rmid_productid_counts.loc[3362.0] == 2, \
        f"Expecting rm_id 3362.0 to be associated with 2 product_id values, found {rmid_productid_counts.loc[3362.0]}"

    mask = rmid_productid_counts.index != 3362.0
    assert (rmid_productid_counts.loc[mask] == 1).all(), \
        f"Found rm_ids other than 3362.0 associated with multiple product_id values"

def test_product_id_product_version_combination_unique():
    """Ensure that for each product_id, the highest product_version is unique."""
    raise NotImplementedError("TODO: Implement this test")
