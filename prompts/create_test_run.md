# Create Test Run in TestRail

I need you to create a test run in TestRail that includes test cases from specified folders.

## Configuration

**Project Location:** /Users/employee/Projects/qa-analysis-claude

**TestRail Configuration:**
- Project ID: {PROJECT_ID} (e.g., 2 for Paysera)
- Suite ID: {SUITE_ID} (e.g., 14 for Nova Tribe)

## Test Run Details

**Test Run Name:**  5567 - Add persisted events for TransferStatusForReservationStatementListener 

**Reference:** CORE-5567

**Description:** https://jira.paysera.net/browse/CORE-5567

**Include Test Cases From Folders:**
-  5567 - Add persisted events for TransferStatusForReservationStatementListener
-  5663-Internal Balances & Credit Limits Migration (BGN → EUR) 
- 

## Instructions

Create a test run in TestRail with the specifications above by:
1. Collecting all test cases from the specified folders
2. Creating the test run with those test cases
3. Verifying the test run was created successfully
4. Returning the test run ID and URL

## Command to Run

```bash
python3 create_test_run.py \
  --project {PROJECT_ID} \
  --suite {SUITE_ID} \
  --name "{TEST_RUN_NAME}" \
  --refs "{REFERENCE}" \
  --description "{DESCRIPTION}" \
  --folders "{FOLDER_NAME_1}" "{FOLDER_NAME_2}" "{FOLDER_NAME_3}"
```

## Expected Output

After creating the test run, provide a summary:

```
✓ Test Run Created Successfully!

Test Run ID: {RUN_ID}
Name: {TEST_RUN_NAME}
Test Cases: {NUMBER_OF_CASES}
References: {REFERENCE}
TestRail URL: https://testrail.paysera.net/index.php?/runs/view/{RUN_ID}
```

---

## Example Usage

### Example 1: Create test run for a single feature

**Test Run Name:** 5567 - Add persisted events for TransferStatusForReservationStatementListener

**Reference:** CORE-5567

**Description:** 5567 - Add persisted events for TransferStatusForReservationStatementListener

**Include Test Cases From Folders:**
- 5567 - Add persisted events for TransferStatusForReservationStatementListener

**Command:**
```bash
python3 create_test_run.py \
  --project 2 \
  --suite 14 \
  --name "5567 - Add persisted events for TransferStatusForReservationStatementListener" \
  --refs "CORE-5567" \
  --description "5567 - Add persisted events for TransferStatusForReservationStatementListener" \
  --folders "5567 - Add persisted events for TransferStatusForReservationStatementListener"
```

**Result:**
```
✓ Test Run Created Successfully!

Test Run ID: 12649
Name: 5567 - Add persisted events for TransferStatusForReservationStatementListener
Test Cases: 2
References: CORE-5567
TestRail URL: https://testrail.paysera.net/index.php?/runs/view/12649
```

---

### Example 2: Create test run for multiple features

**Test Run Name:** Sprint 42 - Regression Test Run

**Reference:** SPRINT-42

**Description:** Full regression testing for Sprint 42 features

**Include Test Cases From Folders:**
- 5567 - Feature A
- 5568 - Feature B
- 5569 - Feature C

**Command:**
```bash
python3 create_test_run.py \
  --project 2 \
  --suite 14 \
  --name "Sprint 42 - Regression Test Run" \
  --refs "SPRINT-42" \
  --description "Full regression testing for Sprint 42 features" \
  --folders "5567 - Feature A" "5568 - Feature B" "5569 - Feature C"
```

---

## Notes

- Folder names must match exactly (case-sensitive)
- The script will automatically collect all test cases from the specified folders
- If a folder doesn't exist or contains no test cases, a warning will be shown
- Multiple folders can be specified to include test cases from different sections
- The test run will include all test cases found in the specified folders
- References can include multiple ticket IDs separated by commas (e.g., "CORE-5567,CORE-5568")
