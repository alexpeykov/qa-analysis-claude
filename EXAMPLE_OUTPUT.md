# Example Output

This document shows what the tool generates and what Claude produces.

## Example Command

```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PAY-1234 \
  --mr https://gitlab.paysera.net/project/payments/-/merge_requests/567
```

## Step 1: Script Output (What You Get)

The script fetches data and generates a comprehensive prompt like this:

```
================================================================================
MAIN JIRA TICKET
================================================================================

Ticket Key: PAY-1234
Summary: Add support for multi-currency payments
Type: Story
Status: In Progress
Priority: High
Assignee: John Doe
Reporter: Jane Smith

Description:
As a user, I want to be able to make payments in multiple currencies
so that I can pay in my preferred currency.

Acceptance Criteria:
- User can select from available currencies
- Exchange rates are fetched in real-time
- Transaction is recorded with both currencies
- Email receipt shows both amounts

--- Comments (3) ---

Comment #1 by Jane Smith on 2024-12-01:
We need to integrate with the ECB API for exchange rates.

Comment #2 by John Doe on 2024-12-02:
Implemented currency selector. Using ECB API as suggested.

Comment #3 by QA Lead on 2024-12-03:
Please ensure proper error handling if API is down.

================================================================================
GITLAB MERGE REQUESTS
================================================================================

--- Merge Request: Add multi-currency support ---
State: opened
Author: John Doe
Branch: feature/multi-currency → main
Files Changed: 8

Description:
This MR implements multi-currency payment support including:
- Currency selector component
- ECB API integration
- Database schema updates
- Email template updates

--- Commits (5) ---
- abc123: Add currency selector to payment form
- def456: Integrate ECB exchange rate API
- ghi789: Update database schema for multi-currency
- jkl012: Add error handling for API failures
- mno345: Update email templates

--- Code Changes ---

File: src/components/PaymentForm.tsx
Status: Modified
Diff:
+ import CurrencySelector from './CurrencySelector';
+ const [selectedCurrency, setSelectedCurrency] = useState('EUR');
...

File: src/api/exchangeRates.ts
Status: New
Diff:
+ export async function getExchangeRate(from: string, to: string) {
+   const response = await fetch(`https://api.ecb.europa.eu/...`);
+   return response.json();
+ }
...

[Additional files and changes...]
```

## Step 2: Claude's Analysis (What Claude Generates)

When you provide the above to Claude, it generates:

```markdown
# QA Analysis Report

## Executive Summary

This feature introduces multi-currency payment support, allowing users to pay in
their preferred currency with real-time exchange rate conversion. The implementation
includes frontend currency selection, integration with the European Central Bank (ECB)
API for exchange rates, database schema modifications to store dual-currency data,
and updated email templates to show amounts in both currencies.

**Key Changes:**
- New CurrencySelector component in the payment form
- ECB API integration with error handling
- Database schema extended to store original and converted amounts
- Email templates updated to display both currency amounts

**Risk Areas:**
- External API dependency (ECB API availability)
- Currency conversion accuracy
- Race conditions in exchange rate fetching
- Data consistency between currencies

## Test Ideas

1. **Functional Testing: Currency Selection**
   - Description: Verify users can select from all available currencies
   - Rationale: Core functionality must work for primary use case

2. **Edge Case: API Failure Handling**
   - Description: Test behavior when ECB API is unavailable or times out
   - Rationale: Critical for system reliability per QA Lead's comment

3. **Integration Testing: End-to-End Payment Flow**
   - Description: Complete payment in non-default currency and verify all systems
   - Rationale: Ensures all components work together correctly

4. **Edge Case: Extreme Exchange Rates**
   - Description: Test with very high/low exchange rates (e.g., 1 EUR = 15000 IDR)
   - Rationale: Ensures UI and calculations handle large numbers

5. **Negative Testing: Invalid Currency Codes**
   - Description: Attempt to use invalid or unsupported currency codes
   - Rationale: Validates input validation and error handling

6. **Security Testing: API Injection**
   - Description: Try to inject malicious data into currency parameters
   - Rationale: External API calls are potential security vulnerabilities

7. **Performance Testing: Exchange Rate Caching**
   - Description: Measure response time and verify caching of exchange rates
   - Rationale: Real-time fetching could impact performance

8. **Regression Testing: Default Currency Payments**
   - Description: Ensure existing EUR-only payments still work correctly
   - Rationale: New feature shouldn't break existing functionality

