import numpy as np
from src.backtesting import BacktestInput, backtest_summary


def load_data():
    pnl = np.random.normal(0, 1, 1000)
    var = np.full(1000, 2.33)
    return pnl, var


def main():
    pnl, var = load_data()
    bt = BacktestInput(pnl=pnl, var=var, alpha=0.99)
    out = backtest_summary(bt)
    print(out)


if __name__ == "__main__":
    main()