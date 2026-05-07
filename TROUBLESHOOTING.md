# Troubleshooting Guide - Materials Approval Agent

## Issue: CERT-2024-001 Shows Rejection Instead of Approval

### Problem
When asking "Process certification CERT-2024-001 from ABC Materials Supply", the agent shows a rejection instead of the expected approval.

### Root Cause
The tools may not have been re-imported after adding the `@tool()` decorators, or there may be a caching issue with the old tool versions.

### Solution: Re-import Tools

Run these commands to force re-import the tools:

```bash
cd ALDOTDemo

# Re-import tools with --force flag to overwrite existing
orchestrate tools import \
    -k python \
    -p tools \
    -f tools/materials_tools.py \
    -r tools/requirements.txt \
    --force

# Verify tools are imported
orchestrate tools list | grep material
```

### Verify Mock Data

The mock data for CERT-2024-001 should show:

```python
"CERT-2024-001": {
    "vendor": "ABC Materials Supply",
    "material_type": "Portland Cement Type II",
    "test_results": {
        "fineness": 3450,              # PASS (≥3300)
        "compressive_strength_7day": 3200,  # PASS (≥2800)
        "sulfate_resistance": 2.5,     # PASS (≤3.0)
        "air_content": 6.0             # PASS (4-7 range)
    }
}
```

All four tests should PASS, resulting in APPROVED status.

### Test Each Tool Individually

You can test the tools individually to verify they're working:

```bash
# Test parse_material_certification
orchestrate tools test parse_material_certification --input '{"cert_id": "CERT-2024-001"}'

# Test lookup_material_specifications
orchestrate tools test lookup_material_specifications --input '{"material_type": "Portland Cement Type II", "project_id": "I-85-2024"}'
```

### Check Agent Configuration

Verify the agent is using the correct tools:

```bash
orchestrate agents get materials_approval_agent
```

Should show all 8 tools listed.

### Alternative: Delete and Re-import Everything

If the issue persists, delete and re-import everything:

```bash
cd ALDOTDemo

# Delete existing tools (one by one)
orchestrate tools delete parse_material_certification
orchestrate tools delete lookup_material_specifications
orchestrate tools delete validate_test_results
orchestrate tools delete check_vendor_qualifications
orchestrate tools delete calculate_approval_decision
orchestrate tools delete generate_approval_letter
orchestrate tools delete update_approved_materials_list
orchestrate tools delete generate_rejection_notice

# Delete agent
orchestrate agents delete materials_approval_agent

# Re-import everything
./deploy_materials_agent.sh
```

## Other Common Issues

### Issue: "Tool not found" Error

**Solution:**
```bash
# List all tools to verify they're imported
orchestrate tools list

# If missing, re-import
cd ALDOTDemo
./deploy_materials_agent.sh
```

### Issue: Agent Not Responding

**Solution:**
1. Check agent status: `orchestrate agents list`
2. Verify agent exists: `orchestrate agents get materials_approval_agent`
3. Check watsonx Orchestrate UI for any error messages

### Issue: Incorrect Test Results

**Solution:**
1. Verify mock_data.py has correct values
2. Re-import tools with `--force` flag
3. Clear any browser cache
4. Try in a new chat session

### Issue: Tools Timing Out

**Solution:**
1. Check if the package size is too large
2. Verify requirements.txt only has necessary dependencies
3. Check watsonx Orchestrate logs for errors

## Verification Steps

After re-importing, test all three scenarios:

### 1. Test Full Approval (CERT-2024-001)
```
Process certification CERT-2024-001 from ABC Materials Supply
```
**Expected**: ✅ APPROVED with approval letter

### 2. Test Conditional (CERT-2024-002)
```
Review certification CERT-2024-002 for XYZ Concrete Co
```
**Expected**: ⚠️ CONDITIONAL with retest requirement

### 3. Test Rejection (CERT-2024-005)
```
Process CERT-2024-005 from Rejected Materials Inc
```
**Expected**: ❌ REJECTED with deficiency list

## Debug Mode

To see detailed tool execution:

1. In watsonx Orchestrate UI, enable "Show reasoning"
2. Watch the tool calls in real-time
3. Check which tools are being called and what they return

## Contact Support

If issues persist after trying these solutions:

1. Export agent logs from watsonx Orchestrate
2. Check tool execution history
3. Verify IBM Cloud watsonx Orchestrate service status
4. Contact IBM watsonx Orchestrate support with:
   - Agent name: materials_approval_agent
   - Tool names: All 8 materials tools
   - Error messages
   - Steps to reproduce

## Quick Fix Command

Run this single command to force re-import everything:

```bash
cd ALDOTDemo && \
orchestrate tools import -k python -p tools -f tools/materials_tools.py -r tools/requirements.txt --force && \
orchestrate agents import -f agents/materials_approval_agent.yaml --force && \
echo "✅ Re-import complete! Test with: Process certification CERT-2024-001 from ABC Materials Supply"