9. **Data Testing: Currency Precision**
   - Description: Verify decimal places and rounding for different currencies
   - Rationale: Different currencies have different precision requirements

10. **Usability Testing: Currency Selector UX**
    - Description: Evaluate ease of finding and selecting preferred currency
    - Rationale: Feature usability affects user satisfaction

11. **Integration Testing: Email Receipt Accuracy**
    - Description: Verify both currency amounts are correct in email receipts
    - Rationale: User communication must be accurate

12. **Edge Case: Concurrent Rate Changes**
    - Description: Test behavior when exchange rate changes during payment
    - Rationale: Ensures data consistency in race conditions

13. **Negative Testing: Unsupported Currencies**
    - Description: Test with currencies not supported by ECB API
    - Rationale: Validates graceful handling of unsupported options

14. **Performance Testing: Multiple Simultaneous Requests**
    - Description: Load test with many users requesting exchange rates
    - Rationale: Ensures scalability under production load

15. **Compliance Testing: Exchange Rate Accuracy**
    - Description: Compare rates with official ECB rates at same timestamp
    - Rationale: Financial accuracy is critical for trust and compliance

## Detailed Test Cases

### TC-001: Select Non-Default Currency and Complete Payment
- **Priority**: High
- **Preconditions**:
  - User is logged in
  - User has sufficient balance/payment method
  - ECB API is accessible
- **Test Steps**:
  1. Navigate to payment page
  2. Click on currency selector
  3. Select "USD" from available currencies
  4. Enter payment amount (e.g., 100 USD)
  5. Review the EUR equivalent amount displayed
  6. Click "Pay" button
  7. Complete payment authorization
  8. Check transaction confirmation
- **Test Data**:
  - Currency: USD
  - Amount: 100.00 USD
- **Expected Results**:
  - Currency selector displays available currencies
  - EUR equivalent is calculated and displayed correctly
  - Payment processes successfully
  - Confirmation shows both USD and EUR amounts
  - Email receipt contains both currencies
- **Acceptance Criteria**:
  - Transaction recorded in database with both currencies
  - Exchange rate used is within 1 minute of payment time
  - Both amounts visible to user

### TC-002: ECB API Unavailable - Fallback Behavior
- **Priority**: High
- **Preconditions**:
  - User is logged in
  - ECB API is down/unreachable (simulate via network blocking)
- **Test Steps**:
  1. Block access to ECB API endpoint
  2. Navigate to payment page
  3. Attempt to select a non-default currency
  4. Observe system behavior
  5. Check error message displayed
  6. Verify user can still pay in default currency (EUR)
- **Test Data**:
  - Simulated API failure
- **Expected Results**:
  - System displays clear error message
  - User informed about currency limitation
  - Default currency (EUR) remains available
  - Payment can proceed in EUR
  - Error logged for monitoring
- **Acceptance Criteria**:
  - No system crash or unhandled exception
  - User not blocked from making payment
  - Clear communication about limitation

### TC-003: Exchange Rate Calculation Accuracy
- **Priority**: High
- **Preconditions**:
  - User is logged in
  - ECB API is accessible
- **Test Steps**:
  1. Note current EUR/USD rate from ECB API directly
  2. Navigate to payment page
  3. Select USD as currency
  4. Enter 100 USD as amount
  5. Observe calculated EUR amount
  6. Manually calculate expected EUR using ECB rate
  7. Compare system calculation with manual calculation
- **Test Data**:
  - Amount: 100 USD
  - Current EUR/USD rate from ECB
- **Expected Results**:
  - System calculation matches manual calculation
  - Calculation accurate to 2 decimal places
  - Rate timestamp shown to user
- **Acceptance Criteria**:
  - Difference is less than 0.01 EUR
  - Calculation follows standard rounding rules

### TC-004: Currency Precision for Different Currencies
- **Priority**: Medium
- **Preconditions**:
  - User is logged in
  - Multiple currencies available
- **Test Steps**:
  1. Test with JPY (0 decimal places): Enter 1000 JPY
  2. Verify EUR equivalent displayed correctly
  3. Test with BHD (3 decimal places): Enter 10.500 BHD
  4. Verify EUR equivalent displayed correctly
  5. Test with USD (2 decimal places): Enter 10.50 USD
  6. Verify EUR equivalent displayed correctly
