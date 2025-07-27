## User

otimo, mas as cores dos temas tão pouco intuitivas... use masi principior do Design de UI/UX, para recolorir os temas white e dark...

## Agent

Vou aplicar princípios modernos de UI/UX para melhorar significativamente as cores dos temas. Vou usar paletas de cores mais intuitivas, contrastes adequados e hierarquia visual clara.

## 1. Primeiro, vou atualizar o tema claro com cores mais modernas e intuitivas:

**Use Tool: edit_file (toolu_01W5r9635GZ6hzuXJFB8kGCi)**
```json
{
  "display_description": "Update light theme with modern UI/UX color principles and better visual hierarchy",
  "mode": "edit",
  "path": "Linux-Coop/src/gui/styles/theme.css"
}
```

**Tool Results: toolu_01W5r9635GZ6hzuXJFB8kGCi**

Edited Linux-Coop/src/gui/styles/theme.css:

```diff
@@ -1,81 +1,144 @@
 /* Theme CSS - Color schemes and theme-specific styles for Linux-Coop GUI */
 
-/* Color Definitions */
-@define-color accent_color #3584e4;
-@define-color accent_bg_color #3584e4;
+/* Modern UI/UX Color Definitions - Light Theme */
+@define-color accent_color #007acc;
+@define-color accent_bg_color #007acc;
 @define-color accent_fg_color #ffffff;
-@define-color destructive_color #e01b24;
-@define-color destructive_bg_color #e01b24;
+@define-color accent_hover_color #005a9e;
+@define-color accent_active_color #004578;
+@define-color destructive_color #dc3545;
+@define-color destructive_bg_color #dc3545;
 @define-color destructive_fg_color #ffffff;
-@define-color success_color #26a269;
-@define-color success_bg_color #26a269;
+@define-color destructive_hover_color #c82333;
+@define-color success_color #28a745;
+@define-color success_bg_color #28a745;
 @define-color success_fg_color #ffffff;
-@define-color warning_color #f5c211;
-@define-color warning_bg_color #f5c211;
-@define-color warning_fg_color #000000;
+@define-color success_hover_color #218838;
+@define-color warning_color #ffc107;
+@define-color warning_bg_color #ffc107;
+@define-color warning_fg_color #212529;
+@define-color warning_hover_color #e0a800;
 
-/* Light Theme Colors */
-@define-color window_bg_color #fafafa;
-@define-color window_fg_color #2e3436;
+/* Modern Light Theme Colors */
+@define-color window_bg_color #f8f9fa;
+@define-color window_fg_color #212529;
 @define-color view_bg_color #ffffff;
-@define-color view_fg_color #2e3436;
-@define-color headerbar_bg_color #ebebeb;
-@define-color headerbar_fg_color #2e3436;
-@define-color sidebar_bg_color #f6f5f4;
-@define-color sidebar_fg_color #2e3436;
-@define-color borders #d4d0c8;
-@define-color view_hover_bg_color #f1f1f1;
+@define-color view_fg_color #343a40;
+@define-color headerbar_bg_color #e9ecef;
+@define-color headerbar_fg_color #495057;
+@define-color sidebar_bg_color #f1f3f4;
+@define-color sidebar_fg_color #495057;
+@define-color borders #dee2e6;
+@define-color view_hover_bg_color #e9ecef;
+@define-color card_bg_color #ffffff;
+@define-color card_border_color #e9ecef;
+@define-color input_bg_color #ffffff;
+@define-color input_border_color #ced4da;
+@define-color input_focus_border_color #007acc;
+@define-color text_secondary_color #6c757d;
+@define-color text_muted_color #868e96;
 
-/* Action Button Styles */
+/* Modern Action Button Styles */
 .suggested-action {
-    background-color: @accent_bg_color;
+    background: linear-gradient(
+        135deg,
+        @accent_bg_color,
+        shade(@accent_bg_color, 0.95)
+    );
     color: @accent_fg_color;
-    border: none;
+    border: 1px solid transparent;
+    border-radius: 6px;
+    box-shadow: 0 2px 4px rgba(0, 123, 204, 0.15);
+    transition: all 0.2s ease;
 }
 
 .suggested-action:hover {
-    background-color: shade(@accent_bg_color, 1.1);
+    background: linear-gradient(
+        135deg,
+        @accent_hover_color,
+        shade(@accent_hover_color, 0.95)
+    );
+    box-shadow: 0 4px 8px rgba(0, 123, 204, 0.25);
+    transform: translateY(-1px);
 }
 
 .suggested-action:active {
-    background-color: shade(@accent_bg_color, 0.9);
+    background-color: @accent_active_color;
+    box-shadow: 0 1px 2px rgba(0, 123, 204, 0.2);
+    transform: translateY(0);
 }
 
 .destructive-action {
-    background-color: @destructive_bg_color;
+    background: linear-gradient(
+        135deg,
+        @destructive_bg_color,
+        shade(@destructive_bg_color, 0.95)
+    );
     color: @destructive_fg_color;
-    border: none;
+    border: 1px solid transparent;
+    border-radius: 6px;
+    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.15);
+    transition: all 0.2s ease;
 }
 
 .destructive-action:hover {
-    background-color: shade(@destructive_bg_color, 1.1);
+    background: linear-gradient(
+        135deg,
+        @destructive_hover_color,
+        shade(@destructive_hover_color, 0.95)
+    );
+    box-shadow: 0 4px 8px rgba(220, 53, 69, 0.25);
+    transform: translateY(-1px);
 }
 
 .destructive-action:active {
-    background-color: shade(@destructive_bg_color, 0.9);
+    background-color: shade(@destructive_bg_color, 0.8);
+    box-shadow: 0 1px 2px rgba(220, 53, 69, 0.2);
+    transform: translateY(0);
 }
 
-/* Success States */
+/* Modern Success States */
 .success {
-    background-color: @success_bg_color;
+    background: linear-gradient(
+        135deg,
+        @success_bg_color,
+        shade(@success_bg_color, 0.95)
+    );
     color: @success_fg_color;
+    border: 1px solid @success_hover_color;
+    border-radius: 4px;
+    box-shadow: 0 2px 4px rgba(40, 167, 69, 0.15);
 }
 
-/* Warning States */
+/* Modern Warning States */
 .warning {
-    background-color: @warning_bg_color;
+    background: linear-gradient(
+        135deg,
+        @warning_bg_color,
+        shade(@warning_bg_color, 0.95)
+    );
     color: @warning_fg_color;
+    border: 1px solid @warning_hover_color;
+    border-radius: 4px;
+    box-shadow: 0 2px 4px rgba(255, 193, 7, 0.15);
 }
 
-/* Focus and Selection States */
+/* Modern Focus and Selection States */
 *:focus {
-    outline: 2px solid @accent_color;
+    outline: 2px solid @input_focus_border_color;
     outline-offset: 2px;
+    outline-style: solid;
+    box-shadow: 0 0 0 3px rgba(0, 123, 204, 0.1);
 }
 
 *:selected {
-    background-color: @accent_bg_color;
+    background: linear-gradient(
+        135deg,
+        @accent_bg_color,
+        shade(@accent_bg_color, 0.95)
+    );
     color: @accent_fg_color;
+    border-radius: 3px;
 }
 
 /* Disabled States */
@@ -95,73 +158,99 @@
     background-color: shade(@destructive_color, 2.5);
 }
 
-/* Game Profile Specific Styling */
+/* Modern Game Profile Styling */
 .profile-item {
-    background-color: @view_bg_color;
-    border: 1px solid @borders;
-    border-radius: 4px;
-    margin: 2px;
-    padding: 8px;
+    background-color: @card_bg_color;
+    border: 1px solid @card_border_color;
+    border-radius: 8px;
+    margin: 4px;
+    padding: 12px;
+    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
+    transition: all 0.2s ease;
 }
 
 .profile-item:hover {
     background-color: @view_hover_bg_color;
     border-color: @accent_color;
+    box-shadow: 0 4px 12px rgba(0, 123, 204, 0.15);
+    transform: translateY(-2px);
 }
 
 .profile-item:selected {
-    background-color: @accent_bg_color;
+    background: linear-gradient(
+        135deg,
+        @accent_bg_color,
+        shade(@accent_bg_color, 0.95)
+    );
     color: @accent_fg_color;
     border-color: @accent_color;
+    box-shadow: 0 6px 16px rgba(0, 123, 204, 0.25);
 }
 
-/* Player Configuration Styling */
+/* Modern Player Configuration Styling */
 .player-frame {
-    background-color: @view_bg_color;
-    border: 1px solid @borders;
-    border-radius: 6px;
+    background-color: @card_bg_color;
+    border: 1px solid @card_border_color;
+    border-radius: 8px;
+    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
 }
 
 .player-frame > label {
     color: @accent_color;
-    font-weight: bold;
+    font-weight: 600;
+    font-size: 1.1em;
 }
 
-/* Environment Variables Styling */
+/* Modern Environment Variables Styling */
 .env-var-row {
-    background-color: @view_bg_color;
-    border: 1px solid @borders;
-    border-radius: 4px;
-    margin: 2px 0;
-    padding: 4px;
+    background-color: @input_bg_color;
+    border: 1px solid @input_border_color;
+    border-radius: 6px;
+    margin: 4px 0;
+    padding: 8px;
+    transition: border-color 0.2s ease;
+}
+
+.env-var-row:hover {
+    border-color: @accent_color;
 }
 
 .env-var-remove-button {
     color: @destructive_color;
     background-color: transparent;
     border: 1px solid @destructive_color;
-    border-radius: 3px;
-    min-width: 24px;
-    min-height: 24px;
+    border-radius: 4px;
+    min-width: 28px;
+    min-height: 28px;
+    transition: all 0.2s ease;
 }
 
 .env-var-remove-button:hover {
     background-color: @destructive_color;
     color: @destructive_fg_color;
+    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
 }
 
-/* Drawing Area Theme */
+/* Modern Drawing Area Theme */
 drawingarea {
-    background-color: #2d2d2d;
-    border: 2px solid @borders;
+    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
+    border: 2px solid @card_border_color;
+    border-radius: 8px;
+    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
 }
 
-/* Status Bar Theme */
+/* Modern Status Bar Theme */
 .statusbar {
-    background-color: @headerbar_bg_color;
-    color: @headerbar_fg_color;
+    background: linear-gradient(
+        180deg,
+        @headerbar_bg_color,
+        shade(@headerbar_bg_color, 0.98)
+    );
+    color: @text_secondary_color;
     border-top: 1px solid @borders;
-    font-size: 0.9em;
+    font-size: 0.85em;
+    font-weight: 500;
+    padding: 4px 8px;
 }
 
 /* Tooltip Theme */

```


Debug Output:

