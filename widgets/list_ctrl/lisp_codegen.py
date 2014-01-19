"""\
Lisp generator functions for wxListCtrl objects

@copyright: 2002-2004 D. H. aka crazyinsomniac on sourceforge
@copyright: 2014 Carsten Grohmann
@license: MIT (see license.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

import common
import wcodegen


class LispListCtrlGenerator(wcodegen.LispWidgetCodeWriter):
    tmpl = '(setf %(name)s (%(klass)s_Create %(parent)s %(id)s ' \
           '-1 -1 -1 -1 %(style)s))\n'
    default_style = 'wxLC_ICON'

# end of class LispListCtrlGenerator


def initialize():
    common.class_names['EditListCtrl'] = 'wxListCtrl'

    codegen = common.code_writers.get('lisp')
    if codegen:
        codegen.add_widget_handler('wxListCtrl', LispListCtrlGenerator())
