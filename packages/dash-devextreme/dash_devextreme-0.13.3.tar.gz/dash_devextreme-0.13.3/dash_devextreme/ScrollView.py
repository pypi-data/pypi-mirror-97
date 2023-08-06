# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ScrollView(Component):
    """A ScrollView component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- bounceEnabled (boolean; default False)
- direction (a value equal to: 'both', 'horizontal', 'vertical'; default 'vertical')
- disabled (boolean; default False)
- elementAttr (dict; optional)
- height (number | string; optional)
- pulledDownText (string; default 'Pull down to refresh...')
- reachBottomText (string; default 'Loading...')
- refreshingText (string; default 'Refreshing...')
- rtlEnabled (boolean; default False)
- scrollByContent (boolean; default False)
- scrollByThumb (boolean; default True)
- showScrollbar (a value equal to: 'onScroll', 'onHover', 'always', 'never'; default 'onHover')
- useNative (boolean; default False)
- width (number | string; optional)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, bounceEnabled=Component.UNDEFINED, direction=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, height=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPullDown=Component.UNDEFINED, onReachBottom=Component.UNDEFINED, onScroll=Component.UNDEFINED, onUpdated=Component.UNDEFINED, pulledDownText=Component.UNDEFINED, reachBottomText=Component.UNDEFINED, refreshingText=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollByContent=Component.UNDEFINED, scrollByThumb=Component.UNDEFINED, showScrollbar=Component.UNDEFINED, useNative=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'bounceEnabled', 'direction', 'disabled', 'elementAttr', 'height', 'pulledDownText', 'reachBottomText', 'refreshingText', 'rtlEnabled', 'scrollByContent', 'scrollByThumb', 'showScrollbar', 'useNative', 'width', 'loading_state']
        self._type = 'ScrollView'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'bounceEnabled', 'direction', 'disabled', 'elementAttr', 'height', 'pulledDownText', 'reachBottomText', 'refreshingText', 'rtlEnabled', 'scrollByContent', 'scrollByThumb', 'showScrollbar', 'useNative', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ScrollView, self).__init__(children=children, **args)
