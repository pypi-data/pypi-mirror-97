# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Accordion(Component):
    """An Accordion component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- animationDuration (number; default 300): A number specifying the time in milliseconds spent on the animation of the expanding or collapsing of a panel
- collapsible (boolean; default False): Specifies whether all items can be collapsed or whether at least one item must always be expanded
- dataSource (string | list of strings | list of dicts | dict; optional): Binds the UI component to data
- deferRendering (boolean; default True): Specifies whether to render the panel's content when it is displayed. If false, the content is rendered immediately
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
- keyExpr (string; optional): Specifies the key property that provides key values to access data items. Each key value must be unique.
- multiple (boolean; default False): Specifies whether the UI component can expand several items or only a single item at once
- noDataText (string; default 'No data to display'): The text or HTML markup displayed by the UI component if the item collection is empty
- onItemClick (string; optional): A function that is executed when a collection item is clicked or tapped
- repaintChangesOnly (boolean; default False): Specifies whether to repaint only those elements whose data changed
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- selectedIndex (number; default 0): The index number of the currently selected item
- selectedItem (dict; optional): The selected item object
- selectedItemKeys (list of boolean | number | string | dict | lists; optional): Specifies an array of currently selected item keys
- selectedItems (list of boolean | number | string | dict | lists; optional): An array of currently selected item objects
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; default 'auto'): Specifies the UI component's width"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, animationDuration=Component.UNDEFINED, collapsible=Component.UNDEFINED, dataSource=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, itemTitleComponent=Component.UNDEFINED, itemTitleRender=Component.UNDEFINED, itemTitleTemplate=Component.UNDEFINED, keyExpr=Component.UNDEFINED, multiple=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onItemTitleClick=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, selectedIndex=Component.UNDEFINED, selectedItem=Component.UNDEFINED, selectedItemKeys=Component.UNDEFINED, selectedItems=Component.UNDEFINED, tabIndex=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'animationDuration', 'collapsible', 'dataSource', 'deferRendering', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'itemTitleComponent', 'itemTitleRender', 'itemTitleTemplate', 'keyExpr', 'multiple', 'noDataText', 'onItemClick', 'repaintChangesOnly', 'rtlEnabled', 'selectedIndex', 'selectedItem', 'selectedItemKeys', 'selectedItems', 'tabIndex', 'visible', 'width']
        self._type = 'Accordion'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'animationDuration', 'collapsible', 'dataSource', 'deferRendering', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'itemTitleComponent', 'itemTitleRender', 'itemTitleTemplate', 'keyExpr', 'multiple', 'noDataText', 'onItemClick', 'repaintChangesOnly', 'rtlEnabled', 'selectedIndex', 'selectedItem', 'selectedItemKeys', 'selectedItems', 'tabIndex', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Accordion, self).__init__(**args)
