# 📖 Technical Specification: AP-Audit Tool

Since Jules requires a GitHub-connected repository to work, I've drafted the full technical specification here. We can implement this locally tomorrow or push it to GitHub to let Jules take over.

## 1. Tool Overview
`ap-audit` is a Python-based CLI utility designed to ingest student FRQ responses and provide "College Board Style" feedback.

## 2. Command Structure
```bash
python ap_audit.py --year [YEAR] --q [NUMBER] --ans "[USER_ANSWER]"
```

## 3. Data Source Mapping
The tool will reference `P:\Data\Education\AP_Chem_FRQs\`:
- **Year 2025:** `ap25-sg-chemistry.pdf`
- **Year 2024:** `ap24-sg-chemistry.pdf`
- ...and so on.

## 4. Scoring Logic (The "Must-Say" Engine)
The core logic uses a dictionary of "Must-Say" phrases mapped to specific topics:
- **IMF Questions:** Requires `polarizable`, `electron cloud`, `London dispersion`.
- **Thermo Questions:** Requires `entropy`, `dispersed`, `microstates`, `favorability`.
- **Acid/Base:** Requires `half-equivalence`, `Henderson-Hasselbalch`, `hydrolysis`.

## 5. Sample Output
```text
>>> AP-AUDIT REPORT (2025 Q5)
---------------------------------------
STATUS: [ 0 / 1 ] Points
USER: "Molecule X is bigger so it has a higher boiling point."

RED INK:
- "Bigger" is a size description, not a chemical mechanism.
- Missing reference to electron cloud polarizability.

UPGRADE:
"Molecule X has a LARGER, MORE POLARIZABLE ELECTRON CLOUD, leading to 
stronger LDFs and a higher boiling point."
---------------------------------------
```

## 6. Implementation Steps
1.  **Extract:** Use `PyPDF2` or similar to extract text from the SG PDFs.
2.  **Analyze:** Use a lightweight LLM call or regex-based scoring.
3.  **Report:** Generate the Markdown/Console report.

---
**Next Move:** Decide whether to push to GitHub or build locally tomorrow morning.
