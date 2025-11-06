import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk, Pango


class TextInputDialog(Adw.MessageDialog):
    def __init__(self, parent, title, message):
        super().__init__(transient_for=parent, modal=True, title=title, body=message)
        self.entry = Gtk.Entry()
        self.set_extra_child(self.entry)
        self.add_response("ok", "OK")
        self.add_response("cancel", "Cancel")
        self.set_default_response("ok")

    def get_input(self):
        return self.entry.get_text()


class ConfirmationDialog(Adw.MessageDialog):
    def __init__(self, parent, title, message):
        super().__init__(transient_for=parent, modal=True, title=title, body=message)
        self.add_response("ok", "OK")
        self.add_response("cancel", "Cancel")
        self.set_default_response("cancel")


class AddGameDialog(Adw.MessageDialog):
    def __init__(self, parent):
        super().__init__(transient_for=parent, modal=True, title="Add New Game")
        self._selected_path = None

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_extra_child(content_box)

        # Entrada para o nome do jogo
        self.name_row = Adw.EntryRow(title="Game Name")
        content_box.append(self.name_row)

        # Seletor de ficheiro para o executável
        exe_row = Adw.ActionRow(title="Executable Path")
        self.path_label = Gtk.Label(
            label="<small><i>None selected</i></small>",
            use_markup=True,
            halign=Gtk.Align.START,
        )
        self.path_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.path_label.set_hexpand(True)

        button = Gtk.Button(label="Browse...")
        button.connect("clicked", self._on_open_file_dialog)

        exe_row.add_suffix(self.path_label)
        exe_row.add_suffix(button)
        content_box.append(exe_row)

        self.add_response("ok", "Add Game")
        self.add_response("cancel", "Cancel")
        self.set_default_response("ok")

    def _on_open_file_dialog(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select Game Executable",
            transient_for=self.get_transient_for(),
            modal=True,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL, "_Open", Gtk.ResponseType.OK
        )
        dialog.connect("response", self._on_file_selected)
        dialog.present()

    def _on_file_selected(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            file = dialog.get_file()
            if file:
                self._selected_path = file.get_path()
                self.path_label.set_markup(
                    f"<small><i>{self._selected_path}</i></small>"
                )
        dialog.destroy()

    def get_game_details(self):
        name = self.name_row.get_text()
        return name, self._selected_path
