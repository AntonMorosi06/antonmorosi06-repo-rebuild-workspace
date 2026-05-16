# Known Limitations

- This is a compact educational CSV analyzer, not a full BI platform.
- Very large CSV files may be slow or memory-heavy because Pandas loads the file into memory.
- Separator detection is based on common separators, not a full dialect inference system.
- The GUI is intentionally simple.
- Plots are basic histograms for numeric columns.
- No database connection is implemented.
- No automatic data cleaning is performed beyond reading and summary generation.
