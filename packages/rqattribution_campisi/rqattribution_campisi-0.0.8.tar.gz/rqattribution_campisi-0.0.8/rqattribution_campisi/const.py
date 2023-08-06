from rqattribution import analysis_context_v2

attr_tree = analysis_context_v2.AttrTree(
    {
        "returns": {
            "deferral_returns": None,
            "all_residual": None,
            "curve_return": {
                "shift_return": None,
                "twist_return": None,
            },
            "campisi_holding_returns_without_curve": {
                "coupon_return": None,
                "pull_to_par_return": None,
                "carry_return": None,
            },
            "spread_return": {"allocation_spread": None, "selection_spread": None},
        }
    }
)
