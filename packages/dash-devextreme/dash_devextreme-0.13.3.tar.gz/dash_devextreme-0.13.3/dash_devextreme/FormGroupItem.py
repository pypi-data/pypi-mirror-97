# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormGroupItem(Component):
    """A FormGroupItem component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- alignItemLabels (boolean; default True): Specifies whether or not all group item labels are aligned
- caption (string; optional): Specifies the group caption
- colCount (number; default 1): The count of columns in the group layout
- colCountByScreen (dict; optional): Specifies the relation between the screen size qualifier and the number of columns in the grouped layout
- colSpan (number; optional): Specifies the number of columns spanned by the item
- component (dict; optional): An alias for the template property specified in React. Accepts a custom component.
- cssClass (string; optional): Specifies a CSS class to be applied to the form item
- items (list of dicts; optional): Holds an array of form items displayed within the group
- itemType (a value equal to: 'empty', 'group', 'simple', 'tabbed', 'button'; default 'simple'): Specifies the item's type. Set it to "group" to create a group item.
- name (string; optional): Specifies a name that identifies the form item
- template (string | dict; optional): A template that can be used to replace the default editor with custom content
- visible (boolean; default True): Specifies whether or not the current form item is visible
- visibleIndex (number; optional): Specifies the sequence number of the item in a form, group or tab
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, alignItemLabels=Component.UNDEFINED, caption=Component.UNDEFINED, colCount=Component.UNDEFINED, colCountByScreen=Component.UNDEFINED, colSpan=Component.UNDEFINED, component=Component.UNDEFINED, cssClass=Component.UNDEFINED, items=Component.UNDEFINED, itemType=Component.UNDEFINED, name=Component.UNDEFINED, render=Component.UNDEFINED, template=Component.UNDEFINED, visible=Component.UNDEFINED, visibleIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'alignItemLabels', 'caption', 'colCount', 'colCountByScreen', 'colSpan', 'component', 'cssClass', 'items', 'itemType', 'name', 'template', 'visible', 'visibleIndex', 'loading_state']
        self._type = 'FormGroupItem'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'alignItemLabels', 'caption', 'colCount', 'colCountByScreen', 'colSpan', 'component', 'cssClass', 'items', 'itemType', 'name', 'template', 'visible', 'visibleIndex', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormGroupItem, self).__init__(children=children, **args)
