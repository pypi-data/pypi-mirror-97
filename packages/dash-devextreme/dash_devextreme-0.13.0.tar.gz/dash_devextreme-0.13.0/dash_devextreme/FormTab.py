# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FormTab(Component):
    """A FormTab component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- alignItemLabels (boolean; default True): Specifies whether or not labels of items displayed within the current tab are aligned
- badge (string; optional): Specifies a badge text for the tab
- colCount (number; default 1): The count of columns in the tab layout
- colCountByScreen (dict; optional): Specifies the relation between the screen size qualifier and the number of columns in the tabbed layout
- component (string | dict; optional): An alias for the template property specified in React. Accepts a custom component.
- disabled (boolean; default False): Specifies whether the tab responds to user interaction
- icon (string; optional): Specifies the icon to be displayed on the tab
- items (list of dicts; optional): Holds an array of form items displayed within the tab
- render (string; optional): An alias for the template property specified in React. Accepts a rendering function.
- tabComponent (string | dict; optional): An alias for the tabTemplate property specified in React. Accepts a custom component.
- tabRender (string; optional): An alias for the tabTemplate property specified in React. Accepts a rendering function.
- tabTemplate (string | dict; optional): The template to be used for rendering the tab
- template (string | dict; optional): The template to be used for rendering the tab content
- title (string; optional): Specifies the tab title
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, alignItemLabels=Component.UNDEFINED, badge=Component.UNDEFINED, colCount=Component.UNDEFINED, colCountByScreen=Component.UNDEFINED, component=Component.UNDEFINED, disabled=Component.UNDEFINED, icon=Component.UNDEFINED, items=Component.UNDEFINED, render=Component.UNDEFINED, tabComponent=Component.UNDEFINED, tabRender=Component.UNDEFINED, tabTemplate=Component.UNDEFINED, template=Component.UNDEFINED, title=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'alignItemLabels', 'badge', 'colCount', 'colCountByScreen', 'component', 'disabled', 'icon', 'items', 'render', 'tabComponent', 'tabRender', 'tabTemplate', 'template', 'title', 'loading_state']
        self._type = 'FormTab'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'alignItemLabels', 'badge', 'colCount', 'colCountByScreen', 'component', 'disabled', 'icon', 'items', 'render', 'tabComponent', 'tabRender', 'tabTemplate', 'template', 'title', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FormTab, self).__init__(children=children, **args)
