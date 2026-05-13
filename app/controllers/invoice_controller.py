from app.models.policy_models import Policy

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import calendar
from app.models.invoice_model import Invoice
from app.models.lead_models import Lead
from app.models.lead_log_models import LeadLog
from app.models.upgrade_models import Upgrade
from app.schemas.invoice_schema import InvoiceCreate, InvoiceGenerateRequest, MonthlyInvoiceRequest, InvoiceUpdate, ReportRequest
import random
import string


def get_revenue_report(req: ReportRequest, db: Session):
    query = text("""
   SELECT 
    x.customer_id,
    x.lead_id,
    x.upgrade_id,
    x.type,

    x.policy_id,
    CASE WHEN x.policy_id = 0 THEN x.budget_allocation ELSE p.price END AS policy_price,
    p.bandwidth,

    x.budget_allocation,
    x.capacity,

    x.start_date,
    x.end_date,

    DATEDIFF(x.end_date, x.start_date) + 1 AS total_days,

    x.expected_revenue,

    ROUND((x.expected_revenue / 30) * 
        (DATEDIFF(x.end_date, x.start_date) + 1), 2
    ) AS amount

FROM
(
    -- 🔹 LEADS
    SELECT 
        l.customer_id,
        l.id AS lead_id,
        NULL AS upgrade_id,
        'lead' AS type,

        l.policy_id,
        l.budget_allocation,
        l.capacity,

        GREATEST(l.activation_date, '2026-04-01') AS start_date,
        LEAST(IFNULL(l.deactivation_date, '2026-04-30'), '2026-04-30') AS end_date,

        l.expected_revenue

    FROM lead l
    WHERE 
        l.activation_date <= '2026-04-30'
        AND (l.deactivation_date IS NULL OR l.deactivation_date >= '2026-05-01')


    UNION ALL


    -- 🔹 UPGRADES
    SELECT 
        l.customer_id,
        u.lead_id,
        u.id AS upgrade_id,
        'upgrade' AS type,

        COALESCE(u.policy, l.policy_id) AS policy_id,  -- 🔥 upgrade override
        COALESCE(u.budget_allocation, l.budget_allocation) AS budget_allocation,
        COALESCE(u.capacity, l.capacity) AS capacity,

        GREATEST(u.activation_date, '2026-04-01') AS start_date,
        LEAST(IFNULL(u.deactivation_date, '2026-04-30'), '2026-04-30') AS end_date,

        u.expected_revenue

    FROM upgrades u
    JOIN lead l ON l.id = u.lead_id
    WHERE 
        u.activation_date <= '2026-04-30'
        AND (u.deactivation_date IS NULL OR u.deactivation_date >= '2026-04-01')

) AS x

-- 🔥 JOIN POLICY TABLE
LEFT JOIN policies p ON p.id = x.policy_id

WHERE x.customer_id = :customer_id

ORDER BY x.customer_id, x.lead_id, x.start_date;
    """)

    result = db.execute(
        query,
        {
            "start_date": req.start_date,
            "end_date": req.end_date,
            "customer_id": req.customer_id,
            "lead_id": req.lead_id
        }
    )

    data = [dict(row._mapping) for row in result]

    return {
        "status": "success",
        "count": len(data),
        "data": data
    }
def create_invoice(payload: InvoiceCreate, db: Session):
    now = datetime.now()
    start = payload.start_date if payload.start_date else (now + timedelta(days=2))
    due = payload.due_date if payload.due_date else (start + timedelta(days=30))
    issn = payload.issue_date if payload.issue_date else now
    
    inv_num = payload.invoice_number or f"INV-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    
    new_inv = Invoice(
        customer_id=payload.customer_id,
        invoice_month=payload.invoice_month,
        total_amount=payload.total_amount,
        status=payload.status or "Pending",
        lead_id=payload.lead_id,
        sub_invoice=payload.sub_invoice,
        amount=payload.amount,
        issue_date=issn,
        start_date=start,
        due_date=due,
        notes=payload.notes,
        currency=payload.currency or "PKR",
        invoice_number=inv_num
    )
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)
    return new_inv

