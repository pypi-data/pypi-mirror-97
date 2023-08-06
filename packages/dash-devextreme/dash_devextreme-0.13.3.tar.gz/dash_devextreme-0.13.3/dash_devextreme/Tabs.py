# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tabs(Component):
    """A Tabs component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional)
- dataSource (string | list of strings | list of dicts | dict; optional)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- focusStateEnabled (boolean; default True)
- height (number | string; default 'auto')
- hint (string; optional)
- hoverStateEnabled (boolean; default True)
- itemHoldTimeout (number; default 750)
- items (list of strings | list of dicts; optional)
- itemTemplate (string | dict; default 'item')
- keyExpr (string; optional)
- noDataText (string; default 'No data to display')
- onItemClick (string; optional)
- repaintChangesOnly (boolean; default False)
- rtlEnabled (boolean; default False)
- scrollByContent (boolean; default False)
- scrollingEnabled (boolean; default True)
- selectedIndex (number; default -1)
- selectedItem (dict; optional)
- selectedItemKeys (number; optional)
- selectedItems (list of boolean | number | string | dict | lists; optional)
- selectionMode (a value equal to: 'multiple', 'single'; default 'single')
- showNavButtons (boolean; default True)
- tabIndex (number; default 0)
- visible (boolean; default True)
- width (number | string; default 'auto')"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, dataSource=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, keyExpr=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollByContent=Component.UNDEFINED, scrollingEnabled=Component.UNDEFINED, selectedIndex=Component.UNDEFINED, selectedItem=Component.UNDEFINED, selectedItemKeys=Component.UNDEFINED, selectedItems=Component.UNDEFINED, selectionMode=Component.UNDEFINED, showNavButtons=Component.UNDEFINED, tabIndex=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'dataSource', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemHoldTimeout', 'items', 'itemTemplate', 'keyExpr', 'noDataText', 'onItemClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'selectedItemKeys', 'selectedItems', 'selectionMode', 'showNavButtons', 'tabIndex', 'visible', 'width']
        self._type = 'Tabs'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'dataSource', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemHoldTimeout', 'items', 'itemTemplate', 'keyExpr', 'noDataText', 'onItemClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'selectedItemKeys', 'selectedItems', 'selectionMode', 'showNavButtons', 'tabIndex', 'visible', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tabs, self).__init__(**args)
