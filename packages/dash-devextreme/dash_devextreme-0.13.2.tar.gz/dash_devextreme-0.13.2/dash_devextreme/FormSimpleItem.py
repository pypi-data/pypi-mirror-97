# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormSimpleItem(Component):
    """A FormSimpleItem component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- buttonOptions (dict; optional)
- colSpan (number; optional): Specifies the number of columns spanned by the item
- component (dict; optional): An alias for the template property specified in React. Accepts a custom component.
- cssClass (string; optional): Specifies a CSS class to be applied to the form item
- dataField (string; optional): Specifies the path to the formData object field bound to the current form item
- editorOptions (dict; optional): Configures the form item's editor
- editorType (a value equal to: 'dxAutocomplete', 'dxCalendar', 'dxCheckBox', 'dxColorBox', 'dxDateBox', 'dxDropDownBox', 'dxHtmlEditor', 'dxLookup', 'dxNumberBox', 'dxRadioGroup', 'dxRangeSlider', 'dxSelectBox', 'dxSlider', 'dxSwitch', 'dxTagBox', 'dxTextArea', 'dxTextBox'; optional): Specifies which editor UI component is used to display and edit the form item value
- helpText (string; optional): Specifies the help text displayed for the current form item
- isRequired (boolean; optional): Specifies whether the current form item is required
- itemType (a value equal to: 'empty', 'group', 'simple', 'tabbed', 'button'; default 'simple'): Specifies the item's type. Set it to "simple" to create a simple item
- label (dict; optional): Specifies properties for the form item label
- name (string; optional): Specifies a name that identifies the form item
- template (string | dict; optional): A template that can be used to replace the default editor with custom content
- validationRules (list of dicts; optional): An array of validation rules to be checked for the form item editor
- visible (boolean; default True): Specifies whether or not the current form item is visible
- visibleIndex (number; optional): Specifies the sequence number of the item in a form, group or tab
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, buttonOptions=Component.UNDEFINED, colSpan=Component.UNDEFINED, component=Component.UNDEFINED, cssClass=Component.UNDEFINED, dataField=Component.UNDEFINED, editorOptions=Component.UNDEFINED, editorType=Component.UNDEFINED, helpText=Component.UNDEFINED, isRequired=Component.UNDEFINED, itemType=Component.UNDEFINED, label=Component.UNDEFINED, name=Component.UNDEFINED, render=Component.UNDEFINED, template=Component.UNDEFINED, validationRules=Component.UNDEFINED, visible=Component.UNDEFINED, visibleIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttonOptions', 'colSpan', 'component', 'cssClass', 'dataField', 'editorOptions', 'editorType', 'helpText', 'isRequired', 'itemType', 'label', 'name', 'template', 'validationRules', 'visible', 'visibleIndex', 'loading_state']
        self._type = 'FormSimpleItem'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttonOptions', 'colSpan', 'component', 'cssClass', 'dataField', 'editorOptions', 'editorType', 'helpText', 'isRequired', 'itemType', 'label', 'name', 'template', 'validationRules', 'visible', 'visibleIndex', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormSimpleItem, self).__init__(**args)