```json
{
  "original_path": "src/gui/styles/theme.css",
  "new_text": "/* Theme CSS - Color schemes and theme-specific styles for Linux-Coop GUI */\n\n/* Modern UI/UX Color Definitions - Light Theme */\n@define-color accent_color #007acc;\n@define-color accent_bg_color #007acc;\n@define-color accent_fg_color #ffffff;\n@define-color accent_hover_color #005a9e;\n@define-color accent_active_color #004578;\n@define-color destructive_color #dc3545;\n@define-color destructive_bg_color #dc3545;\n@define-color destructive_fg_color #ffffff;\n@define-color destructive_hover_color #c82333;\n@define-color success_color #28a745;\n@define-color success_bg_color #28a745;\n@define-color success_fg_color #ffffff;\n@define-color success_hover_color #218838;\n@define-color warning_color #ffc107;\n@define-color warning_bg_color #ffc107;\n@define-color warning_fg_color #212529;\n@define-color warning_hover_color #e0a800;\n\n/* Modern Light Theme Colors */\n@define-color window_bg_color #f8f9fa;\n@define-color window_fg_color #212529;\n@define-color view_bg_color #ffffff;\n@define-color view_fg_color #343a40;\n@define-color headerbar_bg_color #e9ecef;\n@define-color headerbar_fg_color #495057;\n@define-color sidebar_bg_color #f1f3f4;\n@define-color sidebar_fg_color #495057;\n@define-color borders #dee2e6;\n@define-color view_hover_bg_color #e9ecef;\n@define-color card_bg_color #ffffff;\n@define-color card_border_color #e9ecef;\n@define-color input_bg_color #ffffff;\n@define-color input_border_color #ced4da;\n@define-color input_focus_border_color #007acc;\n@define-color text_secondary_color #6c757d;\n@define-color text_muted_color #868e96;\n\n/* Modern Action Button Styles */\n.suggested-action {\n    background: linear-gradient(\n        135deg,\n        @accent_bg_color,\n        shade(@accent_bg_color, 0.95)\n    );\n    color: @accent_fg_color;\n    border: 1px solid transparent;\n    border-radius: 6px;\n    box-shadow: 0 2px 4px rgba(0, 123, 204, 0.15);\n    transition: all 0.2s ease;\n}\n\n.suggested-action:hover {\n    background: linear-gradient(\n        135deg,\n        @accent_hover_color,\n        shade(@accent_hover_color, 0.95)\n    );\n    box-shadow: 0 4px 8px rgba(0, 123, 204, 0.25);\n    transform: translateY(-1px);\n}\n\n.suggested-action:active {\n    background-color: @accent_active_color;\n    box-shadow: 0 1px 2px rgba(0, 123, 204, 0.2);\n    transform: translateY(0);\n}\n\n.destructive-action {\n    background: linear-gradient(\n        135deg,\n        @destructive_bg_color,\n        shade(@destructive_bg_color, 0.95)\n    );\n    color: @destructive_fg_color;\n    border: 1px solid transparent;\n    border-radius: 6px;\n    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.15);\n    transition: all 0.2s ease;\n}\n\n.destructive-action:hover {\n    background: linear-gradient(\n        135deg,\n        @destructive_hover_color,\n        shade(@destructive_hover_color, 0.95)\n    );\n    box-shadow: 0 4px 8px rgba(220, 53, 69, 0.25);\n    transform: translateY(-1px);\n}\n\n.destructive-action:active {\n    background-color: shade(@destructive_bg_color, 0.8);\n    box-shadow: 0 1px 2px rgba(220, 53, 69, 0.2);\n    transform: translateY(0);\n}\n\n/* Modern Success States */\n.success {\n    background: linear-gradient(\n        135deg,\n        @success_bg_color,\n        shade(@success_bg_color, 0.95)\n    );\n    color: @success_fg_color;\n    border: 1px solid @success_hover_color;\n    border-radius: 4px;\n    box-shadow: 0 2px 4px rgba(40, 167, 69, 0.15);\n}\n\n/* Modern Warning States */\n.warning {\n    background: linear-gradient(\n        135deg,\n        @warning_bg_color,\n        shade(@warning_bg_color, 0.95)\n    );\n    color: @warning_fg_color;\n    border: 1px solid @warning_hover_color;\n    border-radius: 4px;\n    box-shadow: 0 2px 4px rgba(255, 193, 7, 0.15);\n}\n\n/* Modern Focus and Selection States */\n*:focus {\n    outline: 2px solid @input_focus_border_color;\n    outline-offset: 2px;\n    outline-style: solid;\n    box-shadow: 0 0 0 3px rgba(0, 123, 204, 0.1);\n}\n\n*:selected {\n    background: linear-gradient(\n        135deg,\n        @accent_bg_color,\n        shade(@accent_bg_color, 0.95)\n    );\n    color: @accent_fg_color;\n    border-radius: 3px;\n}\n\n/* Disabled States */\n*:disabled {\n    opacity: 0.5;\n    color: shade(@window_fg_color, 1.5);\n}\n\n/* Error States */\n.error {\n    color: @destructive_color;\n    border-color: @destructive_color;\n}\n\nentry.error {\n    border: 2px solid @destructive_color;\n    background-color: shade(@destructive_color, 2.5);\n}\n\n/* Modern Game Profile Styling */\n.profile-item {\n    background-color: @card_bg_color;\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    margin: 4px;\n    padding: 12px;\n    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);\n    transition: all 0.2s ease;\n}\n\n.profile-item:hover {\n    background-color: @view_hover_bg_color;\n    border-color: @accent_color;\n    box-shadow: 0 4px 12px rgba(0, 123, 204, 0.15);\n    transform: translateY(-2px);\n}\n\n.profile-item:selected {\n    background: linear-gradient(\n        135deg,\n        @accent_bg_color,\n        shade(@accent_bg_color, 0.95)\n    );\n    color: @accent_fg_color;\n    border-color: @accent_color;\n    box-shadow: 0 6px 16px rgba(0, 123, 204, 0.25);\n}\n\n/* Modern Player Configuration Styling */\n.player-frame {\n    background-color: @card_bg_color;\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);\n}\n\n.player-frame > label {\n    color: @accent_color;\n    font-weight: 600;\n    font-size: 1.1em;\n}\n\n/* Modern Environment Variables Styling */\n.env-var-row {\n    background-color: @input_bg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    margin: 4px 0;\n    padding: 8px;\n    transition: border-color 0.2s ease;\n}\n\n.env-var-row:hover {\n    border-color: @accent_color;\n}\n\n.env-var-remove-button {\n    color: @destructive_color;\n    background-color: transparent;\n    border: 1px solid @destructive_color;\n    border-radius: 4px;\n    min-width: 28px;\n    min-height: 28px;\n    transition: all 0.2s ease;\n}\n\n.env-var-remove-button:hover {\n    background-color: @destructive_color;\n    color: @destructive_fg_color;\n    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);\n}\n\n/* Modern Drawing Area Theme */\ndrawingarea {\n    background: linear-gradient(135deg, #f8f9fa, #e9ecef);\n    border: 2px solid @card_border_color;\n    border-radius: 8px;\n    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);\n}\n\n/* Modern Status Bar Theme */\n.statusbar {\n    background: linear-gradient(\n        180deg,\n        @headerbar_bg_color,\n        shade(@headerbar_bg_color, 0.98)\n    );\n    color: @text_secondary_color;\n    border-top: 1px solid @borders;\n    font-size: 0.85em;\n    font-weight: 500;\n    padding: 4px 8px;\n}\n\n/* Tooltip Theme */\ntooltip {\n    background-color: rgba(0, 0, 0, 0.8);\n    color: white;\n    border-radius: 4px;\n    padding: 4px 8px;\n    font-size: 0.85em;\n}\n\n/* Scrollbar Theme */\nscrollbar {\n    background: transparent;\n}\n\nscrollbar slider {\n    background-color: alpha(@window_fg_color, 0.3);\n    border-radius: 6px;\n    min-width: 8px;\n    min-height: 8px;\n}\n\nscrollbar slider:hover {\n    background-color: alpha(@window_fg_color, 0.5);\n}\n\nscrollbar slider:active {\n    background-color: @accent_color;\n}\n\n/* Dark Theme Colors - can be loaded separately when needed */\n.dark-theme {\n    background-color: #242424;\n    color: #ffffff;\n}\n\n.dark-theme window {\n    background-color: #242424;\n    color: #ffffff;\n}\n\n.dark-theme frame,\n.dark-theme .view {\n    background-color: #1e1e1e;\n    color: #ffffff;\n}\n\n.dark-theme .headerbar {\n    background-color: #2d2d2d;\n    color: #ffffff;\n}\n\n.dark-theme .sidebar {\n    background-color: #2a2a2a;\n    color: #ffffff;\n}\n\n.dark-theme entry,\n.dark-theme button {\n    border-color: #3d3d3d;\n}\n\n.dark-theme *:hover {\n    background-color: #333333;\n}\n",
  "old_text": "/* Theme CSS - Color schemes and theme-specific styles for Linux-Coop GUI */\n\n/* Color Definitions */\n@define-color accent_color #3584e4;\n@define-color accent_bg_color #3584e4;\n@define-color accent_fg_color #ffffff;\n@define-color destructive_color #e01b24;\n@define-color destructive_bg_color #e01b24;\n@define-color destructive_fg_color #ffffff;\n@define-color success_color #26a269;\n@define-color success_bg_color #26a269;\n@define-color success_fg_color #ffffff;\n@define-color warning_color #f5c211;\n@define-color warning_bg_color #f5c211;\n@define-color warning_fg_color #000000;\n\n/* Light Theme Colors */\n@define-color window_bg_color #fafafa;\n@define-color window_fg_color #2e3436;\n@define-color view_bg_color #ffffff;\n@define-color view_fg_color #2e3436;\n@define-color headerbar_bg_color #ebebeb;\n@define-color headerbar_fg_color #2e3436;\n@define-color sidebar_bg_color #f6f5f4;\n@define-color sidebar_fg_color #2e3436;\n@define-color borders #d4d0c8;\n@define-color view_hover_bg_color #f1f1f1;\n\n/* Action Button Styles */\n.suggested-action {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n    border: none;\n}\n\n.suggested-action:hover {\n    background-color: shade(@accent_bg_color, 1.1);\n}\n\n.suggested-action:active {\n    background-color: shade(@accent_bg_color, 0.9);\n}\n\n.destructive-action {\n    background-color: @destructive_bg_color;\n    color: @destructive_fg_color;\n    border: none;\n}\n\n.destructive-action:hover {\n    background-color: shade(@destructive_bg_color, 1.1);\n}\n\n.destructive-action:active {\n    background-color: shade(@destructive_bg_color, 0.9);\n}\n\n/* Success States */\n.success {\n    background-color: @success_bg_color;\n    color: @success_fg_color;\n}\n\n/* Warning States */\n.warning {\n    background-color: @warning_bg_color;\n    color: @warning_fg_color;\n}\n\n/* Focus and Selection States */\n*:focus {\n    outline: 2px solid @accent_color;\n    outline-offset: 2px;\n}\n\n*:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n}\n\n/* Disabled States */\n*:disabled {\n    opacity: 0.5;\n    color: shade(@window_fg_color, 1.5);\n}\n\n/* Error States */\n.error {\n    color: @destructive_color;\n    border-color: @destructive_color;\n}\n\nentry.error {\n    border: 2px solid @destructive_color;\n    background-color: shade(@destructive_color, 2.5);\n}\n\n/* Game Profile Specific Styling */\n.profile-item {\n    background-color: @view_bg_color;\n    border: 1px solid @borders;\n    border-radius: 4px;\n    margin: 2px;\n    padding: 8px;\n}\n\n.profile-item:hover {\n    background-color: @view_hover_bg_color;\n    border-color: @accent_color;\n}\n\n.profile-item:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n    border-color: @accent_color;\n}\n\n/* Player Configuration Styling */\n.player-frame {\n    background-color: @view_bg_color;\n    border: 1px solid @borders;\n    border-radius: 6px;\n}\n\n.player-frame > label {\n    color: @accent_color;\n    font-weight: bold;\n}\n\n/* Environment Variables Styling */\n.env-var-row {\n    background-color: @view_bg_color;\n    border: 1px solid @borders;\n    border-radius: 4px;\n    margin: 2px 0;\n    padding: 4px;\n}\n\n.env-var-remove-button {\n    color: @destructive_color;\n    background-color: transparent;\n    border: 1px solid @destructive_color;\n    border-radius: 3px;\n    min-width: 24px;\n    min-height: 24px;\n}\n\n.env-var-remove-button:hover {\n    background-color: @destructive_color;\n    color: @destructive_fg_color;\n}\n\n/* Drawing Area Theme */\ndrawingarea {\n    background-color: #2d2d2d;\n    border: 2px solid @borders;\n}\n\n/* Status Bar Theme */\n.statusbar {\n    background-color: @headerbar_bg_color;\n    color: @headerbar_fg_color;\n    border-top: 1px solid @borders;\n    font-size: 0.9em;\n}\n\n/* Tooltip Theme */\ntooltip {\n    background-color: rgba(0, 0, 0, 0.8);\n    color: white;\n    border-radius: 4px;\n    padding: 4px 8px;\n    font-size: 0.85em;\n}\n\n/* Scrollbar Theme */\nscrollbar {\n    background: transparent;\n}\n\nscrollbar slider {\n    background-color: alpha(@window_fg_color, 0.3);\n    border-radius: 6px;\n    min-width: 8px;\n    min-height: 8px;\n}\n\nscrollbar slider:hover {\n    background-color: alpha(@window_fg_color, 0.5);\n}\n\nscrollbar slider:active {\n    background-color: @accent_color;\n}\n\n/* Dark Theme Colors - can be loaded separately when needed */\n.dark-theme {\n    background-color: #242424;\n    color: #ffffff;\n}\n\n.dark-theme window {\n    background-color: #242424;\n    color: #ffffff;\n}\n\n.dark-theme frame,\n.dark-theme .view {\n    background-color: #1e1e1e;\n    color: #ffffff;\n}\n\n.dark-theme .headerbar {\n    background-color: #2d2d2d;\n    color: #ffffff;\n}\n\n.dark-theme .sidebar {\n    background-color: #2a2a2a;\n    color: #ffffff;\n}\n\n.dark-theme entry,\n.dark-theme button {\n    border-color: #3d3d3d;\n}\n\n.dark-theme *:hover {\n    background-color: #333333;\n}\n",
  "raw_output": {
    "raw_edits": "<edits>\n\n<old_text line=3>\n/* Color Definitions */\n@define-color accent_color #3584e4;\n@define-color accent_bg_color #3584e4;\n@define-color accent_fg_color #ffffff;\n@define-color destructive_color #e01b24;\n@define-color destructive_bg_color #e01b24;\n@define-color destructive_fg_color #ffffff;\n@define-color success_color #26a269;\n@define-color success_bg_color #26a269;\n@define-color success_fg_color #ffffff;\n@define-color warning_color #f5c211;\n@define-color warning_bg_color #f5c211;\n@define-color warning_fg_color #000000;\n</old_text>\n<new_text>\n/* Modern UI/UX Color Definitions - Light Theme */\n@define-color accent_color #007acc;\n@define-color accent_bg_color #007acc;\n@define-color accent_fg_color #ffffff;\n@define-color accent_hover_color #005a9e;\n@define-color accent_active_color #004578;\n@define-color destructive_color #dc3545;\n@define-color destructive_bg_color #dc3545;\n@define-color destructive_fg_color #ffffff;\n@define-color destructive_hover_color #c82333;\n@define-color success_color #28a745;\n@define-color success_bg_color #28a745;\n@define-color success_fg_color #ffffff;\n@define-color success_hover_color #218838;\n@define-color warning_color #ffc107;\n@define-color warning_bg_color #ffc107;\n@define-color warning_fg_color #212529;\n@define-color warning_hover_color #e0a800;\n</old_text>\n\n<old_text line=17>\n/* Light Theme Colors */\n@define-color window_bg_color #fafafa;\n@define-color window_fg_color #2e3436;\n@define-color view_bg_color #ffffff;\n@define-color view_fg_color #2e3436;\n@define-color headerbar_bg_color #ebebeb;\n@define-color headerbar_fg_color #2e3436;\n@define-color sidebar_bg_color #f6f5f4;\n@define-color sidebar_fg_color #2e3436;\n@define-color borders #d4d0c8;\n@define-color view_hover_bg_color #f1f1f1;\n</old_text>\n<new_text>\n/* Modern Light Theme Colors */\n@define-color window_bg_color #f8f9fa;\n@define-color window_fg_color #212529;\n@define-color view_bg_color #ffffff;\n@define-color view_fg_color #343a40;\n@define-color headerbar_bg_color #e9ecef;\n@define-color headerbar_fg_color #495057;\n@define-color sidebar_bg_color #f1f3f4;\n@define-color sidebar_fg_color #495057;\n@define-color borders #dee2e6;\n@define-color view_hover_bg_color #e9ecef;\n@define-color card_bg_color #ffffff;\n@define-color card_border_color #e9ecef;\n@define-color input_bg_color #ffffff;\n@define-color input_border_color #ced4da;\n@define-color input_focus_border_color #007acc;\n@define-color text_secondary_color #6c757d;\n@define-color text_muted_color #868e96;\n</old_text>\n\n<old_text line=29>\n/* Action Button Styles */\n.suggested-action {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n    border: none;\n}\n\n.suggested-action:hover {\n    background-color: shade(@accent_bg_color, 1.1);\n}\n\n.suggested-action:active {\n    background-color: shade(@accent_bg_color, 0.9);\n}\n</old_text>\n<new_text>\n/* Modern Action Button Styles */\n.suggested-action {\n    background: linear-gradient(135deg, @accent_bg_color, shade(@accent_bg_color, 0.95));\n    color: @accent_fg_color;\n    border: 1px solid transparent;\n    border-radius: 6px;\n    box-shadow: 0 2px 4px rgba(0, 123, 204, 0.15);\n    transition: all 0.2s ease;\n}\n\n.suggested-action:hover {\n    background: linear-gradient(135deg, @accent_hover_color, shade(@accent_hover_color, 0.95));\n    box-shadow: 0 4px 8px rgba(0, 123, 204, 0.25);\n    transform: translateY(-1px);\n}\n\n.suggested-action:active {\n    background-color: @accent_active_color;\n    box-shadow: 0 1px 2px rgba(0, 123, 204, 0.2);\n    transform: translateY(0);\n}\n</new_text>\n\n<old_text line=43>\n.destructive-action {\n    background-color: @destructive_bg_color;\n    color: @destructive_fg_color;\n    border: none;\n}\n\n.destructive-action:hover {\n    background-color: shade(@destructive_bg_color, 1.1);\n}\n\n.destructive-action:active {\n    background-color: shade(@destructive_bg_color, 0.9);\n}\n</old_text>\n<new_text>\n.destructive-action {\n    background: linear-gradient(135deg, @destructive_bg_color, shade(@destructive_bg_color, 0.95));\n    color: @destructive_fg_color;\n    border: 1px solid transparent;\n    border-radius: 6px;\n    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.15);\n    transition: all 0.2s ease;\n}\n\n.destructive-action:hover {\n    background: linear-gradient(135deg, @destructive_hover_color, shade(@destructive_hover_color, 0.95));\n    box-shadow: 0 4px 8px rgba(220, 53, 69, 0.25);\n    transform: translateY(-1px);\n}\n\n.destructive-action:active {\n    background-color: shade(@destructive_bg_color, 0.8);\n    box-shadow: 0 1px 2px rgba(220, 53, 69, 0.2);\n    transform: translateY(0);\n}\n</new_text>\n\n<old_text line=57>\n/* Success States */\n.success {\n    background-color: @success_bg_color;\n    color: @success_fg_color;\n}\n\n/* Warning States */\n.warning {\n    background-color: @warning_bg_color;\n    color: @warning_fg_color;\n}\n</old_text>\n<new_text>\n/* Modern Success States */\n.success {\n    background: linear-gradient(135deg, @success_bg_color, shade(@success_bg_color, 0.95));\n    color: @success_fg_color;\n    border: 1px solid @success_hover_color;\n    border-radius: 4px;\n    box-shadow: 0 2px 4px rgba(40, 167, 69, 0.15);\n}\n\n/* Modern Warning States */\n.warning {\n    background: linear-gradient(135deg, @warning_bg_color, shade(@warning_bg_color, 0.95));\n    color: @warning_fg_color;\n    border: 1px solid @warning_hover_color;\n    border-radius: 4px;\n    box-shadow: 0 2px 4px rgba(255, 193, 7, 0.15);\n}\n</new_text>\n\n<old_text line=67>\n/* Focus and Selection States */\n*:focus {\n    outline: 2px solid @accent_color;\n    outline-offset: 2px;\n}\n\n*:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n}\n</old_text>\n<new_text>\n/* Modern Focus and Selection States */\n*:focus {\n    outline: 2px solid @input_focus_border_color;\n    outline-offset: 2px;\n    outline-style: solid;\n    box-shadow: 0 0 0 3px rgba(0, 123, 204, 0.1);\n}\n\n*:selected {\n    background: linear-gradient(135deg, @accent_bg_color, shade(@accent_bg_color, 0.95));\n    color: @accent_fg_color;\n    border-radius: 3px;\n}\n</new_text>\n\n<old_text line=97>\n/* Game Profile Specific Styling */\n.profile-item {\n    background-color: @view_bg_color;\n    border: 1px solid @borders;\n    border-radius: 4px;\n    margin: 2px;\n    padding: 8px;\n}\n\n.profile-item:hover {\n    background-color: @view_hover_bg_color;\n    border-color: @accent_color;\n}\n\n.profile-item:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n    border-color: @accent_color;\n}\n</old_text>\n<new_text>\n/* Modern Game Profile Styling */\n.profile-item {\n    background-color: @card_bg_color;\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    margin: 4px;\n    padding: 12px;\n    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);\n    transition: all 0.2s ease;\n}\n\n.profile-item:hover {\n    background-color: @view_hover_bg_color;\n    border-color: @accent_color;\n    box-shadow: 0 4px 12px rgba(0, 123, 204, 0.15);\n    transform: translateY(-2px);\n}\n\n.profile-item:selected {\n    background: linear-gradient(135deg, @accent_bg_color, shade(@accent_bg_color, 0.95));\n    color: @accent_fg_color;\n    border-color: @accent_color;\n    box-shadow: 0 6px 16px rgba(0, 123, 204, 0.25);\n}\n</old_text>\n\n<old_text line=115>\n/* Player Configuration Styling */\n.player-frame {\n    background-color: @view_bg_color;\n    border: 1px solid @borders;\n    border-radius: 6px;\n}\n\n.player-frame > label {\n    color: @accent_color;\n    font-weight: bold;\n}\n</old_text>\n<new_text>\n/* Modern Player Configuration Styling */\n.player-frame {\n    background-color: @card_bg_color;\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);\n}\n\n.player-frame > label {\n    color: @accent_color;\n    font-weight: 600;\n    font-size: 1.1em;\n}\n</new_text>\n\n<old_text line=125>\n/* Environment Variables Styling */\n.env-var-row {\n    background-color: @view_bg_color;\n    border: 1px solid @borders;\n    border-radius: 4px;\n    margin: 2px 0;\n    padding: 4px;\n}\n\n.env-var-remove-button {\n    color: @destructive_color;\n    background-color: transparent;\n    border: 1px solid @destructive_color;\n    border-radius: 3px;\n    min-width: 24px;\n    min-height: 24px;\n}\n\n.env-var-remove-button:hover {\n    background-color: @destructive_color;\n    color: @destructive_fg_color;\n}\n</old_text>\n<new_text>\n/* Modern Environment Variables Styling */\n.env-var-row {\n    background-color: @input_bg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    margin: 4px 0;\n    padding: 8px;\n    transition: border-color 0.2s ease;\n}\n\n.env-var-row:hover {\n    border-color: @accent_color;\n}\n\n.env-var-remove-button {\n    color: @destructive_color;\n    background-color: transparent;\n    border: 1px solid @destructive_color;\n    border-radius: 4px;\n    min-width: 28px;\n    min-height: 28px;\n    transition: all 0.2s ease;\n}\n\n.env-var-remove-button:hover {\n    background-color: @destructive_color;\n    color: @destructive_fg_color;\n    box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);\n}\n</new_text>\n\n<old_text line=147>\n/* Drawing Area Theme */\ndrawingarea {\n    background-color: #2d2d2d;\n    border: 2px solid @borders;\n}\n</old_text>\n<new_text>\n/* Modern Drawing Area Theme */\ndrawingarea {\n    background: linear-gradient(135deg, #f8f9fa, #e9ecef);\n    border: 2px solid @card_border_color;\n    border-radius: 8px;\n    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);\n}\n</new_text>\n\n<old_text line=152>\n/* Status Bar Theme */\n.statusbar {\n    background-color: @headerbar_bg_color;\n    color: @headerbar_fg_color;\n    border-top: 1px solid @borders;\n    font-size: 0.9em;\n}\n</old_text>\n<new_text>\n/* Modern Status Bar Theme */\n.statusbar {\n    background: linear-gradient(180deg, @headerbar_bg_color, shade(@headerbar_bg_color, 0.98));\n    color: @text_secondary_color;\n    border-top: 1px solid @borders;\n    font-size: 0.85em;\n    font-weight: 500;\n    padding: 4px 8px;\n}\n</new_text>\n\n</edits>",
    "parser_metrics": {
      "tags": 22,
      "mismatched_tags": 3
    }
  }
}
```

