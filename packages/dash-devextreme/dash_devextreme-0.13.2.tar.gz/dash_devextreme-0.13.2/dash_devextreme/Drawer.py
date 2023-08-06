# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Drawer(Component):
    """A Drawer component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- animationDuration (number; default 400): Specifies the duration of the drawer's opening and closing animation (in milliseconds)
- animationEnabled (boolean; default True): Specifies whether to use an opening and closing animation
- closeOnOutsideClick (boolean; default False): Specifies whether to close the drawer if a user clicks or taps the view area
- itemComponent (string | dict; optional): An alias for the template property specified in React. Accepts a custom component.
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- height (number | string; optional): Specifies the view's height
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default False): Specifies whether the UI component changes its state when a user pauses on it
- maxSize (number; optional): Specifies the drawer's width or height (depending on the drawer's position) in the opened state
- minSize (number; optional): Specifies the drawer's width or height (depending on the drawer's position) in the closed state
- opened (boolean; default False): Specifies whether the drawer is opened
- openedStateMode (a value equal to: 'overlap', 'shrink', 'push'; default 'overlap'): Specifies how the drawer interacts with the view in the opened state
- position (a value equal to: 'left', 'right', 'top', 'bottom', 'before', 'after'; default 'left'): Specifies the drawer's position in relation to the view
- itemRender (string; optional): An alias for the template property specified in React. Accepts a rendering function.
- revealMode (a value equal to: 'slide', 'expand'; default 'slide'): Specifies the drawer's reveal mode
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- shading (boolean; default False): Specifies whether to shade the view when the drawer is opened
- target (string; optional): Specifies a CSS selector for the element in which the drawer should be rendered. Applies only when the openedStateMode is "overlap"
- itemTemplate (string; default 'panel'): Specifies the drawer's content
- visible (boolean; default True): Specifies whether the Drawer UI component (including the view) is visible
- width (number | string; optional): Specifies the view's width"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, animationDuration=Component.UNDEFINED, animationEnabled=Component.UNDEFINED, closeOnOutsideClick=Component.UNDEFINED, itemComponent=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, maxSize=Component.UNDEFINED, minSize=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, opened=Component.UNDEFINED, openedStateMode=Component.UNDEFINED, position=Component.UNDEFINED, itemRender=Component.UNDEFINED, revealMode=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, shading=Component.UNDEFINED, target=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'activeStateEnabled', 'animationDuration', 'animationEnabled', 'closeOnOutsideClick', 'itemComponent', 'disabled', 'elementAttr', 'height', 'hint', 'hoverStateEnabled', 'maxSize', 'minSize', 'opened', 'openedStateMode', 'position', 'itemRender', 'revealMode', 'rtlEnabled', 'shading', 'target', 'itemTemplate', 'visible', 'width']
        self._type = 'Drawer'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'activeStateEnabled', 'animationDuration', 'animationEnabled', 'closeOnOutsideClick', 'itemComponent', 'disabled', 'elementAttr', 'height', 'hint', 'hoverStateEnabled', 'maxSize', 'minSize', 'opened', 'openedStateMode', 'position', 'itemRender', 'revealMode', 'rtlEnabled', 'shading', 'target', 'itemTemplate', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Drawer, self).__init__(children=children, **args)
