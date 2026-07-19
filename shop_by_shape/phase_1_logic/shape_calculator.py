"""
Body Shape Calculator Logic

This module provides the core calculation logic for mapping user inputs
(from both quick quiz and precise measurements) to standard body shapes:
- Women: Pear, Apple, Hourglass, Rectangle, Inverted Triangle.
- Men: Trapezoid, Inverted Triangle, Rectangle, Triangle, Oval.
"""

from typing import Union

def _is_male(gender: str) -> bool:
    """Helper to check if gender string indicates male."""
    if not gender or not isinstance(gender, str):
        return False
    g = gender.strip().lower()
    return g in ["male", "man", "men", "m", "boy"]

def calculate_shape_from_quiz(
    weight_gain: str,
    ratio: str,
    prominent_feature: str,
    gender: str = "female"
) -> str:
    """
    Determine body shape based on quick questionnaire selections.
    
    Parameters:
    - weight_gain: Selection representing weight distribution.
    - ratio: Selection representing shoulder-to-hip comparison or upper-to-lower body ratio.
    - prominent_feature: Selection representing the most prominent feature.
    - gender: Gender string ("female"/"women" or "male"/"men"). Default is "female".
    
    Returns:
    - Standardized body shape name.
      For Women: "Pear", "Apple", "Hourglass", "Rectangle", or "Inverted Triangle".
      For Men: "Trapezoid", "Inverted Triangle", "Rectangle", "Triangle", or "Oval".
    """
    w = str(weight_gain or "").strip().lower()
    r = str(ratio or "").strip().lower()
    p = str(prominent_feature or "").strip().lower()
    
    if _is_male(gender):
        # Male body shape calculation
        # 1. Oval: weight in midsection/abdomen/stomach or prominent midsection/stomach
        if "midsection" in w or "abdomen" in w or "stomach" in w or "midsection" in p or "stomach" in p:
            return "Oval"
            
        # 2. Triangle: weight in hips/thighs or shoulders narrower than hips or prominent hips
        if "hips" in w or "narrower" in r or "hips" in p:
            return "Triangle"
            
        # 3. Inverted Triangle: weight in upper body/shoulders/chest or shoulders wider than hips or prominent chest/shoulders
        if "upper" in w or "shoulder" in w or "chest" in w or "wider" in r or "shoulder" in p or "chest" in p or "v-taper" in r:
            return "Inverted Triangle"
            
        # 4. Trapezoid: broad shoulders with tapered waist / defined waist / athletic build
        if "trapezoid" in r or "tapered" in r or "defined" in r or "athletic" in p:
            return "Trapezoid"
            
        # 5. Rectangle (Default/Fallback)
        return "Rectangle"

    # Female body shape calculation
    # 1. Pear: weight in hips/thighs or shoulders narrower than hips or prominent hips
    if "hips" in w or "narrower" in r or "hips" in p:
        return "Pear"
    
    # 2. Inverted Triangle: weight in upper body/shoulders or shoulders wider than hips or prominent shoulders
    if "upper" in w or "shoulder" in w or "wider" in r or "shoulder" in p:
        return "Inverted Triangle"
        
    # 3. Apple: weight in midsection or prominent midsection or round silhouette
    if "midsection" in w or "abdomen" in w or "midsection" in p:
        return "Apple"
        
    # 4. Hourglass: defined waist with balanced shoulders/hips
    if "defined" in r or "waist" in p:
        return "Hourglass"
        
    # 5. Rectangle (Default/Fallback)
    return "Rectangle"

def calculate_shape_from_measurements(
    bust: Union[int, float],
    waist: Union[int, float],
    hips: Union[int, float],
    gender: str = "female"
) -> str:
    """
    Determine body shape based on exact bust/chest, waist, and hips measurements.
    Supports auto-detection and conversion from centimeters to inches.
    
    Parameters:
    - bust: Bust (women) or Chest (men) measurement in inches or centimeters.
    - waist: Waist measurement in inches or centimeters.
    - hips: Hips measurement in inches or centimeters.
    - gender: Gender string ("female"/"women" or "male"/"men"). Default is "female".
    
    Returns:
    - Standardized body shape name:
      For Women: "Pear", "Apple", "Hourglass", "Rectangle", or "Inverted Triangle".
      For Men: "Trapezoid", "Inverted Triangle", "Rectangle", "Triangle", or "Oval".
    """
    if not isinstance(bust, (int, float)) or not isinstance(waist, (int, float)) or not isinstance(hips, (int, float)):
        raise ValueError("Measurements must be numeric values (int or float).")
        
    if isinstance(bust, bool) or isinstance(waist, bool) or isinstance(hips, bool):
        raise ValueError("Measurements must be numeric values, not boolean.")

    if bust <= 0 or waist <= 0 or hips <= 0:
        raise ValueError("Measurements must be greater than zero.")
        
    # Auto-detect centimeters vs inches
    # If the average measurement is > 50, assume centimeters and convert to inches
    if (bust + waist + hips) / 3.0 > 50.0:
        bust = bust / 2.54
        waist = waist / 2.54
        hips = hips / 2.54
        
    chest = bust  # alias for men's chest measurement

    if _is_male(gender):
        # Male body shape classification based on measurements (chest, waist, hips)
        # 1. Oval Check: Waist is larger than chest and hips
        if waist > chest and waist > hips:
            return "Oval"
            
        # 2. Triangle Check: Hips or waist are significantly larger than chest
        if (hips - chest) >= 2.0 or (waist - chest) >= 2.0:
            return "Triangle"
            
        # 3. Inverted Triangle Check: Chest is significantly larger than waist and hips (sharp V-taper)
        if (chest - waist) >= 7.0 and (chest - hips) >= 3.0:
            return "Inverted Triangle"
            
        # 4. Trapezoid Check: Chest is moderately larger than waist, balanced hips
        if (chest - waist) >= 2.0 and abs(chest - hips) <= 4.0:
            return "Trapezoid"
            
        # 5. Rectangle Check (Default/Fallback): Chest, waist, and hips are close
        return "Rectangle"

    # Female body shape classification based on measurements
    # 1. Hourglass Check
    # Hips and bust are relatively equal, waist is significantly narrower
    if abs(bust - hips) <= 2.0 and (bust - waist) >= 8.0 and (hips - waist) >= 8.0:
        return "Hourglass"
        
    # 2. Pear Check
    # Hips are significantly larger than bust, and waist is smaller than hips
    if (hips - bust) >= 2.0 and (hips - waist) >= 7.0:
        return "Pear"
        
    # 3. Inverted Triangle Check
    # Bust is significantly larger than hips, and waist is smaller than bust
    if (bust - hips) >= 2.0 and (bust - waist) >= 7.0:
        return "Inverted Triangle"
        
    # 4. Apple Check
    # Waist is prominent (close to or larger than hips/bust)
    if waist >= bust - 2.0 or waist >= hips - 2.0:
        return "Apple"
        
    # 5. Rectangle Check (Default/Fallback)
    # Bust, waist, and hips are close
    return "Rectangle"

def calculate_male_shape_from_quiz(weight_gain: str, ratio: str, prominent_feature: str) -> str:
    """Convenience function for calculating male body shape from quiz."""
    return calculate_shape_from_quiz(weight_gain, ratio, prominent_feature, gender="male")

def calculate_male_shape_from_measurements(chest: Union[int, float], waist: Union[int, float], hips: Union[int, float]) -> str:
    """Convenience function for calculating male body shape from measurements."""
    return calculate_shape_from_measurements(chest, waist, hips, gender="male")


