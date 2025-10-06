# GUI UMU Integration - Implementation Summary

## Overview
Successfully implemented UMU launcher support in the Linux-Coop graphical user interface (GUI). Users can now enable and configure UMU launcher directly from the GUI, and all settings are saved to the profile JSON file.

## GUI Changes Made

### 1. New UI Fields (`src/gui/app.py`)

Added the following UI elements in the "Launch Options" section:

#### Use UMU Launcher Checkbox
- **Location**: First field in Launch Options frame
- **Type**: `Gtk.CheckButton`
- **Default**: Unchecked (false)
- **Tooltip**: "Enable UMU launcher instead of traditional Proton (requires umu-run installed)"
- **Behavior**: When toggled, shows/hides relevant fields

#### UMU Game ID (Conditional)
- **Location**: After Proton Version field
- **Type**: `Gtk.Entry`
- **Placeholder**: "umu-default"
- **Tooltip**: "Game ID from umu-database (e.g., umu-borderlands3)"
- **Visibility**: Only shown when "Use UMU" is checked

#### UMU Store (Conditional)
- **Location**: After UMU Game ID
- **Type**: `Gtk.ComboBoxText`
- **Options**: none, egs, gog, steam, origin, uplay
- **Default**: "none"
- **Tooltip**: "Game store identifier (Epic, GOG, Steam, etc.)"
- **Visibility**: Only shown when "Use UMU" is checked

#### UMU Proton Path (Conditional)
- **Location**: After UMU Store
- **Type**: `Gtk.Entry`
- **Placeholder**: "GE-Proton or custom path"
- **Tooltip**: "Use 'GE-Proton' for auto-download or specify custom Proton path"
- **Visibility**: Only shown when "Use UMU" is checked

### 2. Dynamic UI Behavior

#### Field Visibility Logic (`_on_use_umu_toggled` method)
When the "Use UMU Launcher" checkbox is toggled:

**When ENABLED (checked):**
- ✅ Shows: UMU Game ID field
- ✅ Shows: UMU Store combo box
- ✅ Shows: UMU Proton Path field
- ❌ Hides: Proton Version combo box (traditional)

**When DISABLED (unchecked):**
- ❌ Hides: All UMU-specific fields
- ✅ Shows: Traditional Proton Version combo box

Status bar message updates to inform user of mode change.

### 3. Data Persistence

#### Save Profile (`get_profile_data` method)
When saving a profile, the following UMU fields are collected from the UI:

```python
use_umu = self.use_umu_check.get_active()
umu_id = self.umu_id_entry.get_text() or None  # Only if use_umu is True
umu_store = self.umu_store_combo.get_active_text() or None  # Only if use_umu is True
umu_proton_path = self.umu_proton_path_entry.get_text() or None  # Only if use_umu is True
```

These values are passed to the `GameProfile` constructor and saved to the JSON file with the following aliases:
- `USE_UMU`
- `UMU_ID`
- `UMU_STORE`
- `UMU_PROTON_PATH`

#### Load Profile (`_load_proton_settings` method)
When loading a profile, the method now:

1. Checks if `USE_UMU` is set in the profile
2. Sets the checkbox state accordingly
3. If UMU is enabled:
   - Loads `UMU_ID` into the text entry
   - Selects the appropriate `UMU_STORE` in the combo box
   - Loads `UMU_PROTON_PATH` into the text entry
4. If UMU is disabled:
   - Loads traditional `PROTON_VERSION` as before

#### Reset Fields (`_clear_all_fields` method)
When creating a new profile or clearing fields:
- `use_umu_check` is set to `False`
- `umu_id_entry` is cleared
- `umu_store_combo` is set to index 0 ("none")
- `umu_proton_path_entry` is cleared

## User Workflow

### Creating a New Profile with UMU

1. Click "🎮 Add New Profile" or load existing profile
2. Fill in basic game details (name, executable, etc.)
3. Check "Use UMU Launcher" checkbox
4. UMU-specific fields appear automatically
5. (Optional) Enter UMU Game ID (e.g., "umu-borderlands3")
6. (Optional) Select store type (e.g., "egs" for Epic Games Store)
7. (Optional) Enter Proton path (e.g., "GE-Proton" for auto-download)
8. Click "💾 Save Profile"

### Editing Existing Profile

1. Select profile from left sidebar
2. Profile loads with UMU settings if previously configured
3. Toggle "Use UMU Launcher" to enable/disable UMU mode
4. Modify UMU fields as needed
5. Click "💾 Save Profile" to save changes

### Example Profile Output

```json
{
  "GAME_NAME": "Epic Game Example",
  "EXE_PATH": "/home/user/Games/MyGame/game.exe",
  "USE_UMU": true,
  "UMU_ID": "umu-mygame",
  "UMU_STORE": "egs",
  "UMU_PROTON_PATH": "GE-Proton",
  "NUM_PLAYERS": 2,
  "INSTANCE_WIDTH": 1920,
  "INSTANCE_HEIGHT": 1080,
  "PLAYERS": [...],
  "MODE": "splitscreen",
  "SPLITSCREEN": {
    "ORIENTATION": "horizontal"
  }
}
```

## Visual Layout

The Launch Options section now appears as:

```
┌─ Launch Options ────────────────────────────────┐
│                                                  │
│ Use UMU Launcher:      [ ]                      │
│                                                  │
│ Proton Version:        [Combo: GE-Proton10-4 ▼] │
│                                                  │
│ Disable bwrap:         [ ]                      │
│                                                  │
└──────────────────────────────────────────────────┘
```

When UMU is enabled:

```
┌─ Launch Options ────────────────────────────────┐
│                                                  │
│ Use UMU Launcher:      [✓]                      │
│                                                  │
│ UMU Game ID:          [umu-borderlands3      ]  │
│                                                  │
│ UMU Store:            [Combo: egs            ▼] │
│                                                  │
│ UMU Proton Path:      [GE-Proton             ]  │
│                                                  │
│ Disable bwrap:         [ ]                      │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Benefits

1. **User-Friendly**: No need to manually edit JSON files
2. **Visual Feedback**: Clear indication when UMU mode is active
3. **Smart UI**: Only shows relevant fields based on selection
4. **Persistent**: Settings are saved and loaded correctly
5. **Integrated**: Works seamlessly with existing profile system
6. **Discoverable**: Users can easily find and try UMU feature

## Testing Recommendations

1. ✅ Create new profile with UMU enabled
2. ✅ Save and reload profile - verify all UMU fields persist
3. ✅ Toggle UMU on/off - verify field visibility changes
4. ✅ Test with different store types
5. ✅ Test with empty/missing UMU fields (should use defaults)
6. ✅ Test profile deletion with UMU profiles
7. ✅ Test launching game with UMU enabled (requires umu-run installed)

## Compatibility

- ✅ Backward compatible with existing profiles
- ✅ Profiles without UMU fields load correctly (use_umu defaults to false)
- ✅ UMU fields are optional (can be left blank)
- ✅ Works with all existing profile features (splitscreen, controllers, etc.)

## Files Modified

- ✅ `src/gui/app.py` - Added UI fields, callbacks, save/load logic

## Related Documentation

- See `docs/UMU_USAGE.md` for detailed UMU configuration guide
- See `UMU_INTEGRATION_SUMMARY.md` for backend implementation details
- See `README.md` for general UMU feature overview

## Future Enhancements

Potential improvements:
1. Auto-detect umu-run installation and show warning if not found
2. Link to umu-database for game ID lookup
3. Validate UMU fields before saving
4. Show UMU status indicator in profile list
5. Add "Test UMU" button to verify configuration
