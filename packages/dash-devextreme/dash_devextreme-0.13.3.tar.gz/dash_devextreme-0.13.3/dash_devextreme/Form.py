# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Form(Component):
    """A Form component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- alignItemLabels (boolean; default True): Specifies whether or not all root item labels are aligned
- alignItemLabelsInAllGroups (boolean; default True): Specifies whether or not item labels in all groups are aligned
- colCount (number | string; default 1): The count of columns in the form layout
- colCountByScreen (dict; optional): Specifies dependency between the screen factor and the count of columns in the form layout
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- focusStateEnabled (boolean; default False): Specifies whether the UI component can be focused using keyboard navigation
- formData (dict; optional): Provides the Form's data. Gets updated every time form fields change
- height (number | string; default 'auto'): Specifies the UI component's height
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default False): Specifies whether the UI component changes its state when a user pauses on it
- items (list of dicts; optional): Holds an array of form items
- labelLocation (a value equal to: 'left', 'right', 'top'; default 'left'): Specifies the location of a label against the editor
- minColWidth (number; default 200): The minimum column width used for calculating column count in the form layout
- optionalMark (string; default 'optional'): The text displayed for optional fields
- readOnly (boolean; default False): Specifies whether all editors on the form are read-only. Applies only to non-templated items
- requiredMark (string; default '*'): The text displayed for required fields
- requiredMessage (string; default '{0} is required'): Specifies the message that is shown for end-users if a required field value is not specified
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- scrollingEnabled (boolean; default False): A Boolean value specifying whether to enable or disable form scrolling
- showColonAfterLabel (boolean; default True): Specifies whether or not a colon is displayed at the end of form labels
- showOptionalMark (boolean; default False): Specifies whether or not the optional mark is displayed for optional fields
- showRequiredMark (boolean; default True): Specifies whether or not the required mark is displayed for required fields
- showValidationSummary (boolean; default False): Specifies whether or not the total validation summary is displayed on the form
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- validationGroup (string; optional): Gives a name to the internal validation group
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; default 'auto'): Specifies the UI component's width
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, alignItemLabels=Component.UNDEFINED, alignItemLabelsInAllGroups=Component.UNDEFINED, colCount=Component.UNDEFINED, colCountByScreen=Component.UNDEFINED, customizeItem=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, formData=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, items=Component.UNDEFINED, labelLocation=Component.UNDEFINED, minColWidth=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEditorEnterKey=Component.UNDEFINED, onFieldDataChanged=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, optionalMark=Component.UNDEFINED, readOnly=Component.UNDEFINED, requiredMark=Component.UNDEFINED, requiredMessage=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, screenByWidth=Component.UNDEFINED, scrollingEnabled=Component.UNDEFINED, showColonAfterLabel=Component.UNDEFINED, showOptionalMark=Component.UNDEFINED, showRequiredMark=Component.UNDEFINED, showValidationSummary=Component.UNDEFINED, tabIndex=Component.UNDEFINED, validationGroup=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accessKey', 'activeStateEnabled', 'alignItemLabels', 'alignItemLabelsInAllGroups', 'colCount', 'colCountByScreen', 'disabled', 'elementAttr', 'focusStateEnabled', 'formData', 'height', 'hint', 'hoverStateEnabled', 'items', 'labelLocation', 'minColWidth', 'optionalMark', 'readOnly', 'requiredMark', 'requiredMessage', 'rtlEnabled', 'scrollingEnabled', 'showColonAfterLabel', 'showOptionalMark', 'showRequiredMark', 'showValidationSummary', 'tabIndex', 'validationGroup', 'visible', 'width', 'loading_state']
        self._type = 'Form'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'accessKey', 'activeStateEnabled', 'alignItemLabels', 'alignItemLabelsInAllGroups', 'colCount', 'colCountByScreen', 'disabled', 'elementAttr', 'focusStateEnabled', 'formData', 'height', 'hint', 'hoverStateEnabled', 'items', 'labelLocation', 'minColWidth', 'optionalMark', 'readOnly', 'requiredMark', 'requiredMessage', 'rtlEnabled', 'scrollingEnabled', 'showColonAfterLabel', 'showOptionalMark', 'showRequiredMark', 'showValidationSummary', 'tabIndex', 'validationGroup', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Form, self).__init__(children=children, **args)
