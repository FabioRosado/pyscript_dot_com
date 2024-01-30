from pyscript_dot_com import proxy


def test_proxy_happy_path():
    """Test that we can call a proxy."""
    assert proxy("test") == 1
