from datetime import datetime

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from rqdatac import bond

from scipy.interpolate import interp1d
from rqattribution.exceptions import Continue
from rqattribution.analysis.context_v2 import analysis_context


def campisi_attribution_main(
    holding_returns: Series,
    no_deferral_holding_returns: Series,
    previous_valuation: DataFrame,
    current_valuation: DataFrame,
    prev_date: datetime,
    date: datetime,
    coupon_payment: Series,
) -> DataFrame:
    """campisi 归因主入口.

    Args:
        holding_returns: 可以通过中债估值得到的持仓收益, 可通过 `analysis_context_v2.cjhx_attr_utils.calc_valuation_attribution` 计算得到.
        no_deferral_holding_returns: 没有期限跳跃收益部分债券的持仓收益.
        previous_valution: T-1日中债估值.  index - order_book_id.
        current_valuation: T日中债估值.  index - order_book_id.
        prev_date: T-1日
        date: T日
        coupon_payment: 票息信息.  index - order_book_id, value: 票息
    Returns:
        针对 holding_returns 中的给定债券的拆解结果.
        index - order_book_id
    """

    previous_valuation = previous_valuation.dropna(subset=["modified_duration", "ytm", "time_to_maturity"])
    current_valuation = current_valuation.dropna(subset=["ytm", "time_to_maturity"])

    # 缺失所需计算字段的持仓收益计入残余收益
    filtered_bond_list = previous_valuation.index.intersection(current_valuation.index).intersection(
        no_deferral_holding_returns.index
    )
    previous_valuation = previous_valuation.loc[filtered_bond_list]
    current_valuation = current_valuation.loc[filtered_bond_list]
    coupon_payment = coupon_payment.loc[filtered_bond_list]

    campisi_attributions = calc_daily_campisi_attribution(
        no_deferral_holding_returns,
        previous_valuation,
        current_valuation,
        prev_date,
        date,
        coupon_payment,
    )

    campisi_attributions = campisi_attributions.reindex(holding_returns.index)

    campisi_attributions["no_holding_residual"] = np.where(
        pd.isnull(campisi_attributions.coupon_return), holding_returns, 0
    )

    campisi_attributions.fillna(0, inplace=True)
    return campisi_attributions


