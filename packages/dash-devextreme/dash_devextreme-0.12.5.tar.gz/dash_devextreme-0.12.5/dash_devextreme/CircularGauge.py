# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CircularGauge(Component):
    """A CircularGauge component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- animation (dict; optional)
- containerBackgroundColor (string; default 'none')
- disabled (boolean; default False)
- elementAttr (dict; optional)
- export (dict; optional)
- geometry (dict; optional)
- loadingIndicator (dict; optional)
- margin (dict; optional)
- pathModified (boolean; default False)
- rangeContainer (dict; optional)
- redrawOnResize (boolean; default True)
- rtlEnabled (boolean; default False)
- scale (dict; optional)
- size (dict; optional)
- subvalueIndicator (dict; optional)
- subvalues (list of numbers; optional)
- theme (a value equal to: 'generic.dark', 'generic.light', 'generic.contrast', 'ios7.default', 'generic.carmine', 'generic.darkmoon', 'generic.darkviolet', 'generic.greenmist', 'generic.softblue', 'material.blue.light', 'material.lime.light', 'material.orange.light', 'material.purple.light', 'material.teal.light'; default 'generic.light')
- title (dict | string; default '')
- tooltip (dict; optional)
- value (number; default 0)
- valueIndicator (dict; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, animation=Component.UNDEFINED, containerBackgroundColor=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, export=Component.UNDEFINED, geometry=Component.UNDEFINED, loadingIndicator=Component.UNDEFINED, margin=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onDrawn=Component.UNDEFINED, onExported=Component.UNDEFINED, onExporting=Component.UNDEFINED, onFileSaving=Component.UNDEFINED, onIncidentOccurred=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onTooltipHidden=Component.UNDEFINED, onTooltipShown=Component.UNDEFINED, pathModified=Component.UNDEFINED, rangeContainer=Component.UNDEFINED, redrawOnResize=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scale=Component.UNDEFINED, size=Component.UNDEFINED, subvalueIndicator=Component.UNDEFINED, subvalues=Component.UNDEFINED, theme=Component.UNDEFINED, title=Component.UNDEFINED, tooltip=Component.UNDEFINED, value=Component.UNDEFINED, valueIndicator=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'animation', 'containerBackgroundColor', 'disabled', 'elementAttr', 'export', 'geometry', 'loadingIndicator', 'margin', 'pathModified', 'rangeContainer', 'redrawOnResize', 'rtlEnabled', 'scale', 'size', 'subvalueIndicator', 'subvalues', 'theme', 'title', 'tooltip', 'value', 'valueIndicator']
        self._type = 'CircularGauge'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'animation', 'containerBackgroundColor', 'disabled', 'elementAttr', 'export', 'geometry', 'loadingIndicator', 'margin', 'pathModified', 'rangeContainer', 'redrawOnResize', 'rtlEnabled', 'scale', 'size', 'subvalueIndicator', 'subvalues', 'theme', 'title', 'tooltip', 'value', 'valueIndicator']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(CircularGauge, self).__init__(**args)
