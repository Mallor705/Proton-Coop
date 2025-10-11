# Proton-Coop GUI Styles System

A professional, modular CSS styling system for the Proton-Coop GUI application, built following SOLID principles for maintainable and scalable theming with automatic system theme detection.

## Overview

This styles system provides a centralized way to manage CSS styling across the Proton-Coop application, separating presentation concerns from business logic and enabling easy customization and theming. The system automatically detects your system's theme preference (light/dark) and applies appropriate styling without any user intervention.

## Architecture

### Design Principles

- **Single Responsibility Principle (SRP)**: Each CSS file has a single, well-defined purpose
- **Open/Closed Principle**: Easy to extend with new styles without modifying existing code
- **Dependency Inversion**: Application depends on abstractions (CSS files) rather than concrete implementations
- **Separation of Concerns**: Styling is completely separated from application logic

### File Structure

```
src/gui/styles/
├── __init__.py              # Public API exports
├── style_manager.py         # StyleManager class implementation
├── base.css                 # Fundamental styles and resets
├── components.css           # Component-specific styles
├── layout.css               # Structural and positioning styles
├── theme.css                # Colors, themes, and visual states
├── theme-dark.css           # Dark theme specific overrides
├── custom.css.example       # Example custom styling
└── README.md               # This documentation
```

## CSS Files

### `base.css`
Contains fundamental styles and resets that form the foundation of the design system:
- Global font families and text rendering
- Base padding and margins for text elements
- Line height and typography settings
- Cross-browser compatibility fixes

### `components.css`
Component-specific styling for individual GUI widgets:
- Input fields (entry, spinbutton)
- Buttons and controls
- Dropdowns and combo boxes
- Checkboxes and radio buttons
- Notebook tabs and list items
- Frames and containers

### `layout.css`
Structural and positioning styles:
- Window and pane layouts
- Grid and box arrangements
- Spacing and margins between sections
- Responsive design rules
- Drawing area and canvas styling

### `theme.css`
Visual theming including colors and states:
- Color palette definitions
- Light theme styling (default)
- Action button styling (suggested, destructive)
- Focus and selection states
- Error and warning states
- Custom component themes

### `theme-dark.css`
Dark theme specific overrides that are automatically loaded when system uses dark theme:
- Dark color palette overrides
- Dark background and foreground colors
- Adjusted contrast for better readability
- Dark theme specific component styling
- Automatic system theme detection and switching

## StyleManager API

### Basic Usage

```python
from src.gui.styles import initialize_styles, get_style_manager

# Initialize default styles (call once during app startup)
initialize_styles()

# Get the global style manager instance
style_manager = get_style_manager()
```

### Advanced Usage

```python
from src.gui.styles import StyleManager, StyleManagerError

# Create a custom style manager
style_manager = StyleManager(custom_styles_dir)

# Load specific CSS files
try:
    style_manager.load_css_file('custom.css')
    style_manager.load_css_file('dark-theme.css')
except StyleManagerError as e:
    print(f"Failed to load styles: {e}")

# Load CSS from string
custom_css = """
button {
    background-color: #3584e4;
    color: white;
}
"""
style_manager.load_css_from_string(custom_css, "custom-buttons")

# Apply theme variants
style_manager.apply_theme_variant("dark")

# Reload all styles (useful for development)
style_manager.reload_styles()

# Check applied styles
if style_manager.has_style('custom.css'):
    print("Custom styles are applied")

# Get list of applied styles
applied = style_manager.get_applied_styles()
print(f"Applied styles: {applied}")
```

## Customization

### Creating Custom Themes

1. **Copy the example file:**
   ```bash
   cp custom.css.example custom.css
   ```

2. **Modify colors and styling:**
   ```css
   /* Define custom colors */
   @define-color my_accent #ff6b35;
   @define-color my_background #1a1a1a;

   /* Apply to components */
   .suggested-action {
       background-color: @my_accent;
   }
   ```

