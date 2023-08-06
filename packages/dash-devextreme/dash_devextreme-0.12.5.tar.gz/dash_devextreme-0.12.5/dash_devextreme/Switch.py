# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Switch(Component):
    """A Switch component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional)
- activeStateEnabled (boolean; default True)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; default True)
- height (number | string; optional)
- hint (string; optional)
- hoverStateEnabled (boolean; default True)
- isValid (boolean; default True)
- name (string; default '')
- readOnly (boolean; default False)
- rtlEnabled (boolean; default False)
- switchedOffText (string; default 'OFF')
- switchedOnText (string; default 'ON')
- tabIndex (number; default 0)
- validationError (dict; optional)
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto')
- value (boolean; default False)
- visible (boolean; default True)
- width (number | string; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, isValid=Component.UNDEFINED, name=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, readOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, switchedOffText=Component.UNDEFINED, switchedOnText=Component.UNDEFINED, tabIndex=Component.UNDEFINED, validationError=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, value=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'isValid', 'name', 'readOnly', 'rtlEnabled', 'switchedOffText', 'switchedOnText', 'tabIndex', 'validationError', 'validationMessageMode', 'value', 'visible', 'width']
        self._type = 'Switch'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'isValid', 'name', 'readOnly', 'rtlEnabled', 'switchedOffText', 'switchedOnText', 'tabIndex', 'validationError', 'validationMessageMode', 'value', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Switch, self).__init__(**args)