def _compute_lead_summary(lead: Lead, db: Session):
    logs = db.query(LeadLog).filter(LeadLog.lead_id == lead.id).order_by(LeadLog.timestamp).all()
    upgrade_logs = [log for log in logs if log.action and "upgrade" in log.action.lower()]
    first_upgrade_time = upgrade_logs[0].timestamp if upgrade_logs else None
    days_to_first_upgrade = None
    if first_upgrade_time and lead.created_at:
        days_to_first_upgrade = (first_upgrade_time - lead.created_at).days
    total_active_days = None
    if lead.created_at:
        total_active_days = (datetime.now() - lead.created_at).days
    lead_type = "New Lead" if len(upgrade_logs) == 0 else "Upgrade Lead"

    return {
        "lead_id": lead.id,
        "policy_type": lead.policy_type,
        "billing_period": lead.billing_period,
        "lead_type": lead_type,
        "upgrade_count": len(upgrade_logs),
        "days_to_first_upgrade": days_to_first_upgrade,
        "total_active_days": total_active_days,
        "notes": lead.notes,
    }


def generate_invoice_for_customer(payload: InvoiceGenerateRequest, db: Session):
    lead_query = db.query(Lead).filter(Lead.customer_id == payload.customer_id)
    if payload.lead_id:
        lead_query = lead_query.filter(Lead.id == payload.lead_id)
    leads = lead_query.all()

    if not leads:
        raise HTTPException(status_code=404, detail="No leads found for this customer")

    total_leads = len(leads)
    lead_summaries = []
    total_upgrades = 0
    for lead in leads:
        summary = _compute_lead_summary(lead, db)
        lead_summaries.append(summary)
        total_upgrades += summary["upgrade_count"]

    amount = payload.amount
    if amount is None:
        amount = 1000 + 200 * total_leads + 150 * total_upgrades

    invoice_number = payload.invoice_number or f"INV-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    now = datetime.now()
    start = now + timedelta(days=2)
    due = start + timedelta(days=30)
    lead_id = payload.lead_id or leads[0].id

    new_inv = Invoice(
        customer_id=payload.customer_id,
        lead_id=lead_id,
        invoice_number=invoice_number,
        amount=amount,
        currency=payload.currency,
        status=payload.status or "Pending",
        issue_date=now,
        start_date=start,
        due_date=due,
        notes=payload.notes,
    )
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)

    summary_lines = [
        f"Customer {payload.customer_id} has {total_leads} lead(s) and {total_upgrades} total upgrade(s)."
    ]
    for lead_summary in lead_summaries:
        summary_lines.append(
            f"Lead {lead_summary['lead_id']} is {lead_summary['lead_type']}, "
            f"policy {lead_summary['policy_type'] or 'N/A'}, "
            f"billing period {lead_summary['billing_period'] or 'N/A'}, "
            f"upgrades {lead_summary['upgrade_count']}, "
            f"first upgrade after {lead_summary['days_to_first_upgrade'] if lead_summary['days_to_first_upgrade'] is not None else 'N/A'} days, "
            f"active for {lead_summary['total_active_days']} days."
        )
    summary_text = " ".join(summary_lines)
    voice_text = summary_text

    return {
        "invoice": new_inv,
        "total_leads": total_leads,
        "total_upgrades": total_upgrades,
        "leads": lead_summaries,
        "summary": summary_text,
        "voice_text": voice_text,
    }


def generate_complex_invoice(customer_id: int, db: Session):
    leads = db.query(Lead).filter(Lead.customer_id == customer_id).all()
    if not leads:
        raise HTTPException(status_code=404, detail="No leads found for this customer")

    total_leads = len(leads)
    lead_summaries = []
    total_upgrades = 0
    for lead in leads:
        summary = _compute_lead_summary(lead, db)
        lead_summaries.append(summary)
        total_upgrades += summary["upgrade_count"]

    amount = 1000 + 200 * total_leads + 150 * total_upgrades
    invoice_number = f"INV-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    now = datetime.now()
    start = now + timedelta(days=2)
    due = start + timedelta(days=30)

    new_inv = Invoice(
        customer_id=customer_id,
        lead_id=leads[0].id,
        invoice_number=invoice_number,
        amount=amount,
        currency="PKR",
        status="Pending",
        issue_date=now,
        start_date=start,
        due_date=due,
        notes=f"Complex invoice for customer {customer_id}",
    )
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)

    summary_lines = [
        f"Customer {customer_id} has {total_leads} lead(s) and {total_upgrades} total upgrade(s)."
    ]
    for lead_summary in lead_summaries:
        summary_lines.append(
            f"Lead {lead_summary['lead_id']} is {lead_summary['lead_type']}, "
            f"policy {lead_summary['policy_type'] or 'N/A'}, "
            f"billing period {lead_summary['billing_period'] or 'N/A'}, "
            f"upgrades {lead_summary['upgrade_count']}, "
            f"first upgrade after {lead_summary['days_to_first_upgrade'] if lead_summary['days_to_first_upgrade'] is not None else 'N/A'} days, "
            f"active for {lead_summary['total_active_days']} days."
        )
    summary_text = " ".join(summary_lines)
    voice_text = summary_text

    return {
        "invoice": new_inv,
        "total_leads": total_leads,
        "total_upgrades": total_upgrades,
        "leads": lead_summaries,
        "summary": summary_text,
        "voice_text": voice_text,
    }