## Agent

## 2. Agora vou atualizar o tema escuro com cores mais modernas e melhor contraste:

**Use Tool: edit_file (toolu_0119JbD1eJNWNyX7sGmuX2hj)**
```json
{
  "display_description": "Update dark theme with modern UI/UX color principles and better contrast ratios",
  "mode": "edit",
  "path": "Linux-Coop/src/gui/styles/theme-dark.css"
}
```

**Tool Results: toolu_0119JbD1eJNWNyX7sGmuX2hj**

Edited Linux-Coop/src/gui/styles/theme-dark.css:

```diff
@@ -1,199 +1,408 @@
-/* Dark Theme CSS - Specific styling for dark theme in Linux-Coop GUI */
+/* Dark Theme CSS - Modern dark theme with optimal contrast and visual hierarchy */
 
-/* Dark Theme Color Overrides */
+/* Modern UI/UX Dark Theme Color Definitions */
+@define-color accent_color #4fc3f7;
+@define-color accent_bg_color #4fc3f7;
+@define-color accent_fg_color #0d1117;
+@define-color accent_hover_color #29b6f6;
+@define-color accent_active_color #03a9f4;
+@define-color destructive_color #f85149;
+@define-color destructive_bg_color #f85149;
+@define-color destructive_fg_color #ffffff;
+@define-color destructive_hover_color #da3633;
+@define-color success_color #56d364;
+@define-color success_bg_color #56d364;
+@define-color success_fg_color #0d1117;
+@define-color success_hover_color #46d160;
+@define-color warning_color #f0883e;
+@define-color warning_bg_color #f0883e;
+@define-color warning_fg_color #0d1117;
+@define-color warning_hover_color #db6e28;
 
-@define-color window_bg_color #242424;
-@define-color window_fg_color #ffffff;
-@define-color view_bg_color #1e1e1e;
-@define-color view_fg_color #ffffff;
-@define-color headerbar_bg_color #2d2d2d;
-@define-color headerbar_fg_color #ffffff;
-@define-color sidebar_bg_color #2a2a2a;
-@define-color sidebar_fg_color #ffffff;
-@define-color borders #3d3d3d;
-@define-color view_hover_bg_color #333333;
+/* Modern Dark Theme Base Colors */
+@define-color window_bg_color #0d1117;
+@define-color window_fg_color #e6edf3;
+@define-color view_bg_color #161b22;
+@define-color view_fg_color #f0f6fc;
+@define-color headerbar_bg_color #21262d;
+@define-color headerbar_fg_color #e6edf3;
+@define-color sidebar_bg_color #0d1117;
+@define-color sidebar_fg_color #e6edf3;
+@define-color borders #30363d;
+@define-color view_hover_bg_color #21262d;
+@define-color card_bg_color #161b22;
+@define-color card_border_color #30363d;
+@define-color input_bg_color #0d1117;
+@define-color input_border_color #30363d;
+@define-color input_focus_border_color #4fc3f7;
+@define-color text_secondary_color #8b949e;
+@define-color text_muted_color #6e7681;
 
-/* Dark theme specific window styling */
+/* Modern Dark Theme Window Styling */
 window {
-    background-color: @window_bg_color;
+    background: linear-gradient(
+        135deg,
+        @window_bg_color,
+        shade(@window_bg_color, 1.05)
+    );
     color: @window_fg_color;
 }
 
-/* Dark theme frames */
+/* Modern Dark Theme Frames */
 frame {
-    background-color: @view_bg_color;
-    border-color: @borders;
+    background: linear-gradient(
+        135deg,
+        @card_bg_color,
+        shade(@card_bg_color, 1.02)
+    );
+    border: 1px solid @card_border_color;
+    border-radius: 8px;
     color: @view_fg_color;
+    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
 }
 
 frame > label {
     color: @accent_color;
+    font-weight: 600;
+    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
 }
 
-/* Dark theme entries and inputs */
+/* Modern Dark Theme Entries and Inputs */
 entry {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @input_bg_color,
+        shade(@input_bg_color, 1.05)
+    );
     color: @view_fg_color;
-    border-color: @borders;
+    border: 1px solid @input_border_color;
+    border-radius: 6px;
+    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
 }
 
 entry:focus {
-    border-color: @accent_color;
-    box-shadow: inset 0 0 0 1px @accent_color;
+    border-color: @input_focus_border_color;
+    box-shadow:
+        inset 0 1px 3px rgba(0, 0, 0, 0.2),
+        0 0 0 3px rgba(79, 195, 247, 0.15);
+    background: linear-gradient(
+        135deg,
+        shade(@input_bg_color, 1.1),
+        shade(@input_bg_color, 1.15)
+    );
 }
 
-/* Dark theme buttons */
+/* Modern Dark Theme Buttons */
 button {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @card_bg_color,
+        shade(@card_bg_color, 1.05)
+    );
     color: @view_fg_color;
-    border-color: @borders;
+    border: 1px solid @borders;
+    border-radius: 6px;
+    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
+    transition: all 0.2s ease;
 }
 
 button:hover {
-    background-color: @view_hover_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_hover_bg_color,
+        shade(@view_hover_bg_color, 1.05)
+    );
+    border-color: @accent_color;
+    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
+    transform: translateY(-1px);
 }
 
 button:active {
-    background-color: shade(@view_hover_bg_color, 0.8);
+    background: linear-gradient(
+        135deg,
+        shade(@view_hover_bg_color, 0.9),
+        shade(@view_hover_bg_color, 0.95)
+    );
+    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
+    transform: translateY(0);
 }
 
-/* Dark theme combo boxes and dropdowns */
+/* Modern Dark Theme Combo Boxes and Dropdowns */
 combobox,
 dropdown {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @input_bg_color,
+        shade(@input_bg_color, 1.05)
+    );
     color: @view_fg_color;
-    border-color: @borders;
+    border: 1px solid @input_border_color;
+    border-radius: 6px;
+    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
 }
 
 combobox:hover,
 dropdown:hover {
-    background-color: @view_hover_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_hover_bg_color,
+        shade(@view_hover_bg_color, 1.05)
+    );
+    border-color: @accent_color;
+    box-shadow:
+        inset 0 1px 3px rgba(0, 0, 0, 0.2),
+        0 2px 4px rgba(0, 0, 0, 0.15);
 }
 
-/* Dark theme spin buttons */
+/* Modern Dark Theme Spin Buttons */
 spinbutton {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @input_bg_color,
+        shade(@input_bg_color, 1.05)
+    );
     color: @view_fg_color;
-    border-color: @borders;
+    border: 1px solid @input_border_color;
+    border-radius: 6px;
+    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
 }
 
 spinbutton:focus {
-    border-color: @accent_color;
+    border-color: @input_focus_border_color;
+    box-shadow:
+        inset 0 1px 3px rgba(0, 0, 0, 0.2),
+        0 0 0 3px rgba(79, 195, 247, 0.15);
 }
 
-/* Dark theme notebook */
+/* Modern Dark Theme Notebook */
 notebook {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_bg_color,
+        shade(@view_bg_color, 1.02)
+    );
+    border-radius: 8px;
 }
 
 notebook > header {
-    background-color: @headerbar_bg_color;
-    border-color: @borders;
+    background: linear-gradient(
+        180deg,
+        @headerbar_bg_color,
+        shade(@headerbar_bg_color, 0.98)
+    );
+    border-bottom: 1px solid @borders;
+    border-radius: 8px 8px 0 0;
 }
 
 notebook > header > tabs > tab {
-    background-color: transparent;
-    color: @headerbar_fg_color;
-    border-color: @borders;
+    background: transparent;
+    color: @text_secondary_color;
+    border: 1px solid transparent;
+    border-radius: 6px 6px 0 0;
+    margin: 2px;
+    transition: all 0.2s ease;
 }
 
 notebook > header > tabs > tab:checked {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_bg_color,
+        shade(@view_bg_color, 1.05)
+    );
     color: @accent_color;
+    border-color: @borders;
+    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
 }
 
 notebook > stack {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_bg_color,
+        shade(@view_bg_color, 1.02)
+    );
+    border-radius: 0 0 8px 8px;
 }
 
-/* Dark theme listbox */
+/* Modern Dark Theme Listbox */
 listbox {
-    background-color: @view_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_bg_color,
+        shade(@view_bg_color, 1.02)
+    );
     color: @view_fg_color;
+    border-radius: 8px;
+    border: 1px solid @borders;
 }
 
 listbox > row {
-    background-color: transparent;
+    background: transparent;
     color: @view_fg_color;
+    border-radius: 4px;
+    margin: 2px;
+    transition: all 0.2s ease;
 }
 
 listbox > row:hover {
-    background-color: @view_hover_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_hover_bg_color,
+        shade(@view_hover_bg_color, 1.05)
+    );
+    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
 }
 
 listbox > row:selected {
-    background-color: @accent_bg_color;
+    background: linear-gradient(
+        135deg,
+        @accent_bg_color,
+        shade(@accent_bg_color, 0.95)
+    );
     color: @accent_fg_color;
+    box-shadow: 0 4px 8px rgba(79, 195, 247, 0.25);
+    border: 1px solid @accent_color;
 }
 
-/* Dark theme scrolled windows */
+/* Modern Dark Theme Scrolled Windows */
 scrolledwindow {
-    background-color: @view_bg_color;
-    border-color: @borders;
+    background: linear-gradient(
+        135deg,
+        @view_bg_color,
+        shade(@view_bg_color, 1.02)
+    );
+    border: 1px solid @borders;
+    border-radius: 8px;
 }
 
-/* Dark theme drawing area */
+/* Modern Dark Theme Drawing Area */
 drawingarea {
-    background-color: #1a1a1a;
-    border-color: @borders;
+    background: linear-gradient(135deg, #0f1419, #161b22);
+    border: 2px solid @borders;
+    border-radius: 8px;
+    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.4);
 }
 
-/* Dark theme status bar */
+/* Modern Dark Theme Status Bar */
 .statusbar {
-    background-color: @headerbar_bg_color;
-    color: @headerbar_fg_color;
-    border-color: @borders;
+    background: linear-gradient(
+        180deg,
+        @headerbar_bg_color,
+        shade(@headerbar_bg_color, 0.98)
+    );
+    color: @text_secondary_color;
+    border-top: 1px solid @borders;
+    font-size: 0.85em;
+    font-weight: 500;
+    padding: 4px 8px;
+    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
 }
 
-/* Dark theme profile list */
+/* Modern Dark Theme Profile List */
 .profile-list {
-    background-color: @sidebar_bg_color;
-    border-color: @borders;
+    background: linear-gradient(
+        135deg,
+        @sidebar_bg_color,
+        shade(@sidebar_bg_color, 1.05)
+    );
+    border-right: 1px solid @borders;
+    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.2);
 }
 
 .profile-list-item {
-    background-color: transparent;
+    background: transparent;
     color: @sidebar_fg_color;
-    border-color: @borders;
+    border: 1px solid transparent;
+    border-radius: 8px;
+    margin: 4px;
+    padding: 12px;
+    transition: all 0.2s ease;
+    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
 }
 
 .profile-list-item:hover {
-    background-color: @view_hover_bg_color;
+    background: linear-gradient(
+        135deg,
+        @view_hover_bg_color,
+        shade(@view_hover_bg_color, 1.05)
+    );
+    border-color: @accent_color;
+    box-shadow: 0 4px 12px rgba(79, 195, 247, 0.15);
+    transform: translateY(-2px);
 }
 
 .profile-list-item:selected {
-    background-color: @accent_bg_color;
+    background: linear-gradient(
+        135deg,
+        @accent_bg_color,
+        shade(@accent_bg_color, 0.95)
+    );
     color: @accent_fg_color;
+    border-color: @accent_color;
+    box-shadow: 0 6px 16px rgba(79, 195, 247, 0.25);
+    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
 }
 
-/* Dark theme player configuration */
+/* Modern Dark Theme Player Configuration */
 .player-frame {
-    background-color: @view_bg_color;
-    border-color: @borders;
+    background: linear-gradient(
+        135deg,
+        @card_bg_color,
+        shade(@card_bg_color, 1.05)
+    );
+    border: 1px solid @card_border_color;
+    border-radius: 8px;
+    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
 }
 
 .player-frame > label {
     color: @accent_color;
+    font-weight: 600;
+    font-size: 1.1em;
+    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
 }
 
-/* Dark theme environment variables */
+/* Modern Dark Theme Environment Variables */
 .env-var-row {
-    background-color: @view_bg_color;
-    border-color: @borders;
+    background: linear-gradient(
+        135deg,
+        @input_bg_color,
+        shade(@input_bg_color, 1.05)
+    );
+    border: 1px solid @input_border_color;
+    border-radius: 6px;
+    margin: 4px 0;
+    padding: 8px;
+    transition: all 0.2s ease;
+    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
+}
+
+.env-var-row:hover {
+    border-color: @accent_color;
+    box-shadow: 0 2px 6px rgba(79, 195, 247, 0.15);
 }
 
 .env-var-remove-button {
-    background-color: transparent;
+    background: transparent;
     color: @destructive_color;
-    border-color: @destructive_color;
+    border: 1px solid @destructive_color;
+    border-radius: 4px;
+    min-width: 28px;
+    min-height: 28px;
+    transition: all 0.2s ease;
 }
 
 .env-var-remove-button:hover {
-    background-color: @destructive_color;
+    background: linear-gradient(
+        135deg,
+        @destructive_color,
+        shade(@destructive_color, 0.95)
+    );
     color: @destructive_fg_color;
+    box-shadow: 0 2px 4px rgba(248, 81, 73, 0.3);
+    transform: scale(1.05);
 }
 
-/* Dark theme checkboxes and radio buttons */
+/* Modern Dark Theme Controls */
 checkbutton,
 radiobutton {
     color: @view_fg_color;
@@ -202,39 +411,64 @@
 checkbutton:checked,
 radiobutton:checked {
     color: @accent_color;
+    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
 }
 
-/* Dark theme labels */
+/* Modern Dark Theme Labels */
 label {
     color: @view_fg_color;
 }
 
-/* Dark theme separator */
+/* Modern Dark Theme Separators */
 separator {
-    background-color: @borders;
+    background: linear-gradient(90deg, transparent, @borders, transparent);
 }
 
-/* Dark theme paned */
 paned > separator {
-    background-color: @borders;
+    background: linear-gradient(90deg, transparent, @borders, transparent);
+    min-width: 1px;
+    min-height: 1px;
 }
 
-/* Dark theme tooltip */
+/* Modern Dark Theme Tooltips */
 tooltip {
-    background-color: rgba(45, 45, 45, 0.95);
+    background: linear-gradient(
+        135deg,
+        rgba(33, 38, 45, 0.98),
+        rgba(13, 17, 23, 0.98)
+    );
     color: @window_fg_color;
-    border: 1px solid @borders;
+    border: 1px solid @accent_color;
+    border-radius: 6px;
+    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
+    backdrop-filter: blur(8px);
 }
 
-/* Dark theme scrollbars */
+/* Modern Dark Theme Scrollbars */
 scrollbar slider {
-    background-color: alpha(@window_fg_color, 0.4);
+    background: linear-gradient(
+        135deg,
+        rgba(139, 148, 158, 0.5),
+        rgba(110, 118, 129, 0.6)
+    );
+    border-radius: 6px;
+    transition: all 0.2s ease;
 }
 
 scrollbar slider:hover {
-    background-color: alpha(@window_fg_color, 0.6);
+    background: linear-gradient(
+        135deg,
+        rgba(139, 148, 158, 0.7),
+        rgba(110, 118, 129, 0.8)
+    );
+    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
 }
 
 scrollbar slider:active {
-    background-color: @accent_color;
+    background: linear-gradient(
+        135deg,
+        @accent_color,
+        shade(@accent_color, 0.9)
+    );
+    box-shadow: 0 2px 8px rgba(79, 195, 247, 0.3);
 }

```


Debug Output:

