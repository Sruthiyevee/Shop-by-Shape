# Package initialization for phase_3_color
from phase_3_color.color_matcher import (
    load_color_rules,
    normalize_skin_tone,
    get_color_palette,
    filter_catalog_by_color,
    recommend_colors_for_user
)

__all__ = [
    "load_color_rules",
    "normalize_skin_tone",
    "get_color_palette",
    "filter_catalog_by_color",
    "recommend_colors_for_user"
]
