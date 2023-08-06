# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Lookup(Component):
    """A Lookup component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default True): Specifies whether or not the UI component changes its state when interacting with a user
- applyButtonText (string; default 'OK'): The text displayed on the Apply button
- applyValueMode (a value equal to: 'instantly', 'useButtons'; default 'instantly'): Specifies the way an end-user applies the selected value
- cancelButtonText (string; default 'Cancel'): The text displayed on the Cancel button
- cleanSearchOnOpening (boolean; default True): Specifies whether or not the UI component cleans the search box when the popup window is displayed
- clearButtonText (string; default 'Clear'): The text displayed on the Clear button
- dataSource (string | dict | list of boolean | number | string | dict | lists; optional): Binds the UI component to data
- deferRendering (boolean; default True): Specifies whether to render the drop-down field's content when it is displayed. If false, the content is rendered immediately.
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- displayExpr (string; optional): Specifies the data field whose values should be displayed. Defaults to "text" when the data source contains objects
- displayValue (string; optional): Returns the value currently displayed by the UI component
- dropDownCentered (boolean; default False): Specifies whether to vertically align the drop-down menu so that the selected item is in its center. Applies only in Material Design themes.
- dropDownOptions (dict; optional): Configures the drop-down field
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- fieldComponent (string | dict; optional): An alias for the fieldTemplate property specified in React. Accepts a custom component.
- fieldRender (string; optional): An alias for the fieldTemplate property specified in React. Accepts a rendering function.
- fieldTemplate (string | dict; optional): Specifies a custom template for the input field
- focusStateEnabled (boolean; default True): Specifies whether the UI component can be focused using keyboard navigation
- groupComponent (string | dict; optional): An alias for the groupTemplate property specified in React. Accepts a custom component.
- grouped (boolean; default False): Specifies whether data items should be grouped
- groupRender (string; optional): An alias for the groupTemplate property specified in React. Accepts a rendering function.
- groupTemplate (string | dict; default 'group'): Specifies a custom template for group captions
- height (number | string; optional): Specifies the UI component's height
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default True): Specifies whether the UI component changes its state when a user pauses on it
- inputAttr (dict; optional): Specifies the attributes to be passed on to the underlying HTML element
- isValid (boolean; default True): Specifies or indicates whether the editor's value is valid
- itemComponent (string | dict; optional): An alias for the itemTemplate property specified in React. Accepts a custom component.
- itemRender (string; optional): An alias for the itemTemplate property specified in React. Accepts a rendering function.
- items (list of boolean | number | string | dict | lists; optional): An array of items displayed by the UI component
- itemTemplate (string | dict; default 'item'): Specifies a custom template for items
- minSearchLength (number; default 0): The minimum number of characters that must be entered into the text box to begin a search. Applies only if searchEnabled is true.
- name (string; default ''): The value to be assigned to the name attribute of the underlying HTML element
- nextButtonText (string; default 'More'): The text displayed on the button used to load the next page from the data source
- noDataText (string; default 'No data to display'): The text or HTML markup displayed by the UI component if the item collection is empty
- opened (boolean; default False): Specifies whether or not the drop-down editor is displayed
- pageLoadingText (string; default 'Loading...'): Specifies the text shown in the pullDown panel, which is displayed when the list is scrolled to the bottom
- pageLoadMode (a value equal to: 'nextButton', 'scrollBottom'; default 'scrollBottom'): Specifies whether the next page is loaded when a user scrolls the UI component to the bottom or when the "next" button is clicked
- placeholder (string; default 'Select'): The text displayed by the UI component when nothing is selected
- pulledDownText (string; default 'Release to refresh...'): Specifies the text displayed in the pullDown panel when the list is pulled below the refresh threshold
- pullingDownText (string; default 'Pull down to refresh...'): Specifies the text shown in the pullDown panel while the list is being pulled down to the refresh threshold
- pullRefreshEnabled (boolean; default False): A Boolean value specifying whether or not the UI component supports the "pull down to refresh" gesture
- refreshingText (string; default 'Refreshing...'): Specifies the text displayed in the pullDown panel while the list is being refreshed
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- searchEnabled (boolean; default False): Specifies whether the search panel is visible
- searchExpr (string | list of strings; optional): Specifies a data object's field name or an expression whose value is compared to the search string
- searchMode (a value equal to: 'contains', 'startswith', 'equals'; default 'contains'): Specifies a comparison operation used to search UI component items
- searchPlaceholder (string; default 'Search'): The text that is provided as a hint in the lookup's search bar
- searchTimeout (number; default 500): Specifies a delay in milliseconds between when a user finishes typing, and the search is executed
- showCancelButton (boolean; default True): Specifies whether to display the Cancel button in the lookup window
- showClearButton (boolean; default False): Specifies whether to display the Clear button in the lookup window
- showDataBeforeSearch (boolean; default False): Specifies whether or not the UI component displays unfiltered values until a user types a number of characters exceeding the minSearchLength property value
- stylingMode (a value equal to: 'outlined', 'underlined', 'filled'; default 'outlined'): Specifies how the UI component's text field is styled
- tabIndex (number; default 0): Specifies the number of the element when the Tab key is used for navigating
- titleComponent (string | dict; optional): An alias for the titleTemplate property specified in React. Accepts a custom component.
- titleRender (string; optional): An alias for the titleTemplate property specified in React. Accepts a rendering function.
- useNativeScrolling (boolean; default False): Specifies whether or not the UI component uses native scrolling
- usePopover (boolean; default False): Specifies whether to show lookup contents in the Popover UI component
- validationError (dict; optional): Information on the broken validation rule. Contains the first item from the validationErrors array.
- validationErrors (list of dicts; optional): An array of the validation rules that failed
- validationMessageMode (a value equal to: 'always', 'auto'; default 'auto'): Specifies how the message about the validation rules that are not satisfied by this editor's value is displayed
- validationStatus (a value equal to: 'valid', 'invalid', 'pending'; default 'valid'): Indicates or specifies the current validation status
- value (boolean | number | string | dict | list; optional): Specifies the currently selected value. May be an object if dataSource contains objects and valueExpr is not set.
- valueChangeEvent (string; default 'input change keyup'): Specifies the DOM events after which the UI component's search results should be updated
- valueExpr (string; default 'this'): Specifies which data field provides unique values to the UI component's value
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; optional): Specifies the UI component's width
- wrapItemText (boolean; default False): Specifies whether text that exceeds the drop-down list width should be wrapped
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, applyButtonText=Component.UNDEFINED, applyValueMode=Component.UNDEFINED, cancelButtonText=Component.UNDEFINED, cleanSearchOnOpening=Component.UNDEFINED, clearButtonText=Component.UNDEFINED, dataSource=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, displayExpr=Component.UNDEFINED, displayValue=Component.UNDEFINED, dropDownCentered=Component.UNDEFINED, dropDownOptions=Component.UNDEFINED, elementAttr=Component.UNDEFINED, fieldComponent=Component.UNDEFINED, fieldRender=Component.UNDEFINED, fieldTemplate=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, groupComponent=Component.UNDEFINED, grouped=Component.UNDEFINED, groupRender=Component.UNDEFINED, groupTemplate=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, isValid=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, minSearchLength=Component.UNDEFINED, name=Component.UNDEFINED, nextButtonText=Component.UNDEFINED, noDataText=Component.UNDEFINED, onClosed=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onOpened=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPageLoading=Component.UNDEFINED, onPullRefresh=Component.UNDEFINED, onScroll=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, opened=Component.UNDEFINED, pageLoadingText=Component.UNDEFINED, pageLoadMode=Component.UNDEFINED, placeholder=Component.UNDEFINED, pulledDownText=Component.UNDEFINED, pullingDownText=Component.UNDEFINED, pullRefreshEnabled=Component.UNDEFINED, refreshingText=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, searchEnabled=Component.UNDEFINED, searchExpr=Component.UNDEFINED, searchMode=Component.UNDEFINED, searchPlaceholder=Component.UNDEFINED, searchTimeout=Component.UNDEFINED, showCancelButton=Component.UNDEFINED, showClearButton=Component.UNDEFINED, showDataBeforeSearch=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, titleComponent=Component.UNDEFINED, titleRender=Component.UNDEFINED, useNativeScrolling=Component.UNDEFINED, usePopover=Component.UNDEFINED, validationError=Component.UNDEFINED, validationErrors=Component.UNDEFINED, validationMessageMode=Component.UNDEFINED, validationStatus=Component.UNDEFINED, value=Component.UNDEFINED, valueChangeEvent=Component.UNDEFINED, valueExpr=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, wrapItemText=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'applyButtonText', 'applyValueMode', 'cancelButtonText', 'cleanSearchOnOpening', 'clearButtonText', 'dataSource', 'deferRendering', 'disabled', 'displayExpr', 'displayValue', 'dropDownCentered', 'dropDownOptions', 'elementAttr', 'fieldComponent', 'fieldRender', 'fieldTemplate', 'focusStateEnabled', 'groupComponent', 'grouped', 'groupRender', 'groupTemplate', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'itemComponent', 'itemRender', 'items', 'itemTemplate', 'minSearchLength', 'name', 'nextButtonText', 'noDataText', 'opened', 'pageLoadingText', 'pageLoadMode', 'placeholder', 'pulledDownText', 'pullingDownText', 'pullRefreshEnabled', 'refreshingText', 'rtlEnabled', 'searchEnabled', 'searchExpr', 'searchMode', 'searchPlaceholder', 'searchTimeout', 'showCancelButton', 'showClearButton', 'showDataBeforeSearch', 'stylingMode', 'tabIndex', 'titleComponent', 'titleRender', 'useNativeScrolling', 'usePopover', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'valueExpr', 'visible', 'width', 'wrapItemText', 'loading_state']
        self._type = 'Lookup'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'applyButtonText', 'applyValueMode', 'cancelButtonText', 'cleanSearchOnOpening', 'clearButtonText', 'dataSource', 'deferRendering', 'disabled', 'displayExpr', 'displayValue', 'dropDownCentered', 'dropDownOptions', 'elementAttr', 'fieldComponent', 'fieldRender', 'fieldTemplate', 'focusStateEnabled', 'groupComponent', 'grouped', 'groupRender', 'groupTemplate', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'isValid', 'itemComponent', 'itemRender', 'items', 'itemTemplate', 'minSearchLength', 'name', 'nextButtonText', 'noDataText', 'opened', 'pageLoadingText', 'pageLoadMode', 'placeholder', 'pulledDownText', 'pullingDownText', 'pullRefreshEnabled', 'refreshingText', 'rtlEnabled', 'searchEnabled', 'searchExpr', 'searchMode', 'searchPlaceholder', 'searchTimeout', 'showCancelButton', 'showClearButton', 'showDataBeforeSearch', 'stylingMode', 'tabIndex', 'titleComponent', 'titleRender', 'useNativeScrolling', 'usePopover', 'validationError', 'validationErrors', 'validationMessageMode', 'validationStatus', 'value', 'valueChangeEvent', 'valueExpr', 'visible', 'width', 'wrapItemText', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Lookup, self).__init__(**args)
