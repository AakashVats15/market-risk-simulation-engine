from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from scipy.stats import chi2


@dataclass
class BacktestInput:
    pnl: np.ndarray
    var: np.ndarray
    alpha: float

    def validate(self) -> None:
        if len(self.pnl) != len(self.var):
            raise ValueError("PnL and VaR series must have the same length.")
        if not (0 < self.alpha < 1):
            raise ValueError("alpha must be between 0 and 1.")
        if np.any(self.var < 0):
            raise ValueError("VaR values must be non-negative.")


def count_exceptions(pnl: np.ndarray, var: np.ndarray) -> tuple[np.ndarray, int]:
    exceptions = pnl < -var
    return exceptions, int(np.sum(exceptions))


def kupiec_pof_test(exceptions: np.ndarray, alpha: float) -> tuple[float, float, bool]:
    T = len(exceptions)
    x = np.sum(exceptions)
    pi_hat = x / T
    pi_0 = 1 - alpha
    pi_hat = max(min(pi_hat, 1 - 1e-12), 1e-12)
    logL_null = x * np.log(pi_0) + (T - x) * np.log(1 - pi_0)
    logL_alt = x * np.log(pi_hat) + (T - x) * np.log(1 - pi_hat)
    lr_stat = -2 * (logL_null - logL_alt)
    p_value = 1 - chi2.cdf(lr_stat, df=1)
    return lr_stat, p_value, p_value > 0.05


def christoffersen_independence_test(exceptions: np.ndarray) -> tuple[np.ndarray, float, float, bool]:
    n00 = n01 = n10 = n11 = 0
    for t in range(1, len(exceptions)):
        prev, curr = exceptions[t - 1], exceptions[t]
        if prev == 0 and curr == 0:
            n00 += 1
        elif prev == 0 and curr == 1:
            n01 += 1
        elif prev == 1 and curr == 0:
            n10 += 1
        else:
            n11 += 1

    transition_matrix = np.array([[n00, n01], [n10, n11]])
    pi_0 = n01 / (n00 + n01) if (n00 + n01) > 0 else 1e-12
    pi_1 = n11 / (n10 + n11) if (n10 + n11) > 0 else 1e-12
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    logL_null = (n01 + n11) * np.log(pi) + (n00 + n10) * np.log(1 - pi)
    logL_alt = (
        n01 * np.log(pi_0) +
        n00 * np.log(1 - pi_0) +
        n11 * np.log(pi_1) +
        n10 * np.log(1 - pi_1)
    )
    lr_stat = -2 * (logL_null - logL_alt)
    p_value = 1 - chi2.cdf(lr_stat, df=1)
    return transition_matrix, lr_stat, p_value, p_value > 0.05


def backtest_summary(bt: BacktestInput) -> dict:
    bt.validate()
    exceptions, n_exceptions = count_exceptions(bt.pnl, bt.var)
    expected_exceptions = len(bt.pnl) * (1 - bt.alpha)
    kupiec_lr, kupiec_p, kupiec_pass = kupiec_pof_test(exceptions, bt.alpha)
    trans_mat, christ_lr, christ_p, christ_pass = christoffersen_independence_test(exceptions)
    overall_pass = kupiec_pass and christ_pass

    return {
        "exceptions": n_exceptions,
        "expected_exceptions": expected_exceptions,
        "kupiec_lr": kupiec_lr,
        "kupiec_p_value": kupiec_p,
        "kupiec_pass": kupiec_pass,
        "christoffersen_matrix": trans_mat,
        "christoffersen_lr": christ_lr,
        "christoffersen_p_value": christ_p,
        "christoffersen_pass": christ_pass,
        "overall_pass": overall_pass
    }