def get_all_invoices(db: Session):
    return db.query(Invoice).all()

def get_customer_invoices(customer_id: int, db: Session):
    return db.query(Invoice).filter(Invoice.customer_id == customer_id).all()

def update_invoice_status(invoice_id: int, status: str, db: Session):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if inv:
        inv.status = status
        db.commit()
        db.refresh(inv)
    return inv

def update_invoice_controller(invoice_id: int, data: InvoiceUpdate, db: Session):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inv, key, value)
        
    db.commit()
    db.refresh(inv)
    return inv

def create_invoice_for_lead(lead_id: int, db: Session):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if   lead.policy_id==0:
        price =lead.budget_allocation 
    else: 
        amount = db.query(Policy).filter(Policy.id == lead.policy_id).first()
        price = amount.price
    invoice_number = f"INV-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    now = datetime.now()
    start = now + timedelta(days=2)
    due = start + timedelta(days=30)

    new_inv = Invoice(
        customer_id=lead.customer_id,
        lead_id=lead.id,
        invoice_number=invoice_number,
        amount=price,
        currency="PKR",
        status="Pending",
        issue_date=now,
        start_date=start,
        due_date=due,
        notes=f"Invoice for lead {lead.id}",
    )
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)
    return new_inv

def generate_monthly_invoice_controller(payload: MonthlyInvoiceRequest, db: Session):
    start_date = f"{payload.invoice_month}-01"
    year, month = map(int, payload.invoice_month.split('-'))
    _, last_day = calendar.monthrange(year, month)
    end_date = f"{payload.invoice_month}-{last_day}"

    query = text(f"""
        SELECT 
            x.customer_id,
            SUM(ROUND((x.expected_revenue / 30) * (DATEDIFF(x.end_date, x.start_date) + 1), 2)) AS total_amount
        FROM
        (
            SELECT 
                l.customer_id,
                GREATEST(l.activation_date, :start_date) AS start_date,
                LEAST(IFNULL(l.deactivation_date, :end_date), :end_date) AS end_date,
                l.expected_revenue
            FROM lead l
            WHERE 
                l.activation_date <= :end_date
                AND (l.deactivation_date IS NULL OR l.deactivation_date >= :start_date)

            UNION ALL

            SELECT 
                l.customer_id,
                GREATEST(u.activation_date, :start_date) AS start_date,
                LEAST(IFNULL(u.deactivation_date, :end_date), :end_date) AS end_date,
                u.expected_revenue
            FROM upgrades u
            JOIN lead l ON l.id = u.lead_id
            WHERE 
                u.activation_date <= :end_date
                AND (u.deactivation_date IS NULL OR u.deactivation_date >= :start_date)
        ) AS x
        WHERE x.customer_id = :customer_id
        GROUP BY x.customer_id
    """)

    result = db.execute(query, {
        "start_date": start_date,
        "end_date": end_date,
        "customer_id": payload.customer_id
    }).fetchone()

    total_amount = result.total_amount if result and result.total_amount else 0.0

    invoice_number = f"INV-M-{payload.customer_id}-{payload.invoice_month}"
    
    inv = db.query(Invoice).filter(
        Invoice.customer_id == payload.customer_id, 
        Invoice.invoice_month == payload.invoice_month
    ).first()
    
    if inv:
        inv.total_amount = total_amount
        db.commit()
        db.refresh(inv)
        return inv
    else:
        new_inv = Invoice(
            customer_id=payload.customer_id,
            invoice_month=payload.invoice_month,
            total_amount=total_amount,
            invoice_number=invoice_number,
            status="Generated"
        )
        db.add(new_inv)
        db.commit()
        db.refresh(new_inv)
        return new_inv

