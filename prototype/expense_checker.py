"""Deterministic, human-in-the-loop expense compliance pre-check."""
import re
from dataclasses import dataclass

POLICY_LIMITS={"travel":5000.0,"meals":2000.0,"office":3000.0,"other":1000.0}

@dataclass
class CheckResult:
    status:str
    category:str|None
    amount:float|None
    reason:str

def extract_expense(text:str):
    category=None
    lower=text.lower()
    for c in POLICY_LIMITS:
        if c in lower: category=c; break
    m=re.search(r"(?:₹|rs\.?|inr)?\s*([0-9]+(?:,[0-9]{3})*(?:\.\d+)?)",text,re.I)
    amount=float(m.group(1).replace(",","")) if m else None
    return category,amount

def check_expense(category,amount):
    if category not in POLICY_LIMITS or amount is None:
        return CheckResult("HUMAN_REVIEW",category,amount,"missing or unrecognized policy facts")
    limit=POLICY_LIMITS[category]
    if amount<=limit:
        return CheckResult("PRECHECK_PASS",category,amount,f"within {category} limit of {limit:g}")
    return CheckResult("HUMAN_REVIEW",category,amount,f"exceeds {category} limit of {limit:g}")

def main():
    examples=["travel expense INR 4200","meals expense ₹2500","unknown expense 500"]
    for text in examples:
        c,a=extract_expense(text); print(text,"->",check_expense(c,a))

if __name__=="__main__": main()
