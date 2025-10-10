# Load materials
materials = pd.read_csv('./data/extended/materials.csv').dropna()

def parse_deletion_date(s):
    """
    Extracts a deletion date from strings like 'DELETED_12.05:2025_SB 16 B'.
    Returns NaT if no valid date is found.
    """
    if isinstance(s, str) and s.startswith("DELETED_"):
        try:
            # "DELETED_12.05:2025_SB..." → "12.05:2025" → "12.05.2025"
            date_part = s.split("_")[1].replace(":", ".")
            return pd.to_datetime(date_part, format="%d.%m.%Y", errors="coerce")
        except Exception:
            return pd.NaT
    return pd.NaT

materials["deletion_date"] = materials["stock_location"].apply(parse_deletion_date)

# Sort by product_id + version, newest first
materials_sorted = (
    materials
    .sort_values(["product_id", "product_version"], ascending=[True, False])
)

materials_latest = (
    materials_sorted
    .drop_duplicates(subset="product_id", keep="first")
    .reset_index(drop=True)
)

start = pd.Timestamp("2025-01-01")
end = pd.Timestamp("2025-05-31")

# Filter for materials active at any time during that window
materials_active = materials_latest[
    (
        materials_latest["deletion_date"].isna()  # still active
        | (materials_latest["deletion_date"] >= start)  # deleted after our start date
    )
]

# flag which are still active after the horizon
materials_active["is_active_after_horizon"] = (
    materials_active["deletion_date"].isna()
    | (materials_active["deletion_date"] > end)
)

# Extract list of rm_ids
active_rms = materials_active["rm_id"].dropna().unique().tolist()

print(f"Active raw materials in 2025-H1: {len(active_rms)}")

# Create mapping of product_id to rm_id
product_to_rm = (
    materials[["product_id", "rm_id"]]
    .dropna()
    .set_index("product_id")["rm_id"]
    .to_dict()
)

print(f"✅ Created mapping for {len(product_to_rm)} product_ids.")
print("Example mappings:", list(product_to_rm.items())[:10])

return active_rms, product_to_rm