```json
{
  "original_path": "src/gui/styles/theme-dark.css",
  "new_text": "/* Dark Theme CSS - Modern dark theme with optimal contrast and visual hierarchy */\n\n/* Modern UI/UX Dark Theme Color Definitions */\n@define-color accent_color #4fc3f7;\n@define-color accent_bg_color #4fc3f7;\n@define-color accent_fg_color #0d1117;\n@define-color accent_hover_color #29b6f6;\n@define-color accent_active_color #03a9f4;\n@define-color destructive_color #f85149;\n@define-color destructive_bg_color #f85149;\n@define-color destructive_fg_color #ffffff;\n@define-color destructive_hover_color #da3633;\n@define-color success_color #56d364;\n@define-color success_bg_color #56d364;\n@define-color success_fg_color #0d1117;\n@define-color success_hover_color #46d160;\n@define-color warning_color #f0883e;\n@define-color warning_bg_color #f0883e;\n@define-color warning_fg_color #0d1117;\n@define-color warning_hover_color #db6e28;\n\n/* Modern Dark Theme Base Colors */\n@define-color window_bg_color #0d1117;\n@define-color window_fg_color #e6edf3;\n@define-color view_bg_color #161b22;\n@define-color view_fg_color #f0f6fc;\n@define-color headerbar_bg_color #21262d;\n@define-color headerbar_fg_color #e6edf3;\n@define-color sidebar_bg_color #0d1117;\n@define-color sidebar_fg_color #e6edf3;\n@define-color borders #30363d;\n@define-color view_hover_bg_color #21262d;\n@define-color card_bg_color #161b22;\n@define-color card_border_color #30363d;\n@define-color input_bg_color #0d1117;\n@define-color input_border_color #30363d;\n@define-color input_focus_border_color #4fc3f7;\n@define-color text_secondary_color #8b949e;\n@define-color text_muted_color #6e7681;\n\n/* Modern Dark Theme Window Styling */\nwindow {\n    background: linear-gradient(\n        135deg,\n        @window_bg_color,\n        shade(@window_bg_color, 1.05)\n    );\n    color: @window_fg_color;\n}\n\n/* Modern Dark Theme Frames */\nframe {\n    background: linear-gradient(\n        135deg,\n        @card_bg_color,\n        shade(@card_bg_color, 1.02)\n    );\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    color: @view_fg_color;\n    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);\n}\n\nframe > label {\n    color: @accent_color;\n    font-weight: 600;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);\n}\n\n/* Modern Dark Theme Entries and Inputs */\nentry {\n    background: linear-gradient(\n        135deg,\n        @input_bg_color,\n        shade(@input_bg_color, 1.05)\n    );\n    color: @view_fg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\nentry:focus {\n    border-color: @input_focus_border_color;\n    box-shadow:\n        inset 0 1px 3px rgba(0, 0, 0, 0.2),\n        0 0 0 3px rgba(79, 195, 247, 0.15);\n    background: linear-gradient(\n        135deg,\n        shade(@input_bg_color, 1.1),\n        shade(@input_bg_color, 1.15)\n    );\n}\n\n/* Modern Dark Theme Buttons */\nbutton {\n    background: linear-gradient(\n        135deg,\n        @card_bg_color,\n        shade(@card_bg_color, 1.05)\n    );\n    color: @view_fg_color;\n    border: 1px solid @borders;\n    border-radius: 6px;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);\n    transition: all 0.2s ease;\n}\n\nbutton:hover {\n    background: linear-gradient(\n        135deg,\n        @view_hover_bg_color,\n        shade(@view_hover_bg_color, 1.05)\n    );\n    border-color: @accent_color;\n    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);\n    transform: translateY(-1px);\n}\n\nbutton:active {\n    background: linear-gradient(\n        135deg,\n        shade(@view_hover_bg_color, 0.9),\n        shade(@view_hover_bg_color, 0.95)\n    );\n    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);\n    transform: translateY(0);\n}\n\n/* Modern Dark Theme Combo Boxes and Dropdowns */\ncombobox,\ndropdown {\n    background: linear-gradient(\n        135deg,\n        @input_bg_color,\n        shade(@input_bg_color, 1.05)\n    );\n    color: @view_fg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\ncombobox:hover,\ndropdown:hover {\n    background: linear-gradient(\n        135deg,\n        @view_hover_bg_color,\n        shade(@view_hover_bg_color, 1.05)\n    );\n    border-color: @accent_color;\n    box-shadow:\n        inset 0 1px 3px rgba(0, 0, 0, 0.2),\n        0 2px 4px rgba(0, 0, 0, 0.15);\n}\n\n/* Modern Dark Theme Spin Buttons */\nspinbutton {\n    background: linear-gradient(\n        135deg,\n        @input_bg_color,\n        shade(@input_bg_color, 1.05)\n    );\n    color: @view_fg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\nspinbutton:focus {\n    border-color: @input_focus_border_color;\n    box-shadow:\n        inset 0 1px 3px rgba(0, 0, 0, 0.2),\n        0 0 0 3px rgba(79, 195, 247, 0.15);\n}\n\n/* Modern Dark Theme Notebook */\nnotebook {\n    background: linear-gradient(\n        135deg,\n        @view_bg_color,\n        shade(@view_bg_color, 1.02)\n    );\n    border-radius: 8px;\n}\n\nnotebook > header {\n    background: linear-gradient(\n        180deg,\n        @headerbar_bg_color,\n        shade(@headerbar_bg_color, 0.98)\n    );\n    border-bottom: 1px solid @borders;\n    border-radius: 8px 8px 0 0;\n}\n\nnotebook > header > tabs > tab {\n    background: transparent;\n    color: @text_secondary_color;\n    border: 1px solid transparent;\n    border-radius: 6px 6px 0 0;\n    margin: 2px;\n    transition: all 0.2s ease;\n}\n\nnotebook > header > tabs > tab:checked {\n    background: linear-gradient(\n        135deg,\n        @view_bg_color,\n        shade(@view_bg_color, 1.05)\n    );\n    color: @accent_color;\n    border-color: @borders;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);\n}\n\nnotebook > stack {\n    background: linear-gradient(\n        135deg,\n        @view_bg_color,\n        shade(@view_bg_color, 1.02)\n    );\n    border-radius: 0 0 8px 8px;\n}\n\n/* Modern Dark Theme Listbox */\nlistbox {\n    background: linear-gradient(\n        135deg,\n        @view_bg_color,\n        shade(@view_bg_color, 1.02)\n    );\n    color: @view_fg_color;\n    border-radius: 8px;\n    border: 1px solid @borders;\n}\n\nlistbox > row {\n    background: transparent;\n    color: @view_fg_color;\n    border-radius: 4px;\n    margin: 2px;\n    transition: all 0.2s ease;\n}\n\nlistbox > row:hover {\n    background: linear-gradient(\n        135deg,\n        @view_hover_bg_color,\n        shade(@view_hover_bg_color, 1.05)\n    );\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);\n}\n\nlistbox > row:selected {\n    background: linear-gradient(\n        135deg,\n        @accent_bg_color,\n        shade(@accent_bg_color, 0.95)\n    );\n    color: @accent_fg_color;\n    box-shadow: 0 4px 8px rgba(79, 195, 247, 0.25);\n    border: 1px solid @accent_color;\n}\n\n/* Modern Dark Theme Scrolled Windows */\nscrolledwindow {\n    background: linear-gradient(\n        135deg,\n        @view_bg_color,\n        shade(@view_bg_color, 1.02)\n    );\n    border: 1px solid @borders;\n    border-radius: 8px;\n}\n\n/* Modern Dark Theme Drawing Area */\ndrawingarea {\n    background: linear-gradient(135deg, #0f1419, #161b22);\n    border: 2px solid @borders;\n    border-radius: 8px;\n    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.4);\n}\n\n/* Modern Dark Theme Status Bar */\n.statusbar {\n    background: linear-gradient(\n        180deg,\n        @headerbar_bg_color,\n        shade(@headerbar_bg_color, 0.98)\n    );\n    color: @text_secondary_color;\n    border-top: 1px solid @borders;\n    font-size: 0.85em;\n    font-weight: 500;\n    padding: 4px 8px;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);\n}\n\n/* Modern Dark Theme Profile List */\n.profile-list {\n    background: linear-gradient(\n        135deg,\n        @sidebar_bg_color,\n        shade(@sidebar_bg_color, 1.05)\n    );\n    border-right: 1px solid @borders;\n    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.2);\n}\n\n.profile-list-item {\n    background: transparent;\n    color: @sidebar_fg_color;\n    border: 1px solid transparent;\n    border-radius: 8px;\n    margin: 4px;\n    padding: 12px;\n    transition: all 0.2s ease;\n    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\n.profile-list-item:hover {\n    background: linear-gradient(\n        135deg,\n        @view_hover_bg_color,\n        shade(@view_hover_bg_color, 1.05)\n    );\n    border-color: @accent_color;\n    box-shadow: 0 4px 12px rgba(79, 195, 247, 0.15);\n    transform: translateY(-2px);\n}\n\n.profile-list-item:selected {\n    background: linear-gradient(\n        135deg,\n        @accent_bg_color,\n        shade(@accent_bg_color, 0.95)\n    );\n    color: @accent_fg_color;\n    border-color: @accent_color;\n    box-shadow: 0 6px 16px rgba(79, 195, 247, 0.25);\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n}\n\n/* Modern Dark Theme Player Configuration */\n.player-frame {\n    background: linear-gradient(\n        135deg,\n        @card_bg_color,\n        shade(@card_bg_color, 1.05)\n    );\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);\n}\n\n.player-frame > label {\n    color: @accent_color;\n    font-weight: 600;\n    font-size: 1.1em;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);\n}\n\n/* Modern Dark Theme Environment Variables */\n.env-var-row {\n    background: linear-gradient(\n        135deg,\n        @input_bg_color,\n        shade(@input_bg_color, 1.05)\n    );\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    margin: 4px 0;\n    padding: 8px;\n    transition: all 0.2s ease;\n    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\n.env-var-row:hover {\n    border-color: @accent_color;\n    box-shadow: 0 2px 6px rgba(79, 195, 247, 0.15);\n}\n\n.env-var-remove-button {\n    background: transparent;\n    color: @destructive_color;\n    border: 1px solid @destructive_color;\n    border-radius: 4px;\n    min-width: 28px;\n    min-height: 28px;\n    transition: all 0.2s ease;\n}\n\n.env-var-remove-button:hover {\n    background: linear-gradient(\n        135deg,\n        @destructive_color,\n        shade(@destructive_color, 0.95)\n    );\n    color: @destructive_fg_color;\n    box-shadow: 0 2px 4px rgba(248, 81, 73, 0.3);\n    transform: scale(1.05);\n}\n\n/* Modern Dark Theme Controls */\ncheckbutton,\nradiobutton {\n    color: @view_fg_color;\n}\n\ncheckbutton:checked,\nradiobutton:checked {\n    color: @accent_color;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n}\n\n/* Modern Dark Theme Labels */\nlabel {\n    color: @view_fg_color;\n}\n\n/* Modern Dark Theme Separators */\nseparator {\n    background: linear-gradient(90deg, transparent, @borders, transparent);\n}\n\npaned > separator {\n    background: linear-gradient(90deg, transparent, @borders, transparent);\n    min-width: 1px;\n    min-height: 1px;\n}\n\n/* Modern Dark Theme Tooltips */\ntooltip {\n    background: linear-gradient(\n        135deg,\n        rgba(33, 38, 45, 0.98),\n        rgba(13, 17, 23, 0.98)\n    );\n    color: @window_fg_color;\n    border: 1px solid @accent_color;\n    border-radius: 6px;\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);\n    backdrop-filter: blur(8px);\n}\n\n/* Modern Dark Theme Scrollbars */\nscrollbar slider {\n    background: linear-gradient(\n        135deg,\n        rgba(139, 148, 158, 0.5),\n        rgba(110, 118, 129, 0.6)\n    );\n    border-radius: 6px;\n    transition: all 0.2s ease;\n}\n\nscrollbar slider:hover {\n    background: linear-gradient(\n        135deg,\n        rgba(139, 148, 158, 0.7),\n        rgba(110, 118, 129, 0.8)\n    );\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);\n}\n\nscrollbar slider:active {\n    background: linear-gradient(\n        135deg,\n        @accent_color,\n        shade(@accent_color, 0.9)\n    );\n    box-shadow: 0 2px 8px rgba(79, 195, 247, 0.3);\n}\n",
  "old_text": "/* Dark Theme CSS - Specific styling for dark theme in Linux-Coop GUI */\n\n/* Dark Theme Color Overrides */\n\n@define-color window_bg_color #242424;\n@define-color window_fg_color #ffffff;\n@define-color view_bg_color #1e1e1e;\n@define-color view_fg_color #ffffff;\n@define-color headerbar_bg_color #2d2d2d;\n@define-color headerbar_fg_color #ffffff;\n@define-color sidebar_bg_color #2a2a2a;\n@define-color sidebar_fg_color #ffffff;\n@define-color borders #3d3d3d;\n@define-color view_hover_bg_color #333333;\n\n/* Dark theme specific window styling */\nwindow {\n    background-color: @window_bg_color;\n    color: @window_fg_color;\n}\n\n/* Dark theme frames */\nframe {\n    background-color: @view_bg_color;\n    border-color: @borders;\n    color: @view_fg_color;\n}\n\nframe > label {\n    color: @accent_color;\n}\n\n/* Dark theme entries and inputs */\nentry {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\nentry:focus {\n    border-color: @accent_color;\n    box-shadow: inset 0 0 0 1px @accent_color;\n}\n\n/* Dark theme buttons */\nbutton {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\nbutton:hover {\n    background-color: @view_hover_bg_color;\n}\n\nbutton:active {\n    background-color: shade(@view_hover_bg_color, 0.8);\n}\n\n/* Dark theme combo boxes and dropdowns */\ncombobox,\ndropdown {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\ncombobox:hover,\ndropdown:hover {\n    background-color: @view_hover_bg_color;\n}\n\n/* Dark theme spin buttons */\nspinbutton {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\nspinbutton:focus {\n    border-color: @accent_color;\n}\n\n/* Dark theme notebook */\nnotebook {\n    background-color: @view_bg_color;\n}\n\nnotebook > header {\n    background-color: @headerbar_bg_color;\n    border-color: @borders;\n}\n\nnotebook > header > tabs > tab {\n    background-color: transparent;\n    color: @headerbar_fg_color;\n    border-color: @borders;\n}\n\nnotebook > header > tabs > tab:checked {\n    background-color: @view_bg_color;\n    color: @accent_color;\n}\n\nnotebook > stack {\n    background-color: @view_bg_color;\n}\n\n/* Dark theme listbox */\nlistbox {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n}\n\nlistbox > row {\n    background-color: transparent;\n    color: @view_fg_color;\n}\n\nlistbox > row:hover {\n    background-color: @view_hover_bg_color;\n}\n\nlistbox > row:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n}\n\n/* Dark theme scrolled windows */\nscrolledwindow {\n    background-color: @view_bg_color;\n    border-color: @borders;\n}\n\n/* Dark theme drawing area */\ndrawingarea {\n    background-color: #1a1a1a;\n    border-color: @borders;\n}\n\n/* Dark theme status bar */\n.statusbar {\n    background-color: @headerbar_bg_color;\n    color: @headerbar_fg_color;\n    border-color: @borders;\n}\n\n/* Dark theme profile list */\n.profile-list {\n    background-color: @sidebar_bg_color;\n    border-color: @borders;\n}\n\n.profile-list-item {\n    background-color: transparent;\n    color: @sidebar_fg_color;\n    border-color: @borders;\n}\n\n.profile-list-item:hover {\n    background-color: @view_hover_bg_color;\n}\n\n.profile-list-item:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n}\n\n/* Dark theme player configuration */\n.player-frame {\n    background-color: @view_bg_color;\n    border-color: @borders;\n}\n\n.player-frame > label {\n    color: @accent_color;\n}\n\n/* Dark theme environment variables */\n.env-var-row {\n    background-color: @view_bg_color;\n    border-color: @borders;\n}\n\n.env-var-remove-button {\n    background-color: transparent;\n    color: @destructive_color;\n    border-color: @destructive_color;\n}\n\n.env-var-remove-button:hover {\n    background-color: @destructive_color;\n    color: @destructive_fg_color;\n}\n\n/* Dark theme checkboxes and radio buttons */\ncheckbutton,\nradiobutton {\n    color: @view_fg_color;\n}\n\ncheckbutton:checked,\nradiobutton:checked {\n    color: @accent_color;\n}\n\n/* Dark theme labels */\nlabel {\n    color: @view_fg_color;\n}\n\n/* Dark theme separator */\nseparator {\n    background-color: @borders;\n}\n\n/* Dark theme paned */\npaned > separator {\n    background-color: @borders;\n}\n\n/* Dark theme tooltip */\ntooltip {\n    background-color: rgba(45, 45, 45, 0.95);\n    color: @window_fg_color;\n    border: 1px solid @borders;\n}\n\n/* Dark theme scrollbars */\nscrollbar slider {\n    background-color: alpha(@window_fg_color, 0.4);\n}\n\nscrollbar slider:hover {\n    background-color: alpha(@window_fg_color, 0.6);\n}\n\nscrollbar slider:active {\n    background-color: @accent_color;\n}\n",
  "raw_output": {
    "raw_edits": "<edits>\n\n<old_text line=1>\n/* Dark Theme CSS - Specific styling for dark theme in Linux-Coop GUI */\n\n/* Dark Theme Color Overrides */\n@define-color window_bg_color #242424;\n@define-color window_fg_color #ffffff;\n@define-color view_bg_color #1e1e1e;\n@define-color view_fg_color #ffffff;\n@define-color headerbar_bg_color #2d2d2d;\n@define-color headerbar_fg_color #ffffff;\n@define-color sidebar_bg_color #2a2a2a;\n@define-color sidebar_fg_color #ffffff;\n@define-color borders #3d3d3d;\n@define-color view_hover_bg_color #333333;\n</old_text>\n<new_text>\n/* Dark Theme CSS - Modern dark theme with optimal contrast and visual hierarchy */\n\n/* Modern UI/UX Dark Theme Color Definitions */\n@define-color accent_color #4fc3f7;\n@define-color accent_bg_color #4fc3f7;\n@define-color accent_fg_color #0d1117;\n@define-color accent_hover_color #29b6f6;\n@define-color accent_active_color #03a9f4;\n@define-color destructive_color #f85149;\n@define-color destructive_bg_color #f85149;\n@define-color destructive_fg_color #ffffff;\n@define-color destructive_hover_color #da3633;\n@define-color success_color #56d364;\n@define-color success_bg_color #56d364;\n@define-color success_fg_color #0d1117;\n@define-color success_hover_color #46d160;\n@define-color warning_color #f0883e;\n@define-color warning_bg_color #f0883e;\n@define-color warning_fg_color #0d1117;\n@define-color warning_hover_color #db6e28;\n\n/* Modern Dark Theme Base Colors */\n@define-color window_bg_color #0d1117;\n@define-color window_fg_color #e6edf3;\n@define-color view_bg_color #161b22;\n@define-color view_fg_color #f0f6fc;\n@define-color headerbar_bg_color #21262d;\n@define-color headerbar_fg_color #e6edf3;\n@define-color sidebar_bg_color #0d1117;\n@define-color sidebar_fg_color #e6edf3;\n@define-color borders #30363d;\n@define-color view_hover_bg_color #21262d;\n@define-color card_bg_color #161b22;\n@define-color card_border_color #30363d;\n@define-color input_bg_color #0d1117;\n@define-color input_border_color #30363d;\n@define-color input_focus_border_color #4fc3f7;\n@define-color text_secondary_color #8b949e;\n@define-color text_muted_color #6e7681;\n</old_text>\n\n<old_text line=15>\n/* Dark theme specific window styling */\nwindow {\n    background-color: @window_bg_color;\n    color: @window_fg_color;\n}\n\n/* Dark theme frames */\nframe {\n    background-color: @view_bg_color;\n    border-color: @borders;\n    color: @view_fg_color;\n}\n\nframe > label {\n    color: @accent_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Window Styling */\nwindow {\n    background: linear-gradient(135deg, @window_bg_color, shade(@window_bg_color, 1.05));\n    color: @window_fg_color;\n}\n\n/* Modern Dark Theme Frames */\nframe {\n    background: linear-gradient(135deg, @card_bg_color, shade(@card_bg_color, 1.02));\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    color: @view_fg_color;\n    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);\n}\n\nframe > label {\n    color: @accent_color;\n    font-weight: 600;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);\n}\n</new_text>\n\n<old_text line=31>\n/* Dark theme entries and inputs */\nentry {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\nentry:focus {\n    border-color: @accent_color;\n    box-shadow: inset 0 0 0 1px @accent_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Entries and Inputs */\nentry {\n    background: linear-gradient(135deg, @input_bg_color, shade(@input_bg_color, 1.05));\n    color: @view_fg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\nentry:focus {\n    border-color: @input_focus_border_color;\n    box-shadow: \n        inset 0 1px 3px rgba(0, 0, 0, 0.2),\n        0 0 0 3px rgba(79, 195, 247, 0.15);\n    background: linear-gradient(135deg, shade(@input_bg_color, 1.1), shade(@input_bg_color, 1.15));\n}\n</new_text>\n\n<old_text line=43>\n/* Dark theme buttons */\nbutton {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\nbutton:hover {\n    background-color: @view_hover_bg_color;\n}\n\nbutton:active {\n    background-color: shade(@view_hover_bg_color, 0.8);\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Buttons */\nbutton {\n    background: linear-gradient(135deg, @card_bg_color, shade(@card_bg_color, 1.05));\n    color: @view_fg_color;\n    border: 1px solid @borders;\n    border-radius: 6px;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);\n    transition: all 0.2s ease;\n}\n\nbutton:hover {\n    background: linear-gradient(135deg, @view_hover_bg_color, shade(@view_hover_bg_color, 1.05));\n    border-color: @accent_color;\n    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);\n    transform: translateY(-1px);\n}\n\nbutton:active {\n    background: linear-gradient(135deg, shade(@view_hover_bg_color, 0.9), shade(@view_hover_bg_color, 0.95));\n    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);\n    transform: translateY(0);\n}\n</new_text>\n\n<old_text line=58>\n/* Dark theme combo boxes and dropdowns */\ncombobox,\ndropdown {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\ncombobox:hover,\ndropdown:hover {\n    background-color: @view_hover_bg_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Combo Boxes and Dropdowns */\ncombobox,\ndropdown {\n    background: linear-gradient(135deg, @input_bg_color, shade(@input_bg_color, 1.05));\n    color: @view_fg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\ncombobox:hover,\ndropdown:hover {\n    background: linear-gradient(135deg, @view_hover_bg_color, shade(@view_hover_bg_color, 1.05));\n    border-color: @accent_color;\n    box-shadow: \n        inset 0 1px 3px rgba(0, 0, 0, 0.2),\n        0 2px 4px rgba(0, 0, 0, 0.15);\n}\n</new_text>\n\n<old_text line=70>\n/* Dark theme spin buttons */\nspinbutton {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n    border-color: @borders;\n}\n\nspinbutton:focus {\n    border-color: @accent_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Spin Buttons */\nspinbutton {\n    background: linear-gradient(135deg, @input_bg_color, shade(@input_bg_color, 1.05));\n    color: @view_fg_color;\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\nspinbutton:focus {\n    border-color: @input_focus_border_color;\n    box-shadow: \n        inset 0 1px 3px rgba(0, 0, 0, 0.2),\n        0 0 0 3px rgba(79, 195, 247, 0.15);\n}\n</new_text>\n\n<old_text line=80>\n/* Dark theme notebook */\nnotebook {\n    background-color: @view_bg_color;\n}\n\nnotebook > header {\n    background-color: @headerbar_bg_color;\n    border-color: @borders;\n}\n\nnotebook > header > tabs > tab {\n    background-color: transparent;\n    color: @headerbar_fg_color;\n    border-color: @borders;\n}\n\nnotebook > header > tabs > tab:checked {\n    background-color: @view_bg_color;\n    color: @accent_color;\n}\n\nnotebook > stack {\n    background-color: @view_bg_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Notebook */\nnotebook {\n    background: linear-gradient(135deg, @view_bg_color, shade(@view_bg_color, 1.02));\n    border-radius: 8px;\n}\n\nnotebook > header {\n    background: linear-gradient(180deg, @headerbar_bg_color, shade(@headerbar_bg_color, 0.98));\n    border-bottom: 1px solid @borders;\n    border-radius: 8px 8px 0 0;\n}\n\nnotebook > header > tabs > tab {\n    background: transparent;\n    color: @text_secondary_color;\n    border: 1px solid transparent;\n    border-radius: 6px 6px 0 0;\n    margin: 2px;\n    transition: all 0.2s ease;\n}\n\nnotebook > header > tabs > tab:checked {\n    background: linear-gradient(135deg, @view_bg_color, shade(@view_bg_color, 1.05));\n    color: @accent_color;\n    border-color: @borders;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);\n}\n\nnotebook > stack {\n    background: linear-gradient(135deg, @view_bg_color, shade(@view_bg_color, 1.02));\n    border-radius: 0 0 8px 8px;\n}\n</new_text>\n\n<old_text line=102>\n/* Dark theme listbox */\nlistbox {\n    background-color: @view_bg_color;\n    color: @view_fg_color;\n}\n\nlistbox > row {\n    background-color: transparent;\n    color: @view_fg_color;\n}\n\nlistbox > row:hover {\n    background-color: @view_hover_bg_color;\n}\n\nlistbox > row:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Listbox */\nlistbox {\n    background: linear-gradient(135deg, @view_bg_color, shade(@view_bg_color, 1.02));\n    color: @view_fg_color;\n    border-radius: 8px;\n    border: 1px solid @borders;\n}\n\nlistbox > row {\n    background: transparent;\n    color: @view_fg_color;\n    border-radius: 4px;\n    margin: 2px;\n    transition: all 0.2s ease;\n}\n\nlistbox > row:hover {\n    background: linear-gradient(135deg, @view_hover_bg_color, shade(@view_hover_bg_color, 1.05));\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);\n}\n\nlistbox > row:selected {\n    background: linear-gradient(135deg, @accent_bg_color, shade(@accent_bg_color, 0.95));\n    color: @accent_fg_color;\n    box-shadow: 0 4px 8px rgba(79, 195, 247, 0.25);\n    border: 1px solid @accent_color;\n}\n</new_text>\n\n<old_text line=119>\n/* Dark theme scrolled windows */\nscrolledwindow {\n    background-color: @view_bg_color;\n    border-color: @borders;\n}\n\n/* Dark theme drawing area */\ndrawingarea {\n    background-color: #1a1a1a;\n    border-color: @borders;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Scrolled Windows */\nscrolledwindow {\n    background: linear-gradient(135deg, @view_bg_color, shade(@view_bg_color, 1.02));\n    border: 1px solid @borders;\n    border-radius: 8px;\n}\n\n/* Modern Dark Theme Drawing Area */\ndrawingarea {\n    background: linear-gradient(135deg, #0f1419, #161b22);\n    border: 2px solid @borders;\n    border-radius: 8px;\n    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.4);\n}\n</new_text>\n\n<old_text line=129>\n/* Dark theme status bar */\n.statusbar {\n    background-color: @headerbar_bg_color;\n    color: @headerbar_fg_color;\n    border-color: @borders;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Status Bar */\n.statusbar {\n    background: linear-gradient(180deg, @headerbar_bg_color, shade(@headerbar_bg_color, 0.98));\n    color: @text_secondary_color;\n    border-top: 1px solid @borders;\n    font-size: 0.85em;\n    font-weight: 500;\n    padding: 4px 8px;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);\n}\n</new_text>\n\n<old_text line=135>\n/* Dark theme profile list */\n.profile-list {\n    background-color: @sidebar_bg_color;\n    border-color: @borders;\n}\n\n.profile-list-item {\n    background-color: transparent;\n    color: @sidebar_fg_color;\n    border-color: @borders;\n}\n\n.profile-list-item:hover {\n    background-color: @view_hover_bg_color;\n}\n\n.profile-list-item:selected {\n    background-color: @accent_bg_color;\n    color: @accent_fg_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Profile List */\n.profile-list {\n    background: linear-gradient(135deg, @sidebar_bg_color, shade(@sidebar_bg_color, 1.05));\n    border-right: 1px solid @borders;\n    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.2);\n}\n\n.profile-list-item {\n    background: transparent;\n    color: @sidebar_fg_color;\n    border: 1px solid transparent;\n    border-radius: 8px;\n    margin: 4px;\n    padding: 12px;\n    transition: all 0.2s ease;\n    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\n.profile-list-item:hover {\n    background: linear-gradient(135deg, @view_hover_bg_color, shade(@view_hover_bg_color, 1.05));\n    border-color: @accent_color;\n    box-shadow: 0 4px 12px rgba(79, 195, 247, 0.15);\n    transform: translateY(-2px);\n}\n\n.profile-list-item:selected {\n    background: linear-gradient(135deg, @accent_bg_color, shade(@accent_bg_color, 0.95));\n    color: @accent_fg_color;\n    border-color: @accent_color;\n    box-shadow: 0 6px 16px rgba(79, 195, 247, 0.25);\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n}\n</new_text>\n\n<old_text line=151>\n/* Dark theme player configuration */\n.player-frame {\n    background-color: @view_bg_color;\n    border-color: @borders;\n}\n\n.player-frame > label {\n    color: @accent_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Player Configuration */\n.player-frame {\n    background: linear-gradient(135deg, @card_bg_color, shade(@card_bg_color, 1.05));\n    border: 1px solid @card_border_color;\n    border-radius: 8px;\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);\n}\n\n.player-frame > label {\n    color: @accent_color;\n    font-weight: 600;\n    font-size: 1.1em;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);\n}\n</new_text>\n\n<old_text line=160>\n/* Dark theme environment variables */\n.env-var-row {\n    background-color: @view_bg_color;\n    border-color: @borders;\n}\n\n.env-var-remove-button {\n    background-color: transparent;\n    color: @destructive_color;\n    border-color: @destructive_color;\n}\n\n.env-var-remove-button:hover {\n    background-color: @destructive_color;\n    color: @destructive_fg_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Environment Variables */\n.env-var-row {\n    background: linear-gradient(135deg, @input_bg_color, shade(@input_bg_color, 1.05));\n    border: 1px solid @input_border_color;\n    border-radius: 6px;\n    margin: 4px 0;\n    padding: 8px;\n    transition: all 0.2s ease;\n    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);\n}\n\n.env-var-row:hover {\n    border-color: @accent_color;\n    box-shadow: 0 2px 6px rgba(79, 195, 247, 0.15);\n}\n\n.env-var-remove-button {\n    background: transparent;\n    color: @destructive_color;\n    border: 1px solid @destructive_color;\n    border-radius: 4px;\n    min-width: 28px;\n    min-height: 28px;\n    transition: all 0.2s ease;\n}\n\n.env-var-remove-button:hover {\n    background: linear-gradient(135deg, @destructive_color, shade(@destructive_color, 0.95));\n    color: @destructive_fg_color;\n    box-shadow: 0 2px 4px rgba(248, 81, 73, 0.3);\n    transform: scale(1.05);\n}\n</new_text>\n\n<old_text line=175>\n/* Dark theme checkboxes and radio buttons */\ncheckbutton,\nradiobutton {\n    color: @view_fg_color;\n}\n\ncheckbutton:checked,\nradiobutton:checked {\n    color: @accent_color;\n}\n\n/* Dark theme labels */\nlabel {\n    color: @view_fg_color;\n}\n\n/* Dark theme separator */\nseparator {\n    background-color: @borders;\n}\n\n/* Dark theme paned */\npaned > separator {\n    background-color: @borders;\n}\n\n/* Dark theme tooltip */\ntooltip {\n    background-color: rgba(45, 45, 45, 0.95);\n    color: @window_fg_color;\n    border: 1px solid @borders;\n}\n\n/* Dark theme scrollbars */\nscrollbar slider {\n    background-color: alpha(@window_fg_color, 0.4);\n}\n\nscrollbar slider:hover {\n    background-color: alpha(@window_fg_color, 0.6);\n}\n\nscrollbar slider:active {\n    background-color: @accent_color;\n}\n</old_text>\n<new_text>\n/* Modern Dark Theme Controls */\ncheckbutton,\nradiobutton {\n    color: @view_fg_color;\n}\n\ncheckbutton:checked,\nradiobutton:checked {\n    color: @accent_color;\n    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);\n}\n\n/* Modern Dark Theme Labels */\nlabel {\n    color: @view_fg_color;\n}\n\n/* Modern Dark Theme Separators */\nseparator {\n    background: linear-gradient(90deg, transparent, @borders, transparent);\n}\n\npaned > separator {\n    background: linear-gradient(90deg, transparent, @borders, transparent);\n    min-width: 1px;\n    min-height: 1px;\n}\n\n/* Modern Dark Theme Tooltips */\ntooltip {\n    background: linear-gradient(135deg, rgba(33, 38, 45, 0.98), rgba(13, 17, 23, 0.98));\n    color: @window_fg_color;\n    border: 1px solid @accent_color;\n    border-radius: 6px;\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);\n    backdrop-filter: blur(8px);\n}\n\n/* Modern Dark Theme Scrollbars */\nscrollbar slider {\n    background: linear-gradient(135deg, rgba(139, 148, 158, 0.5), rgba(110, 118, 129, 0.6));\n    border-radius: 6px;\n    transition: all 0.2s ease;\n}\n\nscrollbar slider:hover {\n    background: linear-gradient(135deg, rgba(139, 148, 158, 0.7), rgba(110, 118, 129, 0.8));\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);\n}\n\nscrollbar slider:active {\n    background: linear-gradient(135deg, @accent_color, shade(@accent_color, 0.9));\n    box-shadow: 0 2px 8px rgba(79, 195, 247, 0.3);\n}\n</new_text>\n\n</edits>",
    "parser_metrics": {
      "tags": 28,
      "mismatched_tags": 1
    }
  }
}
```

