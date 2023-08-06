from datetime import datetime

from typing import Dict, List, Optional, Any

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

from rqattribution import analysis_context_v2
from rqattribution.analysis.plugin_apis import CachedPriceProvider
from rqattribution.logger import logger
from rqattribution.const import AssetType
from rqattribution_campisi import attribution, allocation_selection
from rqattribution_campisi.const import attr_tree
from rqattribution.exceptions import Continue


def fe_fetcher(id: str, model_name: str) -> Any:
    fetcher = analysis_context_v2.default_result_fetcher
    report = fetcher(id, model_name)
    if report is not None:
        return report["summary"]
    return []


@analysis_context_v2.analysis_func(name="fixed_income/campisi", result_fetcher=fe_fetcher)
class CampisiAttribution:
    @classmethod
    def daily_attribution(cls, weights: Series, returns: Series, benchmark_info: Dict) -> Dict[str, Dict]:
        """ 创金合信 campisi 归因. """
        # extrace out date fields.
        previous_date = weights.index.get_level_values("date")[0]
        date = returns.index.get_level_values("date")[0]

        # only need bond, remove asset_type level.
        previous_weights = weights.xs(AssetType.BOND, level="asset_type")
        current_returns = returns.xs(AssetType.BOND, level="asset_type")
        if previous_weights.empty:
            logger.warn(f"{previous_date} 没有债券权重数据, 跳过")
            return {"portfolio": None, "benchmark": None}

        previous_weights.reset_index(level="date", drop=True, inplace=True)
        current_returns.reset_index(level="date", drop=True, inplace=True)

        attribution = daily_campisi_attribution(
            previous_weights, current_returns, previous_date, date, benchmark_info, as_dict=True
        )
        return attribution

    @classmethod
    def multidays_attribution(
        cls, daily_attribution: Dict, user_start_date: datetime, as_tree=True
    ) -> Dict:
        daily_attribution = analysis_context_v2.daily_attr_converter.daily_to_df(daily_attribution)
        attribution_summary, bonds_attribution = multidays_campisi_attribution(
            daily_attribution["portfolio"], daily_attribution["benchmark"]
        )
        if as_tree:
            return {
                "summary": attr_tree.to_list(attribution_summary),
                "bonds": bonds_attribution.to_dict("records"),
            }
        else:
            return {
                "summary": attribution_summary,
                "bonds": bonds_attribution
            }


def multidays_campisi_attribution(p_daily_attribution, b_daily_attribution):
    linking_coef = analysis_context_v2.linking_algo_api.linking_coef

    p_returns = p_daily_attribution["attribution_terms"]["returns"]
    p_coef = linking_coef(p_returns, Series(0, index=p_returns.index))
    p_attribution_terms = p_daily_attribution["attribution_terms"].T.dot(p_coef)

    b_returns = b_daily_attribution["attribution_terms"]["returns"]
    b_coef = linking_coef(b_returns, Series(0, index=b_returns.index))
    b_attribution_terms = b_daily_attribution["attribution_terms"].T.dot(b_coef)

    active_returns = p_returns - b_returns
    active_coef = linking_coef(p_returns, b_returns)
    active_daily_attribution = p_daily_attribution["attribution_terms"].sub(b_daily_attribution["attribution_terms"], fill_value=0)
    active_daily_attribution["allocation_spread"] = b_daily_attribution["allocation"]["total"]
    active_daily_attribution["selection_spread"] = b_daily_attribution["selection"]["total"]
    active_attribution_terms = active_daily_attribution.T.dot(active_coef)

    # calc brinson, and attach the result to active_attribution_terms.
    # fmt: off
    # 主动的 allocation-selection 都归在benchmark中
    active_attribution_terms["allocation_spread"] = b_daily_attribution["allocation"].T.dot(active_coef)["total"]
    active_attribution_terms["selection_spread"] = b_daily_attribution["selection"].T.dot(active_coef)["total"]

    # for portfolio, benchmark's allocation-selection return.
    # just fill with na value.
    for k in ["allocation_spread", "selection_spread"]:
        p_attribution_terms[k] = float("nan")
        b_attribution_terms[k] = float("nan")

    # calc volatility.
    p_std = p_returns.std()
    p_volatility = p_daily_attribution["attribution_terms"].apply(lambda x: x.cov(p_returns) / p_std)

    b_std = b_returns.std()
    b_volatility = b_daily_attribution["attribution_terms"].apply(lambda x: x.cov(b_returns) / b_std)

    active_std = active_returns.std()
    active_volatility = active_daily_attribution.apply(lambda x: x.cov(active_returns) / active_std)

    # calculate bonds multidays attribution.
    dfs = []
    for order_book_id, df in p_daily_attribution["bonds_attribution_terms"].groupby("order_book_id"):
        p_coef_work = p_coef.reindex(index=df.index)
        df = df.drop(columns=["order_book_id"])
        attribution_terms = df.T.dot(p_coef_work)
        returns = df["returns"]
        std = returns.std()
        volatility = df.apply(lambda x: x.cov(returns) / std)
        df = DataFrame({"attribution_terms": attribution_terms, "volatility": volatility})
        df["order_book_id"] = order_book_id
        dfs.append(df)
    bonds_attribution = pd.concat(dfs)
    bonds_attribution.index.name = "name"
    bonds_attribution.reset_index(inplace=True)

    return (
        DataFrame(
            {
                "p_return": p_attribution_terms,
                "b_return": b_attribution_terms,
                "e_return": active_attribution_terms,
                "p_volatility": p_volatility,
                "b_volatility": b_volatility,
                "tracking_error": active_volatility,
            }
        ),
        bonds_attribution,
    )


