# watsonx Orchestrate ADK Deployment Guide

This guide explains how to deploy the Materials Approval Agent to your IBM Cloud watsonx Orchestrate environment using the Agent Development Kit (ADK).

## Prerequisites

### 1. Install the ADK

```bash
pip install ibm-watsonx-orchestrate>=2.0.0
```

### 2. Configure Authentication

Create a `.env` file in the `ALDOTDemo` directory with your watsonx Orchestrate credentials:

```bash
# .env file
WXO_URL=https://your-instance.watson-orchestrate.cloud.ibm.com
WXO_API_KEY=your-api-key-here
```

Or set environment variables:

```bash
export WXO_URL="https://your-instance.watson-orchestrate.cloud.ibm.com"
export WXO_API_KEY="your-api-key-here"
```

### 3. Verify ADK Installation

```bash
orchestrate --version
```

## Deployment Steps

### Option 1: Automated Deployment (Recommended)

Run the deployment script from the `ALDOTDemo` directory:

```bash
cd ALDOTDemo
./deploy_materials_agent.sh
```

This will:
1. Import all 8 Python tools from `materials_tools.py`
2. Import the `materials_approval_agent` from YAML
3. Verify successful deployment

### Option 2: Manual Deployment

#### Step 1: Import Tools

```bash
cd ALDOTDemo
orchestrate tools import \
    -k python \
    -p tools \
    -f tools/materials_tools.py \
    -r tools/requirements.txt
```

This imports all 8 tools from the materials_tools.py file along with the mock_data.py dependency:
- `parse_material_certification`
- `lookup_material_specifications`
- `validate_test_results`
- `check_vendor_qualifications`
- `calculate_approval_decision`
- `generate_approval_letter`
- `update_approved_materials_list`
- `generate_rejection_notice`

#### Step 2: Verify Tools

```bash
orchestrate tools list
```

You should see all 8 materials tools listed.

#### Step 3: Import Agent

```bash
cd ALDOTDemo
orchestrate agents import agents/materials_approval_agent.yaml
```

#### Step 4: Verify Agent

```bash
orchestrate agents list
```

You should see `materials_approval_agent` in the list.

## Verification

### 1. List Deployed Components

```bash
# List all tools
orchestrate tools list

# List all agents
orchestrate agents list

# Get detailed info about the agent
orchestrate agents get materials_approval_agent
```

### 2. Test in watsonx Orchestrate UI

1. Log into your watsonx Orchestrate instance
2. Navigate to **Manage Agents**
3. Find **materials_approval_agent**
4. Click **Test** or **Chat**
5. Try a test query:
   ```
   Process certification CERT-2024-001 from ABC Materials Supply
   ```

## Understanding the ADK Tool Format

The tools use the `@tool()` decorator from the ADK:

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool()
def parse_material_certification(cert_id: str) -> Dict[str, Any]:
    """
    Parse material certification document and extract test data.
    
    Args:
        cert_id: Certification ID (e.g., "CERT-2024-001")
    
    Returns:
        Dictionary containing certification data or error
    """
    # Tool implementation
    return result
```

Key points:
- **`@tool()` decorator**: Marks the function as a watsonx Orchestrate tool
- **Type hints**: Required for input/output schema generation
- **Google-style docstrings**: Used to generate tool descriptions
- **Return types**: Must be JSON-serializable (Dict, List, str, int, etc.)

## Agent Configuration

The agent is defined in `agents/materials_approval_agent.yaml`:

```yaml
name: materials_approval_agent
description: |
  Processes material certifications for ALDOT construction projects...

model: groq/openai/gpt-oss-120b
style: react

system_prompt: |
  You are a Materials Approval Specialist...

tools:
  - parse_material_certification
  - lookup_material_specifications
  - validate_test_results
  - check_vendor_qualifications
  - calculate_approval_decision
  - generate_approval_letter
  - update_approved_materials_list
  - generate_rejection_notice
