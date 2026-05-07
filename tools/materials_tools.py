"""
Materials Control & Approval Tools for ALDOT
Implements 8 tools for processing material certifications and generating approvals
"""

from datetime import datetime, timedelta
import random
import json
from typing import Dict, Any, List
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from mock_data import (
    MOCK_CERTIFICATIONS,
    APPROVED_VENDORS,
    MATERIAL_SPECS,
    PROJECTS
)


@tool()
def parse_material_certification(cert_id: str) -> Dict[str, Any]:
    """
    Parse material certification document and extract test data.
    
    Args:
        cert_id: Certification ID (e.g., "CERT-2024-001")
    
    Returns:
        Dictionary containing certification data or error
    """
    if cert_id in MOCK_CERTIFICATIONS:
        cert_data = MOCK_CERTIFICATIONS[cert_id]
        return {
            "success": True,
            "cert_id": cert_id,
            "vendor": cert_data["vendor"],
            "material_type": cert_data["material_type"],
            "project": cert_data["project"],
            "cert_number": cert_data["cert_number"],
            "test_date": cert_data["test_date"],
            "test_lab": cert_data["test_lab"],
            "test_results": cert_data["test_results"]
        }
    
    return {
        "success": False,
        "error": f"Certification {cert_id} not found in system",
        "available_certs": list(MOCK_CERTIFICATIONS.keys())
    }


@tool()
def lookup_material_specifications(material_type: str, project_id: str) -> Dict[str, Any]:
    """
    Lookup material specifications from Section 106.
    
    Args:
        material_type: Type of material (e.g., "Portland Cement Type II")
        project_id: Project identifier
    
    Returns:
        Dictionary containing specification requirements
    """
    if material_type in MATERIAL_SPECS:
        specs = MATERIAL_SPECS[material_type]
        project_info = PROJECTS.get(project_id, {})
        
        return {
            "success": True,
            "material_type": material_type,
            "project_id": project_id,
            "project_name": project_info.get("name", "Unknown Project"),
            "standard": specs["standard"],
            "section_reference": specs["section"],
            "requirements": specs["requirements"],
            "sampling_frequency": specs["sampling_frequency"],
            "acceptance_criteria": specs["acceptance_criteria"]
        }
    
    return {
        "success": False,
        "error": f"Material type '{material_type}' not found in specifications",
        "available_materials": list(MATERIAL_SPECS.keys())
    }


