I need you to create a folder in TestRail for organizing test cases.

{FODLER_NAME}: 5567 - Add persisted events for TransferStatusForReservationStatementListener
{DESCRIPTION}: https://jira.paysera.net/browse/CORE-5567

Project Location: /Users/employee/Projects/qa-analysis-claude

TestRail Configuration:
- Project ID: 2 (Paysera)
- Suite ID: 14 (Nova Tribe)
- Parent Folder: Root level (Nova Tribe main section)

Steps:
1. Navigate to the project directory
2. Run the following command:
   ```bash
   python3 create_testrail_folder.py \
     --project 2 \
     --suite 14 \
     --folder "{FOLDER_NAME}" \
     --description "{DESCRIPTION}"
   ```
3. Verify the folder was created successfully
4. Return the TestRail folder ID and URL

Expected Output:
- Folder ID: [new section ID]
- Folder Name: {FOLDER_NAME}
- Parent: None (root level in Nova Tribe)
- TestRail URL: https://testrail.paysera.net/index.php?/suites/view/14

Notes:
- The folder will be created at the root level of the Nova Tribe suite (Suite 14)
- If a folder with the same name already exists, it will return the existing folder ID
- The folder will be in Project 2 (Paysera), Suite 14 (Nova Tribe)
