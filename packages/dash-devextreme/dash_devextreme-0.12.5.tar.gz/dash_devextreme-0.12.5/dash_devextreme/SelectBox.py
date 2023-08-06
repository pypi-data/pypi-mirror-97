# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SelectBox(Component):
    """A SelectBox component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- acceptCustomValue (boolean; default False)
- accessKey (string; optional)
- activeStateEnabled (boolean; default True)
- dataSource (string | dict | list of boolean | number | string | dict | lists; optional)
- deferRendering (boolean; default True)
- disabled (boolean; default False)
- displayExpr (string; optional)
- dropDownButtonTemplate (string; default 'dropDownButton')
- elementAttr (dict; optional)
- fieldTemplate (string; optional)
- focusStateEnabled (boolean; default True)
- grouped (boolean; default False)
- groupTemplate (string; default 'group')
- height (number | string; optional)
- hint (string; optional)
- hoverStateEnabled (boolean; default True)
- inputAttr (dict; optional)
- isValid (boolean; default True)
- items (list of boolean | number | string | dict | lists; optional)
- itemTemplate (string; default 'item')
- maxLength (string | number; optional)
- minSearchLength (number; default 0)
- name (string; default '')
- noDataText (string; default 'No data to display')
- opened (boolean; default False)
- openOnFieldClick (boolean; default True)
- placeholder (string; default 'Select')
- readOnly (boolean; default False)
- rtlEnabled (boolean; default False)
- searchEnabled (boolean; default False)
- searchExpr (string | list of strings; optional)
- searchMode (a value equal to: 'contains', 'startswith'; default 'contains')
- searchTimeout (number; default 500)
- showClearButton (boolean; default False)
- showDataBeforeSearch (boolean; default False)
- showDropDownButton (boolean; default True)
- showSelectionControls (boolean; default False)
- spellcheck (boolean; default False)
- stylingMode (a value equal to: 'outlined', 'underlined', 'filled'; default 'outlined')
- tabIndex (number; default 0)
- validationError (dict; optional)
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto')
- value (boolean | number | string | dict | list; optional)
- valueChangeEvent (string; default 'change')
- valueExpr (string; default 'this')
- visible (boolean; default True)
- width (number | string; optional)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, acceptCustomValue=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, dataSource=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, displayExpr=Component.UNDEFINED, dropDownButtonTemplate=Component.UNDEFINED, elementAttr=Component.UNDEFINED, fieldTemplate=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, grouped=Component.UNDEFINED, groupTemplate=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, isValid=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, maxLength=Component.UNDEFINED, minSearchLength=Component.UNDEFINED, name=Component.UNDEFINED, noDataText=Component.UNDEFINED, onChange=Component.UNDEFINED, onClosed=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onCopy=Component.UNDEFINED, onCustomItemCreating=Component.UNDEFINED, onCut=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEnterKey=Component.UNDEFINED, onFocusIn=Component.UNDEFINED, onFocusOut=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInput=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onKeyPress=Component.UNDEFINED, onKeyUp=Component.UNDEFINED, onOpened=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPaste=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, opened=Component.UNDEFINED, openOnFieldClick=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, searchEnabled=Component.UNDEFINED, searchExpr=Component.UNDEFINED, searchMode=Component.UNDEFINED, searchTimeout=Component.UNDEFINED, showClearButton=Component.UNDEFINED, showDataBeforeSearch=Component.UNDEFINED, showDropDownButton=Component.UNDEFINED, showSelectionControls=Component.UNDEFINED, spellcheck=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, validationError=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, value=Component.UNDEFINED, valueChangeEvent=Component.UNDEFINED, valueExpr=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'acceptCustomValue', 'accessKey', 'activeStateEnabled', 'dataSource', 'deferRendering', 'disabled', 'displayExpr', 'dropDownButtonTemplate', 'elementAttr', 'fieldTemplate', 'focusStateEnabled', 'grouped', 'groupTemplate', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'items', 'itemTemplate', 'maxLength', 'minSearchLength', 'name', 'noDataText', 'opened', 'openOnFieldClick', 'placeholder', 'readOnly', 'rtlEnabled', 'searchEnabled', 'searchExpr', 'searchMode', 'searchTimeout', 'showClearButton', 'showDataBeforeSearch', 'showDropDownButton', 'showSelectionControls', 'spellcheck', 'stylingMode', 'tabIndex', 'validationError', 'validationMessageMode', 'value', 'valueChangeEvent', 'valueExpr', 'visible', 'width', 'loading_state']
        self._type = 'SelectBox'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'acceptCustomValue', 'accessKey', 'activeStateEnabled', 'dataSource', 'deferRendering', 'disabled', 'displayExpr', 'dropDownButtonTemplate', 'elementAttr', 'fieldTemplate', 'focusStateEnabled', 'grouped', 'groupTemplate', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'items', 'itemTemplate', 'maxLength', 'minSearchLength', 'name', 'noDataText', 'opened', 'openOnFieldClick', 'placeholder', 'readOnly', 'rtlEnabled', 'searchEnabled', 'searchExpr', 'searchMode', 'searchTimeout', 'showClearButton', 'showDataBeforeSearch', 'showDropDownButton', 'showSelectionControls', 'spellcheck', 'stylingMode', 'tabIndex', 'validationError', 'validationMessageMode', 'value', 'valueChangeEvent', 'valueExpr', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SelectBox, self).__init__(**args)
