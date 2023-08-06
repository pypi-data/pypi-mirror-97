# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Popup(Component):
    """A Popup component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): A collection of an node's child elements
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- animation (dict; optional): Configures UI component visibility animations. This object contains two fields: show and hide.
- closeOnOutsideClick (boolean; default False): Specifies whether to close the UI component if a user clicks outside it
- container (string; optional): Specifies the container in which to render the UI component
- contentComponent (string | dict; optional): An alias for the contentTemplate property specified in React. Accepts a custom component
- contentRender (string; optional): An alias for the contentTemplate property specified in React. Accepts a rendering function.
- contentTemplate (string | dict; optional): Specifies a custom template for the UI component content
- deferRendering (boolean; default True): Specifies whether to render the UI component's content when it is displayed. If false, the content is rendered immediately.
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- dragEnabled (boolean; default False): Specifies whether or not to allow a user to drag the popup window
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- focusStateEnabled (boolean; default True): Specifies whether the UI component can be focused using keyboard navigation
- fullScreen (boolean; default False): Specifies whether to display the Popup in full-screen mode
- height (number | string; default 'auto'): Specifies the UI component's height in pixels
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default False): Specifies whether the UI component changes its state when a user pauses on it
- maxHeight (number | string; optional): Specifies the maximum height the UI component can reach while resizing
- maxWidth (number | string; optional): Specifies the maximum width the UI component can reach while resizing
- minHeight (number | string; optional): Specifies the minimum height the UI component can reach while resizing
- minWidth (number | string; optional): Specifies the minimum width the UI component can reach while resizing
- position (a value equal to: 'bottom', 'center', 'left', 'left bottom', 'left top', 'right', 'right bottom', 'right top', 'top' | dict; optional): Positions the UI component
- resizeEnabled (boolean; default False): Specifies whether or not an end user can resize the UI component
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- shading (boolean; default True): Specifies whether to shade the background when the UI component is active
- shadingColor (string; default ''): Specifies the shading color. Applies only if shading is enabled
- showCloseButton (boolean; default False): Specifies whether or not the UI component displays the Close button
- showTitle (boolean; default True): A Boolean value specifying whether or not to display the title in the popup window
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- title (string; default ''): The title in the overlay window
- titleComponent (string | dict; optional): An alias for the titleTemplate property specified in React. Accepts a custom component.
- titleRender (string; optional): An alias for the titleTemplate property specified in React. Accepts a rendering function.
- titleTemplate (string | dict; default 'title'): Specifies a custom template for the UI component title. Does not apply if the title is defined.
- toolbarItems (list of dicts; optional): Configures toolbar items
- visible (boolean; default False): A Boolean value specifying whether or not the UI component is visible
- width (number | string; default 'auto'): Specifies the UI component's width in pixels
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, animation=Component.UNDEFINED, closeOnOutsideClick=Component.UNDEFINED, container=Component.UNDEFINED, contentComponent=Component.UNDEFINED, contentRender=Component.UNDEFINED, contentTemplate=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, dragEnabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, fullScreen=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, maxHeight=Component.UNDEFINED, maxWidth=Component.UNDEFINED, minHeight=Component.UNDEFINED, minWidth=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onHidden=Component.UNDEFINED, onHiding=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onResize=Component.UNDEFINED, onResizeEnd=Component.UNDEFINED, onResizeStart=Component.UNDEFINED, onShowing=Component.UNDEFINED, onShown=Component.UNDEFINED, onTitleRendered=Component.UNDEFINED, position=Component.UNDEFINED, resizeEnabled=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, shading=Component.UNDEFINED, shadingColor=Component.UNDEFINED, showCloseButton=Component.UNDEFINED, showTitle=Component.UNDEFINED, tabIndex=Component.UNDEFINED, title=Component.UNDEFINED, titleComponent=Component.UNDEFINED, titleRender=Component.UNDEFINED, titleTemplate=Component.UNDEFINED, toolbarItems=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accessKey', 'animation', 'closeOnOutsideClick', 'container', 'contentComponent', 'contentRender', 'contentTemplate', 'deferRendering', 'disabled', 'dragEnabled', 'elementAttr', 'focusStateEnabled', 'fullScreen', 'height', 'hint', 'hoverStateEnabled', 'maxHeight', 'maxWidth', 'minHeight', 'minWidth', 'position', 'resizeEnabled', 'rtlEnabled', 'shading', 'shadingColor', 'showCloseButton', 'showTitle', 'tabIndex', 'title', 'titleComponent', 'titleRender', 'titleTemplate', 'toolbarItems', 'visible', 'width', 'loading_state']
        self._type = 'Popup'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'accessKey', 'animation', 'closeOnOutsideClick', 'container', 'contentComponent', 'contentRender', 'contentTemplate', 'deferRendering', 'disabled', 'dragEnabled', 'elementAttr', 'focusStateEnabled', 'fullScreen', 'height', 'hint', 'hoverStateEnabled', 'maxHeight', 'maxWidth', 'minHeight', 'minWidth', 'position', 'resizeEnabled', 'rtlEnabled', 'shading', 'shadingColor', 'showCloseButton', 'showTitle', 'tabIndex', 'title', 'titleComponent', 'titleRender', 'titleTemplate', 'toolbarItems', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Popup, self).__init__(children=children, **args)
