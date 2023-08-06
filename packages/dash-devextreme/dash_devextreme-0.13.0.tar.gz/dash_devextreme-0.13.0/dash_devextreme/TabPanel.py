# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TabPanel(Component):
    """A TabPanel component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- animationEnabled (boolean; default True): Specifies whether or not to animate the displayed item change
- dataSource (string | list of strings | list of dicts | dict; optional): Binds the UI component to data
- deferRendering (boolean; default True): Specifies whether to render the view's content when it is displayed. If false, the content is rendered immediately
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- focusStateEnabled (boolean; default False): Specifies whether the UI component can be focused using keyboard navigation
- height (number | string; default 'auto'): Specifies the UI component's height
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default True): Specifies whether the UI component changes its state when a user pauses on it
- itemComponent (string | dict; optional): An alias for the itemTemplate property specified in React. Accepts a custom component.
- itemHoldTimeout (number; default 750): The time period in milliseconds before the onItemHold event is raised
- itemRender (string; optional): An alias for the itemTemplate property specified in React. Accepts a rendering function.
- items (list of strings | list of dicts; default undefined): An array of items displayed by the UI component
- itemTemplate (string | dict; default 'item'): Specifies a custom template for items
- itemTitleComponent (string | dict; optional): An alias for the itemTitleTemplate property specified in React. Accepts a custom component.
- itemTitleRender (string; optional): An alias for the itemTitleTemplate property specified in React. Accepts a rendering function.
- itemTitleTemplate (string | dict; default 'title'): Specifies a custom template for item titles
- loop (boolean; default False): A Boolean value specifying whether or not to scroll back to the first item after the last item is swiped
- noDataText (string; default 'No data to display'): The text or HTML markup displayed by the UI component if the item collection is empty
- onItemClick (string; optional): A function that is executed when a collection item is clicked or tapped
- onTitleClick (string; optional): A function that is executed when a tab is clicked or tapped
- repaintChangesOnly (boolean; default False): Specifies whether to repaint only those elements whose data changed
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- scrollByContent (boolean; default True): A Boolean value specifying if tabs in the title are scrolled by content
- scrollingEnabled (boolean; default True): A Boolean indicating whether or not to add scrolling support for tabs in the title
- selectedIndex (number; default 0): The index of the currently displayed item
- selectedItem (dict; optional): The selected item object
- showNavButtons (boolean; default False): Specifies whether navigation buttons should be available when tabs exceed the UI component's width
- swipeEnabled (boolean; default True): A Boolean value specifying whether or not to allow users to change the selected index by swiping
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; default 'auto'): Specifies the UI component's width
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, animationEnabled=Component.UNDEFINED, dataSource=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, itemTitleComponent=Component.UNDEFINED, itemTitleRender=Component.UNDEFINED, itemTitleTemplate=Component.UNDEFINED, loop=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onTitleClick=Component.UNDEFINED, onTitleHold=Component.UNDEFINED, onTitleRendered=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollByContent=Component.UNDEFINED, scrollingEnabled=Component.UNDEFINED, selectedIndex=Component.UNDEFINED, selectedItem=Component.UNDEFINED, showNavButtons=Component.UNDEFINED, swipeEnabled=Component.UNDEFINED, tabIndex=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'animationEnabled', 'dataSource', 'deferRendering', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'itemTitleComponent', 'itemTitleRender', 'itemTitleTemplate', 'loop', 'noDataText', 'onItemClick', 'onTitleClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'showNavButtons', 'swipeEnabled', 'tabIndex', 'visible', 'width', 'loading_state']
        self._type = 'TabPanel'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'animationEnabled', 'dataSource', 'deferRendering', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'itemTitleComponent', 'itemTitleRender', 'itemTitleTemplate', 'loop', 'noDataText', 'onItemClick', 'onTitleClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'showNavButtons', 'swipeEnabled', 'tabIndex', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TabPanel, self).__init__(**args)
