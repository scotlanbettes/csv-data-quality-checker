\# Quality Score Methodology



\## Overview



The CSV Data Quality Checker calculates a quality score between 0 and 100.



A higher score indicates better dataset quality.



\---



\## Formula



```text

Quality Score =

100 - Missing Percentage - Duplicate Percentage

```



\---



\## Missing Percentage



```text

(Number of Missing Cells / Total Cells) × 100

```



\---



\## Duplicate Percentage



```text

(Number of Duplicate Rows / Total Rows) × 100

```



\---



\## Example



Dataset:



\- Missing Percentage = 13.33%

\- Duplicate Percentage = 16.67%



Score:



```text

100 - 13.33 - 16.67 = 70

```



Final Score:



```text

70

```



\---



\## Score Interpretation



| Score | Interpretation |

|---------|--------------|

| 90-100 | Excellent |

| 75-89 | Good |

| 50-74 | Needs Attention |

| 0-49 | Poor |



\---

