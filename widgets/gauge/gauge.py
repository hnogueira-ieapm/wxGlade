"""\
wxGauge objects

@copyright: 2002-2007 Alberto Griggio
@copyright: 2016-2020 Dietmar Schwertberger
@license: MIT (see LICENSE.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

import wx
import common, misc
import wcodegen
from edit_windows import ManagedBase, EditStylesMixin
import new_properties as np


class EditGauge(ManagedBase, EditStylesMixin):
    "Class to handle wxGauge objects"

    WX_CLASS = "wxGauge"
    _PROPERTIES = ["Widget", "range", "style"]
    PROPERTIES = ManagedBase.PROPERTIES + _PROPERTIES + ManagedBase.EXTRA_PROPERTIES
    recreate_on_style_change = True

    def __init__(self, name, parent, pos, style, instance_class=None):
        ManagedBase.__init__(self, name, parent, pos, instance_class)
        EditStylesMixin.__init__(self)
        if style: self.properties["style"].set(style)

        # initialise instance properties
        self.range = np.SpinProperty(10, val_range=(0,10000000), immediate=True)

    def create_widget(self):
        self.widget = wx.Gauge(self.parent_window.widget, self.id, self.range, style=self.style)
        if self.range>=3: self.widget.SetValue(self.range//3)

    def properties_changed(self, modified):
        if not modified or "range" in modified and self.widget:
            self.widget.SetRange(self.range)
        EditStylesMixin.properties_changed(self, modified)
        ManagedBase.properties_changed(self, modified)


def builder(parent, pos):
    "Factory function for editor objects from GUI"
    dialog = wcodegen.WidgetStyleSelectionDialog( _('wxGauge'), _('Orientation'), 'wxGA_HORIZONTAL|wxGA_VERTICAL')
    with misc.disable_stay_on_top(common.adding_window or parent):
        res = dialog.ShowModal()
    style = dialog.get_selection()
    dialog.Destroy()
    if res != wx.ID_OK: return

    name = parent.toplevel_parent.get_next_contained_name('gauge_%d')
    with parent.frozen():
        editor = EditGauge(name, parent, pos, style)
        editor.properties["flag"].set("wxEXPAND")
        if parent.widget: editor.create()
    return editor


def xml_builder(parent, pos, attrs):
    "Factory to build editor objects from a XML file"
    attrs.set_editor_class(EditGauge)
    name, instance_class = attrs.get_attributes("name", "instance_class")
    return EditGauge(name, parent, pos, '')


def initialize():
    "initialization function for the module: returns a wxBitmapButton to be added to the main palette"
    common.widget_classes['EditGauge'] = EditGauge
    common.widgets['EditGauge'] = builder
    common.widgets_from_xml['EditGauge'] = xml_builder
    return common.make_object_button('EditGauge', 'gauge.xpm')
