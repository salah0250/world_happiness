import numpy as np

def humanize_number(num):
    """
    Convert large numbers to human-readable format
    """
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def percentile_rank(data, value):
    """
    Calculate percentile rank of a value in a dataset
    """
    return np.sum(data <= value) / len(data) * 100

def color_gradient(start_color, end_color, n_steps):
    """
    Generate a color gradient between two colors
    """
    start = np.array(start_color)
    end = np.array(end_color)
    return [tuple((start + (end - start) * i / (n_steps - 1)).astype(int)) for i in range(n_steps)]
def smart_truncate(text, max_length=100):
    """Intelligently truncate text with ellipsis"""
    return text[:max_length] + '...' if len(text) > max_length else text

def format_tooltip(country, data):
    """Create rich, formatted tooltips for visualizations"""
    return f"""
    <b>{country}</b><br>
    Happiness Score: {data['happiness_score']:.2f}<br>
    GDP per Capita: ${data['gdp']:.2f}<br>
    Life Expectancy: {data['life_expectancy']:.2f} years
    """