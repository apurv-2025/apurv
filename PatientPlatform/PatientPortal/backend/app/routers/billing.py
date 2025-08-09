from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from datetime import datetime, date
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter(prefix="/billing", tags=["billing"])

# Mock billing data
MOCK_INVOICES = [
    {
        "id": 1,
        "invoiceNumber": "INV-2024-001",
        "date": "2024-02-15",
        "dueDate": "2024-03-15",
        "serviceDate": "2024-02-10",
        "provider": "Dr. Sarah Johnson",
        "service": "Annual Physical Examination",
        "amount": 285.00,
        "insuranceCovered": 228.00,
        "patientResponsibility": 57.00,
        "status": "pending",
        "description": "Comprehensive annual physical with routine labs",
        "cptCodes": [
            {"code": "99213", "description": "Office visit, established patient", "amount": 150.00},
            {"code": "80053", "description": "Comprehensive metabolic panel", "amount": 85.00},
            {"code": "85025", "description": "Complete blood count", "amount": 50.00}
        ],
        "insuranceClaim": {
            "claimNumber": "CLM-789456123",
            "submittedDate": "2024-02-16",
            "processedDate": "2024-02-20",
            "status": "processed",
            "coveragePercentage": 80,
            "deductibleApplied": 0,
            "copayAmount": 25.00
        }
    },
    {
        "id": 2,
        "invoiceNumber": "INV-2024-002",
        "date": "2024-01-20",
        "dueDate": "2024-02-20",
        "serviceDate": "2024-01-15",
        "provider": "Dr. Michael Chen",
        "service": "Cardiology Consultation",
        "amount": 450.00,
        "insuranceCovered": 360.00,
        "patientResponsibility": 90.00,
        "status": "paid",
        "paidDate": "2024-02-18",
        "paymentMethod": "Credit Card",
        "description": "Follow-up consultation for hypertension management",
        "cptCodes": [
            {"code": "99244", "description": "Cardiology consultation", "amount": 350.00},
            {"code": "93000", "description": "Electrocardiogram", "amount": 100.00}
        ],
        "insuranceClaim": {
            "claimNumber": "CLM-789456124",
            "submittedDate": "2024-01-21",
            "processedDate": "2024-01-25",
            "status": "approved",
            "coveragePercentage": 80,
            "deductibleApplied": 0,
            "copayAmount": 40.00
        }
    },
    {
        "id": 3,
        "invoiceNumber": "INV-2024-003",
        "date": "2024-02-25",
        "dueDate": "2024-03-25",
        "serviceDate": "2024-02-22",
        "provider": "Lab Corp",
        "service": "Laboratory Tests",
        "amount": 125.00,
        "insuranceCovered": 100.00,
        "patientResponsibility": 25.00,
        "status": "overdue",
        "description": "Routine lab work ordered by Dr. Johnson",
        "cptCodes": [
            {"code": "80061", "description": "Lipid panel", "amount": 75.00},
            {"code": "83036", "description": "Hemoglobin A1C", "amount": 50.00}
        ],
        "insuranceClaim": {
            "claimNumber": "CLM-789456125",
            "submittedDate": "2024-02-23",
            "processedDate": "2024-02-27",
            "status": "processed",
            "coveragePercentage": 80,
            "deductibleApplied": 0,
            "copayAmount": 25.00
        }
    }
]

MOCK_INSURANCE_CARDS = [
    {
        "id": 1,
        "type": "primary",
        "insuranceCompany": "Blue Cross Blue Shield",
        "planName": "PPO Select",
        "policyNumber": "BC123456789",
        "groupNumber": "GRP-001234",
        "memberName": "John Smith",
        "memberId": "BC123456789",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2024-12-31",
        "copay": {
            "primaryCare": 25,
            "specialist": 40,
            "emergency": 150,
            "urgentCare": 50
        },
        "deductible": {
            "individual": 1500,
            "family": 3000,
            "met": 250
        },
        "outOfPocketMax": {
            "individual": 6000,
            "family": 12000,
            "met": 340
        },
        "cardImageUrl": "/images/insurance-card-front.jpg",
        "cardBackImageUrl": "/images/insurance-card-back.jpg",
        "customerServicePhone": "1-800-555-0123",
        "website": "www.bcbs.com"
    },
    {
        "id": 2,
        "type": "secondary",
        "insuranceCompany": "Aetna",
        "planName": "Health Fund HDHP",
        "policyNumber": "AET987654321",
        "groupNumber": "GRP-005678",
        "memberName": "John Smith",
        "memberId": "AET987654321",
        "effectiveDate": "2024-01-01",
        "expirationDate": "2024-12-31",
        "copay": {
            "primaryCare": 0,
            "specialist": 0,
            "emergency": 0,
            "urgentCare": 0
        },
        "deductible": {
            "individual": 3000,
            "family": 6000,
            "met": 0
        },
        "outOfPocketMax": {
            "individual": 5000,
            "family": 10000,
            "met": 0
        },
        "cardImageUrl": "/images/aetna-card-front.jpg",
        "cardBackImageUrl": "/images/aetna-card-back.jpg",
        "customerServicePhone": "1-800-555-0456",
        "website": "www.aetna.com"
    }
]

