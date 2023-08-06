# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional)
- activeStateEnabled (boolean; default True)
- component (string; optional)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; default True)
- height (number | string; default 'auto')
- hint (string; optional)
- hoverStateEnabled (boolean; default True)
- icon (string; default '')
- render (string; optional)
- rtlEnabled (boolean; default False)
- stylingMode (a value equal to: 'text', 'outlined', 'contained'; default 'contained')
- tabIndex (number; default 0)
- template (a value equal to: 'content', 'icon', 'text'; default 'content')
- text (string; default '')
- type (a value equal to: 'back', 'danger', 'default', 'normal', 'success'; default 'normal')
- useSubmitBehavior (boolean; default False)
- validationGroup (string; optional)
- visible (boolean; default True)
- width (number | string; default 'inherit')
- n_clicks (number; default 0)
- n_clicks_timestamp (number; default -1)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, component=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, icon=Component.UNDEFINED, onClick=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, render=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, template=Component.UNDEFINED, text=Component.UNDEFINED, type=Component.UNDEFINED, useSubmitBehavior=Component.UNDEFINED, validationGroup=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'component', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'icon', 'render', 'rtlEnabled', 'stylingMode', 'tabIndex', 'template', 'text', 'type', 'useSubmitBehavior', 'validationGroup', 'visible', 'width', 'n_clicks', 'n_clicks_timestamp', 'loading_state']
        self._type = 'Button'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'component', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'icon', 'render', 'rtlEnabled', 'stylingMode', 'tabIndex', 'template', 'text', 'type', 'useSubmitBehavior', 'validationGroup', 'visible', 'width', 'n_clicks', 'n_clicks_timestamp', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Button, self).__init__(**args)