```

## Troubleshooting

### Issue: "orchestrate command not found"

**Solution:**
```bash
pip install --upgrade ibm-watsonx-orchestrate
```

### Issue: "Authentication failed"

**Solution:**
1. Verify your `.env` file or environment variables
2. Check that `WXO_URL` and `WXO_API_KEY` are correct
3. Ensure your API key has proper permissions

### Issue: "Tool import failed"

**Solution:**
1. Verify all tools have the `@tool()` decorator
2. Check that type hints are present on all parameters
3. Ensure docstrings follow Google style format
4. Verify `ibm-watsonx-orchestrate` is installed:
   ```bash
   pip show ibm-watsonx-orchestrate
   ```

### Issue: "Module 'mock_data' not found"

**Solution:**
The `mock_data.py` file must be in the same directory as `materials_tools.py`. Verify:
```bash
ls ALDOTDemo/tools/
# Should show: materials_tools.py, mock_data.py, requirements.txt
```

### Issue: "Agent import failed - tools not found"

**Solution:**
Tools must be imported **before** the agent. Run:
```bash
cd ALDOTDemo/tools
orchestrate tools import materials_tools.py
cd ..
orchestrate agents import agents/materials_approval_agent.yaml
```

## Updating the Agent

### Update Tools

```bash
cd ALDOTDemo/tools
orchestrate tools import materials_tools.py --force
```

The `--force` flag overwrites existing tools.

### Update Agent

```bash
cd ALDOTDemo
orchestrate agents import agents/materials_approval_agent.yaml --force
```

## Deleting Components

### Delete Tools

```bash
orchestrate tools delete parse_material_certification
orchestrate tools delete lookup_material_specifications
# ... repeat for all 8 tools
```

### Delete Agent

```bash
orchestrate agents delete materials_approval_agent
```

## Integration with CAMMS UI

After deployment, update your `index.html` to use the deployed agent:

```javascript
window.wxOConfiguration = {
    orchestrationID: "your-orchestration-id",
    hostURL: "https://your-instance.watson-orchestrate.cloud.ibm.com",
    rootElementID: "root",
    chatOptions: {
        agentId: "materials_approval_agent",  // Use the deployed agent name
        agentEnvironmentId: "your-environment-id"
    }
};
```

## Production Considerations

### 1. Environment Management

Use separate environments for development and production:

```bash
# Development
export WXO_URL="https://dev.watson-orchestrate.cloud.ibm.com"

# Production
export WXO_URL="https://prod.watson-orchestrate.cloud.ibm.com"
```

### 2. Version Control

Tag your deployments:

```bash
git tag -a v1.0.0 -m "Initial Materials Approval Agent deployment"
git push origin v1.0.0
```

### 3. Testing

Always test in a development environment before deploying to production:

```bash
# Deploy to dev
WXO_URL="https://dev..." ./deploy_materials_agent.sh

# Test thoroughly

# Deploy to prod
WXO_URL="https://prod..." ./deploy_materials_agent.sh
```

### 4. Monitoring

Monitor agent performance in the watsonx Orchestrate dashboard:
- Tool execution times
- Success/failure rates
- User interactions
- Error logs

## Next Steps

1. ✅ Deploy the agent using this guide
2. ✅ Test with the demo scenarios in `MATERIALS_AGENT_README.md`
3. ✅ Integrate with your CAMMS UI
4. ✅ Monitor usage and performance
5. ✅ Iterate based on user feedback

## Support Resources

- **ADK Documentation**: https://developer.watson-orchestrate.ibm.com
- **Full README**: `MATERIALS_AGENT_README.md`
- **Quick Start**: `QUICK_START.md`
- **Demo Scenarios**: See MATERIALS_AGENT_README.md

---

**Ready to deploy!** Follow the steps above to get your Materials Approval Agent running in watsonx Orchestrate.