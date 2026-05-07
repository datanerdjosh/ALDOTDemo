# Materials Approval Agent - Quick Start Guide

Get your Materials Control & Approval Agent up and running in 5 minutes.

## Prerequisites

✅ IBM watsonx Orchestrate environment access  
✅ Python 3.8+ installed  
✅ watsonx Orchestrate CLI installed

## Step 1: Install Dependencies (1 minute)

```bash
pip install ibm-watsonx-orchestrate>=2.0.0
```

## Step 2: Deploy the Agent (2 minutes)

```bash
cd ALDOTDemo
./deploy_materials_agent.sh
```

Expected output:
```
✓ wxo CLI found
✓ Directory structure verified
✓ Tools imported successfully
✓ Agent imported successfully
✅ Deployment Complete!
```

## Step 3: Test the Agent (2 minutes)

Open watsonx Orchestrate UI and try these commands:

### Test 1: Full Approval ✅
```
Process certification CERT-2024-001 from ABC Materials Supply
```

**Expected Result:** Material approved with all tests passing

### Test 2: Conditional Approval ⚠️
```
Review certification CERT-2024-002
```

**Expected Result:** Conditional approval requiring fineness retest

### Test 3: Rejection ❌
```
Process CERT-2024-005
```

**Expected Result:** Material rejected with multiple deficiencies

## What You Should See

The agent will:
1. ✅ Parse the certification
2. ✅ Look up Section 106 specifications
3. ✅ Validate all test results
4. ✅ Check vendor qualifications
5. ✅ Make approval decision
6. ✅ Generate formatted documentation
7. ✅ Update materials database

## Demo Flow Example

**You:** "Process certification CERT-2024-001"

**Agent:** 
```
I'll process certification CERT-2024-001 for you.

[Parsing certification...]
✓ Material: Portland Cement Type II
✓ Vendor: ABC Materials Supply
✓ Project: I-85-2024

[Looking up specifications...]
✓ Standard: AASHTO M 85
✓ Section: 106.02 - Portland Cement

[Validating test results...]
✓ Fineness: 3450 cm²/g (PASS - exceeds 3300 minimum)
✓ Compressive Strength: 3200 psi (PASS - exceeds 2800 minimum)
✓ Sulfate Resistance: 2.5% (PASS - below 3.0% maximum)
✓ Air Content: 6.0% (PASS - within 4-7% range)

[Checking vendor...]
✓ ABC Materials Supply - APPROVED vendor
✓ Qualified for Portland Cement Type II
✓ Certification valid until 2025-12-31

[Generating approval...]
✅ MATERIAL APPROVED

Approval Number: MAT-I852024-20240429-1234
Approval Date: April 29, 2024
Valid Until: April 29, 2025

All tests passed specification requirements.
Material approved for use on Project I-85-2024.

Approval letter generated and added to project materials database.
Notifications sent to project engineer and materials lab.
```

## Available Test Certifications

| Cert ID | Result | Use Case |
|---------|--------|----------|
| CERT-2024-001 | ✅ Approved | Show full approval workflow |
| CERT-2024-002 | ⚠️ Conditional | Show single failure handling |
| CERT-2024-003 | ✅ Approved | Show aggregate approval |
| CERT-2024-004 | ✅ Approved | Show asphalt approval |
| CERT-2024-005 | ❌ Rejected | Show multiple failures |

## Troubleshooting

### "wxo CLI not found"
```bash
pip install ibm-watsonx-orchestrate
```

### "Tools import failed"
```bash
cd ALDOTDemo/tools
wxo tool import materials_tools.py
```

### "Agent not responding"
1. Verify agent is deployed: `wxo agent list`
2. Check agent ID in watsonx Orchestrate UI
3. Ensure tools are imported before agent

## Next Steps

1. ✅ **Integrate with CAMMS UI** - See MATERIALS_AGENT_README.md
2. ✅ **Add more material types** - Edit mock_data.py
3. ✅ **Connect to real systems** - Replace mock functions
4. ✅ **Customize approval logic** - Modify calculate_approval_decision()

## Key Files

```
ALDOTDemo/
├── tools/
│   ├── materials_tools.py      # 8 tool implementations
│   └── mock_data.py            # Sample data
├── agents/
│   └── materials_approval_agent.yaml
├── deploy_materials_agent.sh   # Run this to deploy
├── MATERIALS_AGENT_README.md   # Full documentation
└── QUICK_START.md             # This file
```

## Support

- 📖 Full docs: `MATERIALS_AGENT_README.md`
- 🔧 Deployment: `./deploy_materials_agent.sh`
- 💬 Test scenarios: See MATERIALS_AGENT_README.md

---

**Ready to demo!** Your Materials Approval Agent is now processing certifications automatically. 🚀