def daily_campisi_attribution(
    weights: Series, returns: Series, prev_date: datetime, date: datetime, benchmark_info: Dict, as_dict=True
) -> Dict:
    """单日 campisi 归因.

    Args:
        weights: T-1日权重, 其中 index 为 order_book_id, name 为 weight.
        returns: T日收益率, 其中 index 为 order_book_id, name 为 return.
        prev_date: T-1日
        date: T日
        benchmark_info: 基准信息.
    Returns:
        campisi归因结果
    """
    mdprovider = analysis_context_v2.mdprovider_api
    # 计算组合的收益分解(没算上权重)
    bond_list = list(weights.index.get_level_values("order_book_id").unique())
    p_attribution = calc_bond_attribution(bond_list, prev_date, date, mdprovider)
    # 还原了所需的所有债券的收益分解, 针对多余出来的收益率, 计入到残余收益.
    p_attribution = p_attribution.reindex(bond_list, fill_value=0)
    p_attribution["returns"] = returns
    p_attribution["no_valuation_residual"] = returns.sub(p_attribution["valuation_return"], fill_value=0)
    p_attribution["all_residual"] += p_attribution["no_valuation_residual"]

    # 计算基准的收益分解(没算上权重)
    mdprovider = analysis_context_v2.mdprovider_api
    index_weight_api = analysis_context_v2.index_weight_api
    benchmark_id = benchmark_info["detail"]  # 指数作为基准
    b_weights = index_weight_api.get_bond_index_weights(benchmark_id, prev_date)
    if b_weights is None:
        raise Continue(f"获取不到 {benchmark_id} 在 {prev_date} 的权重数据")
    b_prev_valuation, b_cur_valuation = analysis_context_v2.cjhx_attr_utils.get_benchmark_valuation(
        benchmark_id, prev_date, date, mdprovider
    )
    b_returns = (b_cur_valuation / b_prev_valuation) - 1
    b_weights.dropna(inplace=True)
    b_bond_list = list(b_weights.index.get_level_values("order_book_id").unique())
    b_attribution = calc_bond_attribution(b_bond_list, prev_date, date, mdprovider)
    # 由于基准中有的id可能没有归因结果, 这里将指数权重数据重新根据 b_attribution的结果进行归一化.
    b_weights = b_weights.reindex(b_attribution.index, copy=False)
    b_weights = b_weights / b_weights.sum()

    # 根据 sector 分组, 计算brinson.
    info_api = analysis_context_v2.instruments_info_api
    b_sector_classification = info_api.get_sector(b_bond_list, "ch_bondtype")["sector"]
    b_sector_classification.fillna("others")

    p_sector_classification = info_api.get_sector(bond_list, "ch_bondtype")["sector"]
    p_sector_classification.fillna("others")
    p_sector_weight_spread, p_sector_returns_spread = allocation_selection.calc_grouped_weight_return(
        weights, p_attribution.spread_return, p_sector_classification
    )
    b_sector_weight_spread, b_sector_returns_spread = allocation_selection.calc_grouped_weight_return(
        b_weights, b_attribution.spread_return, b_sector_classification
    )
    brinson = allocation_selection.calc_brinson_attribution(
        p_sector_weight_spread, p_sector_returns_spread,
        b_sector_weight_spread, b_sector_returns_spread
    )
    # 带上了权重的归因结果.
    # 按照需求, 需要保存组合的个债归因结果.
    p_bonds_attribution_terms = p_attribution.mul(weights, axis="index")
    p_attribution_terms = p_bonds_attribution_terms.sum()
    b_attribution_terms = b_attribution.mul(b_weights, axis="index").sum()
    # 针对基准价格与基准成份债算出来的收益率之间的差异, 直接计入残余收益.
    b_attribution_terms["all_residual"] += b_returns - b_attribution_terms["valuation_return"]
    b_attribution_terms["returns"] = b_returns

    # campisi_holding_returns 是带上了曲线管理部分的 campisi 持仓收益与利差, 业务上要将 曲线管理, 利差单独提取出来
    # 所以这里附加 campisi_holding_returns_without_curve 这一项.
    # fmt: off
    p_attribution_terms["campisi_holding_returns_without_curve"] = p_attribution_terms.loc["coupon_return"] + p_attribution_terms.loc["pull_to_par_return"] + p_attribution_terms.loc["carry_return"]
    b_attribution_terms["campisi_holding_returns_without_curve"] = b_attribution_terms.loc["coupon_return"] + b_attribution_terms.loc["pull_to_par_return"] + b_attribution_terms.loc["carry_return"]
    p_bonds_attribution_terms["campisi_holding_returns_without_curve"] = p_bonds_attribution_terms["coupon_return"] - p_bonds_attribution_terms["pull_to_par_return"] - p_bonds_attribution_terms["carry_return"]
    # fmt: on
    # 处理结果数据
    if as_dict:
        p_bonds_attribution_terms.reset_index(inplace=True)
        return {
            "portfolio": {
                "bonds_attribution_terms": p_bonds_attribution_terms.to_dict("records"),
                "attribution_terms": p_attribution_terms.to_dict(),
            },
            "benchmark": {
                "attribution_terms": b_attribution_terms.to_dict(),
                "allocation": brinson["allocation"].to_dict(),
                "selection": brinson["selection"].to_dict(),

            },
        }
    else:
        return {
            "portfolio": {
                "bonds_attribution_terms": p_bonds_attribution_terms,
                "attribution_terms": p_attribution_terms,
            },
            "benchmark": {
                "attribution_terms": b_attribution_terms,
                "allocation": brinson["allocation"],
                "selection": brinson["selection"],
            },
        }


