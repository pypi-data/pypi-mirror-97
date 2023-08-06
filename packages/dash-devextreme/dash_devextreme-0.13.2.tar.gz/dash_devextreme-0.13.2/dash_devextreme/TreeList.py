# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TreeList(Component):
    """A TreeList component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional)
- activeStateEnabled (boolean; default False)
- allowColumnReordering (boolean; default False)
- allowColumnResizing (boolean; default False)
- autoExpandAll (boolean; default False)
- cacheEnabled (boolean; default True)
- cellHintEnabled (boolean; default True)
- columnAutoWidth (boolean; default False)
- columnChooser (dict; optional)
- columnFixing (dict; optional)
- columnHidingEnabled (boolean; default False)
- columnMinWidth (number; default undefined)
- columnResizingMode (a value equal to: 'nextColumn', 'widget'; default 'nextColumn')
- columns (list; default undefined)
- columnWidth (number; default undefined)
- dataSource (string | list of dicts; optional)
- dataStructure (a value equal to: 'plain', 'tree'; default 'plain')
- dateSerializationFormat (string; optional)
- disabled (boolean; default False)
- editing (dict; optional)
- elementAttr (dict; optional)
- errorRowEnabled (boolean; default True)
- expandedRowKeys (list of strings | list of numbers; optional)
- expandNodesOnFiltering (boolean; default True)
- filterBuilder (dict; optional)
- filterBuilderPopup (dict; optional)
- filterPanel (dict; optional)
- filterRow (dict; optional)
- filterSyncEnabled (boolean; optional)
- filterValue (dict; optional)
- focusedColumnIndex (number; default -1)
- focusedRowEnabled (boolean; default False)
- focusedRowIndex (number; default -1)
- focusedRowKey (boolean | number | string | dict | list; default undefined)
- focusStateEnabled (boolean; default False)
- hasItemsExpr (string; optional)
- headerFilter (dict; optional)
- height (string | number; default undefined)
- highlightChanges (boolean; default False)
- hint (string; default undefined)
- hoverStateEnabled (boolean; default False)
- itemsExpr (string; default 'items')
- keyExpr (string; default 'id')
- loadPanel (dict; optional)
- noDataText (string; default 'No data')
- onCellClick (string; optional)
- onRowClick (string; optional)
- pager (dict; optional)
- paging (dict; optional)
- parentIdExpr (string; default 'parentId')
- remoteOperations (dict; optional)
- renderAsync (boolean; default False)
- repaintChangesOnly (boolean; default False)
- rootValue (boolean | number | string | dict | list; default 0)
- rowAlternationEnabled (boolean; default False)
- rtlEnabled (boolean; default False)
- scrolling (dict; optional)
- searchPanel (dict; optional)
- selectedRowKeys (list of boolean | number | string | dict | lists; optional)
- selection (dict; optional)
- showBorders (boolean; default False)
- showColumnHeaders (boolean; default True)
- showColumnLines (boolean; default True)
- showRowLines (boolean; default False)
- sorting (dict; optional)
- stateStoring (dict; optional)
- tabIndex (number; default 0)
- twoWayBindingEnabled (boolean; default True)
- visible (boolean; default True)
- width (string | number; default undefined)
- wordWrapEnabled (boolean; default False)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, allowColumnReordering=Component.UNDEFINED, allowColumnResizing=Component.UNDEFINED, autoExpandAll=Component.UNDEFINED, cacheEnabled=Component.UNDEFINED, cellHintEnabled=Component.UNDEFINED, columnAutoWidth=Component.UNDEFINED, columnChooser=Component.UNDEFINED, columnFixing=Component.UNDEFINED, columnHidingEnabled=Component.UNDEFINED, columnMinWidth=Component.UNDEFINED, columnResizingMode=Component.UNDEFINED, columns=Component.UNDEFINED, columnWidth=Component.UNDEFINED, customizeColumns=Component.UNDEFINED, dataSource=Component.UNDEFINED, dataStructure=Component.UNDEFINED, dateSerializationFormat=Component.UNDEFINED, disabled=Component.UNDEFINED, editing=Component.UNDEFINED, elementAttr=Component.UNDEFINED, errorRowEnabled=Component.UNDEFINED, expandedRowKeys=Component.UNDEFINED, expandNodesOnFiltering=Component.UNDEFINED, filterBuilder=Component.UNDEFINED, filterBuilderPopup=Component.UNDEFINED, filterPanel=Component.UNDEFINED, filterRow=Component.UNDEFINED, filterSyncEnabled=Component.UNDEFINED, filterValue=Component.UNDEFINED, focusedColumnIndex=Component.UNDEFINED, focusedRowEnabled=Component.UNDEFINED, focusedRowIndex=Component.UNDEFINED, focusedRowKey=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, hasItemsExpr=Component.UNDEFINED, headerFilter=Component.UNDEFINED, height=Component.UNDEFINED, highlightChanges=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, itemsExpr=Component.UNDEFINED, keyExpr=Component.UNDEFINED, loadPanel=Component.UNDEFINED, noDataText=Component.UNDEFINED, onAdaptiveDetailRowPreparing=Component.UNDEFINED, onCellClick=Component.UNDEFINED, onCellHoverChanged=Component.UNDEFINED, onCellPrepared=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onContextMenuPreparing=Component.UNDEFINED, onDataErrorOccurred=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEditingStart=Component.UNDEFINED, onEditorPrepared=Component.UNDEFINED, onEditorPreparing=Component.UNDEFINED, onFocusedCellChanged=Component.UNDEFINED, onFocusedCellChanging=Component.UNDEFINED, onFocusedRowChanged=Component.UNDEFINED, onFocusedRowChanging=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInitNewRow=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onNodesInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onRowClick=Component.UNDEFINED, onRowCollapsed=Component.UNDEFINED, onRowCollapsing=Component.UNDEFINED, onRowExpanded=Component.UNDEFINED, onRowExpanding=Component.UNDEFINED, onRowInserted=Component.UNDEFINED, onRowInserting=Component.UNDEFINED, onRowPrepared=Component.UNDEFINED, onRowRemoved=Component.UNDEFINED, onRowRemoving=Component.UNDEFINED, onRowUpdated=Component.UNDEFINED, onRowUpdating=Component.UNDEFINED, onRowValidating=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onToolbarPreparing=Component.UNDEFINED, pager=Component.UNDEFINED, paging=Component.UNDEFINED, parentIdExpr=Component.UNDEFINED, remoteOperations=Component.UNDEFINED, renderAsync=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rootValue=Component.UNDEFINED, rowAlternationEnabled=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrolling=Component.UNDEFINED, searchPanel=Component.UNDEFINED, selectedRowKeys=Component.UNDEFINED, selection=Component.UNDEFINED, showBorders=Component.UNDEFINED, showColumnHeaders=Component.UNDEFINED, showColumnLines=Component.UNDEFINED, showRowLines=Component.UNDEFINED, sorting=Component.UNDEFINED, stateStoring=Component.UNDEFINED, tabIndex=Component.UNDEFINED, twoWayBindingEnabled=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, wordWrapEnabled=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'allowColumnReordering', 'allowColumnResizing', 'autoExpandAll', 'cacheEnabled', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columns', 'columnWidth', 'dataSource', 'dataStructure', 'dateSerializationFormat', 'disabled', 'editing', 'elementAttr', 'errorRowEnabled', 'expandedRowKeys', 'expandNodesOnFiltering', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'focusStateEnabled', 'hasItemsExpr', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'itemsExpr', 'keyExpr', 'loadPanel', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'parentIdExpr', 'remoteOperations', 'renderAsync', 'repaintChangesOnly', 'rootValue', 'rowAlternationEnabled', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sorting', 'stateStoring', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self._type = 'TreeList'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'allowColumnReordering', 'allowColumnResizing', 'autoExpandAll', 'cacheEnabled', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columns', 'columnWidth', 'dataSource', 'dataStructure', 'dateSerializationFormat', 'disabled', 'editing', 'elementAttr', 'errorRowEnabled', 'expandedRowKeys', 'expandNodesOnFiltering', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'focusStateEnabled', 'hasItemsExpr', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'itemsExpr', 'keyExpr', 'loadPanel', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'parentIdExpr', 'remoteOperations', 'renderAsync', 'repaintChangesOnly', 'rootValue', 'rowAlternationEnabled', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sorting', 'stateStoring', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TreeList, self).__init__(**args)
