# Type inference notes

Type inference is based on non-missing values.

A column is considered boolean if most present values look like true/false, yes/no or 1/0.

A column is considered integer if most present values can be parsed as integers.

A column is considered float if most present values can be parsed as numbers.

A column is considered date-like if most present values match one of the supported date formats.

Otherwise, the column is treated as categorical.

The threshold is intentionally conservative because CSV files often contain noise, missing values and inconsistent formatting.
