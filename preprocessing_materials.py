import pandas as pd

def load_active_materials(materials_path='./data/extended/materials.csv',
                          start='2025-01-01',
                          end='2025-05-31'):
    """
    Loads and filters material data to return:
      1. active_rms: list of raw material IDs active in the given period
      2. product_to_rm: mapping from product_id to rm_id
      3. materials_status: DataFrame with one row per rm_id (latest version) + 'is_active' flag

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
    materials["deletion_date"] = materials["stock_location"].apply(parse_deletion_date)

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

    # --- 8️⃣ Create product → rm mapping ---
    product_to_rm = (
        materials[["product_id", "rm_id"]]
        .dropna()
        .drop_duplicates()
        .set_index("product_id")["rm_id"]
        .to_dict()
    )

    # --- 9️⃣ Print summary ---
    print(f"✅ Active raw materials in {start.year}-H1: {len(active_rms)}")
    print(f"✅ Created mapping for {len(product_to_rm)} product_ids.")
    print(f"ℹ️ Total distinct rm_ids: {materials_latest['rm_id'].nunique()}")
    if len(product_to_rm) > 0:
        print("Example mappings:", list(product_to_rm.items())[:5])

    # --- 🔟 Return all three ---
    return active_rms, product_to_rm, materials_latest