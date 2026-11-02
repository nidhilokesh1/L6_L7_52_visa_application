import pytest
from visa_application import visa_fee, documents_complete, application_status

# Test cases to achieve 100% Code Coverage

def test_visa_fee_invalid_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("invalid_type", 1, "normal", "B")

def test_visa_fee_negative_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")

def test_visa_fee_included_entries_nationality_a_non_student():
    # tourist base=1, nationality A -> included = 2. entries = 2 -> extra = 0
    assert visa_fee("tourist", 2, "normal", "A") == 0

def test_visa_fee_included_entries_nationality_a_student():
    # student base=2, nationality A -> included remains 2. entries = 2 -> extra = 0
    assert visa_fee("student", 2, "normal", "A") == 0

def test_visa_fee_normal_rate_low_extra():
    # tourist base=1, nationality B -> included = 1. entries = 3 -> extra = 2 (<= 5). speed normal -> rate = 40. fee = 2 * 40 = 80
    assert visa_fee("tourist", 3, "normal", "B") == 80

def test_visa_fee_express_rate_low_extra():
    # tourist base=1, nationality B -> included = 1. entries = 3 -> extra = 2 (<= 5). speed express -> rate = 100. fee = 2 * 100 = 200
    assert visa_fee("tourist", 3, "express", "B") == 200

def test_visa_fee_normal_rate_high_extra():
    # tourist base=1, nationality B -> included = 1. entries = 7 -> extra = 6 (> 5). speed normal -> rate = 40 + 20 = 60. fee = 6 * 60 = 360
    assert visa_fee("tourist", 7, "normal", "B") == 360

def test_visa_fee_express_rate_high_extra():
    # tourist base=1, nationality B -> included = 1. entries = 7 -> extra = 6 (> 5). speed express -> rate = 100 + 20 + 10 = 130. fee = 6 * 130 = 780
    assert visa_fee("tourist", 7, "express", "B") == 780

def test_documents_complete_renewal_true():
    assert documents_complete(forms_filed=1, photos=0, is_renewal=True) is True

def test_documents_complete_renewal_false_forms():
    assert documents_complete(forms_filed=0, photos=0, is_renewal=True) is False

def test_documents_complete_low_photos():
    assert documents_complete(forms_filed=5, photos=1, is_renewal=False) is False

def test_documents_complete_new_success():
    assert documents_complete(forms_filed=3, photos=2, is_renewal=False) is True

def test_documents_complete_new_insufficient_forms():
    assert documents_complete(forms_filed=2, photos=2, is_renewal=False) is False

def test_application_status_express_peak_open():
    # express cutoff=10, peak cutoff=25. days_left=25 -> open
    assert application_status(25, is_express=True, is_peak_season=True) == "open"

def test_application_status_express_non_peak_closing():
    # express cutoff=10, non-peak cutoff=10. cutoff-15 = -5. days_left=0 -> closing
    assert application_status(0, is_express=True, is_peak_season=False) == "closing"

def test_application_status_normal_non_peak_closed():
    # normal cutoff=30, non-peak cutoff=30. cutoff-15 = 15. days_left=10 -> closed
    assert application_status(10, is_express=False, is_peak_season=False) == "closed"

def test_application_status_normal_peak_open():
    # normal cutoff=30, peak cutoff=45. days_left=45 -> open
    assert application_status(45, is_express=False, is_peak_season=True) == "open"