## Agent

## 3. Vou criar um arquivo CSS adicional para estados de interação e animações modernas:

**Use Tool: edit_file (toolu_017NNEof5wFVmadDdy2sbbc8)**
```json
{
  "display_description": "Create modern interactions CSS with smooth animations and micro-interactions",
  "mode": "create",
  "path": "Linux-Coop/src/gui/styles/interactions.css"
}
```

**Tool Results: toolu_017NNEof5wFVmadDdy2sbbc8**

Edited Linux-Coop/src/gui/styles/interactions.css:

```diff
@@ -1,0 +1,419 @@
+/* Interactions CSS - Modern animations and micro-interactions for Linux-Coop GUI */
+
+/* Global Animation Settings */
+* {
+    transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);
+}
+
+/* Button Interactions */
+button {
+    position: relative;
+    overflow: hidden;
+    transition:
+        all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1),
+        box-shadow 0.3s ease,
+        transform 0.15s ease;
+}
+
+button::before {
+    content: '';
+    position: absolute;
+    top: 50%;
+    left: 50%;
+    width: 0;
+    height: 0;
+    background: rgba(255, 255, 255, 0.1);
+    border-radius: 50%;
+    transform: translate(-50%, -50%);
+    transition: width 0.3s ease, height 0.3s ease;
+    pointer-events: none;
+}
+
+button:active::before {
+    width: 300px;
+    height: 300px;
+}
+
+button:hover {
+    transform: translateY(-1px);
+    box-shadow:
+        0 8px 25px rgba(0, 0, 0, 0.15),
+        0 4px 10px rgba(0, 0, 0, 0.1);
+}
+
+button:active {
+    transform: translateY(0) scale(0.98);
+    transition-duration: 0.1s;
+}
+
+/* Suggested Action Button Enhancements */
+.suggested-action {
+    position: relative;
+    background: linear-gradient(135deg, #007acc, #005a9e);
+    box-shadow: 0 2px 8px rgba(0, 122, 204, 0.3);
+}
+
+.suggested-action::after {
+    content: '';
+    position: absolute;
+    top: 0;
+    left: -100%;
+    width: 100%;
+    height: 100%;
+    background: linear-gradient(
+        90deg,
+        transparent,
+        rgba(255, 255, 255, 0.2),
+        transparent
+    );
+    transition: left 0.5s ease;
+}
+
+.suggested-action:hover::after {
+    left: 100%;
+}
+
+.suggested-action:hover {
+    background: linear-gradient(135deg, #29b6f6, #007acc);
+    box-shadow:
+        0 8px 25px rgba(0, 122, 204, 0.4),
+        0 4px 10px rgba(0, 122, 204, 0.2);
+    transform: translateY(-2px) scale(1.02);
+}
+
+/* Destructive Button Enhancements */
+.destructive-action {
+    background: linear-gradient(135deg, #dc3545, #c82333);
+    box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3);
+}
+
+.destructive-action:hover {
+    background: linear-gradient(135deg, #e74c3c, #dc3545);
+    box-shadow:
+        0 8px 25px rgba(220, 53, 69, 0.4),
+        0 4px 10px rgba(220, 53, 69, 0.2);
+    transform: translateY(-2px) scale(1.02);
+}
+
+/* Entry Field Interactions */
+entry {
+    transition:
+        border-color 0.2s ease,
+        box-shadow 0.2s ease,
+        background-color 0.2s ease;
+}
+
+entry:focus {
+    transform: scale(1.01);
+    transition:
+        border-color 0.2s ease,
+        box-shadow 0.2s ease,
+        background-color 0.2s ease,
+        transform 0.2s ease;
+}
+
+/* ComboBox and Dropdown Interactions */
+combobox,
+dropdown {
+    transition:
+        all 0.2s ease,
+        box-shadow 0.3s ease;
+}
+
+combobox:hover,
+dropdown:hover {
+    transform: translateY(-1px);
+    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
+}
+
+/* Frame Animations */
+frame {
+    transition:
+        box-shadow 0.3s ease,
+        transform 0.2s ease;
+}
+
+frame:hover {
+    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
+    transform: translateY(-2px);
+}
+
+/* Profile Item Interactions */
+.profile-item {
+    transition:
+        all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
+    transform-origin: center;
+}
+
+.profile-item:hover {
+    transform: translateY(-4px) scale(1.02);
+    box-shadow:
+        0 12px 30px rgba(0, 0, 0, 0.15),
+        0 6px 15px rgba(0, 0, 0, 0.1);
+}
+
+.profile-item:active {
+    transform: translateY(-2px) scale(1.01);
+    transition-duration: 0.1s;
+}
+
+/* Notebook Tab Interactions */
+notebook > header > tabs > tab {
+    transition:
+        all 0.2s ease,
+        box-shadow 0.3s ease;
+    position: relative;
+    overflow: hidden;
+}
+
+notebook > header > tabs > tab::before {
+    content: '';
+    position: absolute;
+    bottom: 0;
+    left: 50%;
+    width: 0;
+    height: 2px;
+    background: linear-gradient(90deg, transparent, #007acc, transparent);
+    transition: all 0.3s ease;
+    transform: translateX(-50%);
+}
+
+notebook > header > tabs > tab:hover::before {
+    width: 80%;
+}
+
+notebook > header > tabs > tab:checked::before {
+    width: 100%;
+    background: linear-gradient(90deg, #007acc, #29b6f6, #007acc);
+}
+
+notebook > header > tabs > tab:hover {
+    transform: translateY(-1px);
+    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
+}
+
+/* ListBox Row Interactions */
+listbox > row {
+    transition:
+        all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);
+    position: relative;
+}
+
+listbox > row::before {
+    content: '';
+    position: absolute;
+    left: 0;
+    top: 0;
+    width: 0;
+    height: 100%;
+    background: linear-gradient(90deg, #007acc, transparent);
+    transition: width 0.3s ease;
+    border-radius: 4px 0 0 4px;
+}
+
+listbox > row:hover::before {
+    width: 4px;
+}
+
+listbox > row:selected::before {
+    width: 6px;
+    background: linear-gradient(90deg, #29b6f6, #007acc);
+}
+
+listbox > row:hover {
+    transform: translateX(4px);
+    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
+}
+
+/* Scrollbar Interactions */
+scrollbar {
+    transition: opacity 0.3s ease;
+}
+
+scrollbar:hover {
+    opacity: 1;
+}
+
+scrollbar slider {
+    transition:
+        all 0.2s ease,
+        box-shadow 0.3s ease;
+}
+
+scrollbar slider:hover {
+    transform: scale(1.1);
+    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
+}
+
+/* Spinner/Loading Animation */
+@keyframes spin {
+    from {
+        transform: rotate(0deg);
+    }
+    to {
+        transform: rotate(360deg);
+    }
+}
+
+.loading-spinner {
+    animation: spin 1s linear infinite;
+}
+
+/* Fade In Animation */
+@keyframes fadeIn {
+    from {
+        opacity: 0;
+        transform: translateY(20px);
+    }
+    to {
+        opacity: 1;
+        transform: translateY(0);
+    }
+}
+
+.fade-in {
+    animation: fadeIn 0.5s ease forwards;
+}
+
+/* Slide In Animation */
+@keyframes slideInLeft {
+    from {
+        opacity: 0;
+        transform: translateX(-30px);
+    }
+    to {
+        opacity: 1;
+        transform: translateX(0);
+    }
+}
+
+.slide-in-left {
+    animation: slideInLeft 0.4s ease forwards;
+}
+
+/* Pulse Animation for Important Elements */
+@keyframes pulse {
+    0% {
+        box-shadow: 0 0 0 0 rgba(0, 122, 204, 0.4);
+    }
+    70% {
+        box-shadow: 0 0 0 10px rgba(0, 122, 204, 0);
+    }
+    100% {
+        box-shadow: 0 0 0 0 rgba(0, 122, 204, 0);
+    }
+}
+
+.pulse {
+    animation: pulse 2s infinite;
+}
+
+/* Shake Animation for Errors */
+@keyframes shake {
+    0%, 100% {
+        transform: translateX(0);
+    }
+    10%, 30%, 50%, 70%, 90% {
+        transform: translateX(-2px);
+    }
+    20%, 40%, 60%, 80% {
+        transform: translateX(2px);
+    }
+}
+
+.shake {
+    animation: shake 0.5s ease-in-out;
+}
+
+/* Bounce Animation for Success */
+@keyframes bounce {
+    0%, 20%, 53%, 80%, 100% {
+        transform: translateY(0);
+    }
+    40%, 43% {
+        transform: translateY(-8px);
+    }
+    70% {
+        transform: translateY(-4px);
+    }
+    90% {
+        transform: translateY(-2px);
+    }
+}
+
+.bounce {
+    animation: bounce 1s ease;
+}
+
+/* Focus Ring Enhancement */
+*:focus {
+    outline: none;
+    box-shadow:
+        0 0 0 3px rgba(0, 122, 204, 0.15),
+        0 0 0 1px rgba(0, 122, 204, 0.4);
+    transition: box-shadow 0.2s ease;
+}
+
+/* Smooth State Transitions */
+.state-transition {
+    transition:
+        background-color 0.3s ease,
+        color 0.3s ease,
+        border-color 0.3s ease,
+        box-shadow 0.3s ease,
+        transform 0.2s ease;
+}
+
+/* Micro-interaction for Checkboxes */
+checkbutton {
+    transition: transform 0.1s ease;
+}
+
+checkbutton:active {
+    transform: scale(0.95);
+}
+
+checkbutton:checked {
+    transform: scale(1.05);
+    transition: transform 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
+}
+
+/* Progress Bar Animation */
+@keyframes progress {
+    0% {
+        width: 0%;
+    }
+    100% {
+        width: var(--progress-value, 0%);
+    }
+}
+
+.progress-bar {
+    animation: progress 1s ease-out forwards;
+}
+
+/* Glow Effect for Active Elements */
+.glow {
+    box-shadow:
+        0 0 5px rgba(0, 122, 204, 0.3),
+        0 0 10px rgba(0, 122, 204, 0.2),
+        0 0 15px rgba(0, 122, 204, 0.1);
+}
+
+/* Smooth Layout Shifts */
+.layout-shift {
+    transition:
+        width 0.3s ease,
+        height 0.3s ease,
+        margin 0.3s ease,
+        padding 0.3s ease;
+}
+
+/* Reduced Motion for Accessibility */
+@media (prefers-reduced-motion: reduce) {
+    * {
+        animation-duration: 0.01ms !important;
+        animation-iteration-count: 1 !important;
+        transition-duration: 0.01ms !important;
+    }
+}

```


