#!/bin/bash

# Deploy Materials Approval Agent to watsonx Orchestrate using ADK
# This script imports the agent and all its tools

set -e  # Exit on error

echo "=========================================="
echo "ALDOT Materials Approval Agent Deployment"
echo "=========================================="
echo ""

# Check if orchestrate CLI is available
if ! command -v orchestrate &> /dev/null; then
    echo "❌ Error: orchestrate CLI not found"
    echo "Please install: pip install ibm-watsonx-orchestrate"
    exit 1
fi

echo "✓ orchestrate CLI found"
echo ""

# Check if we're in the right directory
if [ ! -d "tools" ] || [ ! -d "agents" ]; then
    echo "❌ Error: Must run from ALDOTDemo directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "✓ Directory structure verified"
echo ""

# Step 1: Import tools
echo "Step 1: Importing materials tools..."
echo "────────────────────────────────────────"

if [ ! -f "tools/materials_tools.py" ]; then
    echo "❌ Error: materials_tools.py not found"
    exit 1
fi

if [ ! -f "tools/mock_data.py" ]; then
    echo "❌ Error: mock_data.py not found"
    exit 1
fi

echo "Importing 8 material approval tools from materials_tools.py..."
echo "Package includes: materials_tools.py, mock_data.py"
echo ""

orchestrate tools import \
    -k python \
    -p tools \
    -f tools/materials_tools.py \
    -r tools/requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Tools imported successfully"
else
    echo ""
    echo "❌ Tool import failed"
    exit 1
fi

echo ""

# Step 2: Import agent
echo "Step 2: Importing materials approval agent..."
echo "────────────────────────────────────────"

if [ ! -f "agents/materials_approval_agent.yaml" ]; then
    echo "❌ Error: materials_approval_agent.yaml not found"
    exit 1
fi

orchestrate agents import -f agents/materials_approval_agent.yaml

if [ $? -eq 0 ]; then
    echo "✓ Agent imported successfully"
else
    echo "❌ Agent import failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "The following components have been deployed:"
echo ""
echo "Tools (8):"
echo "  • parse_material_certification"
echo "  • lookup_material_specifications"
echo "  • validate_test_results"
echo "  • check_vendor_qualifications"
echo "  • calculate_approval_decision"
echo "  • generate_approval_letter"
echo "  • update_approved_materials_list"
echo "  • generate_rejection_notice"
echo ""
echo "Agent:"
echo "  • materials_approval_agent"
echo ""
echo "Verify deployment:"
echo "  orchestrate tools list"
echo "  orchestrate agents list"
echo ""
echo "Next Steps:"
echo "  1. Test the agent in watsonx Orchestrate UI"
echo "  2. Try demo scenarios from MATERIALS_AGENT_README.md"
echo "  3. Integrate with your existing CAMMS interface"
echo ""
echo "Demo Certification IDs to try:"
echo "  • CERT-2024-001 (Full Approval)"
echo "  • CERT-2024-002 (Conditional Approval)"
echo "  • CERT-2024-005 (Rejection)"
echo ""

# Made with Bob