def calc_bond_attribution(
    bond_list: List[str],
    prev_date: datetime,
    date: datetime,
    mdprovider: Optional[CachedPriceProvider] = None,
) -> DataFrame:
    """计算个债单日归因.

    Args:
        bond_list: 债券id列表.
        prev_date: T-1日
        date: T日
        mdprovider: 价格获取器

    Returns:
        个债单日归因结果.
        index - order_book_id
        columns - 各归因项, 包括
            valuation_return,holding_returns,deferral_returns,coupon_return,pull_to_par_return,carry_return,
            shift_return,twist_return,spread_return,campisi_residual,campisi_holding_returns,no_holding_residual,
            all_residual,no_valuation_residual

            注: valuation_return, holding_returns, campisi_residual, no_holding_residual 是帮助调试使用的辅助项.
            这里推出来的收益率是通过中债估值算出来的收益率, 总的收益率应该通过估值表(重估后)获取.
    """
    if mdprovider is None:
        mdprovider = analysis_context_v2.mdprovider_api

    previous_valuation, current_valuation = analysis_context_v2.cjhx_attr_utils.get_valuation(bond_list, prev_date, date, mdprovider)
    day_interval = (date - prev_date).days
    # 计算票息支付, 本金支付.
    principal_payment = previous_valuation["residual_principal"] - current_valuation["residual_principal"]
    coupon_payment = analysis_context_v2.cjhx_attr_utils.get_coupon_payment(previous_valuation, current_valuation, day_interval)
    # 根据中债估值算出来的收益分解.
    valuation_attribution = analysis_context_v2.cjhx_attr_utils.calc_valuation_attribution(
        previous_valuation, current_valuation, principal_payment + coupon_payment
    )
    holding_returns = valuation_attribution.holding_returns
    no_deferral_holding_returns = valuation_attribution[valuation_attribution["deferral_returns"] == 0].holding_returns
    campisi_attribution = attribution.campisi_attribution_main(
        holding_returns, no_deferral_holding_returns, previous_valuation, current_valuation, prev_date, date, coupon_payment
    )
    # no_holding_residual 与 campisi_residual 区别
    # no_holding_residual 是由于中债估值缺少必要的属性产生的.
    # campisi_residual 是中债估值没有缺少必要的属性, 但是在内部计算中产生的差异.
    campisi_attribution["all_residual"] = campisi_attribution[
        ["campisi_residual", "no_holding_residual"]
    ].sum(axis=1)
    all_attributioins = pd.concat([valuation_attribution, campisi_attribution], axis=1)
    all_attributioins.fillna(0, inplace=True)
    return all_attributioins
