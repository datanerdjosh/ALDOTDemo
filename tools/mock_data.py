"""
Mock data for Materials Control & Approval Agent
Simulates material certifications, vendor database, and specifications
"""

from datetime import datetime, timedelta

# Sample material certifications (3 scenarios: approve, conditional, reject)
MOCK_CERTIFICATIONS = {
    "CERT-2024-001": {
        "vendor": "ABC Materials Supply",
        "material_type": "Portland Cement Type II",
        "project": "I-85-2024",
        "cert_number": "ABC-PC2-2024-001",
        "test_date": "2024-03-15",
        "test_lab": "Alabama Materials Testing Laboratory",
        "test_results": {
            "fineness": 3450,  # cm²/g (PASS - above 3300)
            "compressive_strength_7day": 3200,  # psi (PASS - above 2800)
            "sulfate_resistance": 2.5,  # % SO₃ (PASS - below 3.0)
            "air_content": 6.0  # % (PASS - within 4-7 range)
        }
    },
    "CERT-2024-002": {
        "vendor": "XYZ Concrete Co",
        "material_type": "Portland Cement Type II",
        "project": "SR-280-2024",
        "cert_number": "XYZ-PC2-2024-045",
        "test_date": "2024-03-20",
        "test_lab": "Independent Testing Services",
        "test_results": {
            "fineness": 3150,  # cm²/g (FAIL - below 3300)
            "compressive_strength_7day": 3400,  # psi (PASS)
            "sulfate_resistance": 2.8,  # % SO₃ (PASS)
            "air_content": 5.5  # % (PASS)
        }
    },
    "CERT-2024-003": {
        "vendor": "Quality Aggregates Inc",
        "material_type": "Coarse Aggregate #57",
        "project": "US-431-2024",
        "cert_number": "QAI-AGG-2024-089",
        "test_date": "2024-03-18",
        "test_lab": "Alabama Materials Testing Laboratory",
        "test_results": {
            "gradation_pass": True,
            "la_abrasion": 28,  # % (PASS - below 40)
            "soundness": 8,  # % loss (PASS - below 12)
            "deleterious": 1.5  # % (PASS - below 3)
        }
    },
    "CERT-2024-004": {
        "vendor": "Southern Asphalt Corp",
        "material_type": "Asphalt Binder PG 67-22",
        "project": "I-65-2024",
        "cert_number": "SAC-AB-2024-112",
        "test_date": "2024-03-22",
        "test_lab": "Asphalt Testing Facility",
        "test_results": {
            "viscosity": 3200,  # Pa·s (PASS)
            "penetration": 58,  # dmm (PASS - 50-70 range)
            "flash_point": 235,  # °C (PASS - above 230)
            "ductility": 105  # cm (PASS - above 100)
        }
    },
    "CERT-2024-005": {
        "vendor": "Rejected Materials Inc",
        "material_type": "Portland Cement Type II",
        "project": "SR-59-2024",
        "cert_number": "RMI-PC2-2024-033",
        "test_date": "2024-03-25",
        "test_lab": "Budget Testing Lab",
        "test_results": {
            "fineness": 3050,  # cm²/g (FAIL - below 3300)
            "compressive_strength_7day": 2600,  # psi (FAIL - below 2800)
            "sulfate_resistance": 3.5,  # % SO₃ (FAIL - above 3.0)
            "air_content": 8.5  # % (FAIL - above 7.0)
        }
    }
}

