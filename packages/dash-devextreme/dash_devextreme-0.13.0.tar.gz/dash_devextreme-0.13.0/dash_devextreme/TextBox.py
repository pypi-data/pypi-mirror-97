# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TextBox(Component):
    """A TextBox component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- buttons (list of string | dicts; optional): Allows you to add custom buttons to the input text field
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- focusStateEnabled (boolean; default True): Specifies whether the UI component can be focused using keyboard navigation
- height (number | string; default undefined): Specifies the UI component's height
- hint (string; default undefined): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default True): Specifies whether the UI component changes its state when a user pauses on it
- inputAttr (dict; optional): Specifies the attributes to be passed on to the underlying HTML element
- isValid (boolean; default True): Specifies or indicates whether the editor's value is valid
- mask (string; default ''): The editor mask that specifies the custom format of the entered string
- maskChar (string; default '_'): Specifies a mask placeholder. A single character is recommended
- maskInvalidMessage (string; default 'Value is invalid'): A message displayed when the entered text does not match the specified pattern
- maskRules (dict; optional): Specifies custom mask rules
- maxLength (string | number; optional): Specifies the maximum number of characters you can enter into the textbox
- mode (a value equal to: 'email', 'password', 'search', 'tel', 'text', 'url'; default 'text'): The "mode" attribute value of the actual HTML input element representing the text box
- name (string; default ''): The value to be assigned to the name attribute of the underlying HTML element
- placeholder (string; default ''): The text displayed by the UI component when the UI component value is empty
- readOnly (boolean; default False): Specifies whether the editor is read-only
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- showClearButton (boolean; default False): Specifies whether to display the Clear button in the UI component
- showMaskMode (a value equal to: 'always', 'onFocus'; default 'always'): Specifies when the UI component shows the mask. Applies only if useMaskedValue is true.
- spellcheck (boolean; default False): Specifies whether or not the UI component checks the inner text for spelling mistakes
- stylingMode (a value equal to: 'outlined', 'underlined', 'filled'; default 'outlined'): Specifies how the UI component's text field is styled
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- useMaskedValue (boolean; default False): Specifies whether the value should contain mask characters or not
- validationError (dict; optional): Information on the broken validation rule. Contains the first item from the validationErrors array
- validationErrors (dict; optional): An array of the validation rules that failed
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto'): Specifies how the message about the validation rules that are not satisfied by this editor's value is displayed
- validationStatus (a value equal to: 'valid', 'invalid', 'pending'; default 'valid'): Indicates or specifies the current validation status
- value (string; default ''): Specifies a value the UI component displays
- valueChangeEvent (string; default 'change'): Specifies the DOM events after which the UI component's value should be updated
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; default undefined): Specifies the UI component's width"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, buttons=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, isValid=Component.UNDEFINED, mask=Component.UNDEFINED, maskChar=Component.UNDEFINED, maskInvalidMessage=Component.UNDEFINED, maskRules=Component.UNDEFINED, maxLength=Component.UNDEFINED, mode=Component.UNDEFINED, name=Component.UNDEFINED, onChange=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onCopy=Component.UNDEFINED, onCut=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEnterKey=Component.UNDEFINED, onFocusIn=Component.UNDEFINED, onFocusOut=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInput=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onKeyUp=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPaste=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, showClearButton=Component.UNDEFINED, showMaskMode=Component.UNDEFINED, spellcheck=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, useMaskedValue=Component.UNDEFINED, validationError=Component.UNDEFINED, validationErrors=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, validationStatus=Component.UNDEFINED, value=Component.UNDEFINED, valueChangeEvent=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accessKey', 'activeStateEnabled', 'buttons', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'mask', 'maskChar', 'maskInvalidMessage', 'maskRules', 'maxLength', 'mode', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'showClearButton', 'showMaskMode', 'spellcheck', 'stylingMode', 'tabIndex', 'useMaskedValue', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width']
        self._type = 'TextBox'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'accessKey', 'activeStateEnabled', 'buttons', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'mask', 'maskChar', 'maskInvalidMessage', 'maskRules', 'maxLength', 'mode', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'showClearButton', 'showMaskMode', 'spellcheck', 'stylingMode', 'tabIndex', 'useMaskedValue', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TextBox, self).__init__(children=children, **args)
