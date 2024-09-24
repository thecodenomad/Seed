from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/org/thecodenomad/seeds/window.ui')
class SeedsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'SeedsWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
