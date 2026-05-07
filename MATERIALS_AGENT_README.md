# ALDOT Materials Control & Approval Agent

An intelligent agent that automates the material certification approval process for Alabama Department of Transportation construction projects. This agent validates material test results against Section 106 specifications and generates official approval documentation.

## Overview

This agent extends your existing ALDOT RAG Q&A demo by adding **action-oriented capabilities**. Instead of just answering questions about material requirements, the agent can:

- ✅ Process material certifications automatically
- ✅ Validate test results against specifications
- ✅ Make approval decisions (APPROVED/CONDITIONAL/REJECTED)
- ✅ Generate official approval letters
- ✅ Update project materials databases
- ✅ Create rejection notices with corrective actions

## Architecture

```
User Request
     ↓
Materials Approval Agent
     ↓
┌────────────────────────────────────────┐
│  1. parse_material_certification       │ → Extract test data
│  2. lookup_material_specifications     │ → Get Section 106 requirements
│  3. validate_test_results              │ → Compare against specs
│  4. check_vendor_qualifications        │ → Verify vendor status
│  5. calculate_approval_decision        │ → Make approval decision
│  6. generate_approval_letter           │ → Create documentation
│  7. update_approved_materials_list     │ → Update database
│  8. generate_rejection_notice          │ → Create rejection docs
└────────────────────────────────────────┘
     ↓
Formatted Approval/Rejection Documentation
```

## Components

### Tools (8 total)

| Tool | Purpose |
|------|---------|
| `parse_material_certification` | Extracts test data from certification documents |
| `lookup_material_specifications` | Retrieves Section 106 requirements for material type |
| `validate_test_results` | Compares test results against specification limits |
| `check_vendor_qualifications` | Verifies vendor approval status and qualifications |
| `calculate_approval_decision` | Determines APPROVED/CONDITIONAL/REJECTED status |
| `generate_approval_letter` | Creates formatted approval documentation |
| `update_approved_materials_list` | Adds approved materials to project database |
| `generate_rejection_notice` | Creates rejection notice with corrective actions |

### Mock Data

The implementation includes realistic mock data for:

- **5 Material Certifications** (approve, conditional, reject scenarios)
- **5 Approved Vendors** with qualification details
- **3 Material Types** with Section 106 specifications:
  - Portland Cement Type II (AASHTO M 85)
  - Coarse Aggregate #57 (AASHTO M 80)
  - Asphalt Binder PG 67-22 (AASHTO M 320)
- **5 Active Projects** for tracking approved materials

## Installation

### Prerequisites

```bash
pip install ibm-watsonx-orchestrate>=2.0.0
```

### Deployment

1. Navigate to the ALDOTDemo directory:
```bash
cd ALDOTDemo
```

2. Run the deployment script:
```bash
./deploy_materials_agent.sh
```

The script will:
- Import all 8 tools to watsonx Orchestrate
- Import the materials_approval_agent
- Verify successful deployment

## Demo Scenarios

### Scenario 1: Full Approval ✅

**User Input:**
```
Process certification CERT-2024-001 from ABC Materials Supply
```

**Expected Flow:**
1. Agent parses certification → Portland Cement Type II
2. Looks up Section 106 specs → AASHTO M 85 requirements
3. Validates all test results:
   - ✓ Fineness: 3450 cm²/g (passes ≥3300)
   - ✓ Strength: 3200 psi (passes ≥2800)
   - ✓ Sulfate: 2.5% (passes ≤3.0%)
   - ✓ Air Content: 6.0% (passes 4-7% range)
4. Checks vendor → ABC Materials approved and qualified
5. Calculates decision → **APPROVED**
6. Generates approval letter with 1-year validity
7. Updates I-85-2024 project materials list

**Result:**
```
✅ MATERIAL APPROVED
Approval Number: MAT-I852024-20240329-1234
All tests passed. Material approved for use on Project I-85-2024.
Approval valid until: 2025-03-29
```

