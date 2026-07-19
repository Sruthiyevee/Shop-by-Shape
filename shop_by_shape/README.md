# Shop by Shape

Shop by Shape is an e-commerce recommendation engine designed to match clothing items from a catalog to a user's specific body shape and skin tone. The system supports multiple onboarding methodologies to calculate body shapes for both women and men, filtering matching products dynamically with color recommendations.

## Features

### Dual Onboarding Flow & Gender Support
- **Multi-Gender Support**: Full support for both women's and men's body shape classification logic.
  - **Women's Shapes**: Pear, Apple, Hourglass, Rectangle, Inverted Triangle.
  - **Men's Shapes**: Trapezoid, Inverted Triangle, Rectangle, Triangle, Oval.
- **Quick Assessment**: A questionnaire form evaluating weight distribution, ratio (shoulder-to-hip / taper), and prominent visual features to estimate body shape.
- **Precision Calculator**: An advanced interface accepting exact measurements for Bust/Chest, Waist, and Hips (with strict positive value validation and auto-detection of inches vs centimeters) to calculate body shape via mathematical proportion ratios.

### E-Commerce Recommendation Grid
- Filters items based on the calculated body shape, selected gender, and skin tone.
- Provides a clean product grid featuring item images, titles, prices, and color recommendations.
- Supports side-panel filtering by product category and occasion.

### AI-Powered Body Shape Mapping & Groq LLM Integration
- **Groq LLM Integration**: Enriches body shape mappings with personalized styling advice, color palette guidance, and fabric recommendations powered by Groq API.
- **Token Optimization & Caching**: Employs strictly bounded response tokens (`max_tokens=250`) and memory caching to prevent token exhaustion.
- **Configurable & Safe**: Uses environment variables (`GROQ_API_KEY`, `GROQ_MODEL`) loaded from a `.env` file (which is git-ignored). Includes rule-based fallback when no API key is provided.

## Environment Setup
Create a `.env` file in the project root or copy from `.env.example`:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
*(Note: `.env` is listed in `.gitignore` to prevent committing sensitive keys).*

## Directory Architecture
The application is structured into five distinct architectural phases:

- `phase_1_logic/`: Core body shape calculation algorithms (supporting both women and men).
- `phase_2_data/`: Catalog data store (`mock_catalog.csv`), shape rules engine (`shape_rules.json`), and Pandas retrieval logic.
- `phase_3_color/`: Skin tone classification and dress color palette matching engine.
- `phase_4_mvp/`: Streamlit dashboard and modular layout components.
- `phase_5_ai_integration/`: LangChain-driven RAG and Groq LLM explainers with strict token limit optimization.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. Navigate to the project directory:
   ```bash
   cd shop_by_shape
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Option 1: One-Click Launch (Windows)**
Simply double-click `run_app.bat` in the project root directory.

**Option 2: Command Line**
```bash
streamlit run phase_4_mvp/app.py
```