3. **Load in your application:**
   ```python
   style_manager.load_css_file('custom.css')
   ```

### Color Variables

The theme system uses CSS custom properties (variables) for consistent theming:

```css
/* Light theme colors */
@define-color accent_color #3584e4;
@define-color window_bg_color #fafafa;
@define-color window_fg_color #2e3436;
@define-color view_bg_color #ffffff;
@define-color borders #d4d0c8;

/* Action colors */
@define-color destructive_color #e01b24;
@define-color success_color #26a269;
@define-color warning_color #f5c211;
```

### Component Classes

Use these CSS classes for consistent styling:

- `.suggested-action` - Primary action buttons
- `.destructive-action` - Dangerous action buttons
- `.success` - Success states
- `.warning` - Warning states
- `.error` - Error states
- `.profile-item` - Profile list items
- `.player-frame` - Player configuration frames
- `.env-var-row` - Environment variable rows

## Best Practices

### For Developers

1. **Load styles early**: Call `initialize_styles()` during application startup
2. **Handle errors**: Always wrap style loading in try-catch blocks
3. **Use semantic classes**: Prefer semantic class names over direct styling
4. **Test themes**: Verify styling works in both light and dark themes
5. **Document changes**: Update this README when adding new styling features

### For CSS Authors

1. **Follow the cascade**: Respect the loading order (base → components → layout → theme)
2. **Use variables**: Always use color variables instead of hardcoded colors
3. **Be specific**: Use appropriate selectors to avoid unintended side effects
4. **Test responsiveness**: Ensure styles work at different window sizes
5. **Validate CSS**: Use CSS validation tools to catch syntax errors

## Automatic Theme Detection

The system automatically detects and follows your system's theme preference:

### How It Works

1. **System Detection**: Uses Adwaita StyleManager to detect system theme preference
2. **Automatic Loading**: Loads `theme-dark.css` when system prefers dark theme
3. **Real-time Switching**: Automatically switches themes when system preference changes
4. **Seamless Integration**: No user intervention required

### Theme Files

- **Light Theme**: Uses default `theme.css` with light colors
- **Dark Theme**: Automatically loads `theme-dark.css` with dark-specific overrides

### Configuration

The theme detection is configured automatically during application startup:

```python
# Automatic theme detection (no user code needed)
style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
```

### Manual Theme Testing

To test theme switching manually (for development):

```bash
# Switch to dark theme
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'

# Switch to light theme
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
```

## Troubleshooting

### Common Issues

1. **Styles not applying**: Check that `initialize_styles()` is called before window creation
2. **CSS parse errors**: Validate CSS syntax and check the console for errors
3. **Color variables not working**: Ensure variables are defined before use
4. **Styles overridden**: Check CSS specificity and loading order

### Debug Mode

Enable debug logging to troubleshoot style loading:

```python
import logging
logging.getLogger('src.gui.styles.style_manager').setLevel(logging.DEBUG)
```

### Style Inspection

Use GTK Inspector to debug applied styles:
```bash
GTK_DEBUG=interactive ./run.sh
```

## Contributing

When contributing to the styles system:

1. **Follow the architecture**: Keep styles in appropriate files
2. **Test thoroughly**: Verify changes work in both light and dark themes
3. **Document changes**: Update this README and add code comments
4. **Maintain backwards compatibility**: Don't break existing custom themes
5. **Use semantic versioning**: Update version numbers for breaking changes

## Version History

- **v1.1.0**: Added automatic system theme detection and switching
  - Real-time dark/light theme switching following system preference
  - Dedicated `theme-dark.css` for dark theme specific styling
  - Seamless integration with Adwaita StyleManager
  - No user configuration required for theme switching

- **v1.0.0**: Initial modular styles system with StyleManager
  - CSS files separated by concern (base, components, layout, theme)
  - Support for custom themes and color variables
  - Professional error handling and logging
  - Comprehensive documentation and examples

## License

This styles system is part of the Proton-Coop project and follows the same license terms.
