# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LoadPanel(Component):
    """A LoadPanel component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- animation (dict; default {show: {type: 'fade', from: 0, to: 1}, hide: {type: 'fade', to: 0}})
- closeOnOutsideClick (boolean; default True)
- container (string; optional)
- deferRendering (boolean; default True)
- delay (number; default 0)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; default False)
- height (number | string; default 90)
- hint (string; optional)
- hoverStateEnabled (boolean; default False)
- indicatorSrc (string; default '')
- maxHeight (number | string; optional)
- maxWidth (number | string; optional)
- message (string; default 'Loading...')
- minHeight (number | string; optional)
- minWidth (number | string; optional)
- position (a value equal to: 'bottom', 'center', 'left', 'left bottom', 'left top', 'right', 'right bottom', 'right top', 'top' | dict; default {my: 'center', at: 'center', of: window})
- rtlEnabled (boolean; default False)
- shading (boolean; default True)
- shadingColor (string; default 'transparent')
- showIndicator (boolean; default True)
- showPane (boolean; default True)
- visible (boolean; default False)
- width (number | string; default 222)
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, animation=Component.UNDEFINED, closeOnOutsideClick=Component.UNDEFINED, container=Component.UNDEFINED, deferRendering=Component.UNDEFINED, delay=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, indicatorSrc=Component.UNDEFINED, maxHeight=Component.UNDEFINED, maxWidth=Component.UNDEFINED, message=Component.UNDEFINED, minHeight=Component.UNDEFINED, minWidth=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onHidden=Component.UNDEFINED, onHiding=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onShowing=Component.UNDEFINED, onShown=Component.UNDEFINED, position=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, shading=Component.UNDEFINED, shadingColor=Component.UNDEFINED, showIndicator=Component.UNDEFINED, showPane=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'animation', 'closeOnOutsideClick', 'container', 'deferRendering', 'delay', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'indicatorSrc', 'maxHeight', 'maxWidth', 'message', 'minHeight', 'minWidth', 'position', 'rtlEnabled', 'shading', 'shadingColor', 'showIndicator', 'showPane', 'visible', 'width', 'loading_state']
        self._type = 'LoadPanel'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'animation', 'closeOnOutsideClick', 'container', 'deferRendering', 'delay', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'indicatorSrc', 'maxHeight', 'maxWidth', 'message', 'minHeight', 'minWidth', 'position', 'rtlEnabled', 'shading', 'shadingColor', 'showIndicator', 'showPane', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(LoadPanel, self).__init__(**args)
