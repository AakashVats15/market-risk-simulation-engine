import numpy as np
from src.backtesting import (
    BacktestInput,
    count_exceptions,
    kupiec_pof_test,
    christoffersen_independence_test,
    backtest_summary
)


def test_exception_counting():
    pnl = np.array([1, -5, 2, -3])
    var = np.array([2, 4, 1, 2])
    exceptions, n = count_exceptions(pnl, var)
    assert n == 2
    assert exceptions.tolist() == [False, True, False, True]


def test_kupiec_pof_test():
    exceptions = np.array([0, 0, 0, 1, 0, 0, 0, 0])
    lr, p, passed = kupiec_pof_test(exceptions, 0.99)
    assert lr >= 0
    assert 0 <= p <= 1
    assert isinstance(passed, bool)


def test_christoffersen_independence_test():
    exceptions = np.array([0, 1, 0, 1, 0, 1])
    mat, lr, p, passed = christoffersen_independence_test(exceptions)
    assert mat.shape == (2, 2)
    assert lr >= 0
    assert 0 <= p <= 1
    assert isinstance(passed, bool)


def test_backtest_summary():
    pnl = np.array([1, -3, 2, -4, 1])
    var = np.array([2, 2, 1, 3, 1])
    bt = BacktestInput(pnl=pnl, var=var, alpha=0.99)
    out = backtest_summary(bt)
    assert "exceptions" in out
    assert "kupiec_p_value" in out
    assert "christoffersen_matrix" in out
    assert isinstance(out["overall_pass"], bool)