@tool()
def validate_test_results(
    test_results: Dict[str, Any],
    specifications: Dict[str, Any],
    material_type: str
) -> Dict[str, Any]:
    """
    Validate test results against specification requirements.
    
    Args:
        test_results: Dictionary of test measurements
        specifications: Specification requirements
        material_type: Type of material being tested
    
    Returns:
        Dictionary containing validation results with pass/fail for each parameter
    """
    validation = {
        "passed": [],
        "failed": [],
        "overall_status": "PASS"
    }
    
    specs = specifications.get("requirements", {})
    
    if material_type == "Portland Cement Type II":
        # Validate fineness
        fineness = test_results.get("fineness", 0)
        fineness_min = specs.get("fineness_min", 0)
        if fineness >= fineness_min:
            validation["passed"].append({
                "parameter": "Fineness (Blaine)",
                "value": f"{fineness} cm²/g",
                "requirement": f"≥ {fineness_min} cm²/g",
                "status": "PASS",
                "margin": f"+{fineness - fineness_min} cm²/g"
            })
        else:
            validation["failed"].append({
                "parameter": "Fineness (Blaine)",
                "value": f"{fineness} cm²/g",
                "requirement": f"≥ {fineness_min} cm²/g",
                "status": "FAIL",
                "variance": f"{((fineness - fineness_min) / fineness_min * 100):.1f}%",
                "deficiency": f"{fineness_min - fineness} cm²/g below minimum"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate compressive strength
        strength = test_results.get("compressive_strength_7day", 0)
        strength_min = specs.get("compressive_strength_7day_min", 0)
        if strength >= strength_min:
            validation["passed"].append({
                "parameter": "Compressive Strength (7-day)",
                "value": f"{strength} psi",
                "requirement": f"≥ {strength_min} psi",
                "status": "PASS",
                "margin": f"+{strength - strength_min} psi"
            })
        else:
            validation["failed"].append({
                "parameter": "Compressive Strength (7-day)",
                "value": f"{strength} psi",
                "requirement": f"≥ {strength_min} psi",
                "status": "FAIL",
                "deficiency": f"{strength_min - strength} psi below minimum"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate sulfate resistance
        sulfate = test_results.get("sulfate_resistance", 0)
        sulfate_max = specs.get("sulfate_resistance_max", 0)
        if sulfate <= sulfate_max:
            validation["passed"].append({
                "parameter": "Sulfate Resistance (SO₃)",
                "value": f"{sulfate}%",
                "requirement": f"≤ {sulfate_max}%",
                "status": "PASS",
                "margin": f"{sulfate_max - sulfate}% below maximum"
            })
        else:
            validation["failed"].append({
                "parameter": "Sulfate Resistance (SO₃)",
                "value": f"{sulfate}%",
                "requirement": f"≤ {sulfate_max}%",
                "status": "FAIL",
                "deficiency": f"{sulfate - sulfate_max}% above maximum"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate air content
        air_content = test_results.get("air_content", 0)
        air_range = specs.get("air_content_range", [0, 0])
        if air_range[0] <= air_content <= air_range[1]:
            validation["passed"].append({
                "parameter": "Air Content",
                "value": f"{air_content}%",
                "requirement": f"{air_range[0]}-{air_range[1]}%",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Air Content",
                "value": f"{air_content}%",
                "requirement": f"{air_range[0]}-{air_range[1]}%",
                "status": "FAIL",
                "deficiency": "Outside acceptable range"
            })
            validation["overall_status"] = "FAIL"
    
    elif material_type == "Coarse Aggregate #57":
        # Validate LA Abrasion
        la_abrasion = test_results.get("la_abrasion", 0)
        la_max = specs.get("la_abrasion_max", 0)
        if la_abrasion <= la_max:
            validation["passed"].append({
                "parameter": "LA Abrasion",
                "value": f"{la_abrasion}%",
                "requirement": f"≤ {la_max}%",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "LA Abrasion",
                "value": f"{la_abrasion}%",
                "requirement": f"≤ {la_max}%",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate soundness
        soundness = test_results.get("soundness", 0)
        soundness_max = specs.get("soundness_max", 0)
        if soundness <= soundness_max:
            validation["passed"].append({
                "parameter": "Soundness",
                "value": f"{soundness}% loss",
                "requirement": f"≤ {soundness_max}% loss",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Soundness",
                "value": f"{soundness}% loss",
                "requirement": f"≤ {soundness_max}% loss",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate deleterious materials
        deleterious = test_results.get("deleterious", 0)
        deleterious_max = specs.get("deleterious_max", 0)
        if deleterious <= deleterious_max:
            validation["passed"].append({
                "parameter": "Deleterious Materials",
                "value": f"{deleterious}%",
                "requirement": f"≤ {deleterious_max}%",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Deleterious Materials",
                "value": f"{deleterious}%",
                "requirement": f"≤ {deleterious_max}%",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate gradation
        gradation = test_results.get("gradation_pass", False)
        if gradation:
            validation["passed"].append({
                "parameter": "Gradation",
                "value": "Within limits",
                "requirement": "Must meet gradation curve",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Gradation",
                "value": "Outside limits",
                "requirement": "Must meet gradation curve",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
    
    elif material_type == "Asphalt Binder PG 67-22":
        # Validate viscosity
        viscosity = test_results.get("viscosity", 0)
        visc_range = specs.get("viscosity_range", [0, 0])
        if visc_range[0] <= viscosity <= visc_range[1]:
            validation["passed"].append({
                "parameter": "Viscosity",
                "value": f"{viscosity} Pa·s",
                "requirement": f"{visc_range[0]}-{visc_range[1]} Pa·s",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Viscosity",
                "value": f"{viscosity} Pa·s",
                "requirement": f"{visc_range[0]}-{visc_range[1]} Pa·s",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate penetration
        penetration = test_results.get("penetration", 0)
        pen_range = specs.get("penetration_range", [0, 0])
        if pen_range[0] <= penetration <= pen_range[1]:
            validation["passed"].append({
                "parameter": "Penetration",
                "value": f"{penetration} dmm",
                "requirement": f"{pen_range[0]}-{pen_range[1]} dmm",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Penetration",
                "value": f"{penetration} dmm",
                "requirement": f"{pen_range[0]}-{pen_range[1]} dmm",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate flash point
        flash_point = test_results.get("flash_point", 0)
        flash_min = specs.get("flash_point_min", 0)
        if flash_point >= flash_min:
            validation["passed"].append({
                "parameter": "Flash Point",
                "value": f"{flash_point}°C",
                "requirement": f"≥ {flash_min}°C",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Flash Point",
                "value": f"{flash_point}°C",
                "requirement": f"≥ {flash_min}°C",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
        
        # Validate ductility
        ductility = test_results.get("ductility", 0)
        duct_min = specs.get("ductility_min", 0)
        if ductility >= duct_min:
            validation["passed"].append({
                "parameter": "Ductility",
                "value": f"{ductility} cm",
                "requirement": f"≥ {duct_min} cm",
                "status": "PASS"
            })
        else:
            validation["failed"].append({
                "parameter": "Ductility",
                "value": f"{ductility} cm",
                "requirement": f"≥ {duct_min} cm",
                "status": "FAIL"
            })
            validation["overall_status"] = "FAIL"
    
    return {
        "success": True,
        "validation": validation,
        "total_tests": len(validation["passed"]) + len(validation["failed"]),
        "passed_count": len(validation["passed"]),
        "failed_count": len(validation["failed"])
    }


@tool()
def check_vendor_qualifications(vendor_name: str, material_type: str) -> Dict[str, Any]:
    """
    Check if vendor is approved and qualified for the material type.
    
    Args:
        vendor_name: Name of the vendor/supplier
        material_type: Type of material being supplied
    
    Returns:
        Dictionary containing vendor qualification status
    """
    if vendor_name in APPROVED_VENDORS:
        vendor = APPROVED_VENDORS[vendor_name]
        is_qualified = material_type in vendor["materials"]
        
        # Check if certification is expired
        cert_exp = datetime.strptime(vendor["cert_expiration"], "%Y-%m-%d")
        is_current = cert_exp > datetime.now()
        
        return {
            "success": True,
            "vendor_name": vendor_name,
            "vendor_id": vendor["vendor_id"],
            "status": vendor["status"],
            "qualified_for_material": is_qualified,
            "approved_materials": vendor["materials"],
            "cert_expiration": vendor["cert_expiration"],
            "cert_is_current": is_current,
            "performance_rating": vendor["performance_rating"],
            "years_approved": vendor["years_approved"],
            "contact": vendor["contact"],
            "notes": vendor.get("notes", "No special notes")
        }
    
    return {
        "success": False,
        "error": f"Vendor '{vendor_name}' not found in approved vendor list",
        "vendor_name": vendor_name,
        "status": "NOT APPROVED",
        "qualified_for_material": False,
        "available_vendors": list(APPROVED_VENDORS.keys())
    }


@tool()
def calculate_approval_decision(
    validation_results: Dict[str, Any],
    vendor_status: Dict[str, Any],
    material_type: str,
    project_id: str
) -> Dict[str, Any]:
    """
    Calculate final approval decision based on validation and vendor status.
    
    Args:
        validation_results: Test validation outcomes
        vendor_status: Vendor qualification check results
        material_type: Type of material
        project_id: Project identifier
    
    Returns:
        Dictionary containing approval decision and conditions
    """
    decision = {
        "approval_status": "APPROVED",
        "approval_number": f"MAT-{project_id.replace('-', '')}-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
        "approval_date": datetime.now().strftime("%Y-%m-%d"),
        "conditions": [],
        "required_actions": [],
        "expiration_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
        "approved_by": "ALDOT Materials Testing Laboratory"
    }
    
    # Check vendor qualification first
    if not vendor_status.get("qualified_for_material", False):
        decision["approval_status"] = "REJECTED"
        decision["required_actions"].append(
            f"Vendor not qualified for {material_type}. Must be added to approved vendor list."
        )
        decision["expiration_date"] = None
        return {"success": True, "decision": decision}
    
    # Check if vendor certification is expired
    if not vendor_status.get("cert_is_current", False):
        decision["approval_status"] = "REJECTED"
        decision["required_actions"].append(
            f"Vendor certification expired on {vendor_status.get('cert_expiration')}. Must renew certification."
        )
        decision["expiration_date"] = None
        return {"success": True, "decision": decision}
    
    # Check vendor status
    if vendor_status.get("status") == "CONDITIONAL":
        decision["conditions"].append(
            f"Vendor is under conditional approval status. Enhanced quality monitoring required."
        )
    
    # Check test validation results
    validation = validation_results.get("validation", {})
    failed_count = len(validation.get("failed", []))
    
    if validation.get("overall_status") == "FAIL":
        if failed_count == 1:
            # Single failure - conditional approval possible
            decision["approval_status"] = "CONDITIONAL"
            failed_param = validation["failed"][0]
            decision["conditions"].append(
                f"RETEST REQUIRED: {failed_param['parameter']} - {failed_param['deficiency']}"
            )
            decision["conditions"].append(
                f"Must meet requirement: {failed_param['requirement']}"
            )
            decision["required_actions"].append(
                "Submit retest results within 30 days for full approval"
            )
            decision["expiration_date"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        else:
            # Multiple failures - rejection
            decision["approval_status"] = "REJECTED"
            decision["expiration_date"] = None
            for failed in validation["failed"]:
                decision["required_actions"].append(
                    f"Correct {failed['parameter']}: {failed['deficiency']}"
                )
            decision["required_actions"].append(
                "Resubmit complete certification after all deficiencies are corrected"
            )
    
    return {"success": True, "decision": decision}


@tool()
def generate_approval_letter(
    decision: Dict[str, Any],
    material_details: Dict[str, Any],
    test_summary: Dict[str, Any],
    specifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate formatted approval letter document.
    
    Args:
        decision: Approval decision details
        material_details: Material and vendor information
        test_summary: Summary of test results
        specifications: Specification requirements
    
    Returns:
        Dictionary containing formatted approval letter
    """
    # Format passed tests
    passed_tests = "\n".join([
        f"  ✓ {p['parameter']}: {p['value']} - {p['status']}"
        for p in test_summary.get("passed", [])
    ])
    
    # Format failed tests
    failed_tests = "\n".join([
        f"  ✗ {p['parameter']}: {p['value']} - {p['status']} ({p.get('deficiency', 'Does not meet requirement')})"
        for p in test_summary.get("failed", [])
    ]) if test_summary.get("failed") else ""
    
    # Format conditions
    conditions_text = "\n".join([
        f"  • {c}" for c in decision.get("conditions", [])
    ]) if decision.get("conditions") else "None"
    
    # Format required actions
    actions_text = "\n".join([
        f"  • {a}" for a in decision.get("required_actions", [])
    ]) if decision.get("required_actions") else "None"
    
    # Status-specific header
    status_header = {
        "APPROVED": "✅ MATERIAL APPROVED",
        "CONDITIONAL": "⚠️ CONDITIONAL APPROVAL",
        "REJECTED": "❌ MATERIAL REJECTED"
    }.get(decision["approval_status"], decision["approval_status"])
    
    letter_template = f"""
═══════════════════════════════════════════════════════════════════
ALABAMA DEPARTMENT OF TRANSPORTATION
MATERIALS APPROVAL LETTER
═══════════════════════════════════════════════════════════════════

{status_header}

Approval Number: {decision['approval_number']}
Date: {datetime.now().strftime('%B %d, %Y')}

───────────────────────────────────────────────────────────────────
MATERIAL INFORMATION
───────────────────────────────────────────────────────────────────
Material Type:      {material_details['material_type']}
Vendor:             {material_details['vendor']}
Project:            {material_details['project']}
Certification No:   {material_details['cert_number']}
Test Date:          {material_details['test_date']}
Test Laboratory:    {material_details.get('test_lab', 'N/A')}

───────────────────────────────────────────────────────────────────
SPECIFICATION REFERENCE
───────────────────────────────────────────────────────────────────
Standard:           {specifications.get('standard', 'N/A')}
Section:            {specifications.get('section_reference', 'Section 106')}

───────────────────────────────────────────────────────────────────
TEST RESULTS SUMMARY
───────────────────────────────────────────────────────────────────
Tests Passed: {test_summary.get('passed_count', 0)}
Tests Failed: {test_summary.get('failed_count', 0)}

PASSED TESTS:
{passed_tests if passed_tests else "  None"}

{f"FAILED TESTS:\n{failed_tests}\n" if failed_tests else ""}
───────────────────────────────────────────────────────────────────
APPROVAL CONDITIONS
───────────────────────────────────────────────────────────────────
{conditions_text}

───────────────────────────────────────────────────────────────────
REQUIRED ACTIONS
───────────────────────────────────────────────────────────────────
{actions_text}

───────────────────────────────────────────────────────────────────
APPROVAL DETAILS
───────────────────────────────────────────────────────────────────
Approval Status:    {decision['approval_status']}
Expiration Date:    {decision.get('expiration_date', 'N/A')}
Approved By:        {decision.get('approved_by', 'ALDOT Materials Lab')}

───────────────────────────────────────────────────────────────────
For questions regarding this approval, contact:
ALDOT Materials Testing Laboratory
Phone: (334) 242-6000
Email: materials@aldot.gov
═══════════════════════════════════════════════════════════════════
    """
    
    return {
        "success": True,
        "letter_content": letter_template.strip(),
        "approval_number": decision['approval_number'],
        "approval_status": decision['approval_status'],
        "pdf_generated": True,  # Mock - would actually generate PDF in production
        "file_name": f"{decision['approval_number']}.pdf"
    }


@tool()
def update_approved_materials_list(
    approval_number: str,
    material_details: Dict[str, Any],
    project_id: str,
    expiration_date: str,
    approval_status: str
) -> Dict[str, Any]:
    """
    Update project's approved materials database.
    
    Args:
        approval_number: Generated approval number
        material_details: Complete material information
        project_id: Project identifier
        expiration_date: Approval validity date
        approval_status: APPROVED, CONDITIONAL, or REJECTED
    
    Returns:
        Dictionary confirming database update
    """
    # Mock database update
    material_entry = {
        "approval_number": approval_number,
        "material_type": material_details["material_type"],
        "vendor": material_details["vendor"],
        "cert_number": material_details["cert_number"],
        "approval_status": approval_status,
        "approval_date": datetime.now().strftime("%Y-%m-%d"),
        "expiration_date": expiration_date,
        "added_to_database": datetime.now().isoformat()
    }
    
    # Get project info
    project_info = PROJECTS.get(project_id, {})
    project_name = project_info.get("name", "Unknown Project")
    project_engineer = project_info.get("engineer", "Unknown Engineer")
    
    # Simulate adding to project's approved materials list
    if project_id in PROJECTS:
        PROJECTS[project_id]["approved_materials"].append(material_entry)
    
    # Generate notification list
    notifications = [
        f"{project_engineer} <{project_engineer.lower().replace(' ', '.').replace(',', '')}@aldot.gov>",
        "materials.lab@aldot.gov",
        "quality.assurance@aldot.gov"
    ]
    
    return {
        "success": True,
        "message": f"Material {'approved' if approval_status == 'APPROVED' else 'processed'} and added to {project_name} materials list",
        "approval_number": approval_number,
        "project_id": project_id,
        "project_name": project_name,
        "approval_status": approval_status,
        "database_updated": True,
        "database_timestamp": datetime.now().isoformat(),
        "notifications_sent": notifications,
        "notification_count": len(notifications)
    }


@tool()
def generate_rejection_notice(
    validation_results: Dict[str, Any],
    material_details: Dict[str, Any],
    vendor_status: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate formal rejection notice with deficiency details.
    
    Args:
        validation_results: Test validation results
        material_details: Material and vendor information
        vendor_status: Vendor qualification status
    
    Returns:
        Dictionary containing formatted rejection notice
    """
    # Format deficiencies
    deficiencies = []
    
    # Check vendor issues
    if not vendor_status.get("qualified_for_material", False):
        deficiencies.append(
            f"Vendor '{material_details['vendor']}' is not qualified for {material_details['material_type']}"
        )
    
    if not vendor_status.get("cert_is_current", False):
        deficiencies.append(
            f"Vendor certification expired on {vendor_status.get('cert_expiration', 'unknown date')}"
        )
    
    # Add test failures
    validation = validation_results.get("validation", {})
    for failed in validation.get("failed", []):
        deficiencies.append(
            f"{failed['parameter']}: {failed['value']} does not meet requirement {failed['requirement']} - {failed.get('deficiency', 'Outside acceptable limits')}"
        )
    
    deficiencies_text = "\n".join([f"  {i+1}. {d}" for i, d in enumerate(deficiencies)])
    
    notice = f"""
═══════════════════════════════════════════════════════════════════
ALABAMA DEPARTMENT OF TRANSPORTATION
MATERIAL REJECTION NOTICE
═══════════════════════════════════════════════════════════════════

❌ MATERIAL REJECTED

Date: {datetime.now().strftime('%B %d, %Y')}
Rejection ID: REJ-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}

───────────────────────────────────────────────────────────────────
MATERIAL INFORMATION
───────────────────────────────────────────────────────────────────
Material Type:      {material_details['material_type']}
Vendor:             {material_details['vendor']}
Project:            {material_details['project']}
Certification No:   {material_details['cert_number']}
Test Date:          {material_details['test_date']}

───────────────────────────────────────────────────────────────────
DEFICIENCIES IDENTIFIED
───────────────────────────────────────────────────────────────────
{deficiencies_text}

───────────────────────────────────────────────────────────────────
CORRECTIVE ACTIONS REQUIRED
───────────────────────────────────────────────────────────────────
  1. Address all deficiencies listed above
  2. Retest all failed parameters at an approved laboratory
  3. Ensure vendor qualifications are current and valid
  4. Submit new certification with compliant test results
  5. Include corrective action report with resubmission

───────────────────────────────────────────────────────────────────
RESUBMISSION PROCESS
───────────────────────────────────────────────────────────────────
  1. Correct all identified deficiencies
  2. Obtain new test results from ALDOT-approved laboratory
  3. Verify all tests meet Section 106 requirements
  4. Submit new certification for review
  5. Allow 5-7 business days for review of resubmission

───────────────────────────────────────────────────────────────────
IMPORTANT NOTES
───────────────────────────────────────────────────────────────────
• This material may NOT be used on ALDOT projects
• Vendor must address all deficiencies before resubmission
• Repeated rejections may result in vendor review
• Contact Materials Lab with questions before resubmitting

───────────────────────────────────────────────────────────────────
For questions or to schedule resubmission review, contact:
ALDOT Materials Testing Laboratory
Phone: (334) 242-6000
Email: materials@aldot.gov
═══════════════════════════════════════════════════════════════════
    """
    
    return {
        "success": True,
        "notice_content": notice.strip(),
        "rejection_date": datetime.now().strftime("%Y-%m-%d"),
        "rejection_id": f"REJ-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
        "deficiency_count": len(deficiencies),
        "deficiencies": deficiencies,
        "resubmission_allowed": True
    }

# Made with Bob