Debug Output:

```json
{
  "original_path": "src/gui/styles/interactions.css",
  "new_text": "/* Interactions CSS - Modern animations and micro-interactions for Linux-Coop GUI */\n\n/* Global Animation Settings */\n* {\n    transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);\n}\n\n/* Button Interactions */\nbutton {\n    position: relative;\n    overflow: hidden;\n    transition:\n        all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1),\n        box-shadow 0.3s ease,\n        transform 0.15s ease;\n}\n\nbutton::before {\n    content: '';\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    width: 0;\n    height: 0;\n    background: rgba(255, 255, 255, 0.1);\n    border-radius: 50%;\n    transform: translate(-50%, -50%);\n    transition: width 0.3s ease, height 0.3s ease;\n    pointer-events: none;\n}\n\nbutton:active::before {\n    width: 300px;\n    height: 300px;\n}\n\nbutton:hover {\n    transform: translateY(-1px);\n    box-shadow:\n        0 8px 25px rgba(0, 0, 0, 0.15),\n        0 4px 10px rgba(0, 0, 0, 0.1);\n}\n\nbutton:active {\n    transform: translateY(0) scale(0.98);\n    transition-duration: 0.1s;\n}\n\n/* Suggested Action Button Enhancements */\n.suggested-action {\n    position: relative;\n    background: linear-gradient(135deg, #007acc, #005a9e);\n    box-shadow: 0 2px 8px rgba(0, 122, 204, 0.3);\n}\n\n.suggested-action::after {\n    content: '';\n    position: absolute;\n    top: 0;\n    left: -100%;\n    width: 100%;\n    height: 100%;\n    background: linear-gradient(\n        90deg,\n        transparent,\n        rgba(255, 255, 255, 0.2),\n        transparent\n    );\n    transition: left 0.5s ease;\n}\n\n.suggested-action:hover::after {\n    left: 100%;\n}\n\n.suggested-action:hover {\n    background: linear-gradient(135deg, #29b6f6, #007acc);\n    box-shadow:\n        0 8px 25px rgba(0, 122, 204, 0.4),\n        0 4px 10px rgba(0, 122, 204, 0.2);\n    transform: translateY(-2px) scale(1.02);\n}\n\n/* Destructive Button Enhancements */\n.destructive-action {\n    background: linear-gradient(135deg, #dc3545, #c82333);\n    box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3);\n}\n\n.destructive-action:hover {\n    background: linear-gradient(135deg, #e74c3c, #dc3545);\n    box-shadow:\n        0 8px 25px rgba(220, 53, 69, 0.4),\n        0 4px 10px rgba(220, 53, 69, 0.2);\n    transform: translateY(-2px) scale(1.02);\n}\n\n/* Entry Field Interactions */\nentry {\n    transition:\n        border-color 0.2s ease,\n        box-shadow 0.2s ease,\n        background-color 0.2s ease;\n}\n\nentry:focus {\n    transform: scale(1.01);\n    transition:\n        border-color 0.2s ease,\n        box-shadow 0.2s ease,\n        background-color 0.2s ease,\n        transform 0.2s ease;\n}\n\n/* ComboBox and Dropdown Interactions */\ncombobox,\ndropdown {\n    transition:\n        all 0.2s ease,\n        box-shadow 0.3s ease;\n}\n\ncombobox:hover,\ndropdown:hover {\n    transform: translateY(-1px);\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);\n}\n\n/* Frame Animations */\nframe {\n    transition:\n        box-shadow 0.3s ease,\n        transform 0.2s ease;\n}\n\nframe:hover {\n    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);\n    transform: translateY(-2px);\n}\n\n/* Profile Item Interactions */\n.profile-item {\n    transition:\n        all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);\n    transform-origin: center;\n}\n\n.profile-item:hover {\n    transform: translateY(-4px) scale(1.02);\n    box-shadow:\n        0 12px 30px rgba(0, 0, 0, 0.15),\n        0 6px 15px rgba(0, 0, 0, 0.1);\n}\n\n.profile-item:active {\n    transform: translateY(-2px) scale(1.01);\n    transition-duration: 0.1s;\n}\n\n/* Notebook Tab Interactions */\nnotebook > header > tabs > tab {\n    transition:\n        all 0.2s ease,\n        box-shadow 0.3s ease;\n    position: relative;\n    overflow: hidden;\n}\n\nnotebook > header > tabs > tab::before {\n    content: '';\n    position: absolute;\n    bottom: 0;\n    left: 50%;\n    width: 0;\n    height: 2px;\n    background: linear-gradient(90deg, transparent, #007acc, transparent);\n    transition: all 0.3s ease;\n    transform: translateX(-50%);\n}\n\nnotebook > header > tabs > tab:hover::before {\n    width: 80%;\n}\n\nnotebook > header > tabs > tab:checked::before {\n    width: 100%;\n    background: linear-gradient(90deg, #007acc, #29b6f6, #007acc);\n}\n\nnotebook > header > tabs > tab:hover {\n    transform: translateY(-1px);\n    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);\n}\n\n/* ListBox Row Interactions */\nlistbox > row {\n    transition:\n        all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);\n    position: relative;\n}\n\nlistbox > row::before {\n    content: '';\n    position: absolute;\n    left: 0;\n    top: 0;\n    width: 0;\n    height: 100%;\n    background: linear-gradient(90deg, #007acc, transparent);\n    transition: width 0.3s ease;\n    border-radius: 4px 0 0 4px;\n}\n\nlistbox > row:hover::before {\n    width: 4px;\n}\n\nlistbox > row:selected::before {\n    width: 6px;\n    background: linear-gradient(90deg, #29b6f6, #007acc);\n}\n\nlistbox > row:hover {\n    transform: translateX(4px);\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);\n}\n\n/* Scrollbar Interactions */\nscrollbar {\n    transition: opacity 0.3s ease;\n}\n\nscrollbar:hover {\n    opacity: 1;\n}\n\nscrollbar slider {\n    transition:\n        all 0.2s ease,\n        box-shadow 0.3s ease;\n}\n\nscrollbar slider:hover {\n    transform: scale(1.1);\n    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);\n}\n\n/* Spinner/Loading Animation */\n@keyframes spin {\n    from {\n        transform: rotate(0deg);\n    }\n    to {\n        transform: rotate(360deg);\n    }\n}\n\n.loading-spinner {\n    animation: spin 1s linear infinite;\n}\n\n/* Fade In Animation */\n@keyframes fadeIn {\n    from {\n        opacity: 0;\n        transform: translateY(20px);\n    }\n    to {\n        opacity: 1;\n        transform: translateY(0);\n    }\n}\n\n.fade-in {\n    animation: fadeIn 0.5s ease forwards;\n}\n\n/* Slide In Animation */\n@keyframes slideInLeft {\n    from {\n        opacity: 0;\n        transform: translateX(-30px);\n    }\n    to {\n        opacity: 1;\n        transform: translateX(0);\n    }\n}\n\n.slide-in-left {\n    animation: slideInLeft 0.4s ease forwards;\n}\n\n/* Pulse Animation for Important Elements */\n@keyframes pulse {\n    0% {\n        box-shadow: 0 0 0 0 rgba(0, 122, 204, 0.4);\n    }\n    70% {\n        box-shadow: 0 0 0 10px rgba(0, 122, 204, 0);\n    }\n    100% {\n        box-shadow: 0 0 0 0 rgba(0, 122, 204, 0);\n    }\n}\n\n.pulse {\n    animation: pulse 2s infinite;\n}\n\n/* Shake Animation for Errors */\n@keyframes shake {\n    0%, 100% {\n        transform: translateX(0);\n    }\n    10%, 30%, 50%, 70%, 90% {\n        transform: translateX(-2px);\n    }\n    20%, 40%, 60%, 80% {\n        transform: translateX(2px);\n    }\n}\n\n.shake {\n    animation: shake 0.5s ease-in-out;\n}\n\n/* Bounce Animation for Success */\n@keyframes bounce {\n    0%, 20%, 53%, 80%, 100% {\n        transform: translateY(0);\n    }\n    40%, 43% {\n        transform: translateY(-8px);\n    }\n    70% {\n        transform: translateY(-4px);\n    }\n    90% {\n        transform: translateY(-2px);\n    }\n}\n\n.bounce {\n    animation: bounce 1s ease;\n}\n\n/* Focus Ring Enhancement */\n*:focus {\n    outline: none;\n    box-shadow:\n        0 0 0 3px rgba(0, 122, 204, 0.15),\n        0 0 0 1px rgba(0, 122, 204, 0.4);\n    transition: box-shadow 0.2s ease;\n}\n\n/* Smooth State Transitions */\n.state-transition {\n    transition:\n        background-color 0.3s ease,\n        color 0.3s ease,\n        border-color 0.3s ease,\n        box-shadow 0.3s ease,\n        transform 0.2s ease;\n}\n\n/* Micro-interaction for Checkboxes */\ncheckbutton {\n    transition: transform 0.1s ease;\n}\n\ncheckbutton:active {\n    transform: scale(0.95);\n}\n\ncheckbutton:checked {\n    transform: scale(1.05);\n    transition: transform 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);\n}\n\n/* Progress Bar Animation */\n@keyframes progress {\n    0% {\n        width: 0%;\n    }\n    100% {\n        width: var(--progress-value, 0%);\n    }\n}\n\n.progress-bar {\n    animation: progress 1s ease-out forwards;\n}\n\n/* Glow Effect for Active Elements */\n.glow {\n    box-shadow:\n        0 0 5px rgba(0, 122, 204, 0.3),\n        0 0 10px rgba(0, 122, 204, 0.2),\n        0 0 15px rgba(0, 122, 204, 0.1);\n}\n\n/* Smooth Layout Shifts */\n.layout-shift {\n    transition:\n        width 0.3s ease,\n        height 0.3s ease,\n        margin 0.3s ease,\n        padding 0.3s ease;\n}\n\n/* Reduced Motion for Accessibility */\n@media (prefers-reduced-motion: reduce) {\n    * {\n        animation-duration: 0.01ms !important;\n        animation-iteration-count: 1 !important;\n        transition-duration: 0.01ms !important;\n    }\n}\n",
  "old_text": "",
  "raw_output": {
    "raw_edits": "```\n/* Interactions CSS - Modern animations and micro-interactions for Linux-Coop GUI */\n\n/* Global Animation Settings */\n* {\n    transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);\n}\n\n/* Button Interactions */\nbutton {\n    position: relative;\n    overflow: hidden;\n    transition: \n        all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1),\n        box-shadow 0.3s ease,\n        transform 0.15s ease;\n}\n\nbutton::before {\n    content: '';\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    width: 0;\n    height: 0;\n    background: rgba(255, 255, 255, 0.1);\n    border-radius: 50%;\n    transform: translate(-50%, -50%);\n    transition: width 0.3s ease, height 0.3s ease;\n    pointer-events: none;\n}\n\nbutton:active::before {\n    width: 300px;\n    height: 300px;\n}\n\nbutton:hover {\n    transform: translateY(-1px);\n    box-shadow: \n        0 8px 25px rgba(0, 0, 0, 0.15),\n        0 4px 10px rgba(0, 0, 0, 0.1);\n}\n\nbutton:active {\n    transform: translateY(0) scale(0.98);\n    transition-duration: 0.1s;\n}\n\n/* Suggested Action Button Enhancements */\n.suggested-action {\n    position: relative;\n    background: linear-gradient(135deg, #007acc, #005a9e);\n    box-shadow: 0 2px 8px rgba(0, 122, 204, 0.3);\n}\n\n.suggested-action::after {\n    content: '';\n    position: absolute;\n    top: 0;\n    left: -100%;\n    width: 100%;\n    height: 100%;\n    background: linear-gradient(\n        90deg,\n        transparent,\n        rgba(255, 255, 255, 0.2),\n        transparent\n    );\n    transition: left 0.5s ease;\n}\n\n.suggested-action:hover::after {\n    left: 100%;\n}\n\n.suggested-action:hover {\n    background: linear-gradient(135deg, #29b6f6, #007acc);\n    box-shadow: \n        0 8px 25px rgba(0, 122, 204, 0.4),\n        0 4px 10px rgba(0, 122, 204, 0.2);\n    transform: translateY(-2px) scale(1.02);\n}\n\n/* Destructive Button Enhancements */\n.destructive-action {\n    background: linear-gradient(135deg, #dc3545, #c82333);\n    box-shadow: 0 2px 8px rgba(220, 53, 69, 0.3);\n}\n\n.destructive-action:hover {\n    background: linear-gradient(135deg, #e74c3c, #dc3545);\n    box-shadow: \n        0 8px 25px rgba(220, 53, 69, 0.4),\n        0 4px 10px rgba(220, 53, 69, 0.2);\n    transform: translateY(-2px) scale(1.02);\n}\n\n/* Entry Field Interactions */\nentry {\n    transition: \n        border-color 0.2s ease,\n        box-shadow 0.2s ease,\n        background-color 0.2s ease;\n}\n\nentry:focus {\n    transform: scale(1.01);\n    transition: \n        border-color 0.2s ease,\n        box-shadow 0.2s ease,\n        background-color 0.2s ease,\n        transform 0.2s ease;\n}\n\n/* ComboBox and Dropdown Interactions */\ncombobox,\ndropdown {\n    transition: \n        all 0.2s ease,\n        box-shadow 0.3s ease;\n}\n\ncombobox:hover,\ndropdown:hover {\n    transform: translateY(-1px);\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);\n}\n\n/* Frame Animations */\nframe {\n    transition: \n        box-shadow 0.3s ease,\n        transform 0.2s ease;\n}\n\nframe:hover {\n    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);\n    transform: translateY(-2px);\n}\n\n/* Profile Item Interactions */\n.profile-item {\n    transition: \n        all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);\n    transform-origin: center;\n}\n\n.profile-item:hover {\n    transform: translateY(-4px) scale(1.02);\n    box-shadow: \n        0 12px 30px rgba(0, 0, 0, 0.15),\n        0 6px 15px rgba(0, 0, 0, 0.1);\n}\n\n.profile-item:active {\n    transform: translateY(-2px) scale(1.01);\n    transition-duration: 0.1s;\n}\n\n/* Notebook Tab Interactions */\nnotebook > header > tabs > tab {\n    transition: \n        all 0.2s ease,\n        box-shadow 0.3s ease;\n    position: relative;\n    overflow: hidden;\n}\n\nnotebook > header > tabs > tab::before {\n    content: '';\n    position: absolute;\n    bottom: 0;\n    left: 50%;\n    width: 0;\n    height: 2px;\n    background: linear-gradient(90deg, transparent, #007acc, transparent);\n    transition: all 0.3s ease;\n    transform: translateX(-50%);\n}\n\nnotebook > header > tabs > tab:hover::before {\n    width: 80%;\n}\n\nnotebook > header > tabs > tab:checked::before {\n    width: 100%;\n    background: linear-gradient(90deg, #007acc, #29b6f6, #007acc);\n}\n\nnotebook > header > tabs > tab:hover {\n    transform: translateY(-1px);\n    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);\n}\n\n/* ListBox Row Interactions */\nlistbox > row {\n    transition: \n        all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);\n    position: relative;\n}\n\nlistbox > row::before {\n    content: '';\n    position: absolute;\n    left: 0;\n    top: 0;\n    width: 0;\n    height: 100%;\n    background: linear-gradient(90deg, #007acc, transparent);\n    transition: width 0.3s ease;\n    border-radius: 4px 0 0 4px;\n}\n\nlistbox > row:hover::before {\n    width: 4px;\n}\n\nlistbox > row:selected::before {\n    width: 6px;\n    background: linear-gradient(90deg, #29b6f6, #007acc);\n}\n\nlistbox > row:hover {\n    transform: translateX(4px);\n    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);\n}\n\n/* Scrollbar Interactions */\nscrollbar {\n    transition: opacity 0.3s ease;\n}\n\nscrollbar:hover {\n    opacity: 1;\n}\n\nscrollbar slider {\n    transition: \n        all 0.2s ease,\n        box-shadow 0.3s ease;\n}\n\nscrollbar slider:hover {\n    transform: scale(1.1);\n    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);\n}\n\n/* Spinner/Loading Animation */\n@keyframes spin {\n    from {\n        transform: rotate(0deg);\n    }\n    to {\n        transform: rotate(360deg);\n    }\n}\n\n.loading-spinner {\n    animation: spin 1s linear infinite;\n}\n\n/* Fade In Animation */\n@keyframes fadeIn {\n    from {\n        opacity: 0;\n        transform: translateY(20px);\n    }\n    to {\n        opacity: 1;\n        transform: translateY(0);\n    }\n}\n\n.fade-in {\n    animation: fadeIn 0.5s ease forwards;\n}\n\n/* Slide In Animation */\n@keyframes slideInLeft {\n    from {\n        opacity: 0;\n        transform: translateX(-30px);\n    }\n    to {\n        opacity: 1;\n        transform: translateX(0);\n    }\n}\n\n.slide-in-left {\n    animation: slideInLeft 0.4s ease forwards;\n}\n\n/* Pulse Animation for Important Elements */\n@keyframes pulse {\n    0% {\n        box-shadow: 0 0 0 0 rgba(0, 122, 204, 0.4);\n    }\n    70% {\n        box-shadow: 0 0 0 10px rgba(0, 122, 204, 0);\n    }\n    100% {\n        box-shadow: 0 0 0 0 rgba(0, 122, 204, 0);\n    }\n}\n\n.pulse {\n    animation: pulse 2s infinite;\n}\n\n/* Shake Animation for Errors */\n@keyframes shake {\n    0%, 100% {\n        transform: translateX(0);\n    }\n    10%, 30%, 50%, 70%, 90% {\n        transform: translateX(-2px);\n    }\n    20%, 40%, 60%, 80% {\n        transform: translateX(2px);\n    }\n}\n\n.shake {\n    animation: shake 0.5s ease-in-out;\n}\n\n/* Bounce Animation for Success */\n@keyframes bounce {\n    0%, 20%, 53%, 80%, 100% {\n        transform: translateY(0);\n    }\n    40%, 43% {\n        transform: translateY(-8px);\n    }\n    70% {\n        transform: translateY(-4px);\n    }\n    90% {\n        transform: translateY(-2px);\n    }\n}\n\n.bounce {\n    animation: bounce 1s ease;\n}\n\n/* Focus Ring Enhancement */\n*:focus {\n    outline: none;\n    box-shadow: \n        0 0 0 3px rgba(0, 122, 204, 0.15),\n        0 0 0 1px rgba(0, 122, 204, 0.4);\n    transition: box-shadow 0.2s ease;\n}\n\n/* Smooth State Transitions */\n.state-transition {\n    transition: \n        background-color 0.3s ease,\n        color 0.3s ease,\n        border-color 0.3s ease,\n        box-shadow 0.3s ease,\n        transform 0.2s ease;\n}\n\n/* Micro-interaction for Checkboxes */\ncheckbutton {\n    transition: transform 0.1s ease;\n}\n\ncheckbutton:active {\n    transform: scale(0.95);\n}\n\ncheckbutton:checked {\n    transform: scale(1.05);\n    transition: transform 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);\n}\n\n/* Progress Bar Animation */\n@keyframes progress {\n    0% {\n        width: 0%;\n    }\n    100% {\n        width: var(--progress-value, 0%);\n    }\n}\n\n.progress-bar {\n    animation: progress 1s ease-out forwards;\n}\n\n/* Glow Effect for Active Elements */\n.glow {\n    box-shadow: \n        0 0 5px rgba(0, 122, 204, 0.3),\n        0 0 10px rgba(0, 122, 204, 0.2),\n        0 0 15px rgba(0, 122, 204, 0.1);\n}\n\n/* Smooth Layout Shifts */\n.layout-shift {\n    transition: \n        width 0.3s ease,\n        height 0.3s ease,\n        margin 0.3s ease,\n        padding 0.3s ease;\n}\n\n/* Reduced Motion for Accessibility */\n@media (prefers-reduced-motion: reduce) {\n    * {\n        animation-duration: 0.01ms !important;\n        animation-iteration-count: 1 !important;\n        transition-duration: 0.01ms !important;\n    }\n}\n```",
    "parser_metrics": {
      "tags": 0,
      "mismatched_tags": 0
    }
  }
}
```

## User

continue

## Agent

Vou continuar implementando as melhorias no design da UI/UX. Já atualizei os arquivos de tema claro e escuro e criei um novo arquivo para interações. Agora, vou atualizar o `StyleManager` para carregar o novo arquivo `interactions.css` na ordem correta, garantindo que as interações visuais sejam aplicadas sobre os estilos base.

## 4. Atualizar o `StyleManager` para carregar `interactions.css`:

**Use Tool: edit_file (edit_file-0)**
```json
{
  "mode": "edit",
  "path": "Linux-Coop/src/gui/styles/style_manager.py",
  "display_description": "Update StyleManager to load the new interactions.css file for modern UI/UX animations"
}
```

**Tool Results: edit_file-0**

Edited Linux-Coop/src/gui/styles/style_manager.py:

```diff
@@ -65,7 +65,8 @@
             'base.css',
             'components.css',
             'layout.css',
