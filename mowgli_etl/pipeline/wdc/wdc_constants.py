from mowgli_etl.paths import DATA_DIR

WDC_NAMESPCE = "wdc"
WDC_DATASOURCE_ID = "wdc"

WDC_ARCHIVE_PATH = DATA_DIR / "wdc" / "extracted"
WDC_CSV_FILE_KEY = "wdc_csv_file"

# Placeholder predicates
# MUCH_SMALLER_THAN = "/r/MuchSmallerThan"
SMALLER_THAN = "/r/SmallerThan"
EQUIVALENT_TO = "/r/EquivalentTo"
LARGER_THAN = "/r/LargerThan"
# MUCH_LARGER_THAN = "/r/MuchLargerThan"
CANT_COMPARE = "/r/Can'tCompare"