# Vendor qualification database
APPROVED_VENDORS = {
    "ABC Materials Supply": {
        "status": "APPROVED",
        "vendor_id": "ALDOT-V-001",
        "materials": ["Portland Cement Type I", "Portland Cement Type II", "Portland Cement Type III"],
        "cert_expiration": "2027-12-31",  # Updated to future date
        "performance_rating": "Excellent",
        "years_approved": 15,
        "contact": "John Smith, Quality Manager"
    },
    "XYZ Concrete Co": {
        "status": "APPROVED",
        "vendor_id": "ALDOT-V-045",
        "materials": ["Portland Cement Type II", "Ready Mix Concrete", "Concrete Masonry Units"],
        "cert_expiration": "2027-06-30",  # Updated to future date
        "performance_rating": "Good",
        "years_approved": 8,
        "contact": "Jane Doe, Technical Director"
    },
    "Quality Aggregates Inc": {
        "status": "APPROVED",
        "vendor_id": "ALDOT-V-089",
        "materials": ["Coarse Aggregate", "Fine Aggregate", "Base Course Material"],
        "cert_expiration": "2027-09-30",  # Updated to future date
        "performance_rating": "Excellent",
        "years_approved": 20,
        "contact": "Bob Johnson, Operations Manager"
    },
    "Southern Asphalt Corp": {
        "status": "APPROVED",
        "vendor_id": "ALDOT-V-112",
        "materials": ["Asphalt Binder PG 67-22", "Asphalt Binder PG 76-22", "Emulsified Asphalt"],
        "cert_expiration": "2027-11-30",  # Updated to future date
        "performance_rating": "Excellent",
        "years_approved": 12,
        "contact": "Sarah Williams, Quality Control"
    },
    "Rejected Materials Inc": {
        "status": "CONDITIONAL",
        "vendor_id": "ALDOT-V-033",
        "materials": ["Portland Cement Type II"],
        "cert_expiration": "2025-12-31",  # Intentionally expired for rejection scenario
        "performance_rating": "Fair",
        "years_approved": 2,
        "contact": "Mike Brown, Plant Manager",
        "notes": "Recent quality issues - under review"
    }
}

# Material specifications (from Section 106)
MATERIAL_SPECS = {
    "Portland Cement Type II": {
        "standard": "AASHTO M 85",
        "section": "Section 106.02 - Portland Cement",
        "requirements": {
            "fineness_min": 3300,  # cm²/g (Blaine)
            "compressive_strength_7day_min": 2800,  # psi
            "sulfate_resistance_max": 3.0,  # % SO₃
            "air_content_range": [4.0, 7.0]  # %
        },
        "sampling_frequency": "One test per 100 tons or fraction thereof",
        "acceptance_criteria": "All parameters must meet minimum requirements"
    },
    "Coarse Aggregate #57": {
        "standard": "AASHTO M 80",
        "section": "Section 106.03 - Aggregates",
        "requirements": {
            "la_abrasion_max": 40,  # %
            "soundness_max": 12,  # % loss
            "deleterious_max": 3.0,  # %
            "gradation_required": True
        },
        "sampling_frequency": "One test per 1000 tons or daily, whichever is more frequent",
        "acceptance_criteria": "All tests must pass specified limits"
    },
    "Asphalt Binder PG 67-22": {
        "standard": "AASHTO M 320",
        "section": "Section 106.04 - Asphalt Materials",
        "requirements": {
            "viscosity_range": [2800, 3600],  # Pa·s
            "penetration_range": [50, 70],  # dmm
            "flash_point_min": 230,  # °C
            "ductility_min": 100  # cm
        },
        "sampling_frequency": "One test per shipment or 200 tons",
        "acceptance_criteria": "Must meet all performance grade requirements"
    }
}

# Project database (for tracking approved materials)
PROJECTS = {
    "I-85-2024": {
        "name": "Interstate 85 Widening",
        "county": "Montgomery",
        "engineer": "Laura Smith, PE",
        "start_date": "2024-01-15",
        "approved_materials": []
    },
    "SR-280-2024": {
        "name": "State Route 280 Resurfacing",
        "county": "Jefferson",
        "engineer": "Michael Johnson, PE",
        "start_date": "2024-02-01",
        "approved_materials": []
    },
    "US-431-2024": {
        "name": "US Highway 431 Bridge Replacement",
        "county": "Madison",
        "engineer": "Sarah Williams, PE",
        "start_date": "2024-03-01",
        "approved_materials": []
    },
    "I-65-2024": {
        "name": "Interstate 65 Pavement Rehabilitation",
        "county": "Mobile",
        "engineer": "David Brown, PE",
        "start_date": "2024-01-20",
        "approved_materials": []
    },
    "SR-59-2024": {
        "name": "State Route 59 Reconstruction",
        "county": "Baldwin",
        "engineer": "Jennifer Davis, PE",
        "start_date": "2024-02-15",
        "approved_materials": []
    }
}

# Made with Bob
