# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class List(Component):
    """A List component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default True): Specifies whether or not the UI component changes its state when interacting with a user
- allowItemDeleting (boolean; default False): Specifies whether or not an end user can delete list items
- bounceEnabled (boolean; default False): A Boolean value specifying whether to enable or disable the bounce-back effect
- collapsibleGroups (boolean; default False): Specifies whether or not an end-user can collapse groups
- dataSource (string | dict | list of boolean | number | string | dict | lists; optional): Binds the UI component to data
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- displayExpr (string; optional): Specifies the data field whose values should be displayed. Defaults to "text" when the data source contains objects
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- focusStateEnabled (boolean; default True): Specifies whether the UI component can be focused using keyboard navigation
- groupComponent (string | dict; optional): An alias for the groupTemplate property specified in React. Accepts a custom component.
- grouped (boolean; default False): Specifies whether data items should be grouped
- groupRender (string; optional): An alias for the groupTemplate property specified in React. Accepts a rendering function.
- groupTemplate (string | dict; default 'group'): Specifies a custom template for group captions
- height (number | string; optional): Specifies the UI component's height
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default True): Specifies whether the UI component changes its state when a user pauses on it
- indicateLoading (boolean; default True): Specifies whether or not to show the loading panel when the DataSource bound to the UI component is loading data
- itemComponent (string | dict; optional): An alias for the itemTemplate property specified in React. Accepts a custom component.
- itemDeleteMode (a value equal to: 'context', 'slideButton', 'slideItem', 'static', 'swipe', 'toggle'; default 'static'): Specifies the way a user can delete items from the list
- itemDragging (dict; optional): Configures item reordering using drag and drop gestures
- itemHoldTimeout (number; default 750): The time period in milliseconds before the onItemHold event is raised
- itemRender (string; optional): An alias for the itemTemplate property specified in React. Accepts a rendering function.
- items (list of boolean | number | string | dict | lists; optional): An array of items displayed by the UI component
- itemTemplate (string | dict; default 'item'): Specifies a custom template for items
- keyExpr (string; optional): Specifies the key property that provides key values to access data items. Each key value must be unique.
- menuItems (list of dicts; optional): Specifies the array of items for a context menu called for a list item
- menuMode (a value equal to: 'context', 'slide'; default 'context'): Specifies whether an item context menu is shown when a user holds or swipes an item
- nextButtonText (string; default 'More'): The text displayed on the button used to load the next page from the data source
- noDataText (string; default 'No data to display'): The text or HTML markup displayed by the UI component if the item collection is empty
- pageLoadingText (string; default 'Loading...'): Specifies the text shown in the pullDown panel, which is displayed when the list is scrolled to the bottom
- pageLoadMode (a value equal to: 'nextButton', 'scrollBottom'; default 'nextButton'): Specifies whether the next page is loaded when a user scrolls the UI component to the bottom or when the "next" button is clicked
- pulledDownText (string; default 'Release to refresh...'): Specifies the text displayed in the pullDown panel when the list is pulled below the refresh threshold
- pullingDownText (string; default 'Pull down to refresh...'): Specifies the text shown in the pullDown panel while the list is being pulled down to the refresh threshold
- pullRefreshEnabled (boolean; default False): A Boolean value specifying whether or not the UI component supports the "pull down to refresh" gesture
- refreshingText (string; default 'Refreshing...'): Specifies the text displayed in the pullDown panel while the list is being refreshed
- repaintChangesOnly (boolean; default False): Specifies whether to repaint only those elements whose data changed
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- scrollByContent (boolean; default False): A Boolean value specifying if the list is scrolled by content
- scrollByThumb (boolean; default True): A Boolean value specifying if the list is scrolled using the scrollbar
- scrollingEnabled (boolean; default True): A Boolean value specifying whether to enable or disable list scrolling
- searchEditorOptions (dict; optional): Configures the search panel
- searchEnabled (boolean; default False): Specifies whether the search panel is visible
- searchExpr (string | list of strings; optional): Specifies a data object's field name or an expression whose value is compared to the search string
- searchMode (a value equal to: 'contains', 'startswith', 'equals'; default 'contains'): Specifies a comparison operation used to search UI component items
- searchTimeout (number; default 300): Specifies a delay in milliseconds between when a user finishes typing, and the search is executed
- searchValue (string; default ''): Specifies the current search string
- selectAllMode (a value equal to: 'allPages', 'page'; default 'page'): Specifies the mode in which all items are selected
- selectedItemKeys (list of boolean | number | string | dict | lists; optional): Specifies an array of currently selected item keys
- selectedItems (list of boolean | number | string | dict | lists; optional): An array of currently selected item objects
- selectionMode (a value equal to: 'all', 'multiple', 'none', 'single'; default 'none'): Specifies item selection mode
- showScrollbar (a value equal to: 'always', 'never', 'onHover', 'onScroll'; default 'onHover'): Specifies when the UI component shows the scrollbar
- showSelectionControls (boolean; default False): Specifies whether or not to display controls used to select list items
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- useNativeScrolling (boolean; default False): Specifies whether or not the UI component uses native scrolling
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; optional): Specifies the UI component's width
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, allowItemDeleting=Component.UNDEFINED, bounceEnabled=Component.UNDEFINED, collapsibleGroups=Component.UNDEFINED, dataSource=Component.UNDEFINED, disabled=Component.UNDEFINED, displayExpr=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, groupComponent=Component.UNDEFINED, grouped=Component.UNDEFINED, groupRender=Component.UNDEFINED, groupTemplate=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, indicateLoading=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemDeleteMode=Component.UNDEFINED, itemDragging=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, keyExpr=Component.UNDEFINED, menuItems=Component.UNDEFINED, menuMode=Component.UNDEFINED, nextButtonText=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onGroupRendered=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemDeleted=Component.UNDEFINED, onItemDeleting=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onItemReordered=Component.UNDEFINED, onItemSwipe=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPageLoading=Component.UNDEFINED, onPullRefresh=Component.UNDEFINED, onScroll=Component.UNDEFINED, onSelectAllValueChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, pageLoadingText=Component.UNDEFINED, pageLoadMode=Component.UNDEFINED, pulledDownText=Component.UNDEFINED, pullingDownText=Component.UNDEFINED, pullRefreshEnabled=Component.UNDEFINED, refreshingText=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollByContent=Component.UNDEFINED, scrollByThumb=Component.UNDEFINED, scrollingEnabled=Component.UNDEFINED, searchEditorOptions=Component.UNDEFINED, searchEnabled=Component.UNDEFINED, searchExpr=Component.UNDEFINED, searchMode=Component.UNDEFINED, searchTimeout=Component.UNDEFINED, searchValue=Component.UNDEFINED, selectAllMode=Component.UNDEFINED, selectedItemKeys=Component.UNDEFINED, selectedItems=Component.UNDEFINED, selectionMode=Component.UNDEFINED, showScrollbar=Component.UNDEFINED, showSelectionControls=Component.UNDEFINED, tabIndex=Component.UNDEFINED, useNativeScrolling=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'allowItemDeleting', 'bounceEnabled', 'collapsibleGroups', 'dataSource', 'disabled', 'displayExpr', 'elementAttr', 'focusStateEnabled', 'groupComponent', 'grouped', 'groupRender', 'groupTemplate', 'height', 'hint', 'hoverStateEnabled', 'indicateLoading', 'itemComponent', 'itemDeleteMode', 'itemDragging', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'keyExpr', 'menuItems', 'menuMode', 'nextButtonText', 'noDataText', 'pageLoadingText', 'pageLoadMode', 'pulledDownText', 'pullingDownText', 'pullRefreshEnabled', 'refreshingText', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollByThumb', 'scrollingEnabled', 'searchEditorOptions', 'searchEnabled', 'searchExpr', 'searchMode', 'searchTimeout', 'searchValue', 'selectAllMode', 'selectedItemKeys', 'selectedItems', 'selectionMode', 'showScrollbar', 'showSelectionControls', 'tabIndex', 'useNativeScrolling', 'visible', 'width', 'loading_state']
        self._type = 'List'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'allowItemDeleting', 'bounceEnabled', 'collapsibleGroups', 'dataSource', 'disabled', 'displayExpr', 'elementAttr', 'focusStateEnabled', 'groupComponent', 'grouped', 'groupRender', 'groupTemplate', 'height', 'hint', 'hoverStateEnabled', 'indicateLoading', 'itemComponent', 'itemDeleteMode', 'itemDragging', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'keyExpr', 'menuItems', 'menuMode', 'nextButtonText', 'noDataText', 'pageLoadingText', 'pageLoadMode', 'pulledDownText', 'pullingDownText', 'pullRefreshEnabled', 'refreshingText', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollByThumb', 'scrollingEnabled', 'searchEditorOptions', 'searchEnabled', 'searchExpr', 'searchMode', 'searchTimeout', 'searchValue', 'selectAllMode', 'selectedItemKeys', 'selectedItems', 'selectionMode', 'showScrollbar', 'showSelectionControls', 'tabIndex', 'useNativeScrolling', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(List, self).__init__(**args)
