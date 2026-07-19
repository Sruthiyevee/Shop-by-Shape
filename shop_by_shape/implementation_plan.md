# Implementation Plan: Phase 2 - Outfit Rules Data Store, Catalog & Recommendation Engine

This plan details the implementation of Phase 2 (`phase_2_data`) using the user-provided shape & outfit rules dataset. It establishes the catalog data store, shape rules lookup, filtering engine, and unit test suite.

---

## Technical Specifications & Architecture

### 1. Data Rules Store (`shape_rules.json`)
- Stores the exact user-provided JSON dataset for female (`pear`, `apple`, `hourglass`, `rectangle`, `inverted_triangle`) and male (`trapezoid`, `inverted_triangle`, `rectangle`, `triangle`, `oval`) body shapes.
- Includes traits, goals, recommended garment types (`tops`, `bottoms`, `dresses`, `outerwear`, `suits`), items to avoid, and occasion notes (`formal`, `casual`, `party`).

### 2. Catalog Dataset (`mock_catalog.csv`)
- A comprehensive CSV database containing clothing items for both women and men across all body shapes and categories.
- Columns:
  - `id`: Unique product ID
  - `name`: Product title
  - `gender`: Target gender (`female` or `male`)
  - `category`: Garment category (`tops`, `bottoms`, `dresses`, `outerwear`, `suits`)
  - `ideal_shapes`: Pipe-separated list of ideal body shape keys
  - `avoid_shapes`: Pipe-separated list of body shapes that should avoid this item
  - `occasion`: Target occasion (`casual`, `formal`, `party`, `all`)
  - `image_url`: Product image URL/placeholder
  - `price`: Item price in USD ($)
  - `description`: Product description highlighting fit features

### 3. Data Retrieval & Recommendation Engine (`data_loader.py`)
Functions:
- `load_shape_rules(filepath: str = None) -> dict`: Loads and caches the JSON dataset.
- `normalize_shape_name(shape: str) -> str`: Normalizes shape strings (e.g., `"Inverted Triangle"` -> `"inverted_triangle"`).
- `get_shape_profile(shape: str, gender: str = "female") -> dict`: Returns traits, goals, recommendations, avoids, and occasion notes for a given shape and gender.
- `load_catalog(filepath: str = None) -> pd.DataFrame`: Loads `mock_catalog.csv` into a Pandas DataFrame.
- `filter_catalog(df: pd.DataFrame, shape: str, gender: str = "female", category: str = None, occasion: str = None) -> pd.DataFrame`: Filters catalog for items that match the user's shape and optional category/occasion.
- `suggest_outfit(shape: str, gender: str = "female", occasion: str = None, catalog_df: pd.DataFrame = None) -> dict`: Generates a complete structured outfit recommendation.

---

## Verification Plan

### Automated Tests
Execute the unit test suite:
```bash
py -m unittest discover -v -s shop_by_shape/tests
```