-            'theme.css'
+            'theme.css',
+            'interactions.css' # New: for modern UI/UX animations and micro-interactions
         ]
 
         for style_file in default_styles:

```


Debug Output:

```json
{
  "original_path": "src/gui/styles/style_manager.py",
  "new_text": "\"\"\"\nStyleManager - Professional CSS management for Linux-Coop GUI\n\nThis module provides a centralized way to manage and apply CSS styles\nfollowing SOLID principles for maintainable and modular styling.\n\"\"\"\n\nimport logging\nfrom pathlib import Path\nfrom typing import List, Optional\nfrom gi.repository import Gtk, Gdk, Adw\n\n\nclass StyleManagerError(Exception):\n    \"\"\"Custom exception for StyleManager errors\"\"\"\n    pass\n\n\nclass StyleManager:\n    \"\"\"\n    Manages CSS styling for the Linux-Coop GUI application.\n\n    This class follows the Single Responsibility Principle by handling\n    only CSS-related operations and the Dependency Inversion Principle\n    by depending on abstractions (file paths) rather than concrete implementations.\n    \"\"\"\n\n    def __init__(self, styles_dir: Optional[Path] = None):\n        \"\"\"\n        Initialize the StyleManager.\n\n        Args:\n            styles_dir: Path to the styles directory. If None, uses default location.\n        \"\"\"\n        self.logger = logging.getLogger(__name__)\n        self._styles_dir = styles_dir or self._get_default_styles_dir()\n        self._providers: List[Gtk.CssProvider] = []\n        self._applied_styles: List[str] = []\n        self._theme_provider: Optional[Gtk.CssProvider] = None\n\n        # Validate styles directory\n        if not self._styles_dir.exists():\n            raise StyleManagerError(f\"Styles directory not found: {self._styles_dir}\")\n\n        # Connect to Adwaita style manager for automatic theme switching\n        try:\n            adw_style_manager = Adw.StyleManager.get_default()\n            adw_style_manager.connect(\"notify::dark\", self._on_system_theme_changed)\n        except Exception as e:\n            self.logger.warning(f\"Could not connect to Adwaita StyleManager for theme detection: {e}\")\n\n    @staticmethod\n    def _get_default_styles_dir() -> Path:\n        \"\"\"Get the default styles directory path.\"\"\"\n        return Path(__file__).parent\n\n    def load_default_styles(self) -> None:\n        \"\"\"\n        Load all default CSS files in the correct order.\n\n        The order ensures that base styles are applied first,\n        followed by components, layout, and theme styles.\n        \"\"\"\n        default_styles = [\n            'base.css',\n            'components.css',\n            'layout.css',\n            'theme.css',\n            'interactions.css' # New: for modern UI/UX animations and micro-interactions\n        ]\n\n        for style_file in default_styles:\n            try:\n                self.load_css_file(style_file)\n            except StyleManagerError as e:\n                self.logger.warning(f\"Failed to load default style {style_file}: {e}\")\n\n        # Load theme-specific CSS based on current system theme\n        self._load_theme_specific_styles()\n\n    def load_css_file(self, filename: str) -> None:\n        \"\"\"\n        Load a CSS file and apply it to the application.\n\n        Args:\n            filename: Name of the CSS file to load\n\n        Raises:\n            StyleManagerError: If the file cannot be loaded or applied\n        \"\"\"\n        css_path = self._styles_dir / filename\n\n        if not css_path.exists():\n            raise StyleManagerError(f\"CSS file not found: {css_path}\")\n\n        try:\n            css_provider = Gtk.CssProvider()\n            css_provider.load_from_path(str(css_path))\n\n            display = Gdk.Display.get_default()\n            if display is None:\n                raise StyleManagerError(\"No default display available\")\n\n            Gtk.StyleContext.add_provider_for_display(\n                display,\n                css_provider,\n                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION\n            )\n\n            self._providers.append(css_provider)\n            self._applied_styles.append(filename)\n\n            self.logger.info(f\"Successfully loaded CSS file: {filename}\")\n\n        except Exception as e:\n            raise StyleManagerError(f\"Failed to load CSS file {filename}: {e}\") from e\n\n    def load_css_from_string(self, css_content: str, identifier: str = \"custom\") -> None:\n        \"\"\"\n        Load CSS from a string and apply it to the application.\n\n        Args:\n            css_content: CSS content as string\n            identifier: Identifier for this CSS content (for logging/tracking)\n\n        Raises:\n            StyleManagerError: If the CSS cannot be loaded or applied\n        \"\"\"\n        try:\n            css_provider = Gtk.CssProvider()\n            css_provider.load_from_data(css_content.encode('utf-8'))\n\n            display = Gdk.Display.get_default()\n            if display is None:\n                raise StyleManagerError(\"No default display available\")\n\n            Gtk.StyleContext.add_provider_for_display(\n                display,\n                css_provider,\n                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION\n            )\n\n            self._providers.append(css_provider)\n            self._applied_styles.append(identifier)\n\n            self.logger.info(f\"Successfully loaded CSS from string: {identifier}\")\n\n        except Exception as e:\n            raise StyleManagerError(f\"Failed to load CSS from string {identifier}: {e}\") from e\n\n    def apply_theme_variant(self, variant: str = \"light\") -> None:\n        \"\"\"\n        Apply a specific theme variant.\n\n        Args:\n            variant: Theme variant (\"light\" or \"dark\")\n        \"\"\"\n        if variant not in [\"light\", \"dark\"]:\n            self.logger.warning(f\"Unknown theme variant: {variant}. Using 'light'.\")\n            variant = \"light\"\n\n        # This could be extended to load variant-specific CSS files\n        theme_css = f\"theme-{variant}.css\"\n        theme_path = self._styles_dir / theme_css\n\n        if theme_path.exists():\n            try:\n                self.load_css_file(theme_css)\n                self.logger.info(f\"Applied theme variant: {variant}\")\n            except StyleManagerError as e:\n                self.logger.warning(f\"Failed to apply theme variant {variant}: {e}\")\n        else:\n            self.logger.debug(f\"Theme variant file not found: {theme_css}\")\n\n    def reload_styles(self) -> None:\n        \"\"\"\n        Reload all previously applied styles.\n\n        This method clears all current providers and reapplies styles,\n        useful for development or dynamic theme switching.\n        \"\"\"\n        self.logger.info(\"Reloading all styles...\")\n\n        # Store applied styles before clearing\n        styles_to_reload = self._applied_styles.copy()\n\n        # Clear current providers\n        self.clear_styles()\n\n        # Reload styles\n        for style in styles_to_reload:\n            if style.endswith('.css'):\n                try:\n                    self.load_css_file(style)\n                except StyleManagerError as e:\n                    self.logger.error(f\"Failed to reload style {style}: {e}\")\n\n    def clear_styles(self) -> None:\n        \"\"\"Remove all applied CSS providers.\"\"\"\n        display = Gdk.Display.get_default()\n        if display is None:\n            self.logger.warning(\"No default display available for clearing styles\")\n            return\n\n        for provider in self._providers:\n            Gtk.StyleContext.remove_provider_for_display(display, provider)\n\n        self._providers.clear()\n        self._applied_styles.clear()\n        self.logger.info(\"Cleared all applied styles\")\n\n    def get_applied_styles(self) -> List[str]:\n        \"\"\"\n        Get a list of currently applied style identifiers.\n\n        Returns:\n            List of applied style identifiers\n        \"\"\"\n        return self._applied_styles.copy()\n\n    def has_style(self, identifier: str) -> bool:\n        \"\"\"\n        Check if a specific style is currently applied.\n\n        Args:\n            identifier: Style identifier to check\n\n        Returns:\n            True if the style is applied, False otherwise\n        \"\"\"\n        return identifier in self._applied_styles\n\n    def get_styles_directory(self) -> Path:\n        \"\"\"\n        Get the current styles directory path.\n\n        Returns:\n            Path to the styles directory\n        \"\"\"\n        return self._styles_dir\n\n    def set_styles_directory(self, new_dir: Path) -> None:\n        \"\"\"\n        Set a new styles directory.\n\n        Args:\n            new_dir: New path to the styles directory\n\n        Raises:\n            StyleManagerError: If the directory doesn't exist\n        \"\"\"\n        if not new_dir.exists():\n            raise StyleManagerError(f\"Styles directory not found: {new_dir}\")\n\n        self._styles_dir = new_dir\n        self.logger.info(f\"Styles directory changed to: {new_dir}\")\n\n    def _on_system_theme_changed(self, style_manager, param):\n        \"\"\"Handle system theme changes automatically\"\"\"\n        try:\n            is_dark = style_manager.get_dark()\n            theme_name = \"dark\" if is_dark else \"light\"\n            self.logger.info(f\"System theme changed to: {theme_name}\")\n\n            # Reload theme-specific styles\n            self._load_theme_specific_styles()\n        except Exception as e:\n            self.logger.error(f\"Error handling system theme change: {e}\")\n\n    def _load_theme_specific_styles(self):\n        \"\"\"Load CSS file specific to current system theme\"\"\"\n        try:\n            # Remove existing theme provider if it exists\n            if self._theme_provider:\n                display = Gdk.Display.get_default()\n                if display:\n                    Gtk.StyleContext.remove_provider_for_display(display, self._theme_provider)\n                self._theme_provider = None\n\n            # Detect current theme\n            adw_style_manager = Adw.StyleManager.get_default()\n            is_dark = adw_style_manager.get_dark()\n\n            if is_dark:\n                theme_file = \"theme-dark.css\"\n                theme_path = self._styles_dir / theme_file\n\n                if theme_path.exists():\n                    try:\n                        self._theme_provider = Gtk.CssProvider()\n                        self._theme_provider.load_from_path(str(theme_path))\n\n                        display = Gdk.Display.get_default()\n                        if display:\n                            Gtk.StyleContext.add_provider_for_display(\n                                display,\n                                self._theme_provider,\n                                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1  # Higher priority than base styles\n                            )\n\n                            self.logger.info(f\"Applied dark theme styling\")\n                            self._applied_styles.append(f\"theme-dark\")\n                        else:\n                            self.logger.warning(\"No default display available for dark theme\")\n                    except Exception as e:\n                        self.logger.error(f\"Failed to load dark theme CSS: {e}\")\n                else:\n                    self.logger.debug(\"Dark theme CSS not found, using default styling\")\n            else:\n                self.logger.info(\"Applied light theme styling\")\n\n        except Exception as e:\n            self.logger.error(f\"Error loading theme-specific styles: {e}\")\n\n\n# Singleton instance for global access\n_style_manager_instance: Optional[StyleManager] = None\n\n\ndef get_style_manager() -> StyleManager:\n    \"\"\"\n    Get the global StyleManager instance.\n\n    Returns:\n        Global StyleManager instance\n    \"\"\"\n    global _style_manager_instance\n    if _style_manager_instance is None:\n        _style_manager_instance = StyleManager()\n    return _style_manager_instance\n\n\ndef initialize_styles() -> None:\n    \"\"\"\n    Initialize the global style manager with default styles.\n\n    This function should be called once during application startup.\n    \"\"\"\n    style_manager = get_style_manager()\n    style_manager.load_default_styles()\n",
  "old_text": "\"\"\"\nStyleManager - Professional CSS management for Linux-Coop GUI\n\nThis module provides a centralized way to manage and apply CSS styles\nfollowing SOLID principles for maintainable and modular styling.\n\"\"\"\n\nimport logging\nfrom pathlib import Path\nfrom typing import List, Optional\nfrom gi.repository import Gtk, Gdk, Adw\n\n\nclass StyleManagerError(Exception):\n    \"\"\"Custom exception for StyleManager errors\"\"\"\n    pass\n\n\nclass StyleManager:\n    \"\"\"\n    Manages CSS styling for the Linux-Coop GUI application.\n\n    This class follows the Single Responsibility Principle by handling\n    only CSS-related operations and the Dependency Inversion Principle\n    by depending on abstractions (file paths) rather than concrete implementations.\n    \"\"\"\n\n    def __init__(self, styles_dir: Optional[Path] = None):\n        \"\"\"\n        Initialize the StyleManager.\n\n        Args:\n            styles_dir: Path to the styles directory. If None, uses default location.\n        \"\"\"\n        self.logger = logging.getLogger(__name__)\n        self._styles_dir = styles_dir or self._get_default_styles_dir()\n        self._providers: List[Gtk.CssProvider] = []\n        self._applied_styles: List[str] = []\n        self._theme_provider: Optional[Gtk.CssProvider] = None\n\n        # Validate styles directory\n        if not self._styles_dir.exists():\n            raise StyleManagerError(f\"Styles directory not found: {self._styles_dir}\")\n\n        # Connect to Adwaita style manager for automatic theme switching\n        try:\n            adw_style_manager = Adw.StyleManager.get_default()\n            adw_style_manager.connect(\"notify::dark\", self._on_system_theme_changed)\n        except Exception as e:\n            self.logger.warning(f\"Could not connect to Adwaita StyleManager for theme detection: {e}\")\n\n    @staticmethod\n    def _get_default_styles_dir() -> Path:\n        \"\"\"Get the default styles directory path.\"\"\"\n        return Path(__file__).parent\n\n    def load_default_styles(self) -> None:\n        \"\"\"\n        Load all default CSS files in the correct order.\n\n        The order ensures that base styles are applied first,\n        followed by components, layout, and theme styles.\n        \"\"\"\n        default_styles = [\n            'base.css',\n            'components.css',\n            'layout.css',\n            'theme.css'\n        ]\n\n        for style_file in default_styles:\n            try:\n                self.load_css_file(style_file)\n            except StyleManagerError as e:\n                self.logger.warning(f\"Failed to load default style {style_file}: {e}\")\n\n        # Load theme-specific CSS based on current system theme\n        self._load_theme_specific_styles()\n\n    def load_css_file(self, filename: str) -> None:\n        \"\"\"\n        Load a CSS file and apply it to the application.\n\n        Args:\n            filename: Name of the CSS file to load\n\n        Raises:\n            StyleManagerError: If the file cannot be loaded or applied\n        \"\"\"\n        css_path = self._styles_dir / filename\n\n        if not css_path.exists():\n            raise StyleManagerError(f\"CSS file not found: {css_path}\")\n\n        try:\n            css_provider = Gtk.CssProvider()\n            css_provider.load_from_path(str(css_path))\n\n            display = Gdk.Display.get_default()\n            if display is None:\n                raise StyleManagerError(\"No default display available\")\n\n            Gtk.StyleContext.add_provider_for_display(\n                display,\n                css_provider,\n                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION\n            )\n\n            self._providers.append(css_provider)\n            self._applied_styles.append(filename)\n\n            self.logger.info(f\"Successfully loaded CSS file: {filename}\")\n\n        except Exception as e:\n            raise StyleManagerError(f\"Failed to load CSS file {filename}: {e}\") from e\n\n    def load_css_from_string(self, css_content: str, identifier: str = \"custom\") -> None:\n        \"\"\"\n        Load CSS from a string and apply it to the application.\n\n        Args:\n            css_content: CSS content as string\n            identifier: Identifier for this CSS content (for logging/tracking)\n\n        Raises:\n            StyleManagerError: If the CSS cannot be loaded or applied\n        \"\"\"\n        try:\n            css_provider = Gtk.CssProvider()\n            css_provider.load_from_data(css_content.encode('utf-8'))\n\n            display = Gdk.Display.get_default()\n            if display is None:\n                raise StyleManagerError(\"No default display available\")\n\n            Gtk.StyleContext.add_provider_for_display(\n                display,\n                css_provider,\n                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION\n            )\n\n            self._providers.append(css_provider)\n            self._applied_styles.append(identifier)\n\n            self.logger.info(f\"Successfully loaded CSS from string: {identifier}\")\n\n        except Exception as e:\n            raise StyleManagerError(f\"Failed to load CSS from string {identifier}: {e}\") from e\n\n    def apply_theme_variant(self, variant: str = \"light\") -> None:\n        \"\"\"\n        Apply a specific theme variant.\n\n        Args:\n            variant: Theme variant (\"light\" or \"dark\")\n        \"\"\"\n        if variant not in [\"light\", \"dark\"]:\n            self.logger.warning(f\"Unknown theme variant: {variant}. Using 'light'.\")\n            variant = \"light\"\n\n        # This could be extended to load variant-specific CSS files\n        theme_css = f\"theme-{variant}.css\"\n        theme_path = self._styles_dir / theme_css\n\n        if theme_path.exists():\n            try:\n                self.load_css_file(theme_css)\n                self.logger.info(f\"Applied theme variant: {variant}\")\n            except StyleManagerError as e:\n                self.logger.warning(f\"Failed to apply theme variant {variant}: {e}\")\n        else:\n            self.logger.debug(f\"Theme variant file not found: {theme_css}\")\n\n    def reload_styles(self) -> None:\n        \"\"\"\n        Reload all previously applied styles.\n\n        This method clears all current providers and reapplies styles,\n        useful for development or dynamic theme switching.\n        \"\"\"\n        self.logger.info(\"Reloading all styles...\")\n\n        # Store applied styles before clearing\n        styles_to_reload = self._applied_styles.copy()\n\n        # Clear current providers\n        self.clear_styles()\n\n        # Reload styles\n        for style in styles_to_reload:\n            if style.endswith('.css'):\n                try:\n                    self.load_css_file(style)\n                except StyleManagerError as e:\n                    self.logger.error(f\"Failed to reload style {style}: {e}\")\n\n    def clear_styles(self) -> None:\n        \"\"\"Remove all applied CSS providers.\"\"\"\n        display = Gdk.Display.get_default()\n        if display is None:\n            self.logger.warning(\"No default display available for clearing styles\")\n            return\n\n        for provider in self._providers:\n            Gtk.StyleContext.remove_provider_for_display(display, provider)\n\n        self._providers.clear()\n        self._applied_styles.clear()\n        self.logger.info(\"Cleared all applied styles\")\n\n    def get_applied_styles(self) -> List[str]:\n        \"\"\"\n        Get a list of currently applied style identifiers.\n\n        Returns:\n            List of applied style identifiers\n        \"\"\"\n        return self._applied_styles.copy()\n\n    def has_style(self, identifier: str) -> bool:\n        \"\"\"\n        Check if a specific style is currently applied.\n\n        Args:\n            identifier: Style identifier to check\n\n        Returns:\n            True if the style is applied, False otherwise\n        \"\"\"\n        return identifier in self._applied_styles\n\n    def get_styles_directory(self) -> Path:\n        \"\"\"\n        Get the current styles directory path.\n\n        Returns:\n            Path to the styles directory\n        \"\"\"\n        return self._styles_dir\n\n    def set_styles_directory(self, new_dir: Path) -> None:\n        \"\"\"\n        Set a new styles directory.\n\n        Args:\n            new_dir: New path to the styles directory\n\n        Raises:\n            StyleManagerError: If the directory doesn't exist\n        \"\"\"\n        if not new_dir.exists():\n            raise StyleManagerError(f\"Styles directory not found: {new_dir}\")\n\n        self._styles_dir = new_dir\n        self.logger.info(f\"Styles directory changed to: {new_dir}\")\n\n    def _on_system_theme_changed(self, style_manager, param):\n        \"\"\"Handle system theme changes automatically\"\"\"\n        try:\n            is_dark = style_manager.get_dark()\n            theme_name = \"dark\" if is_dark else \"light\"\n            self.logger.info(f\"System theme changed to: {theme_name}\")\n\n            # Reload theme-specific styles\n            self._load_theme_specific_styles()\n        except Exception as e:\n            self.logger.error(f\"Error handling system theme change: {e}\")\n\n    def _load_theme_specific_styles(self):\n        \"\"\"Load CSS file specific to current system theme\"\"\"\n        try:\n            # Remove existing theme provider if it exists\n            if self._theme_provider:\n                display = Gdk.Display.get_default()\n                if display:\n                    Gtk.StyleContext.remove_provider_for_display(display, self._theme_provider)\n                self._theme_provider = None\n\n            # Detect current theme\n            adw_style_manager = Adw.StyleManager.get_default()\n            is_dark = adw_style_manager.get_dark()\n\n            if is_dark:\n                theme_file = \"theme-dark.css\"\n                theme_path = self._styles_dir / theme_file\n\n                if theme_path.exists():\n                    try:\n                        self._theme_provider = Gtk.CssProvider()\n                        self._theme_provider.load_from_path(str(theme_path))\n\n                        display = Gdk.Display.get_default()\n                        if display:\n                            Gtk.StyleContext.add_provider_for_display(\n                                display,\n                                self._theme_provider,\n                                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1  # Higher priority than base styles\n                            )\n\n                            self.logger.info(f\"Applied dark theme styling\")\n                            self._applied_styles.append(f\"theme-dark\")\n                        else:\n                            self.logger.warning(\"No default display available for dark theme\")\n                    except Exception as e:\n                        self.logger.error(f\"Failed to load dark theme CSS: {e}\")\n                else:\n                    self.logger.debug(\"Dark theme CSS not found, using default styling\")\n            else:\n                self.logger.info(\"Applied light theme styling\")\n\n        except Exception as e:\n            self.logger.error(f\"Error loading theme-specific styles: {e}\")\n\n\n# Singleton instance for global access\n_style_manager_instance: Optional[StyleManager] = None\n\n\ndef get_style_manager() -> StyleManager:\n    \"\"\"\n    Get the global StyleManager instance.\n\n    Returns:\n        Global StyleManager instance\n    \"\"\"\n    global _style_manager_instance\n    if _style_manager_instance is None:\n        _style_manager_instance = StyleManager()\n    return _style_manager_instance\n\n\ndef initialize_styles() -> None:\n    \"\"\"\n    Initialize the global style manager with default styles.\n\n    This function should be called once during application startup.\n    \"\"\"\n    style_manager = get_style_manager()\n    style_manager.load_default_styles()\n",
  "raw_output": {
    "raw_edits": "```\n<<<<<<< SEARCH line=65\n            \\'base.css\\',\n            \\'components.css\\',\\\n            \\'layout.css\\',\\\n            \\'theme.css\\'\n        ]\n=======\n            'base.css',\n            'components.css',\n            'layout.css',\n            'theme.css',\n            'interactions.css' # New: for modern UI/UX animations and micro-interactions\n        ]\n>>>>>>> REPLACE\n```",
    "parser_metrics": {
      "tags": 0,
      "mismatched_tags": 0
    }
  }
}
```