MOCK_COVERAGE_DETAILS = [
    {
        "id": 1,
        "category": "Preventive Care",
        "covered": True,
        "coveragePercentage": 100,
        "copayAmount": 0,
        "deductibleApplies": False,
        "description": "Annual physical, mammograms, colonoscopies, vaccinations",
        "limitations": "Once per calendar year"
    },
    {
        "id": 2,
        "category": "Primary Care Visits",
        "covered": True,
        "coveragePercentage": 80,
        "copayAmount": 25,
        "deductibleApplies": False,
        "description": "Routine office visits with primary care physician",
        "limitations": "Copay applies after insurance payment"
    },
    {
        "id": 3,
        "category": "Specialist Visits",
        "covered": True,
        "coveragePercentage": 80,
        "copayAmount": 40,
        "deductibleApplies": True,
        "description": "Consultations with specialists",
        "limitations": "Referral may be required"
    },
    {
        "id": 4,
        "category": "Laboratory Tests",
        "covered": True,
        "coveragePercentage": 80,
        "copayAmount": 0,
        "deductibleApplies": True,
        "description": "Blood work, urine tests, diagnostic labs",
        "limitations": "Must be medically necessary"
    },
    {
        "id": 5,
        "category": "Prescription Drugs",
        "covered": True,
        "coveragePercentage": 80,
        "copayAmount": 0,
        "deductibleApplies": True,
        "description": "Generic and brand name medications",
        "limitations": "Formulary restrictions may apply"
    }
]

MOCK_PAYMENTS = [
    {
        "id": 1,
        "date": "2024-02-18",
        "amount": 90.00,
        "method": "Credit Card (**** 4532)",
        "invoiceNumber": "INV-2024-002",
        "confirmationNumber": "PAY-789123456",
        "status": "completed"
    },
    {
        "id": 2,
        "date": "2024-01-15",
        "amount": 150.00,
        "method": "Bank Transfer",
        "invoiceNumber": "INV-2023-045",
        "confirmationNumber": "PAY-789123455",
        "status": "completed"
    }
]

