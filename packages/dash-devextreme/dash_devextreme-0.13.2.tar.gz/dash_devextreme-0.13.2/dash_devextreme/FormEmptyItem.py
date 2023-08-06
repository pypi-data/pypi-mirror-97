# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormEmptyItem(Component):
    """A FormEmptyItem component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- colSpan (number; optional): Specifies the number of columns spanned by the item
- cssClass (string; optional): Specifies a CSS class to be applied to the form item
- itemType (a value equal to: 'empty', 'group', 'simple', 'tabbed', 'button'; default 'simple'): Specifies the item's type. Set it to "simple" to create a simple item
- name (string; optional): Specifies a name that identifies the form item
- visible (boolean; default True): Specifies whether or not the current form item is visible
- visibleIndex (number; optional): Specifies the sequence number of the item in a form, group or tab
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, colSpan=Component.UNDEFINED, cssClass=Component.UNDEFINED, itemType=Component.UNDEFINED, name=Component.UNDEFINED, visible=Component.UNDEFINED, visibleIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'colSpan', 'cssClass', 'itemType', 'name', 'visible', 'visibleIndex', 'loading_state']
        self._type = 'FormEmptyItem'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'colSpan', 'cssClass', 'itemType', 'name', 'visible', 'visibleIndex', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormEmptyItem, self).__init__(**args)
