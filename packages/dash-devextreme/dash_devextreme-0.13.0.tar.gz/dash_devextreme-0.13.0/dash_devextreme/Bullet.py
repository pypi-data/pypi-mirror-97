# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Bullet(Component):
    """A Bullet component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- color (string; default '#e8c267')
- disabled (boolean; default False)
- elementAttr (dict; optional)
- endScaleValue (number; optional)
- margin (dict; optional)
- pathModified (boolean; default False)
- rtlEnabled (boolean; default False)
- showTarget (boolean; default True)
- showZeroLevel (boolean; default True)
- size (dict; optional)
- startScaleValue (number; default 0)
- target (number; default 0)
- targetColor (string; default '#666666')
- targetWidth (number; default 4)
- theme (a value equal to: 'generic.dark', 'generic.light', 'generic.contrast', 'ios7.default', 'generic.carmine', 'generic.darkmoon', 'generic.darkviolet', 'generic.greenmist', 'generic.softblue', 'material.blue.light', 'material.lime.light', 'material.orange.light', 'material.purple.light', 'material.teal.light'; default 'generic.light')
- tooltip (dict; optional)
- value (number; default 0)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, endScaleValue=Component.UNDEFINED, margin=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onDrawn=Component.UNDEFINED, onExported=Component.UNDEFINED, onExporting=Component.UNDEFINED, onFileSaving=Component.UNDEFINED, onIncidentOccurred=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onTooltipHidden=Component.UNDEFINED, onTooltipShown=Component.UNDEFINED, pathModified=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, showTarget=Component.UNDEFINED, showZeroLevel=Component.UNDEFINED, size=Component.UNDEFINED, startScaleValue=Component.UNDEFINED, target=Component.UNDEFINED, targetColor=Component.UNDEFINED, targetWidth=Component.UNDEFINED, theme=Component.UNDEFINED, tooltip=Component.UNDEFINED, value=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'color', 'disabled', 'elementAttr', 'endScaleValue', 'margin', 'pathModified', 'rtlEnabled', 'showTarget', 'showZeroLevel', 'size', 'startScaleValue', 'target', 'targetColor', 'targetWidth', 'theme', 'tooltip', 'value', 'loading_state']
        self._type = 'Bullet'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'color', 'disabled', 'elementAttr', 'endScaleValue', 'margin', 'pathModified', 'rtlEnabled', 'showTarget', 'showZeroLevel', 'size', 'startScaleValue', 'target', 'targetColor', 'targetWidth', 'theme', 'tooltip', 'value', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Bullet, self).__init__(**args)
