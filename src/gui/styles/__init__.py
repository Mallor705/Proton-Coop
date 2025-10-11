"""
GUI Styles Module for Proton-Coop

This module provides professional CSS styling management following SOLID principles.
It includes modular CSS files and a centralized StyleManager for maintainable theming.

Public API:
    - StyleManager: Main class for managing CSS styles
    - get_style_manager(): Get the global StyleManager instance
    - initialize_styles(): Initialize default styles
    - StyleManagerError: Exception for style-related errors

Usage:
    from src.gui.styles import initialize_styles, get_style_manager

    # Initialize styles during app startup
    initialize_styles()

    # Get style manager for custom styling
    style_manager = get_style_manager()
    style_manager.load_css_file('custom.css')
"""

from .style_manager import (
    StyleManager,
    StyleManagerError,
    get_style_manager,
    initialize_styles
)

__all__ = [
    'StyleManager',
    'StyleManagerError',
    'get_style_manager',
    'initialize_styles'
]

__version__ = '1.0.0'
__author__ = 'Proton-Coop Team'