@router.get("/overview")
async def get_billing_overview(current_user: User = Depends(get_current_user)):
    """Get billing overview with summary statistics"""
    try:
        total_balance = sum([inv["patientResponsibility"] for inv in MOCK_INVOICES if inv["status"] != "paid"])
        overdue_balance = sum([inv["patientResponsibility"] for inv in MOCK_INVOICES if inv["status"] == "overdue"])
        
        recent_invoices = sorted(MOCK_INVOICES, key=lambda x: x["date"], reverse=True)[:3]
        
        return {
            "totalBalance": total_balance,
            "overdueBalance": overdue_balance,
            "recentInvoices": recent_invoices,
            "insuranceCount": len(MOCK_INSURANCE_CARDS),
            "primaryInsurance": next((card for card in MOCK_INSURANCE_CARDS if card["type"] == "primary"), None)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching billing overview: {str(e)}")

@router.get("/invoices")
async def get_invoices(
    status: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all invoices with optional filtering"""
    try:
        invoices = MOCK_INVOICES.copy()
        
        # Filter by status
        if status and status != "all":
            invoices = [inv for inv in invoices if inv["status"] == status]
        
        # Filter by date range
        if date_from:
            invoices = [inv for inv in invoices if inv["date"] >= date_from]
        if date_to:
            invoices = [inv for inv in invoices if inv["date"] <= date_to]
        
        # Search functionality
        if search:
            search_lower = search.lower()
            invoices = [
                inv for inv in invoices 
                if (search_lower in inv["invoiceNumber"].lower() or
                    search_lower in inv["provider"].lower() or
                    search_lower in inv["service"].lower() or
                    search_lower in inv["description"].lower())
            ]
        
        # Sort by date (newest first)
        invoices.sort(key=lambda x: x["date"], reverse=True)
        
        return invoices
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching invoices: {str(e)}")

@router.get("/invoices/{invoice_id}")
async def get_invoice_detail(invoice_id: int, current_user: User = Depends(get_current_user)):
    """Get detailed information for a specific invoice"""
    try:
        invoice = next((inv for inv in MOCK_INVOICES if inv["id"] == invoice_id), None)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching invoice detail: {str(e)}")

@router.get("/insurance-cards")
async def get_insurance_cards(current_user: User = Depends(get_current_user)):
    """Get all insurance cards for the current user"""
    try:
        return MOCK_INSURANCE_CARDS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insurance cards: {str(e)}")

@router.post("/insurance-cards")
async def add_insurance_card(
    card_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Add a new insurance card"""
    try:
        # In a real implementation, this would save to database
        new_card = {
            "id": len(MOCK_INSURANCE_CARDS) + 1,
            **card_data,
            "addedDate": datetime.now().isoformat()
        }
        MOCK_INSURANCE_CARDS.append(new_card)
        return new_card
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding insurance card: {str(e)}")

@router.put("/insurance-cards/{card_id}")
async def update_insurance_card(
    card_id: int,
    card_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Update an existing insurance card"""
    try:
        card_index = next((i for i, card in enumerate(MOCK_INSURANCE_CARDS) if card["id"] == card_id), None)
        if card_index is None:
            raise HTTPException(status_code=404, detail="Insurance card not found")
        
        MOCK_INSURANCE_CARDS[card_index].update(card_data)
        return MOCK_INSURANCE_CARDS[card_index]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating insurance card: {str(e)}")

@router.delete("/insurance-cards/{card_id}")
async def delete_insurance_card(card_id: int, current_user: User = Depends(get_current_user)):
    """Delete an insurance card"""
    try:
        card_index = next((i for i, card in enumerate(MOCK_INSURANCE_CARDS) if card["id"] == card_id), None)
        if card_index is None:
            raise HTTPException(status_code=404, detail="Insurance card not found")
        
        deleted_card = MOCK_INSURANCE_CARDS.pop(card_index)
        return {"message": "Insurance card deleted successfully", "deletedCard": deleted_card}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting insurance card: {str(e)}")

@router.post("/insurance-cards/{card_id}/upload-image")
async def upload_insurance_card_image(
    card_id: int,
    side: str,  # 'front' or 'back'
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload insurance card image"""
    try:
        # In a real implementation, this would save the file and update the card record
        card_index = next((i for i, card in enumerate(MOCK_INSURANCE_CARDS) if card["id"] == card_id), None)
        if card_index is None:
            raise HTTPException(status_code=404, detail="Insurance card not found")
        
        # Simulate file upload
        filename = f"insurance_card_{card_id}_{side}_{file.filename}"
        file_url = f"/uploads/insurance_cards/{filename}"
        
        # Update card with image URL
        if side == "front":
            MOCK_INSURANCE_CARDS[card_index]["cardImageUrl"] = file_url
        else:
            MOCK_INSURANCE_CARDS[card_index]["cardBackImageUrl"] = file_url
        
        return {
            "message": f"Insurance card {side} image uploaded successfully",
            "fileUrl": file_url,
            "card": MOCK_INSURANCE_CARDS[card_index]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading insurance card image: {str(e)}")

@router.get("/coverage")
async def get_coverage_details(current_user: User = Depends(get_current_user)):
    """Get insurance coverage details"""
    try:
        return MOCK_COVERAGE_DETAILS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching coverage details: {str(e)}")

@router.get("/payments")
async def get_payment_history(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get payment history"""
    try:
        payments = MOCK_PAYMENTS.copy()
        
        # Filter by date range
        if date_from:
            payments = [pay for pay in payments if pay["date"] >= date_from]
        if date_to:
            payments = [pay for pay in payments if pay["date"] <= date_to]
        
        # Sort by date (newest first)
        payments.sort(key=lambda x: x["date"], reverse=True)
        
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching payment history: {str(e)}")

@router.post("/payments")
async def process_payment(
    payment_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Process a payment for an invoice"""
    try:
        # In a real implementation, this would integrate with a payment processor
        new_payment = {
            "id": len(MOCK_PAYMENTS) + 1,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "amount": payment_data["amount"],
            "method": payment_data["method"],
            "invoiceNumber": payment_data.get("invoiceNumber"),
            "confirmationNumber": f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "status": "completed"
        }
        
        MOCK_PAYMENTS.append(new_payment)
        
        # Update invoice status if payment covers full amount
        if payment_data.get("invoiceNumber"):
            invoice = next((inv for inv in MOCK_INVOICES if inv["invoiceNumber"] == payment_data["invoiceNumber"]), None)
            if invoice and payment_data["amount"] >= invoice["patientResponsibility"]:
                invoice["status"] = "paid"
                invoice["paidDate"] = new_payment["date"]
                invoice["paymentMethod"] = payment_data["method"]
        
        return {
            "message": "Payment processed successfully",
            "payment": new_payment,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing payment: {str(e)}")

@router.get("/statements")
async def get_billing_statements(
    year: Optional[int] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """Get billing statements"""
    try:
        statements = [
            {
                "id": 1,
                "month": "February 2024",
                "statementDate": "2024-03-01",
                "totalCharges": 860.00,
                "insurancePayments": 688.00,
                "patientPayments": 90.00,
                "adjustments": 0.00,
                "balance": 82.00,
                "dueDate": "2024-03-25"
            },
            {
                "id": 2,
                "month": "January 2024",
                "statementDate": "2024-02-01",
                "totalCharges": 450.00,
                "insurancePayments": 360.00,
                "patientPayments": 90.00,
                "adjustments": 0.00,
                "balance": 0.00,
                "dueDate": None
            }
        ]
        
        # Filter by year/month if provided
        if year or month:
            filtered_statements = []
            for stmt in statements:
                stmt_date = datetime.strptime(stmt["statementDate"], "%Y-%m-%d")
                if year and stmt_date.year != year:
                    continue
                if month and stmt_date.month != month:
                    continue
                filtered_statements.append(stmt)
            statements = filtered_statements
        
        return statements
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching billing statements: {str(e)}")

@router.get("/summary")
async def get_billing_summary(current_user: User = Depends(get_current_user)):
    """Get comprehensive billing summary"""
    try:
        total_invoices = len(MOCK_INVOICES)
        total_amount = sum([inv["amount"] for inv in MOCK_INVOICES])
        total_insurance_covered = sum([inv["insuranceCovered"] for inv in MOCK_INVOICES])
        total_patient_responsibility = sum([inv["patientResponsibility"] for inv in MOCK_INVOICES])
        pending_balance = sum([inv["patientResponsibility"] for inv in MOCK_INVOICES if inv["status"] != "paid"])
        
        return {
            "totalInvoices": total_invoices,
            "totalAmount": total_amount,
            "totalInsuranceCovered": total_insurance_covered,
            "totalPatientResponsibility": total_patient_responsibility,
            "pendingBalance": pending_balance,
            "insuranceCards": len(MOCK_INSURANCE_CARDS),
            "paymentsThisMonth": len([p for p in MOCK_PAYMENTS if p["date"].startswith("2024-02")])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching billing summary: {str(e)}")

@router.get("/download/invoice/{invoice_id}")
async def download_invoice(invoice_id: int, current_user: User = Depends(get_current_user)):
    """Download invoice as PDF"""
    try:
        invoice = next((inv for inv in MOCK_INVOICES if inv["id"] == invoice_id), None)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # In a real implementation, this would generate and return a PDF file
        return {
            "downloadUrl": f"/downloads/invoice_{invoice['invoiceNumber']}.pdf",
            "filename": f"Invoice_{invoice['invoiceNumber']}.pdf",
            "message": "PDF generation would be handled here"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading invoice: {str(e)}")

@router.get("/download/statement/{statement_id}")
async def download_statement(statement_id: int, current_user: User = Depends(get_current_user)):
    """Download billing statement as PDF"""
    try:
        # In a real implementation, this would generate and return a PDF file
        return {
            "downloadUrl": f"/downloads/statement_{statement_id}.pdf",
            "filename": f"Statement_{statement_id}.pdf",
            "message": "PDF generation would be handled here"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading statement: {str(e)}")