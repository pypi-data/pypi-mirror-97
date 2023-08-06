# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DataGrid(Component):
    """A DataGrid component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- accessKey (string; optional): Specifies the shortcut key that sets focus on the UI component
- activeStateEnabled (boolean; default False): Specifies whether or not the UI component changes its state when interacting with a user
- allowColumnReordering (boolean; default False): Specifies whether a user can reorder columns
- allowColumnResizing (boolean; default False): Specifies whether a user can resize columns
- autoNavigateToFocusedRow (boolean; default True): Automatically scrolls to the focused row when the focusedRowKey is changed
- cacheEnabled (boolean; default True): Specifies whether data should be cached
- cellHintEnabled (boolean; default True): Enables a hint that appears when a user hovers the mouse pointer over a cell with truncated content
- columnAutoWidth (boolean; default False): Specifies whether columns should adjust their widths to the content
- columnChooser (dict; optional): Configures the column chooser
- columnFixing (dict; optional): Configures column fixing
- columnHidingEnabled (boolean; default False): Specifies whether the UI component should hide columns to adapt to the screen or container size. Ignored if allowColumnResizing is true and columnResizingMode is "widget"
- columnMinWidth (number; optional): Specifies the minimum width of columns
- columnResizingMode (a value equal to: 'nextColumn', 'widget'; default 'nextColumn'): Specifies how the UI component resizes columns. Applies only if allowColumnResizing is true.
- columns (list of dicts; optional): An array of grid columns
- columnWidth (number; optional): Specifies the width for all data columns. Has a lower priority than the column.width property.
- dataSource (dict | list of dicts; optional): Binds the UI component to data
- dateSerializationFormat (string; optional): Specifies the format in which date-time values should be sent to the server. Use it only if you do not specify the dataSource at design time
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- editing (dict; optional): Configures editing
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- errorRowEnabled (boolean; default True): Indicates whether to show the error row
- export (dict; optional): Configures client-side exporting
- filterBuilder (dict; optional): Configures the integrated filter builder
- filterBuilderPopup (dict; optional): Configures the popup in which the integrated filter builder is shown
- filterPanel (dict; optional): Configures the filter panel
- filterRow (dict; optional): Configures the filter row
- filterSyncEnabled (boolean; optional): Specifies whether to synchronize the filter row, header filter, and filter builder. The synchronized filter expression is stored in the filterValue property.
- filterValue (dict; optional): Specifies a filter expression
- focusedColumnIndex (number; default -1): The index of the column that contains the focused data cell. This index is taken from the columns array.
- focusedRowEnabled (boolean; default False): Specifies whether the focused row feature is enabled
- focusedRowIndex (number; default -1): Specifies or indicates the focused data row's index. Use this property when focusedRowEnabled is true.
- focusedRowKey (boolean | number | string | dict | list; optional): Specifies initially or currently focused grid row's key. Use it when focusedRowEnabled is true.
- focusStateEnabled (boolean; default False): Specifies whether the UI component can be focused using keyboard navigation
- grouping (dict; optional): Configures grouping
- groupPanel (dict; optional): Configures the group panel
- headerFilter (dict; optional): Configures the header filter feature
- height (number | string; optional): Specifies the UI component's height
- highlightChanges (boolean; default False)
- hint (string; optional)
- hoverStateEnabled (boolean; default False)
- keyExpr (string | list of strings; optional)
- loadPanel (dict; optional)
- masterDetail (dict; optional)
- noDataText (string; default 'No data')
- onCellClick (string; optional)
- onRowClick (string; optional)
- pager (dict; optional)
- paging (dict; optional)
- remoteOperations (boolean | dict; optional)
- renderAsync (boolean; default False)
- repaintChangesOnly (boolean; default False)
- rowAlternationEnabled (boolean; default False)
- rowClick (dict; optional)
- rowDblClick (dict; optional)
- rowRemoved (dict; optional)
- rowRemoving (dict; optional)
- rowUpdated (dict; optional)
- rowUpdating (dict; optional)
- rowTemplate (string; optional)
- rtlEnabled (boolean; default False)
- scrolling (dict; optional)
- searchPanel (dict; optional)
- selectedRowKeys (list of boolean | number | string | dict | lists; optional)
- selection (dict; optional)
- selectionFilter (list; optional)
- showBorders (boolean; default False)
- showColumnHeaders (boolean; default True)
- showColumnLines (boolean; default True)
- showRowLines (boolean; default False)
- sortByGroupSummaryInfo (list of dicts; optional)
- sorting (dict; optional)
- stateStoring (dict; optional)
- summary (dict; optional)
- tabIndex (number; default 0)
- twoWayBindingEnabled (boolean; default True)
- visible (boolean; default True)
- width (number | string; optional)
- wordWrapEnabled (boolean; default False)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, allowColumnReordering=Component.UNDEFINED, allowColumnResizing=Component.UNDEFINED, autoNavigateToFocusedRow=Component.UNDEFINED, cacheEnabled=Component.UNDEFINED, cellHintEnabled=Component.UNDEFINED, columnAutoWidth=Component.UNDEFINED, columnChooser=Component.UNDEFINED, columnFixing=Component.UNDEFINED, columnHidingEnabled=Component.UNDEFINED, columnMinWidth=Component.UNDEFINED, columnResizingMode=Component.UNDEFINED, columns=Component.UNDEFINED, columnWidth=Component.UNDEFINED, customizeColumns=Component.UNDEFINED, dataSource=Component.UNDEFINED, dateSerializationFormat=Component.UNDEFINED, disabled=Component.UNDEFINED, editing=Component.UNDEFINED, elementAttr=Component.UNDEFINED, errorRowEnabled=Component.UNDEFINED, export=Component.UNDEFINED, filterBuilder=Component.UNDEFINED, filterBuilderPopup=Component.UNDEFINED, filterPanel=Component.UNDEFINED, filterRow=Component.UNDEFINED, filterSyncEnabled=Component.UNDEFINED, filterValue=Component.UNDEFINED, focusedColumnIndex=Component.UNDEFINED, focusedRowEnabled=Component.UNDEFINED, focusedRowIndex=Component.UNDEFINED, focusedRowKey=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, grouping=Component.UNDEFINED, groupPanel=Component.UNDEFINED, headerFilter=Component.UNDEFINED, height=Component.UNDEFINED, highlightChanges=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, keyExpr=Component.UNDEFINED, loadPanel=Component.UNDEFINED, masterDetail=Component.UNDEFINED, noDataText=Component.UNDEFINED, onAdaptiveDetailRowPreparing=Component.UNDEFINED, onCellClick=Component.UNDEFINED, onCellHoverChanged=Component.UNDEFINED, onCellPrepared=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onContextMenuPreparing=Component.UNDEFINED, onDataErrorOccurred=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEditingStart=Component.UNDEFINED, onEditorPrepared=Component.UNDEFINED, onEditorPreparing=Component.UNDEFINED, onExported=Component.UNDEFINED, onExporting=Component.UNDEFINED, onFileSaving=Component.UNDEFINED, onFocusedCellChanged=Component.UNDEFINED, onFocusedCellChanging=Component.UNDEFINED, onFocusedRowChanged=Component.UNDEFINED, onFocusedRowChanging=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInitNewRow=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onRowClick=Component.UNDEFINED, onRowCollapsed=Component.UNDEFINED, onRowCollapsing=Component.UNDEFINED, onRowExpanded=Component.UNDEFINED, onRowExpanding=Component.UNDEFINED, onRowInserted=Component.UNDEFINED, onRowInserting=Component.UNDEFINED, onRowPrepared=Component.UNDEFINED, onRowRemoved=Component.UNDEFINED, onRowRemoving=Component.UNDEFINED, onRowUpdated=Component.UNDEFINED, onRowUpdating=Component.UNDEFINED, onRowValidating=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onToolbarPreparing=Component.UNDEFINED, pager=Component.UNDEFINED, paging=Component.UNDEFINED, remoteOperations=Component.UNDEFINED, renderAsync=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rowAlternationEnabled=Component.UNDEFINED, rowClick=Component.UNDEFINED, rowDblClick=Component.UNDEFINED, rowRemoved=Component.UNDEFINED, rowRemoving=Component.UNDEFINED, rowUpdated=Component.UNDEFINED, rowUpdating=Component.UNDEFINED, rowTemplate=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrolling=Component.UNDEFINED, searchPanel=Component.UNDEFINED, selectedRowKeys=Component.UNDEFINED, selection=Component.UNDEFINED, selectionFilter=Component.UNDEFINED, showBorders=Component.UNDEFINED, showColumnHeaders=Component.UNDEFINED, showColumnLines=Component.UNDEFINED, showRowLines=Component.UNDEFINED, sortByGroupSummaryInfo=Component.UNDEFINED, sorting=Component.UNDEFINED, stateStoring=Component.UNDEFINED, summary=Component.UNDEFINED, tabIndex=Component.UNDEFINED, twoWayBindingEnabled=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, wordWrapEnabled=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'allowColumnReordering', 'allowColumnResizing', 'autoNavigateToFocusedRow', 'cacheEnabled', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columns', 'columnWidth', 'dataSource', 'dateSerializationFormat', 'disabled', 'editing', 'elementAttr', 'errorRowEnabled', 'export', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'focusStateEnabled', 'grouping', 'groupPanel', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'keyExpr', 'loadPanel', 'masterDetail', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'remoteOperations', 'renderAsync', 'repaintChangesOnly', 'rowAlternationEnabled', 'rowClick', 'rowDblClick', 'rowRemoved', 'rowRemoving', 'rowUpdated', 'rowUpdating', 'rowTemplate', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'selectionFilter', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sortByGroupSummaryInfo', 'sorting', 'stateStoring', 'summary', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self._type = 'DataGrid'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'allowColumnReordering', 'allowColumnResizing', 'autoNavigateToFocusedRow', 'cacheEnabled', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columns', 'columnWidth', 'dataSource', 'dateSerializationFormat', 'disabled', 'editing', 'elementAttr', 'errorRowEnabled', 'export', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'focusStateEnabled', 'grouping', 'groupPanel', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'keyExpr', 'loadPanel', 'masterDetail', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'remoteOperations', 'renderAsync', 'repaintChangesOnly', 'rowAlternationEnabled', 'rowClick', 'rowDblClick', 'rowRemoved', 'rowRemoving', 'rowUpdated', 'rowUpdating', 'rowTemplate', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'selectionFilter', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sortByGroupSummaryInfo', 'sorting', 'stateStoring', 'summary', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DataGrid, self).__init__(**args)
