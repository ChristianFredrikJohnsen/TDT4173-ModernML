import pandas as pd

def load_active_materials(materials_path='./data/extended/materials.csv',
                          start='2025-01-01',
                          end='2025-05-31'):
    """
    Loads and filters material data to return:
      active_rms: list of raw material IDs active in the given period

    Logic:
      - Only keep newest product_version per rm_id
      - Parse 'DELETED_<date>' as deletion date
      - A material is active if deletion_date is NA or >= start
    """

    # --- 1️⃣ Helper: parse deletion date ---
    def parse_deletion_date(s):
        if isinstance(s, str) and s.startswith("DELETED_"):
            try:
                # Extract only the part after DELETED_ up to the next underscore or space
                after_prefix = s.split("_", 1)[1]
                date_str = after_prefix.split("_")[0].split()[0].replace(":", ".")
                return pd.to_datetime(date_str, format="%d.%m.%Y", errors="coerce")
            except Exception:
                return pd.NaT
        return pd.NaT

    # --- 2️⃣ Load data ---
    materials = pd.read_csv(materials_path).dropna(subset=["product_id", "rm_id"])

    # --- 3️⃣ Add deletion_date ---
    materials["deletion_date"] = materials["stock_location"].apply(parse_deletion_date) # type: ignore

    # --- 4️⃣ Keep only newest version per rm_id ---
    materials_sorted = materials.sort_values(["rm_id", "product_version"], ascending=[True, False])
    materials_latest = materials_sorted.drop_duplicates(subset="rm_id", keep="first").reset_index(drop=True)

    # --- 5️⃣ Convert time window ---
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)

    # --- 6️⃣ Define activity flags ---
    materials_latest["is_active"] = (
        materials_latest["deletion_date"].isna() |
        (materials_latest["deletion_date"] >= start)
    )
    materials_latest["is_active_after_horizon"] = (
        materials_latest["deletion_date"].isna() |
        (materials_latest["deletion_date"] > end)
    )

    # --- 7️⃣ Extract subsets ---
    materials_active = materials_latest[materials_latest["is_active"]].copy()
    active_rms = materials_active["rm_id"].dropna().unique().tolist()

    return active_rms
