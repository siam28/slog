import pytest
from slog import *

def test_old_imports():
    with pytest.raises(ImportError) as e:
        from slog import slog
    assert "cannot import name slog" in str(e.value)

    with pytest.raises(ImportError) as e:
        from slog.slog import Slog
    assert "No module named slog" in str(e.value)

    with pytest.raises(ImportError) as e:
        import slog.slog
    assert "No module named slog" in str(e.value)

