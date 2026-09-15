from prototype.expense_checker import check_expense,extract_expense

def test_passes_within_limit():
    assert check_expense('travel',4200).status=='PRECHECK_PASS'

def test_escalates_exception():
    assert check_expense('meals',2500).status=='HUMAN_REVIEW'

def test_extracts_facts():
    c,a=extract_expense('travel expense INR 4200')
    assert c=='travel' and a==4200
