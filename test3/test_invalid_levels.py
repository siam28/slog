import pytest
from slog import *

def test_invalid_log_levels():
    for invalid_num in [-1, 6, 1.5]:
        with pytest.raises(SlogLevelError) as e:
            s = Slog(loglvl=invalid_num)
        assert 'is not a valid Slog log level.'.format(invalid_num) in str(e.value)

    for num_str in ['foo', '0', '-1', '6', '1.5']:
        with pytest.raises(SlogLevelError) as e:
            s = Slog(loglvl=num_str)
        assert 'is not a valid Slog log level.' in str(e.value)

    for invalid_str in ['foo', '0', '-1', '6', '1.5']:
        with pytest.raises(SlogLevelError) as e:
            s = Slog(loglvl=invalid_str)
        assert 'is not a valid Slog log level.' in str(e.value)