### Scenario 2: Conditional Approval ⚠️

**User Input:**
```
Review certification CERT-2024-002 for XYZ Concrete Co
```

**Expected Flow:**
1. Agent parses certification → Portland Cement Type II
2. Looks up specifications
3. Validates test results:
   - ✗ Fineness: 3150 cm²/g (fails - below 3300 minimum)
   - ✓ Strength: 3400 psi (passes)
   - ✓ Sulfate: 2.8% (passes)
   - ✓ Air Content: 5.5% (passes)
4. Checks vendor → XYZ Concrete approved and qualified
5. Calculates decision → **CONDITIONAL** (single failure)
6. Generates conditional approval letter
7. Updates SR-280-2024 with conditional status

**Result:**
```
⚠️ CONDITIONAL APPROVAL
Approval Number: MAT-SR2802024-20240329-5678

CONDITION: Retest Fineness within 30 days
- Current: 3150 cm²/g
- Required: ≥3300 cm²/g
- Deficiency: 150 cm²/g below minimum

All other tests passed. Conditional approval valid for 30 days.
```

### Scenario 3: Rejection ❌

**User Input:**
```
Process CERT-2024-005 from Rejected Materials Inc
```

**Expected Flow:**
1. Agent parses certification → Portland Cement Type II
2. Looks up specifications
3. Validates test results:
   - ✗ Fineness: 3050 cm²/g (fails)
   - ✗ Strength: 2600 psi (fails)
   - ✗ Sulfate: 3.5% (fails)
   - ✗ Air Content: 8.5% (fails)
4. Checks vendor → Conditional status with quality issues
5. Calculates decision → **REJECTED** (multiple failures)
6. Generates rejection notice with corrective actions

**Result:**
```
❌ MATERIAL REJECTED
Rejection ID: REJ-20240329-9012

DEFICIENCIES (4):
1. Fineness: 3050 cm²/g - 250 cm²/g below minimum
2. Compressive Strength: 2600 psi - 200 psi below minimum
3. Sulfate Resistance: 3.5% - 0.5% above maximum
4. Air Content: 8.5% - Outside 4-7% range

REQUIRED ACTIONS:
- Address all deficiencies
- Retest at approved laboratory
- Submit new certification with compliant results
```

### Scenario 4: Information Query (RAG Only)

**User Input:**
```
What are the requirements for Portland Cement Type II?
```

**Expected Flow:**
1. Agent queries RAG knowledge base (Section 106)
2. Returns specification information
3. No tool calls needed (information only)

**Result:**
```
Portland Cement Type II requirements per Section 106.02:

Standard: AASHTO M 85

Requirements:
- Fineness (Blaine): ≥3300 cm²/g
- Compressive Strength (7-day): ≥2800 psi
- Sulfate Resistance (SO₃): ≤3.0%
- Air Content: 4-7%

Sampling: One test per 100 tons or fraction thereof
```

## Available Test Certifications

Use these certification IDs for testing:

| Cert ID | Material | Vendor | Expected Result |
|---------|----------|--------|-----------------|
| CERT-2024-001 | Portland Cement Type II | ABC Materials Supply | ✅ APPROVED |
| CERT-2024-002 | Portland Cement Type II | XYZ Concrete Co | ⚠️ CONDITIONAL |
| CERT-2024-003 | Coarse Aggregate #57 | Quality Aggregates Inc | ✅ APPROVED |
| CERT-2024-004 | Asphalt Binder PG 67-22 | Southern Asphalt Corp | ✅ APPROVED |
| CERT-2024-005 | Portland Cement Type II | Rejected Materials Inc | ❌ REJECTED |

## Integration with CAMMS UI

To integrate with your existing CAMMS interface:

