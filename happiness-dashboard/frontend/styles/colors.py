import dash_bootstrap_components as dbc
from dash import html, dcc

class ColorPalette:
    # Enhanced color palette with more nuanced colors
    PRIMARY = '#2980b9'    # Deep Blue
    SECONDARY = '#27ae60'  # Vibrant Green
    ACCENT = '#e74c3c'     # Coral Red

    # Neutral Colors
    BACKGROUND = '#f4f6f9'
    TEXT_DARK = '#34495e'
    TEXT_LIGHT = '#ecf0f1'

    # Semantic Colors
    SUCCESS = '#2ecc71'
    WARNING = '#f39c12'
    DANGER = '#e74c3c'

    # Gradient for Happiness
    HAPPINESS_GRADIENT = [
        '#1a9850',  # Rich Green (High Happiness)
        '#91cf60',  # Light Green
        '#d9ef8b',  # Pale Yellow-Green
        '#fee08b',  # Soft Yellow
        '#fc8d59',  # Warm Orange
        '#d73027'   # Deep Red (Low Happiness)
    ]

    @classmethod
    def get_happiness_color(cls, score):
        """Intelligent color mapping for happiness scores"""
        normalized_score = min(max(score / 10, 0), 1)
        return cls.HAPPINESS_GRADIENT[int(normalized_score * (len(cls.HAPPINESS_GRADIENT) - 1))]
