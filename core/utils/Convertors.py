def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert HEX color to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in range(0, 6, 2))