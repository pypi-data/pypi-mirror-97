# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DateBox(Component):
    """A DateBox component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- acceptCustomValue (boolean; default True): Specifies whether or not the UI component allows an end-user to enter a custom value
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- adaptivityEnabled (boolean; default False): Specifies whether or not adaptive UI component rendering is enabled on a small screen
- applyButtonText (string; default 'OK'): The text displayed on the Apply button
- applyValueMode (a value equal to: 'instantly', 'useButtons'; default 'instantly'): Specifies the way an end-user applies the selected value
- buttons (list of string | dicts; optional): Allows you to add custom buttons to the input text field
- calendarOptions (dict; optional): Configures the calendar's value picker. Applies only if the pickerType is "calendar"
- cancelButtonText (string; default 'Cancel'): The text displayed on the Cancel button
- dateOutOfRangeMessage (string; default 'Value is out of range'): Specifies the message displayed if the specified date is later than the max value or earlier than the min value
- dateSerializationFormat (string; optional): Specifies the date-time value serialization format. Use it only if you do not specify the value at design time
- deferRendering (boolean; default True): Specifies whether to render the drop-down field's content when it is displayed. If false, the content is rendered immediately
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- disabledDates (list; optional): Specifies dates that users cannot select. Applies only if pickerType is "calendar"
- displayFormat (string | dict; optional): Specifies the date display format. Ignored if the pickerType property is "native"
- dropDownButtonComponent (string | dict; optional): An alias for the dropDownButtonTemplate property specified in React. Accepts a custom component. Refer to Using a Custom Component for more information.
- dropDownButtonRender (string; optional): An alias for the dropDownButtonTemplate property specified in React. Accepts a rendering function. Refer to Using a Rendering Function for more information.
- dropDownButtonTemplate (string | dict; default 'dropDownButton'): Specifies a custom template for the drop-down button
- dropDownOptions (dict; optional): Configures the drop-down field which holds the content
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- focusStateEnabled (boolean; default True): Specifies whether the UI component can be focused using keyboard navigation
- height (number | string; default undefined): Specifies the UI component's height
- hint (string; default undefined): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default True): Specifies whether the UI component changes its state when a user pauses on it
- inputAttr (dict; optional): Specifies the attributes to be passed on to the underlying HTML element
- interval (number; default 30): Specifies the interval between neighboring values in the popup list in minutes
- invalidDateMessage (string; default 'Value must be a date or time'): Specifies the message displayed if the typed value is not a valid date or time
- isValid (boolean; default True): Specifies or indicates whether the editor's value is valid
- max (number | string; optional): The last date that can be selected within the UI component
- maxLength (string | number; optional): Specifies the maximum number of characters you can enter into the textbox
- min (number | string; optional): The minimum date that can be selected within the UI component
- name (string; default ''): The value to be assigned to the name attribute of the underlying HTML element
- opened (boolean; default False): Specifies whether or not the drop-down editor is displayed
- openOnFieldClick (boolean; default False): Specifies whether a user can open the drop-down list by clicking a text field
- pickerType (a value equal to: 'calendar', 'list', 'native', 'rollers'; default 'calendar'): Specifies the type of the date/time picker.
- placeholder (string; default ''): The text displayed by the UI component when the UI component value is empty
- readOnly (boolean; default False): Specifies whether the editor is read-only
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- showAnalogClock (boolean; default True): Specifies whether to show the analog clock in the value picker. Applies only if type is "datetime" and pickerType is "calendar".
- showClearButton (boolean; default False): Specifies whether to display the Clear button in the UI component
- showDropDownButton (boolean; default True): Specifies whether the drop-down button is visible
- spellcheck (boolean; default False): Specifies whether or not the UI component checks the inner text for spelling mistakes
- stylingMode (a value equal to: 'outlined', 'underlined', 'filled'; default 'outlined'): Specifies how the UI component's text field is styled
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- type (a value equal to: 'date', 'datetime', 'time'; default 'date'): A format used to display date/time information
- useMaskBehavior (boolean; default False): Specifies whether to control user input using a mask created based on the displayFormat
- validationError (dict; optional): Information on the broken validation rule. Contains the first item from the validationErrors array
- validationErrors (dict; optional): An array of the validation rules that failed
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto'): Specifies how the message about the validation rules that are not satisfied by this editor's value is displayed
- validationStatus (a value equal to: 'valid', 'invalid', 'pending'; default 'valid'): Indicates or specifies the current validation status
- value (number | string | dict; optional): An object or a value specifying the date and time currently selected using the date box
- valueChangeEvent (string; default 'change'): Specifies the DOM events after which the UI component's value should be updated
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; default undefined): Specifies the UI component's width"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, acceptCustomValue=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, adaptivityEnabled=Component.UNDEFINED, applyButtonText=Component.UNDEFINED, applyValueMode=Component.UNDEFINED, buttons=Component.UNDEFINED, calendarOptions=Component.UNDEFINED, cancelButtonText=Component.UNDEFINED, dateOutOfRangeMessage=Component.UNDEFINED, dateSerializationFormat=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, disabledDates=Component.UNDEFINED, displayFormat=Component.UNDEFINED, dropDownButtonComponent=Component.UNDEFINED, dropDownButtonRender=Component.UNDEFINED, dropDownButtonTemplate=Component.UNDEFINED, dropDownOptions=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, interval=Component.UNDEFINED, invalidDateMessage=Component.UNDEFINED, isValid=Component.UNDEFINED, max=Component.UNDEFINED, maxLength=Component.UNDEFINED, min=Component.UNDEFINED, name=Component.UNDEFINED, onChange=Component.UNDEFINED, onClosed=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onCopy=Component.UNDEFINED, onCut=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEnterKey=Component.UNDEFINED, onFocusIn=Component.UNDEFINED, onFocusOut=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInput=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onKeyUp=Component.UNDEFINED, onOpened=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPaste=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, opened=Component.UNDEFINED, openOnFieldClick=Component.UNDEFINED, pickerType=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, showAnalogClock=Component.UNDEFINED, showClearButton=Component.UNDEFINED, showDropDownButton=Component.UNDEFINED, spellcheck=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, type=Component.UNDEFINED, useMaskBehavior=Component.UNDEFINED, validationError=Component.UNDEFINED, validationErrors=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, validationStatus=Component.UNDEFINED, value=Component.UNDEFINED, valueChangeEvent=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'acceptCustomValue', 'accessKey', 'activeStateEnabled', 'adaptivityEnabled', 'applyButtonText', 'applyValueMode', 'buttons', 'calendarOptions', 'cancelButtonText', 'dateOutOfRangeMessage', 'dateSerializationFormat', 'deferRendering', 'disabled', 'disabledDates', 'displayFormat', 'dropDownButtonComponent', 'dropDownButtonRender', 'dropDownButtonTemplate', 'dropDownOptions', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'interval', 'invalidDateMessage', 'isValid', 'max', 'maxLength', 'min', 'name', 'opened', 'openOnFieldClick', 'pickerType', 'placeholder', 'readOnly', 'rtlEnabled', 'showAnalogClock', 'showClearButton', 'showDropDownButton', 'spellcheck', 'stylingMode', 'tabIndex', 'type', 'useMaskBehavior', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width']
        self._type = 'DateBox'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'acceptCustomValue', 'accessKey', 'activeStateEnabled', 'adaptivityEnabled', 'applyButtonText', 'applyValueMode', 'buttons', 'calendarOptions', 'cancelButtonText', 'dateOutOfRangeMessage', 'dateSerializationFormat', 'deferRendering', 'disabled', 'disabledDates', 'displayFormat', 'dropDownButtonComponent', 'dropDownButtonRender', 'dropDownButtonTemplate', 'dropDownOptions', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'interval', 'invalidDateMessage', 'isValid', 'max', 'maxLength', 'min', 'name', 'opened', 'openOnFieldClick', 'pickerType', 'placeholder', 'readOnly', 'rtlEnabled', 'showAnalogClock', 'showClearButton', 'showDropDownButton', 'spellcheck', 'stylingMode', 'tabIndex', 'type', 'useMaskBehavior', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DateBox, self).__init__(**args)
