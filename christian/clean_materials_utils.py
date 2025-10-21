import pandas as pd
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)
print(f"Changed directory to: {project_root}")

def extract_unique_rm_pairs(materials: pd.DataFrame) -> pd.DataFrame:
    """Extracts unique (rm_id, product_id) pairs from the given CSV data."""
    return materials[["rm_id", "product_id"]].dropna().drop_duplicates()

def reduce_to_latest_product_versions(materials: pd.DataFrame) -> None:
    """In-place reduces the materials DataFrame to only the latest product version per rm_id"""
    idx = materials.groupby("rm_id")["product_version"].idxmax()
    materials.drop(materials.index.difference(idx), inplace=True) # type: ignore
    materials.reset_index(drop=True, inplace=True)
 
if __name__ == "__main__":
    materials = pd.read_csv('data/extended/materials.csv').dropna()
    print(materials.head(3))
    reduce_to_latest_product_versions(materials)
    print(materials.head(3))

