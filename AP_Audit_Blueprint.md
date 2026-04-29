# 🛠️ Project: AP-Audit CLI (Conceptual Blueprint)

## 🎯 Objective
A specialized tool that turns the Gemini CLI into a **College Board Grader**. It will analyze practice FRQ responses against the 17-year historical database to ensure "Must-Say" phrases are present.

## 🏗️ Architecture
1.  **The Dataset:** Uses the existing `P:\Data\Education\AP_Chem_FRQs\` folder as the primary source of truth.
2.  **The Logic:**
    *   `INPUT`: User's handwritten or typed response + Year/Question number.
    *   `PROCESS`:
        *   Retrieve the specific Scoring Guideline PDF.
        *   Scan for "Acceptable Responses" and "Must-Say" technical vocabulary.
        *   Compare User Input vs. Official Key.
    *   `OUTPUT`: A "Red Ink" report highlighting point losses and "Upgrade Suggestions."

## ⌨️ Command Interface (Ideas)
*   `ap-audit --year 2025 --q 1 --input "Molecule A is bigger so it has a higher BP"`
*   **Gemini's Response:** 
    > ❌ **0/1 Points.** 
    > **Reason:** Lacks mechanism. "Bigger" is insufficient.
    > **Upgrade:** "Molecule A has a **larger, more polarizable electron cloud**, leading to stronger LDFs."

## 🚀 Deployment Plan (using `skill-creator`)
1.  **Step 1:** Create an `AP_AUDITOR.md` instructions file that defines the "Grader Persona."
2.  **Step 2:** Define a specific prompt template for the `universal-converter` or a custom script to extract text from the FRQ PDFs for faster searching.
3.  **Step 3:** Activate the skill whenever you start a "Workout" or "Simulation" session.

---
**Status:** Brainstorming Phase. Ready to build tomorrow?
