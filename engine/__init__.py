"""Engine: motor de optimización de inventarios."""

from engine.cleaning import clean_inventory, clean_sales
from engine.demo_data import get_demo_dataset
from engine.optimization import (
    abc_classification,
    apply_industrial_guardrails,
    build_demand_metrics,
    calculate_opportunity_cost,
    calculate_reorder_point,
    calculate_safety_stock,
    full_analysis,
    simulate_service_level_impact,
    xyz_classification,
)

__all__ = [
    "clean_inventory",
    "clean_sales",
    "get_demo_dataset",
    "abc_classification",
    "xyz_classification",
    "calculate_opportunity_cost",
    "calculate_safety_stock",
    "calculate_reorder_point",
    "build_demand_metrics",
    "apply_industrial_guardrails",
    "full_analysis",
    "simulate_service_level_impact",
]
