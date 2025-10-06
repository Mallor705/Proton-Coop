# UMU Launcher Integration - Implementation Summary

## Overview
This document summarizes the implementation of UMU (Unified Launcher) integration into the Linux-Coop project, allowing users to choose between traditional Proton and UMU launcher for game execution.

## Changes Made

### 1. Core Model Changes (`src/models/profile.py`)
Added new optional fields to the `GameProfile` model:
- `use_umu` (bool): Enable/disable UMU launcher mode
- `umu_id` (str): Game ID from umu-database
- `umu_store` (str): Store identifier (egs, gog, steam, none)
- `umu_proton_path` (str): Custom Proton path or "GE-Proton"

### 2. New UMU Service (`src/services/umu.py`)
Created a dedicated service for UMU launcher management with the following functionality:
- **Dependency Validation**: Checks if `umu-run` is installed
- **Environment Preparation**: Sets up UMU-specific environment variables (WINEPREFIX, GAMEID, STORE, PROTONPATH)
- **Command Building**: Constructs proper umu-run commands
- **Information Retrieval**: Provides UMU installation details

Key methods:
- `is_umu_available()`: Checks for umu-run availability
- `validate_umu_dependency()`: Validates UMU installation
- `prepare_umu_environment()`: Prepares environment variables
- `build_umu_command()`: Builds the umu-run command

### 3. Instance Service Updates (`src/services/instance.py`)
Modified the `InstanceService` to support UMU execution:
- Added `UmuService` initialization
- Updated `validate_dependencies()` to check UMU when enabled
- Modified `launch_instances()` to handle UMU mode
- Updated `_prepare_environment()` to set UMU-specific variables
- Modified `_build_base_game_command()` to use umu-run instead of proton

### 4. CLI Updates (`src/cli/commands.py`)
Updated validation flow to pass profile information to dependency validation, enabling UMU-specific checks.

### 5. Documentation
Created comprehensive documentation:
- **`docs/UMU_USAGE.md`**: Complete guide for UMU usage
  - Installation instructions
  - Configuration examples
  - Field descriptions
  - Troubleshooting guide
  - Multiple example profiles

- **Updated READMEs**:
  - Main `README.md`: Added UMU feature, prerequisites, and example
  - Portuguese `docs/README.pt.md`: Added UMU support information

### 6. Example Profile
Created `profiles/ExampleUMU.json` demonstrating UMU configuration.

## How It Works

### UMU Mode Flow
1. User sets `"use_umu": true` in game profile
2. Linux-Coop validates umu-run is installed
3. UMU environment variables are prepared:
   - `WINEPREFIX`: Points to instance Wine prefix
   - `GAMEID`: Game ID for fixes (default: umu-default)
   - `STORE`: Store type (default: none)
   - `PROTONPATH`: Custom Proton path (optional)
4. Command is built using `umu-run` instead of Proton
5. Game launches through UMU's Steam Runtime container

### Traditional Proton Mode (Unchanged)
1. User keeps `"use_umu": false` or omits the field
2. Standard Proton lookup and execution proceeds
3. Games run through traditional Proton/Steam Runtime

## Configuration Examples

### Minimal UMU Configuration
```json
{
  "use_umu": true,
  "exe_path": "/path/to/game.exe",
  ...
}
```

### Full UMU Configuration
```json
{
  "use_umu": true,
  "umu_id": "umu-borderlands3",
  "umu_store": "egs",
  "umu_proton_path": "GE-Proton",
  "exe_path": "/path/to/game.exe",
  ...
}
```

## Benefits of UMU Integration

1. **No Steam Required**: Run games without Steam installation
2. **Better Non-Steam Support**: Improved compatibility with Epic, GOG, etc.
3. **Automatic Fixes**: Access to umu-database game fixes
4. **Flexible Proton Management**: Auto-download GE-Proton or use custom versions
5. **Container Isolation**: Uses Steam Runtime containerization
6. **Multi-Store Support**: Better support for different game stores

## Backward Compatibility

All changes are backward compatible:
- Existing profiles continue to work without modification
- UMU is completely optional
- Default behavior remains unchanged
- Traditional Proton mode is still the default

## Testing Recommendations

1. Test with UMU disabled (existing functionality)
2. Test with UMU enabled but minimal config
3. Test with full UMU configuration
4. Test with different game stores (egs, gog, steam)
5. Test with auto-download GE-Proton
6. Verify error handling when umu-run is not installed

## Dependencies

### New Optional Dependency
- `umu-run` command (from umu-launcher package)

### Existing Dependencies (Unchanged)
- gamescope
- bwrap
- Python 3.8+
- Proton (optional when using UMU)

## Files Modified

1. `src/models/profile.py` - Added UMU fields
2. `src/services/umu.py` - NEW FILE - UMU service
3. `src/services/instance.py` - UMU integration
4. `src/cli/commands.py` - Validation updates
5. `README.md` - Documentation updates
6. `docs/README.pt.md` - Portuguese documentation
7. `docs/UMU_USAGE.md` - NEW FILE - UMU guide
8. `profiles/ExampleUMU.json` - NEW FILE - Example profile

## Error Handling

The implementation includes proper error handling:
- Checks for umu-run availability before execution
- Provides clear error messages if UMU is not installed
- Falls back gracefully if UMU is misconfigured
- Logs UMU-specific information for debugging

## Future Enhancements

Potential future improvements:
1. GUI support for UMU configuration
2. Auto-detection of game store type
3. Integration with umu-database for game ID lookup
4. UMU version checking and updates
5. Better Steam Runtime management

## Conclusion

The UMU launcher integration provides Linux-Coop users with a modern, flexible alternative to traditional Proton execution, especially beneficial for non-Steam games while maintaining full backward compatibility with existing configurations.
