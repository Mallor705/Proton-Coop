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


class AddGameDialog(Gtk.FileChooserDialog):
    def __init__(self, parent):
        super().__init__(
            title="Select Game Archive",
            transient_for=parent,
            modal=True,
            action=Gtk.FileChooserAction.OPEN,
        )
        self.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL, "_Open", Gtk.ResponseType.OK
        )

        filter_zip = Gtk.FileFilter()
        filter_zip.set_name("Zip files")
        filter_zip.add_mime_type("application/zip")
        filter_zip.add_pattern("*.nc")
        self.add_filter(filter_zip)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.add_filter(filter_any)
