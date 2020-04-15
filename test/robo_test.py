from app.robo_advisor import to_usd

def test_to_usd():
    result = to_usd(3.47)
    assert result == f"${3.47:,.2f}"
