from mowgli_etl.paths import DATA_DIR

WDC_NAMESPCE = 'wdc'
WDC_DATASOURCE_ID = 'wdc'

WDC_ARCHIVE_PATH = DATA_DIR / 'wdc' / 'extracted'
WDC_CSV_FILE_KEY = 'wdc_csv_file'

WDC_RE_DIMENSION_DECIMAL_STR = r"\d+\s\d+[hwl]\s"
WDC_RE_DIMENSION_STR = r"\d+[hwl]\s"
WDC_RE_DIMENSION_UNIT_STR = r"(?<=\d\w\s)\w\w"
WDC_UNITS = ["ml", "cm", "mm", "in", "ft", "m"]

WDC_HAS_DIMENSIONS = "has dimensions"
