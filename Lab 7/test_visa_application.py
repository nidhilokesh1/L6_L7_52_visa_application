from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee

# -------------------------------------------------------------
# Fuzzing / Property-Based Tests with Hypothesis
# Goal: Uncover edge cases automatically and ensure no crashes occur.
# -------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    """
    Fuzz test for parse_application.
    Verifies that for any random unicode string or None, the function never crashes.
    """
    try:
        result = parse_application(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
    except Exception as e:
        assert False, f"parse_application crashed with: {e}"


@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    """
    Fuzz test for processing_average.
    Verifies that for any random unicode string or None, the function never crashes.
    """
    try:
        result = processing_average(s)
        assert isinstance(result, int)
        assert result >= 0
    except Exception as e:
        assert False, f"processing_average crashed with: {e}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    """
    Fuzz test for payable_fee.
    Verifies that for any random unicode string or None, the function never crashes.
    """
    try:
        result = payable_fee(s)
        assert isinstance(result, float)
        assert result >= 0.0
    except Exception as e:
        assert False, f"payable_fee crashed with: {e}"


# -------------------------------------------------------------
# Targeted Property and Specific Input Tests
# -------------------------------------------------------------

@given(
    visa_name=st.text(alphabet=st.characters(categories=["L"]), min_size=1, max_size=20),
    entries=st.integers(min_value=0, max_value=100)
)
def test_parse_application_valid_inputs(visa_name, entries):
    """Verifies that valid inputs are parsed correctly."""
    text = f"{visa_name}:{entries}"
    parsed_type, parsed_entries = parse_application(text)
    assert parsed_type == visa_name.strip().title()
    assert parsed_entries == entries


@given(st.lists(st.integers(min_value=1, max_value=365), min_size=1, max_size=50))
def test_processing_average_valid_list(days):
    """Verifies that valid comma-separated days compute correct integer average."""
    days_csv = ",".join(str(d) for d in days)
    avg = processing_average(days_csv)
    expected = sum(days) // len(days)
    assert avg == expected


@given(
    fee=st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=1e5, allow_nan=False, allow_infinity=False)
)
def test_payable_fee_valid_inputs(fee, discount):
    """Verifies fee calculation with 18% tax and discount."""
    text = f"{fee}|{discount}"
    result = payable_fee(text)
    expected = round(max(fee * 1.18 - discount, 0.0), 2)
    assert abs(result - expected) < 1e-2


def test_edge_cases_and_invalid_inputs():
    """Specific regression edge case tests identified during fuzzing."""
    # Empty and None inputs
    assert parse_application("") == (None, None)
    assert parse_application(None) == (None, None)
    assert parse_application(":") == (None, None)
    assert parse_application("tourist:notanumber") == (None, None)
    assert parse_application("student:-5") == (None, None)
    assert parse_application("tourist:1:extra") == (None, None)

    # Empty and None for processing_average
    assert processing_average("") == 0
    assert processing_average(None) == 0
    assert processing_average(",,,") == 0
    assert processing_average("invalid,values,only") == 0
    assert processing_average("5,invalid,15") == 10  # skips invalid item gracefully

    # Empty and None for payable_fee
    assert payable_fee("") == 0.0
    assert payable_fee(None) == 0.0
    assert payable_fee("|") == 0.0
    assert payable_fee("abc|def") == 0.0
    assert payable_fee("-500|50") == 0.0
    assert payable_fee("100|500") == 0.0  # discount exceeds fee+tax, clamps to 0.0
