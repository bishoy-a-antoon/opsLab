"""
Nuvoro Data Generator
=====================
Generates 9 realistic CSV datasets for the Nuvoro B2B SaaS learning roadmap.
Run: python nuvoro_data_generator.py
Output: ./nuvoro_data/ directory with 9 CSV files

Use these datasets with:
  - Salesforce (data import via Data Loader or Import Wizard)
  - Excel (open CSVs directly or via Power Query)
  - SQL (load into SQLite / PostgreSQL)
  - Metabase (connect to SQL database)
"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)
OUTPUT_DIR = "./nuvoro_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Reference Data ────────────────────────────────────────────────────────

INDUSTRIES = {
    "HVAC": 0.34, "Plumbing": 0.18, "Electrical": 0.14,
    "Pest Control": 0.12, "Facilities Management": 0.11,
    "Landscaping": 0.07, "Other": 0.04,
}

PLANS = {
    "Starter":    {"price": 299,  "tech_range": (1, 5),   "weight": 0.42},
    "Growth":     {"price": 699,  "tech_range": (5, 20),  "weight": 0.31},
    "Pro":        {"price": 1499, "tech_range": (20, 60), "weight": 0.19},
    "Enterprise": {"price": 4200, "tech_range": (60, 200),"weight": 0.08},
}

LEAD_SOURCES = ["Inbound-SEO", "Inbound-Referral", "Outbound-SDR",
                "Content-Webinar", "G2-Capterra", "Partner-Channel"]
LEAD_SOURCE_WEIGHTS = [0.34, 0.18, 0.22, 0.10, 0.08, 0.08]

SMB_AES  = ["Marcus Webb", "Leila Farouk", "Tom Szymanski", "Aisha Okafor",
            "Derek Pham", "Carla Nunez", "Josh Reinhart", "Priya Kapoor"]
MM_AES   = ["Natasha Ivanova", "Sam Okonkwo", "Rachel Thornton", "Diego Vargas"]
CSMS     = ["Jordan Blake", "Emma Solis", "Ravi Mehta", "Tanya Oluoch",
            "Felix Brennan", "Sadia Islam", "Omar Castillo", "Lena Fischer"]
SUPPORT_AGENTS = ["Alex Kim", "Brenda Cruz", "Chidi Eze", "Diana Patel",
                  "Evan Marsh", "Fiona Huang", "George Tanner", "Hana Yoshida",
                  "Ivan Sousa", "Julia Moraes", "Kyle Barros"]

LOST_REASONS = [
    "Lost to ServiceTitan", "Lost to Jobber", "No decision – stayed with current system",
    "Price too high", "Missing integration", "Champion left company",
    "Implementation too complex", "Budget cut",
]
WIN_REASONS = [
    "Best mobile app", "QuickBooks integration", "Competitive pricing",
    "Fast implementation", "Strong G2 reviews", "Referral from existing customer",
]
CHURN_REASONS = [
    "Technician adoption failure", "Switched to competitor",
    "Business closed/downsized", "Price sensitivity",
    "Integration failure", "Onboarding never completed",
]
TICKET_CATEGORIES = [
    "QuickBooks Integration", "Scheduling & Dispatch", "Mobile App",
    "Invoicing & Payments", "User Access & Permissions",
    "Data Import/Export", "Reporting & Dashboard", "General",
]
TICKET_CATEGORY_WEIGHTS = [0.22, 0.18, 0.17, 0.14, 0.10, 0.09, 0.07, 0.03]
PRIORITIES = ["P1", "P2", "P3", "P4"]
PRIORITY_WEIGHTS = [0.03, 0.10, 0.42, 0.45]

COMPANY_PREFIXES = ["Allied", "Premier", "Metro", "Summit", "Apex", "Pinnacle",
                    "BlueStar", "ProServ", "Reliable", "Elite", "National", "Regional",
                    "Heritage", "Dynamic", "TrustWorks", "OneCall", "RapidFix", "SwiftLine"]
COMPANY_SUFFIXES = ["Services", "Group", "Solutions", "Technologies", "Partners",
                    "Works", "Systems", "Professionals", "Experts", "Associates"]

STATES = ["TX", "CA", "FL", "NY", "OH", "IL", "PA", "GA", "NC", "AZ",
          "CO", "WA", "TN", "VA", "MN", "IN", "WI", "MO", "OR", "NV"]

NOTE_TYPES = ["Call", "Email", "QBR", "Health Check", "Escalation", "Renewal Discussion", "Upsell Attempt"]

# ─── Helper Functions ──────────────────────────────────────────────────────

def rand_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def rand_company(industry):
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    return f"{prefix} {industry} {suffix}"

def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

def rand_plan():
    plans = list(PLANS.keys())
    weights = [PLANS[p]["weight"] for p in plans]
    return weighted_choice(plans, weights)

def rand_industry():
    return weighted_choice(list(INDUSTRIES.keys()), list(INDUSTRIES.values()))

def rand_tech_count(plan):
    lo, hi = PLANS[plan]["tech_range"]
    return random.randint(lo, hi)

def health_score(login_freq, jobs, mobile_pct, nps, open_tickets, plan):
    score = (
        min(login_freq / 20, 1.0) * 25 +
        min(jobs / 25, 1.0) * 20 +
        (mobile_pct / 100) * 20 +
        min(nps / 10, 1.0) * 10 +
        (1 - min(open_tickets / 5, 1.0)) * 10 +
        15  # base
    )
    return round(min(max(score, 0), 100), 1)

def health_status(score):
    if score >= 70: return "Green"
    if score >= 40: return "Yellow"
    return "Red"

NOW = datetime(2025, 6, 1)
START = datetime(2022, 1, 1)

# ─── 1. LEADS ──────────────────────────────────────────────────────────────

def gen_leads(n=500):
    rows = []
    stages = ["New Lead", "Contacted", "Discovery", "Demo/Evaluation",
              "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"]
    stage_weights = [0.08, 0.12, 0.15, 0.18, 0.12, 0.08, 0.14, 0.13]

    for i in range(1, n + 1):
        industry = rand_industry()
        plan = rand_plan()
        tech_count = rand_tech_count(plan)
        source = weighted_choice(LEAD_SOURCES, LEAD_SOURCE_WEIGHTS)
        created = rand_date(datetime(2024, 1, 1), NOW)
        stage = weighted_choice(stages, stage_weights)
        ae = random.choice(SMB_AES if tech_count < 20 else MM_AES)
        mql_date = created + timedelta(days=random.randint(1, 5)) if stage not in ["New Lead", "Contacted"] else ""
        lead_score = random.randint(20, 95)

        rows.append({
            "lead_id": f"L-{i:04d}",
            "first_name": random.choice(["James", "Maria", "David", "Sarah", "Michael", "Jennifer",
                                         "Robert", "Linda", "Carlos", "Priya", "Mohamed", "Aisha"]),
            "last_name": random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                                        "Miller", "Davis", "Martinez", "Anderson", "Taylor", "Thomas"]),
            "company": rand_company(industry),
            "industry": industry,
            "state": random.choice(STATES),
            "lead_source": source,
            "tech_count": tech_count,
            "likely_plan": plan,
            "current_system": random.choice(["Spreadsheets", "ServiceTitan", "Jobber", "FieldEdge",
                                              "Paper/Manual", "Housecall Pro", "Other software"]),
            "stage": stage,
            "assigned_rep": ae,
            "lead_score": lead_score,
            "created_date": created.strftime("%Y-%m-%d"),
            "mql_date": mql_date.strftime("%Y-%m-%d") if mql_date else "",
            "email_opened": random.choice(["Yes", "No", "Yes", "Yes"]),
            "demo_requested": "Yes" if stage in ["Demo/Evaluation", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"] else "No",
        })
    return rows

# ─── 2. OPPORTUNITIES ─────────────────────────────────────────────────────

def gen_opportunities(leads):
    rows = []
    qualified_leads = [l for l in leads if l["stage"] not in ["New Lead", "Contacted"]]
    opp_leads = random.sample(qualified_leads, min(280, len(qualified_leads)))

    for i, lead in enumerate(opp_leads, 1):
        plan = lead["likely_plan"]
        mrr = PLANS[plan]["price"] * random.uniform(0.85, 1.30)
        acv = round(mrr * 12, -2)
        stage = lead["stage"]
        created = datetime.strptime(lead["created_date"], "%Y-%m-%d")
        days_in_pipeline = random.randint(5, 120)
        close_date = created + timedelta(days=days_in_pipeline)

        won_date = close_date.strftime("%Y-%m-%d") if stage == "Closed Won" else ""
        lost_reason = random.choice(LOST_REASONS) if stage == "Closed Lost" else ""
        win_reason = random.choice(WIN_REASONS) if stage == "Closed Won" else ""
        competitors = random.sample(["ServiceTitan", "Jobber", "FieldEdge", "Housecall Pro", "None"], k=random.randint(1, 2))

        rows.append({
            "opp_id": f"OPP-{i:04d}",
            "lead_id": lead["lead_id"],
            "company": lead["company"],
            "industry": lead["industry"],
            "state": lead["state"],
            "plan_type": plan,
            "tech_count": lead["tech_count"],
            "acv": int(acv),
            "mrr": int(mrr),
            "stage": stage,
            "ae_owner": lead["assigned_rep"],
            "created_date": lead["created_date"],
            "close_date": close_date.strftime("%Y-%m-%d"),
            "sales_cycle_days": days_in_pipeline,
            "demo_completed": "Yes" if stage not in ["New Lead", "Contacted"] else "No",
            "trial_started": random.choice(["Yes", "No"]) if stage in ["Demo/Evaluation", "Proposal Sent", "Closed Won"] else "No",
            "competitors_evaluated": "; ".join(competitors),
            "win_reason": win_reason,
            "lost_reason": lost_reason,
            "won_date": won_date,
            "probability_pct": {"Closed Won": 100, "Closed Lost": 0, "Negotiation": 75,
                                "Proposal Sent": 50, "Demo/Evaluation": 30, "Discovery": 15,
                                "Contacted": 5, "New Lead": 2}.get(stage, 10),
        })
    return rows

# ─── 3. CUSTOMERS ─────────────────────────────────────────────────────────

def gen_customers(n=640):
    rows = []
    for i in range(1, n + 1):
        plan = rand_plan()
        industry = rand_industry()
        tech_count = rand_tech_count(plan)
        mrr = round(PLANS[plan]["price"] * random.uniform(0.85, 1.4), 2)
        start = rand_date(datetime(2019, 6, 1), datetime(2024, 12, 1))
        contract_months = random.choice([12, 12, 12, 24, 24, 36])
        renewal = start + timedelta(days=contract_months * 30)
        csm = random.choice(CSMS)

        logins_30d = random.randint(0, 40)
        jobs_30d = random.randint(0, 60)
        mobile_pct = random.randint(10, 100)
        nps = random.randint(0, 10)
        open_tickets = random.randint(0, 6)
        hs = health_score(logins_30d, jobs_30d, mobile_pct, nps, open_tickets, plan)

        rows.append({
            "account_id": f"ACC-{i:04d}",
            "company": rand_company(industry),
            "industry": industry,
            "state": random.choice(STATES),
            "plan": plan,
            "tech_count": tech_count,
            "mrr": mrr,
            "arr": round(mrr * 12, 2),
            "contract_months": contract_months,
            "start_date": start.strftime("%Y-%m-%d"),
            "renewal_date": renewal.strftime("%Y-%m-%d"),
            "csm_owner": csm,
            "health_score": hs,
            "health_status": health_status(hs),
            "logins_last_30d": logins_30d,
            "jobs_dispatched_30d": jobs_30d,
            "mobile_adoption_pct": mobile_pct,
            "nps_score": nps,
            "open_p1p2_tickets": open_tickets,
            "last_login_date": (NOW - timedelta(days=random.randint(0, 45))).strftime("%Y-%m-%d"),
            "last_qbr_date": (NOW - timedelta(days=random.randint(30, 180))).strftime("%Y-%m-%d") if plan in ["Pro", "Enterprise"] else "",
            "analytics_addon": random.choice(["Yes", "No", "No", "No"]),
            "inventory_addon": random.choice(["Yes", "No", "No"]),
            "portal_pro_addon": random.choice(["Yes", "No", "No", "No"]),
            "churn_risk_flag": "Yes" if hs < 40 else "No",
            "expansion_potential": random.choice(["None", "Low", "Medium", "High"]),
        })
    return rows

# ─── 4. SUPPORT TICKETS ──────────────────────────────────────────────────

def gen_support_tickets(customers, n=1840):
    rows = []
    account_ids = [c["account_id"] for c in customers]
    # High-ticket accounts more likely to appear
    weights = [1 + (c["health_score"] < 40) * 3 for c in customers]

    for i in range(1, n + 1):
        account_id = random.choices(account_ids, weights=weights, k=1)[0]
        customer = next(c for c in customers if c["account_id"] == account_id)
        category = weighted_choice(TICKET_CATEGORIES, TICKET_CATEGORY_WEIGHTS)
        priority = weighted_choice(PRIORITIES, PRIORITY_WEIGHTS)
        agent = random.choice(SUPPORT_AGENTS)
        created = rand_date(datetime(2024, 1, 1), NOW)

        # Resolution time based on priority and category
        base_hours = {"P1": 4, "P2": 14, "P3": 28, "P4": 56}[priority]
        resolution_hours = base_hours * random.uniform(0.5, 2.5)
        resolved = created + timedelta(hours=resolution_hours)
        sla_target = {"P1": 4, "P2": 12, "P3": 48, "P4": 120}[priority]
        sla_breached = "Yes" if resolution_hours > sla_target else "No"
        csat = random.choices([1, 2, 3, 4, 5], weights=[0.04, 0.08, 0.15, 0.40, 0.33])[0]
        escalated = "Yes" if priority in ["P1", "P2"] and random.random() < 0.35 else "No"

        rows.append({
            "ticket_id": f"TKT-{i:05d}",
            "account_id": account_id,
            "company": customer["company"],
            "plan": customer["plan"],
            "category": category,
            "priority": priority,
            "status": random.choice(["Resolved", "Resolved", "Resolved", "Open", "Pending Customer"]),
            "subject": f"{category} issue — {random.choice(['urgent', 'help needed', 'not working', 'question', 'error'])}",
            "agent_assigned": agent,
            "created_date": created.strftime("%Y-%m-%d"),
            "created_time": created.strftime("%H:%M"),
            "resolved_date": resolved.strftime("%Y-%m-%d"),
            "resolution_hours": round(resolution_hours, 1),
            "sla_target_hours": sla_target,
            "sla_breached": sla_breached,
            "first_response_hours": round(resolution_hours * random.uniform(0.05, 0.3), 1),
            "escalated_to_tier2": escalated,
            "csat_score": csat,
            "reopened": "Yes" if random.random() < 0.11 else "No",
            "channel": random.choice(["Chat", "Chat", "Email", "Email", "Phone"]),
        })
    return rows

# ─── 5. ESCALATIONS ──────────────────────────────────────────────────────

def gen_escalations(tickets):
    escalated = [t for t in tickets if t["escalated_to_tier2"] == "Yes"]
    rows = []
    for i, ticket in enumerate(escalated[:220], 1):
        tier = random.choice(["Tier 2 – Senior SE", "Tier 2 – Senior SE", "Tier 3 – Engineering"])
        reason = random.choice([
            "Complex integration failure", "Data corruption concern",
            "Repeated escalation by same account", "SLA breach imminent",
            "Customer threatening churn", "P1 outage confirmed",
        ])
        resolved_hours = random.uniform(2, 72)
        rows.append({
            "escalation_id": f"ESC-{i:04d}",
            "ticket_id": ticket["ticket_id"],
            "account_id": ticket["account_id"],
            "company": ticket["company"],
            "plan": ticket["plan"],
            "original_priority": ticket["priority"],
            "escalated_to": tier,
            "escalation_reason": reason,
            "escalation_date": ticket["created_date"],
            "resolution_hours": round(resolved_hours, 1),
            "resolved": "Yes" if random.random() < 0.92 else "No",
            "root_cause": random.choice([
                "Third-party API change (QuickBooks)", "Known platform bug – patch released",
                "Customer misconfiguration", "Network/infrastructure issue",
                "Data migration error", "Permissions misconfiguration",
            ]),
            "customer_satisfaction_after": random.choices([1, 2, 3, 4, 5], weights=[0.06, 0.10, 0.20, 0.40, 0.24])[0],
            "required_engineering": "Yes" if "Engineering" in tier else "No",
        })
    return rows

# ─── 6. CHURN CASES ──────────────────────────────────────────────────────

def gen_churn_cases(customers, n=88):
    at_risk = [c for c in customers if c["health_status"] in ["Red", "Yellow"]]
    churned = random.sample(at_risk, min(n, len(at_risk)))
    rows = []
    for i, customer in enumerate(churned, 1):
        churn_date = rand_date(datetime(2024, 1, 1), NOW)
        reason = weighted_choice(CHURN_REASONS, [0.28, 0.21, 0.17, 0.16, 0.11, 0.07])
        save_attempted = random.random() < 0.72
        save_succeeded = False  # these are confirmed churns
        rows.append({
            "churn_id": f"CHR-{i:04d}",
            "account_id": customer["account_id"],
            "company": customer["company"],
            "plan": customer["plan"],
            "arr_lost": round(customer["arr"], 2),
            "mrr_lost": round(customer["mrr"], 2),
            "churn_date": churn_date.strftime("%Y-%m-%d"),
            "churn_reason_primary": reason,
            "churn_reason_secondary": random.choice(CHURN_REASONS + ["None"]),
            "health_score_at_churn": customer["health_score"],
            "health_status_at_churn": customer["health_status"],
            "days_since_last_login": random.randint(7, 90),
            "csm_owner": customer["csm_owner"],
            "save_attempted": "Yes" if save_attempted else "No",
            "save_offer_type": random.choice(["1-month credit", "Plan downgrade", "Price discount", "None"]) if save_attempted else "None",
            "save_succeeded": "No",
            "win_back_eligible": "Yes" if random.random() < 0.4 else "No",
            "competitor_moved_to": random.choice(["ServiceTitan", "Jobber", "FieldEdge", "None known"]),
            "contract_remaining_months": random.randint(0, 8),
        })
    return rows

# ─── 7. RENEWAL CASES ────────────────────────────────────────────────────

def gen_renewal_cases(customers, n=310):
    eligible = [c for c in customers if c["health_status"] in ["Green", "Yellow"]]
    sample = random.sample(eligible, min(n, len(eligible)))
    rows = []
    for i, customer in enumerate(sample, 1):
        original_acv = round(customer["arr"], 2)
        outcome = weighted_choice(["Renewed", "Renewed", "Renewed", "Renewed with Upsell", "Churned", "Downgraded"],
                                   [0.35, 0.25, 0.15, 0.18, 0.04, 0.03])
        upsell_amount = round(original_acv * random.uniform(0.08, 0.25), 2) if "Upsell" in outcome else 0
        new_acv = original_acv + upsell_amount if "Renewed" in outcome else (original_acv * 0.7 if "Downgraded" in outcome else 0)
        renewal_date = rand_date(datetime(2024, 1, 1), NOW + timedelta(days=180))
        rows.append({
            "renewal_id": f"RNW-{i:04d}",
            "account_id": customer["account_id"],
            "company": customer["company"],
            "plan": customer["plan"],
            "csm_owner": customer["csm_owner"],
            "renewal_date": renewal_date.strftime("%Y-%m-%d"),
            "original_acv": original_acv,
            "new_acv": round(new_acv, 2),
            "acv_change": round(new_acv - original_acv, 2),
            "outcome": outcome,
            "upsell_product_added": random.choice(["Analytics Add-On", "Parts Inventory", "Portal Pro", "Extra Seats", "None"]) if upsell_amount > 0 else "None",
            "upsell_arr_added": upsell_amount,
            "renewal_cycle_days": random.randint(14, 75),
            "multi_year": random.choice(["Yes", "No", "No", "No"]),
            "discount_offered": random.choice(["None", "None", "None", "5%", "8%", "10%"]),
            "health_score_at_renewal": customer["health_score"],
            "qbr_held_before_renewal": random.choice(["Yes", "Yes", "No"]) if customer["plan"] in ["Pro", "Enterprise"] else "No",
            "days_to_renewal_when_engaged": random.randint(30, 90),
        })
    return rows

# ─── 8. ONBOARDING CASES ────────────────────────────────────────────────

def gen_onboarding_cases(customers, n=420):
    sample = random.sample(customers, min(n, len(customers)))
    rows = []
    delays = [
        "Customer unresponsive", "Data migration issues", "QuickBooks sync failure",
        "Technician app resistance", "Champion left – restart required", "None",
    ]
    for i, customer in enumerate(sample, 1):
        kickoff = rand_date(datetime(2022, 6, 1), datetime(2024, 10, 1))
        target_days = 21
        actual_days = random.choices(
            [14, 18, 21, 25, 30, 38, 48, 60],
            weights=[0.05, 0.10, 0.20, 0.20, 0.18, 0.12, 0.10, 0.05]
        )[0]
        go_live = kickoff + timedelta(days=actual_days)
        primary_delay = random.choice(delays) if actual_days > 21 else "None"
        phase = random.choice(["Kickoff", "Configuration", "Data Migration", "Integrations", "Training", "Go-Live", "Completed"])
        rows.append({
            "onboarding_id": f"ONB-{i:04d}",
            "account_id": customer["account_id"],
            "company": customer["company"],
            "plan": customer["plan"],
            "csm_owner": customer["csm_owner"],
            "kickoff_date": kickoff.strftime("%Y-%m-%d"),
            "go_live_date": go_live.strftime("%Y-%m-%d"),
            "target_days_to_value": target_days,
            "actual_days_to_value": actual_days,
            "on_time": "Yes" if actual_days <= target_days else "No",
            "delay_days": max(0, actual_days - target_days),
            "primary_delay_reason": primary_delay,
            "current_phase": phase if phase != "Completed" else "Completed",
            "completed": "Yes" if phase == "Completed" else "No",
            "kickoff_call_held": "Yes" if random.random() > 0.05 else "No",
            "data_migration_complete": "Yes" if actual_days >= 18 else "No",
            "quickbooks_connected": "Yes" if actual_days >= 21 and customer["plan"] != "Starter" else random.choice(["Yes", "No"]),
            "tech_app_adopted": "Yes" if customer["mobile_adoption_pct"] >= 60 else "No",
            "first_invoice_sent": "Yes" if actual_days <= 28 else "No",
            "health_score_at_day30": customer["health_score"],
            "nps_at_day30": customer["nps_score"],
        })
    return rows

# ─── 9. ACCOUNT NOTES ────────────────────────────────────────────────────

def gen_account_notes(customers, n=2200):
    rows = []
    account_ids = [c["account_id"] for c in customers]
    account_map = {c["account_id"]: c for c in customers}
    note_templates = {
        "Call": ["Spoke with {contact} re: {topic}. Action: {action}.",
                 "Check-in call completed. Customer {sentiment}. Next step: {action}."],
        "Email": ["Sent renewal email — awaiting response.", "Followed up on {topic}. No response yet.",
                  "Customer replied re: {topic}. {sentiment}."],
        "QBR": ["QBR held with {contact}. Reviewed usage metrics, discussed {topic}. Customer {sentiment}.",
                "Quarterly review completed. Key wins discussed. Upsell opportunity: {action}."],
        "Health Check": ["Health score reviewed: {score}. Status: {status}. {action} flagged.",
                         "Weekly health check — score {score}. Mobile adoption at risk."],
        "Escalation": ["Escalated ticket re: QuickBooks sync. Engineering engaged.",
                       "Customer escalated billing issue. Resolved within {hours} hours."],
        "Renewal Discussion": ["Renewal discussion initiated. Contract ends in {days} days. Customer {sentiment}.",
                               "Renewal proposal sent. Upsell discussed: Analytics Add-On."],
        "Upsell Attempt": ["Presented Analytics Add-On demo. Customer {sentiment}.",
                           "Discussed seat expansion — customer added {n} techs. MRR increase: ${mrr}."],
    }
    contacts = ["the owner", "ops director", "office manager", "IT lead", "the GM"]
    topics = ["billing", "QuickBooks integration", "mobile app adoption", "scheduling features", "reporting", "pricing"]
    actions = ["schedule follow-up", "send documentation", "loop in SE", "escalate to VP CS", "send upsell proposal"]
    sentiments = ["positive", "neutral", "frustrated", "excited about new features", "considering cancellation"]

    for i in range(1, n + 1):
        account_id = random.choice(account_ids)
        customer = account_map[account_id]
        note_type = weighted_choice(NOTE_TYPES, [0.25, 0.20, 0.12, 0.15, 0.08, 0.12, 0.08])
        created = rand_date(datetime(2023, 1, 1), NOW)
        templates = note_templates.get(note_type, ["Note recorded."])
        template = random.choice(templates)
        note = (template
                .replace("{contact}", random.choice(contacts))
                .replace("{topic}", random.choice(topics))
                .replace("{action}", random.choice(actions))
                .replace("{sentiment}", random.choice(sentiments))
                .replace("{score}", str(customer["health_score"]))
                .replace("{status}", customer["health_status"])
                .replace("{hours}", str(random.randint(2, 24)))
                .replace("{days}", str(random.randint(30, 90)))
                .replace("{n}", str(random.randint(1, 5)))
                .replace("{mrr}", str(random.randint(100, 500))))

        rows.append({
            "note_id": f"NOTE-{i:05d}",
            "account_id": account_id,
            "company": customer["company"],
            "note_type": note_type,
            "author": customer["csm_owner"],
            "created_date": created.strftime("%Y-%m-%d"),
            "note_content": note,
            "follow_up_required": random.choice(["Yes", "No", "No"]),
            "follow_up_date": (created + timedelta(days=random.randint(3, 14))).strftime("%Y-%m-%d") if random.random() < 0.4 else "",
        })
    return rows

# ─── Writer ───────────────────────────────────────────────────────────────

def write_csv(filename, rows):
    if not rows:
        print(f"  ⚠ No rows for {filename}")
        return
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✓ {filename:35s} {len(rows):>5} rows  →  {path}")

# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    print("\n🚀 Nuvoro Data Generator — Starting\n")
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}\n")

    print("Generating datasets...")
    leads = gen_leads(500)
    write_csv("leads.csv", leads)

    opportunities = gen_opportunities(leads)
    write_csv("opportunities.csv", opportunities)

    customers = gen_customers(640)
    write_csv("customers.csv", customers)

    tickets = gen_support_tickets(customers, 1840)
    write_csv("support_tickets.csv", tickets)

    escalations = gen_escalations(tickets)
    write_csv("escalations.csv", escalations)

    churns = gen_churn_cases(customers, 88)
    write_csv("churn_cases.csv", churns)

    renewals = gen_renewal_cases(customers, 310)
    write_csv("renewal_cases.csv", renewals)

    onboardings = gen_onboarding_cases(customers, 420)
    write_csv("onboarding_cases.csv", onboardings)

    notes = gen_account_notes(customers, 2200)
    write_csv("account_notes.csv", notes)

    print(f"""
╔══════════════════════════════════════════════════════════╗
║           Nuvoro Data Generation Complete ✓              ║
╠══════════════════════════════════════════════════════════╣
║  9 CSV files saved to: ./nuvoro_data/                    ║
║                                                          ║
║  Next steps:                                             ║
║  1. Open CSVs in Excel — start with customers.csv        ║
║  2. Import into SQLite: sqlite3 nuvoro.db                ║
║     then: .import nuvoro_data/customers.csv customers    ║
║  3. Import into Salesforce via Data Import Wizard        ║
║  4. Connect SQLite to Metabase as a database source      ║
╚══════════════════════════════════════════════════════════╝
""")

if __name__ == "__main__":
    main()
