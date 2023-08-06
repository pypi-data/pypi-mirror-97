from typing import Tuple

import pandas as pd
from pandas import Series, DataFrame


def calc_grouped_weight_return(
    weights: Series, returns: Series, classification: Series
) -> Tuple[Series, Series]:
    """针对权重与收益率数据进行分组, 获取该分组下的权重与收益率.

    Args:
        weights: 权重数据, index - order_book_id
        returns: 收益率数据, index - order_book_id
        classification: 分类数据, index - order_book_id; 应确保 weights与returns的index在 classification 下都存在.
    Returns:
        (分组权重, 分组收益率); index - order_book_id
    """
    sector_weights = weights.groupby(classification).sum()

    # 计算组合在每一个板块的利差变动收益
    sector_renormalized_weight = (weights.groupby(classification)).apply(lambda x: x / x.sum())
    sector_returns = (sector_renormalized_weight * returns).groupby(classification).sum()

    return sector_weights, sector_returns


# fmt: off
def calc_brinson_attribution(
    p_sector_weight: Series, p_sector_returns: Series,
    b_sector_weights: Series, b_sector_returns: Series,
) -> DataFrame:

    b_sector_returns_sum = b_sector_returns.sum()

    p_unallocated_sectors = b_sector_weights.index.difference(p_sector_weight.index)
    b_unallocated_sectors = p_sector_weight.index.difference(b_sector_weights.index)
    both_allocated_sectors = p_sector_weight.index.intersection(b_sector_weights.index)

    both_allocated_allocation_return = (
        p_sector_weight.loc[both_allocated_sectors] - b_sector_weights.loc[both_allocated_sectors]
    ) * (b_sector_returns.loc[both_allocated_sectors] - b_sector_returns_sum)
    both_allocated_selection_return = p_sector_weight.loc[both_allocated_sectors] * (
        p_sector_returns.loc[both_allocated_sectors] - b_sector_returns.loc[both_allocated_sectors]
    )

    # 对于投资组合不配置，基准组合配置的组合，板块配置收益 = -基准板块收益；板块选券收益 = 0
    p_unallocated_allocation_return = -b_sector_weights.loc[p_unallocated_sectors] * (
        b_sector_returns.loc[p_unallocated_sectors] - b_sector_returns_sum
    )
    p_unallocated_selection_return = Series(0, index=p_unallocated_sectors)

    # 对于投资组合配置，基准组合不配置的组合，板块配置收益 = 投资组合板块收益；板块选券收益 = 0
    b_unallocated_allocation_return = p_sector_weight.loc[b_unallocated_sectors] * (
        p_sector_returns.loc[b_unallocated_sectors] - b_sector_returns_sum
    )
    b_unallocated_selection_return = Series(0, index=b_unallocated_sectors)

    sector_allocation_return = pd.concat(
        [
            b_unallocated_allocation_return,
            both_allocated_allocation_return,
            p_unallocated_allocation_return,
        ]
    )
    sector_selection_return = pd.concat(
        [
            both_allocated_selection_return,
            b_unallocated_selection_return,
            p_unallocated_selection_return,
        ]
    )

    attribution_terms = pd.concat([sector_allocation_return, sector_selection_return], axis=1)
    attribution_terms.columns = ["allocation", "selection"]
    attribution_terms.loc["total"] = attribution_terms.sum()

    return attribution_terms
