# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Popover(Component):
    """A Popover component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- animation (dict; default {show: {type: 'fade', from: 0, to: 1}, hide: {type: 'fade', to: 0}})
- closeOnBackButton (boolean; default True)
- closeOnOutsideClick (boolean; default True)
- container (string; optional)
- deferRendering (boolean; default True)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- height (number | string; default 'auto')
- hideEvent (dict | string; optional)
- hint (string; optional)
- hoverStateEnabled (boolean; default False)
- maxHeight (number | string; optional)
- maxWidth (number | string; optional)
- minHeight (number | string; optional)
- minWidth (number | string; optional)
- position (a value equal to: 'bottom', 'left', 'right', 'top' | dict; default 'bottom')
- rtlEnabled (boolean; default False)
- shading (boolean; default False)
- shadingColor (string; default '')
- showCloseButton (boolean; default False)
- showEvent (dict | string; optional)
- showTitle (boolean; default False)
- target (string; optional)
- title (string; default '')
- titleTemplate (string; default 'title')
- toolbarItems (list of dicts; optional)
- visible (boolean; default False)
- width (number | string; default 'auto')
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, animation=Component.UNDEFINED, closeOnBackButton=Component.UNDEFINED, closeOnOutsideClick=Component.UNDEFINED, container=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, height=Component.UNDEFINED, hideEvent=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, maxHeight=Component.UNDEFINED, maxWidth=Component.UNDEFINED, minHeight=Component.UNDEFINED, minWidth=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onHidden=Component.UNDEFINED, onHiding=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onShowing=Component.UNDEFINED, onShown=Component.UNDEFINED, position=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, shading=Component.UNDEFINED, shadingColor=Component.UNDEFINED, showCloseButton=Component.UNDEFINED, showEvent=Component.UNDEFINED, showTitle=Component.UNDEFINED, target=Component.UNDEFINED, title=Component.UNDEFINED, titleTemplate=Component.UNDEFINED, toolbarItems=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'animation', 'closeOnBackButton', 'closeOnOutsideClick', 'container', 'deferRendering', 'disabled', 'elementAttr', 'height', 'hideEvent', 'hint', 'hoverStateEnabled', 'maxHeight', 'maxWidth', 'minHeight', 'minWidth', 'position', 'rtlEnabled', 'shading', 'shadingColor', 'showCloseButton', 'showEvent', 'showTitle', 'target', 'title', 'titleTemplate', 'toolbarItems', 'visible', 'width', 'loading_state']
        self._type = 'Popover'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'animation', 'closeOnBackButton', 'closeOnOutsideClick', 'container', 'deferRendering', 'disabled', 'elementAttr', 'height', 'hideEvent', 'hint', 'hoverStateEnabled', 'maxHeight', 'maxWidth', 'minHeight', 'minWidth', 'position', 'rtlEnabled', 'shading', 'shadingColor', 'showCloseButton', 'showEvent', 'showTitle', 'target', 'title', 'titleTemplate', 'toolbarItems', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Popover, self).__init__(children=children, **args)