def calc_daily_campisi_attribution(
    holding_returns: Series,
    previous_valuation: DataFrame,
    current_valuation: DataFrame,
    previous_date: datetime,
    date: datetime,
    coupon_payment: Series,
) -> DataFrame:

    # 计算应计利息变动
    # 应计利息变动 = 当日应计利息 - 前一日应计利息 + 当日票息支付
    # fmt: off
    accrued_interest_change = current_valuation["accrued_interest_eod"] - previous_valuation["accrued_interest_eod"] + coupon_payment
    # fmt: on

    # 获取曲线数据和基准利率
    mdprovider = analysis_context.mdprovider_api
    prev_curve = mdprovider.get_yield_curve("中债国债收益率曲线", previous_date)
    if prev_curve is None:
        raise Continue(f"中债国债收益率曲线在 {previous_date} 缺失, 跳过该日计算")
    cur_curve = mdprovider.get_yield_curve("中债国债收益率曲线", date)
    if cur_curve is None:
        raise Continue(f"中债国债收益率曲线在 {date} 缺失, 跳过该日计算")
    interest_rate_df = calc_yield_curve_change(previous_valuation, current_valuation, prev_curve, cur_curve)
    key_rate = [0.25, 0.5, 1, 3, 5, 7, 10, 30]
    yield_curve_averaged_shift = (cur_curve - prev_curve).loc[key_rate].mean()

    day_interval = (date - previous_date).days
    delta_time = day_interval / 365
    previous_modified_duration = previous_valuation.modified_duration

    attribution_terms_dict = {}

    # 1 票息收益 = 当日应计利息变动/前一日日终全价
    attribution_terms_dict["coupon_return"] = accrued_interest_change / previous_valuation.dirty_price_eod

    # 2 收敛收益 = 当天ytm * 时间间隔 - 当天的票息收益
    attribution_terms_dict["pull_to_par_return"] = (
        current_valuation.ytm * delta_time - attribution_terms_dict["coupon_return"]
    )

    # 3 骑乘收益 = - 前一日修正久期 * （前一日曲线当日ttm - 前一日曲线前一日ttm）
    attribution_terms_dict["carry_return"] = -previous_modified_duration * (
        interest_rate_df.previous_curve_current_ttm - interest_rate_df.previous_curve_previous_ttm
    )

    # 4 平移收益 = - 前一日修正久期*当日国债曲线利率变动均值
    attribution_terms_dict["shift_return"] = -previous_modified_duration.multiply(yield_curve_averaged_shift)

    # 5 扭转收益 = - 前一日修正久期*(当日曲线当日ttm - 前一日曲线当日ttm - 当天曲线关键利率均值 + 前一天曲线关键利率均值)
    current_yield_keys_rate_mean = cur_curve.loc[key_rate].mean()
    previous_yield_keys_rate_mean = prev_curve.loc[key_rate].mean()
    twist_change = (
        interest_rate_df.current_curve_current_ttm
        - interest_rate_df.previous_curve_current_ttm
        - current_yield_keys_rate_mean
        + previous_yield_keys_rate_mean
    )
    attribution_terms_dict["twist_return"] = -previous_modified_duration.multiply(twist_change)

    # 7 利差收益 = - 前一日修正久期 *（当日ytm - 当日曲线当日ttm - 前一日ytm + 前一日曲线当日ttm）
    spread_change = (
        current_valuation["ytm"]
        - previous_valuation["ytm"]
        - interest_rate_df.current_curve_current_ttm
        + interest_rate_df.previous_curve_current_ttm
    )
    attribution_terms_dict["spread_return"] = -previous_modified_duration.multiply(spread_change)

    attribution_terms_df = pd.DataFrame.from_dict(attribution_terms_dict)

    # 残余收益
    attribution_terms_df["campisi_residual"] = holding_returns.loc[
        attribution_terms_df.index
    ] - attribution_terms_df.sum(axis=1)

    # 需要额外增加曲线管理 = 平移 + 扭转 (这里最后算, 否则残余收益会算不对)
    attribution_terms_df["curve_return"] = (
        attribution_terms_df["shift_return"] + attribution_terms_df["twist_return"]
    )

    attribution_terms_df["campisi_holding_returns"] = holding_returns.loc[attribution_terms_df.index]

    return attribution_terms_df


def calc_yield_curve_change(
    previous_valuation: DataFrame,
    current_valuation: DataFrame,
    previous_curve: Series,
    current_curve: Series,
):
    # 线性插值获取曲线到期收益率
    def _yield_curve_fitting(period_of_repayment, benchmark_yield_curve):
        curve_fitting = interp1d(
            np.array(benchmark_yield_curve.index),
            benchmark_yield_curve.values.reshape(1, (len(benchmark_yield_curve)))[0],
            kind="linear",
            fill_value="extrapolate",
        )
        return pd.Series(data=curve_fitting(period_of_repayment), index=period_of_repayment.index)

    interest_rate_df = pd.DataFrame()
    # fmt: off
    interest_rate_df['previous_curve_previous_ttm'] = _yield_curve_fitting(previous_valuation.time_to_maturity, previous_curve)
    interest_rate_df['previous_curve_current_ttm'] = _yield_curve_fitting(current_valuation.time_to_maturity, previous_curve)
    interest_rate_df['current_curve_current_ttm'] = _yield_curve_fitting(current_valuation.time_to_maturity, current_curve)
    interest_rate_df['current_curve_previous_ttm'] = _yield_curve_fitting(previous_valuation.time_to_maturity, current_curve)
    # fmt: on

    return interest_rate_df
