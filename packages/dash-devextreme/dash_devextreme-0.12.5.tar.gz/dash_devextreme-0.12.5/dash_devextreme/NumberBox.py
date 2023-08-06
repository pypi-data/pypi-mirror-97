# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class NumberBox(Component):
    """A NumberBox component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional)
- activeStateEnabled (boolean; default True)
- buttons (list of string | dicts; optional)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; default True)
- format (string | dict; default '')
- height (number | string; optional)
- hint (string; optional)
- hoverStateEnabled (boolean; default True)
- inputAttr (dict; optional)
- invalidValueMessage (string; default 'Value must be a number')
- isValid (boolean; default True)
- max (number; optional)
- min (number; optional)
- mode (a value equal to: 'number', 'text', 'tel'; default 'number')
- name (string; default '')
- placeholder (string; default '')
- readOnly (boolean; default False)
- rtlEnabled (boolean; default False)
- showClearButton (boolean; default False)
- showSpinButtons (boolean; default False)
- step (number; default 1)
- stylingMode (a value equal to: 'outlined', 'underlined', 'filled'; default 'outlined')
- tabIndex (number; default 0)
- text (string; optional)
- useLargeSpinButtons (boolean; default False)
- validationError (dict; optional)
- validationErrors (list of dicts; optional)
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto')
- validationStatus (a value equal to: 'valid', 'invalid', 'pending'; default 'valid')
- value (number | dict; default 0)
- valueChangeEvent (string; default 'change')
- visible (boolean; default True)
- width (number | string; optional)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, buttons=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, format=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, invalidValueMessage=Component.UNDEFINED, isValid=Component.UNDEFINED, max=Component.UNDEFINED, min=Component.UNDEFINED, mode=Component.UNDEFINED, name=Component.UNDEFINED, onChange=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onCopy=Component.UNDEFINED, onCut=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEnterKey=Component.UNDEFINED, onFocusIn=Component.UNDEFINED, onFocusOut=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInput=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onKeyUp=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPaste=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, showClearButton=Component.UNDEFINED, showSpinButtons=Component.UNDEFINED, step=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, text=Component.UNDEFINED, useLargeSpinButtons=Component.UNDEFINED, validationError=Component.UNDEFINED, validationErrors=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, validationStatus=Component.UNDEFINED, value=Component.UNDEFINED, valueChangeEvent=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accessKey', 'activeStateEnabled', 'buttons', 'disabled', 'elementAttr', 'focusStateEnabled', 'format', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'invalidValueMessage', 'isValid', 'max', 'min', 'mode', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'showClearButton', 'showSpinButtons', 'step', 'stylingMode', 'tabIndex', 'text', 'useLargeSpinButtons', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width', 'loading_state']
        self._type = 'NumberBox'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'accessKey', 'activeStateEnabled', 'buttons', 'disabled', 'elementAttr', 'focusStateEnabled', 'format', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'invalidValueMessage', 'isValid', 'max', 'min', 'mode', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'showClearButton', 'showSpinButtons', 'step', 'stylingMode', 'tabIndex', 'text', 'useLargeSpinButtons', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(NumberBox, self).__init__(children=children, **args)
