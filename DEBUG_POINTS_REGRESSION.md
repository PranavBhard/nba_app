# Debugging Points Regression Discrepancy

## Issue
UI workflow returns negative R² values and different metrics than agent workflow for the same configuration.

## Root Cause Analysis

### Problem 1: Time-Based Calibration Not Enabled
When `use_time_based_split = False`, the code evaluates on the **full dataset** (including training data), which causes:
- Negative R² values (model evaluated on data it was trained on)
- Different metrics than evaluation set

### Problem 2: Evaluation Bug (Fixed)
When time-based calibration IS enabled, the retrained model wasn't being re-evaluated on the evaluation set. This has been fixed.

## Debugging Steps

### 1. Check Browser Console
When you click "Train Model", check the browser console for:
```javascript
Form state: { checkboxChecked: true/false, beginYear: ..., calibrationYears: ..., evaluationYear: ... }
Training config being sent: { use_time_calibration: true/false, ... }
```

### 2. Check Server Logs
Look for these log messages in the Flask server output:
```
Training configuration:
  use_time_calibration: True/False (type: ...)
  calibration_years: [2023] (type: ...)
  evaluation_year: 2024 (type: ...)
  
Split strategy determination:
  use_time_calibration parameter: True/False
  use_time_based_split: True/False
```

### 3. Verify Checkbox State
- **Before training**: Ensure the "Use Time-Based Calibration" checkbox is **checked**
- The checkbox should be automatically checked if you loaded a saved config that has `use_time_calibration: true`
- If checkbox is unchecked, time-based calibration will be disabled even if year fields are filled

### 4. Verify Year Fields
Ensure these fields are filled:
- **Begin Year**: e.g., `2012`
- **Calibration Years**: e.g., `2023` (comma-separated if multiple)
- **Evaluation Year**: e.g., `2024`

### 5. Expected Behavior

#### When Time-Based Calibration is ENABLED:
- Logs show: `Time-based calibration splits: Train set: X games, Calibration set: Y games, Evaluation set: Z games`
- Metrics are computed on **evaluation set only**
- Positive R² values (typically)

#### When Time-Based Calibration is DISABLED:
- Logs show: `Time-based split is DISABLED. This will use TimeSeriesSplit CV and evaluate on full dataset`
- Metrics are computed on **full dataset** (including training data)
- **Negative R² values are expected** in this case

## What to Check

1. **Is the checkbox checked?** 
   - Open browser console and check the `Form state` log
   - Verify `checkboxChecked: true`

2. **Are values being sent correctly?**
   - Check `Training config being sent` log in console
   - Verify `use_time_calibration: true` and year fields are not null

3. **What does the server receive?**
   - Check server logs for `Training configuration:` output
   - Verify `use_time_calibration: True` (boolean, not string)

4. **Is time-based split being used?**
   - Check server logs for `Split strategy determination:`
   - Verify `use_time_based_split: True`

5. **What dataset is being evaluated?**
   - If time-based: Should show evaluation set size (much smaller than full dataset)
   - If not time-based: Will evaluate on full dataset (15,836 samples)

## Fix Summary

1. ✅ Fixed evaluation bug: Retrained model is now re-evaluated on evaluation set
2. ✅ Added comprehensive logging at both frontend and backend
3. ⚠️  **Action Required**: Verify checkbox is checked and year fields are filled before training

## Next Steps

1. Run a training job through the UI
2. Check browser console logs
3. Check server logs
4. Share the logs if issue persists