- **Test Data**:
  - 1000 JPY, 10.500 BHD, 10.50 USD
- **Expected Results**:
  - Each currency displays with correct decimal places
  - Conversions maintain proper precision
  - No rounding errors visible
- **Acceptance Criteria**:
  - JPY shows 0 decimals
  - BHD shows 3 decimals
  - USD shows 2 decimals

### TC-005: Concurrent Payment with Rate Change
- **Priority**: Medium
- **Preconditions**:
  - User is logged in
  - Payment in progress
- **Test Steps**:
  1. Start payment in USD
  2. Note exchange rate shown
  3. Pause before confirming payment
  4. Wait for exchange rate to potentially change (or simulate)
  5. Complete payment
  6. Verify which rate was applied
  7. Check database for stored rate
- **Test Data**:
  - Initial rate: e.g., 1 USD = 0.85 EUR
  - Changed rate: e.g., 1 USD = 0.86 EUR
- **Expected Results**:
  - Rate locked at time of selection, not confirmation
  - OR rate updated with clear notification to user
  - Database stores the actual applied rate
  - User not charged incorrectly
- **Acceptance Criteria**:
  - Rate handling is consistent
  - User is aware of rate changes if applicable
  - No financial discrepancies

### TC-006: Email Receipt Contains Both Currencies
- **Priority**: High
- **Preconditions**:
  - User is logged in with valid email
  - User completes payment in non-default currency
- **Test Steps**:
  1. Complete payment of 50 USD
  2. Wait for email receipt
  3. Open email
  4. Verify USD amount is shown
  5. Verify EUR amount is shown
  6. Verify exchange rate is mentioned
  7. Verify timestamp of transaction
- **Test Data**:
  - Payment: 50 USD
  - Expected EUR equivalent
- **Expected Results**:
  - Email contains: "50.00 USD (42.50 EUR)"
  - Exchange rate displayed
  - Timestamp included
  - Email formatted correctly
- **Acceptance Criteria**:
  - Both amounts are clearly visible
  - Format is user-friendly
  - Information is accurate

### TC-007: Invalid Currency Code Handling
- **Priority**: Medium
- **Preconditions**:
  - API testing tool available
- **Test Steps**:
  1. Use API testing tool to send payment request
  2. Include invalid currency code (e.g., "XXX")
  3. Submit request
  4. Observe API response
  5. Check error message
  6. Verify payment not processed
- **Test Data**:
  - Currency: "XXX" (invalid)
  - Amount: 100
- **Expected Results**:
  - API returns 400 Bad Request
  - Error message: "Invalid currency code"
  - No payment record created
  - No charge processed
- **Acceptance Criteria**:
  - Input validation prevents invalid currencies
  - Clear error messaging
  - Security: no system exposure

### TC-008: Currency Selector UI Elements
- **Priority**: Low
- **Preconditions**:
  - User is on payment page
- **Test Steps**:
  1. Locate currency selector
  2. Click to open dropdown
  3. Verify list of currencies displayed
  4. Check for search/filter functionality
  5. Verify currency codes and names shown
  6. Test keyboard navigation
  7. Select a currency
  8. Verify selector updates
- **Test Data**:
  - Available currencies: EUR, USD, GBP, JPY, etc.
- **Expected Results**:
  - Selector is easy to find
  - Dropdown shows all available currencies
  - Search works if present
  - Keyboard accessible
  - Selection updates immediately
- **Acceptance Criteria**:
  - Meets accessibility standards
  - Intuitive user experience
  - No UI bugs

## Additional Notes

**Recommendations:**
1. Implement exchange rate caching with 5-10 minute TTL
2. Add monitoring alerts for ECB API failures
3. Consider fallback to secondary exchange rate provider
4. Add admin panel to view currency-related metrics
5. Document exchange rate update frequency

**Risks:**
- ECB API has no SLA guarantees
- Exchange rates can be volatile
- Currency list may need updates for new currencies

**Test Data Needed:**
- Test accounts with different default currencies
- Access to staging ECB API or mock
- Test payment methods for various currencies

**Dependencies:**
- ECB API availability
- Database migration must complete first
- Email service must be updated
```

## Summary

The tool provides:
1. **Automated data gathering** from Jira, GitLab, Confluence
2. **Structured prompt** with all context
3. **Claude's comprehensive analysis** with actionable test cases

Total time saved: **2-3 hours per ticket** of manual research and test case writing!