1. **Update Agent Configuration** in `index.html`:
```javascript
window.wxOConfiguration = {
    orchestrationID: "your-orchestration-id",
    hostURL: "your-host-url",
    rootElementID: "root",
    chatOptions: {
        agentId: "materials_approval_agent_id",  // Use your deployed agent ID
        agentEnvironmentId: "your-environment-id"
    }
};
```

2. **Add Materials Section** to the info cards:
```html
<div class="info-card">
    <div class="info-card-icon">📋</div>
    <div class="info-card-body">
        <h4>Material Approvals</h4>
        <p>Process certifications, validate test results, and generate approval documentation</p>
    </div>
</div>
```

3. **Update Assistant Banner**:
```html
<div class="assistant-banner">
    <strong>AI Assistant Active</strong> — Ask about CAMMS tasks, material requirements, 
    or say "Process certification CERT-2024-001" to approve materials automatically.
</div>
```

## File Structure

```
ALDOTDemo/
├── agents/
│   └── materials_approval_agent.yaml      # Agent configuration
├── tools/
│   ├── materials_tools.py                 # 8 tool implementations
│   ├── mock_data.py                       # Sample certifications and specs
│   └── requirements.txt                   # Python dependencies
├── deploy_materials_agent.sh              # Deployment script
└── MATERIALS_AGENT_README.md              # This file
```

## Key Features

### 1. Multi-Step Validation
The agent orchestrates 6-8 tool calls per certification, demonstrating complex workflow automation.

### 2. Intelligent Decision Making
Uses business logic to determine:
- Full approval (all tests pass)
- Conditional approval (single failure, retest allowed)
- Rejection (multiple failures or vendor issues)

### 3. Professional Documentation
Generates formatted approval letters and rejection notices with:
- Specific test values and requirements
- Pass/fail indicators with margins
- Corrective actions for failures
- Section 106 and AASHTO standard references

### 4. Database Integration
Simulates updating project materials databases and sending notifications to project teams.

### 5. Vendor Management
Tracks vendor qualifications, certification expiration, and performance ratings.

## Extending the Agent

### Adding New Material Types

1. Add specifications to `mock_data.py`:
```python
MATERIAL_SPECS["New Material Type"] = {
    "standard": "AASHTO M XX",
    "section": "Section 106.XX",
    "requirements": {
        "parameter1_min": value,
        "parameter2_max": value
    }
}
```

2. Add validation logic to `validate_test_results()` in `materials_tools.py`

3. Add sample certifications to `MOCK_CERTIFICATIONS`

### Connecting to Real Systems

Replace mock data with actual API calls:

1. **Document Parsing**: Integrate OCR/PDF parsing service
2. **Database**: Connect to project management database
3. **Notifications**: Add email/SMS notification service
4. **PDF Generation**: Use ReportLab or similar for actual PDFs

## Troubleshooting

### Tools Not Found
```bash
# Verify tools are in correct location
ls -la ALDOTDemo/tools/materials_tools.py

# Reinstall if needed
cd ALDOTDemo/tools
wxo tool import materials_tools.py
```

### Agent Import Failed
```bash
# Check YAML syntax
cat agents/materials_approval_agent.yaml

# Verify tools are imported first
wxo tool list | grep material
```

### Mock Data Issues
```bash
# Test tools locally
cd ALDOTDemo/tools
python3 -c "from materials_tools import parse_material_certification; print(parse_material_certification('CERT-2024-001'))"
```

## Support

For questions or issues:
- Review the demo scenarios above
- Check the deployment script output
- Verify all files are in correct locations
- Ensure watsonx Orchestrate CLI is properly configured

## Next Steps

1. ✅ Deploy the agent using `./deploy_materials_agent.sh`
2. ✅ Test with the 3 demo scenarios
3. ✅ Integrate with your CAMMS UI
4. ✅ Customize for additional material types
5. ✅ Connect to real systems (optional)

---

**Built with IBM watsonx Orchestrate** | Demonstrates action-oriented AI agents with tool orchestration