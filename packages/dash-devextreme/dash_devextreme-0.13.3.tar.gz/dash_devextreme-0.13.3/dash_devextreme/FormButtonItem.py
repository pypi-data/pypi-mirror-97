# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormButtonItem(Component):
    """A FormButtonItem component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- buttonOptions (dict; optional): Configures the button
- colSpan (number; optional): Specifies how many columns the item spans
- cssClass (string; optional): Specifies a CSS class to be applied to the item
- horizontalAlignment (a value equal to: 'center', 'left', 'right'; default 'right'): Specifies the button's horizontal alignment
- itemType (a value equal to: 'empty', 'group', 'simple', 'tabbed', 'button'; default 'simple'): Specifies the item's type. Set it to "button" to create a button item.
- name (string; optional): Specifies a name that identifies the form item
- verticalAlignment (a value equal to: 'bottom', 'center', 'top'; default 'top'): Specifies the button's vertical alignment
- visible (boolean; default True): Specifies whether the item is visible
- visibleIndex (number; optional): Specifies the sequence number of the item in a form, group or tab
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, buttonOptions=Component.UNDEFINED, colSpan=Component.UNDEFINED, cssClass=Component.UNDEFINED, horizontalAlignment=Component.UNDEFINED, itemType=Component.UNDEFINED, name=Component.UNDEFINED, verticalAlignment=Component.UNDEFINED, visible=Component.UNDEFINED, visibleIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttonOptions', 'colSpan', 'cssClass', 'horizontalAlignment', 'itemType', 'name', 'verticalAlignment', 'visible', 'visibleIndex', 'loading_state']
        self._type = 'FormButtonItem'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttonOptions', 'colSpan', 'cssClass', 'horizontalAlignment', 'itemType', 'name', 'verticalAlignment', 'visible', 'visibleIndex', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormButtonItem, self).__init__(**args)
