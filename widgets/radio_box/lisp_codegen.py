"""
Lisp generator functions for wxRadioBox objects

@copyright: 2002-2004 D.H. aka crazyinsomniac on sourceforge.net
@license: MIT (see license.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

import common
from ChoicesCodeHandler import *


class LispCodeGenerator:
    def get_code(self, obj):
        init = []
        codegen = common.code_writers['lisp']
        prop = obj.properties
        id_name, id = codegen.generate_code_id(obj)
        label = codegen.quote_str(prop.get('label', ''))
        choices = prop.get('choices', [])
        major_dim = prop.get('dimension', '0')

        if not obj.parent.is_toplevel:
            parent = '(slot-%s obj)' % obj.parent.name
        else:
            parent = '(slot-top-window obj)'

        style = prop.get("style")
        if not style:
            style = '0'
        else:
            style = codegen.cn_f(style)

        if id_name:
            init.append(id_name)

        length = len(choices)
        choices = ' '.join([codegen.quote_str(c) for c in choices])
        init.append(
            '(setf (slot-%s obj) (wxRadioBox_Create %s %s %s -1 -1 -1 -1 '
            '%s (vector %s) %s %s))\n' % (
                obj.name,
                parent,
                id,
                label,
                length,
                choices,
                major_dim,
                style)
            )

        props_buf = codegen.generate_common_properties(obj)
        selection = prop.get('selection')
        if selection is not None:
            props_buf.append('(wxRadioBox_SetSelection (slot-%s obj) %s)\n' %
                             (obj.name, selection))
        return init, props_buf, []

# end of class LispCodeGenerator


def initialize():
    common.class_names['EditRadioBox'] = 'wxRadioBox'

    codegen = common.code_writers.get('lisp')
    if codegen:
        codegen.add_widget_handler('wxRadioBox', LispCodeGenerator())
        codegen.add_property_handler('choices', ChoicesCodeHandler)
