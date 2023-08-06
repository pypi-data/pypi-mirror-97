# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TextArea(Component):
    """A TextArea component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- autoResizeEnabled (boolean; default False): A Boolean value specifying whether or not the auto resizing mode is enabled
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- focusStateEnabled (boolean; default True): Specifies whether the UI component can be focused using keyboard navigation
- height (number | string; optional): Specifies the UI component's height
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default True): Specifies whether the UI component changes its state when a user pauses on it
- inputAttr (dict; optional): Specifies the attributes to be passed on to the underlying HTML element
- isValid (boolean; default True): Specifies or indicates whether the editor's value is valid
- maxHeight (string | number; optional): Specifies the maximum height of the UI component
- maxLength (string | number; optional): Specifies the maximum number of characters you can enter into the textbox
- minHeight (string | number; optional): Specifies the minimum height of the UI component
- name (string; default ''): The value to be assigned to the name attribute of the underlying HTML element
- placeholder (string; default ''): The text displayed by the UI component when the UI component value is empty
- readOnly (boolean; default False): Specifies whether the editor is read-only
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- spellcheck (boolean; default False): Specifies whether or not the UI component checks the inner text for spelling mistakes
- stylingMode (a value equal to: 'outlined', 'underlined', 'filled'; default 'outlined'): Specifies how the UI component's text field is styled
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- validationError (dict; optional): Information on the broken validation rule. Contains the first item from the validationErrors array
- validationErrors (dict; optional): An array of the validation rules that failed
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto'): Specifies how the message about the validation rules that are not satisfied by this editor's value is displayed
- validationStatus (a value equal to: 'valid', 'invalid', 'pending'; default 'valid'): Indicates or specifies the current validation status
- value (string; default ''): Specifies a value the UI component displays
- valueChangeEvent (string; default 'change'): Specifies the DOM events after which the UI component's value should be updated
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; default undefined): Specifies the UI component's width"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, autoResizeEnabled=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, isValid=Component.UNDEFINED, maxHeight=Component.UNDEFINED, maxLength=Component.UNDEFINED, minHeight=Component.UNDEFINED, name=Component.UNDEFINED, onChange=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onCopy=Component.UNDEFINED, onCut=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEnterKey=Component.UNDEFINED, onFocusIn=Component.UNDEFINED, onFocusOut=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInput=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onKeyUp=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPaste=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, spellcheck=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, validationError=Component.UNDEFINED, validationErrors=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, validationStatus=Component.UNDEFINED, value=Component.UNDEFINED, valueChangeEvent=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accessKey', 'activeStateEnabled', 'autoResizeEnabled', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'maxHeight', 'maxLength', 'minHeight', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'spellcheck', 'stylingMode', 'tabIndex', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width']
        self._type = 'TextArea'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'accessKey', 'activeStateEnabled', 'autoResizeEnabled', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'maxHeight', 'maxLength', 'minHeight', 'name', 'placeholder', 'readOnly', 'rtlEnabled', 'spellcheck', 'stylingMode', 'tabIndex', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TextArea, self).__init__(children=children, **args)
