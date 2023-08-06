# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Chart(Component):
    """A Chart component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- adaptiveLayout (dict; optional)
- adjustOnZoom (boolean; default True)
- animation (dict | boolean; optional)
- annotations (list of dicts; optional)
- argumentAxis (dict; optional)
- autoHidePointMarkers (boolean; default True)
- barGroupPadding (number; default 0.3)
- barGroupWidth (number; optional)
- commonAnnotationSettings (dict; optional)
- commonAxisSettings (dict; optional)
- commonPaneSettings (dict; optional)
- commonSeriesSettings (dict; optional)
- containerBackgroundColor (string; default '#ffffff')
- crosshair (dict; optional)
- dataPrepareSettings (dict; optional)
- dataSource (list of boolean | number | string | dict | lists | dict | string; optional)
- defaultPane (string; optional)
- disabled (boolean; default False)
- elementAttr (dict; optional)
- export (dict; optional)
- legend (dict; optional)
- loadingIndicator (dict; optional)
- margin (dict; optional)
- maxBubbleSize (number; default 0.2)
- minBubbleSize (number; default 12)
- negativesAsZeroes (boolean; default False)
- onLegendClick (string; optional)
- onPointClick (string; optional)
- onSeriesClick (string; optional)
- palette (list of strings | a value equal to: 'Bright', 'Harmony Light', 'Ocean', 'Pastel', 'Soft', 'Soft Pastel', 'Vintage', 'Violet', 'Carmine', 'Dark Moon', 'Dark Violet', 'Green Mist', 'Soft Blue', 'Material', 'Office'; default 'Material')
- paletteExtensionMode (a value equal to: 'alternate', 'blend', 'extrapolate'; default 'blend')
- panes (list of dicts | dict; optional)
- pathModified (boolean; default False)
- pointSelectionMode (a value equal to: 'multiple', 'single'; default 'single')
- redrawOnResize (boolean; default True)
- resizePanesOnZoom (boolean; default False)
- resolveLabelOverlapping (a value equal to: 'hide', 'none', 'shift'; default 'none')
- rotated (boolean; default False)
- rtlEnabled (boolean; default False)
- scrollBar (dict; optional)
- series (dict | list of dicts; optional)
- seriesSelectionMode (a value equal to: 'multiple', 'single'; default 'single')
- seriesTemplate (dict; optional)
- size (dict; optional)
- stickyHovering (boolean; default True)
- synchronizeMultiAxes (boolean; default True)
- theme (a value equal to: 'generic.dark', 'generic.light', 'generic.contrast', 'ios7.default', 'generic.carmine', 'generic.darkmoon', 'generic.darkviolet', 'generic.greenmist', 'generic.softblue', 'material.blue.light', 'material.lime.light', 'material.orange.light', 'material.purple.light', 'material.teal.light'; default 'generic.light')
- title (dict | string; optional)
- tooltip (dict; optional)
- valueAxis (dict | list of dicts; optional)
- zoomAndPan (dict; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, adaptiveLayout=Component.UNDEFINED, adjustOnZoom=Component.UNDEFINED, animation=Component.UNDEFINED, annotations=Component.UNDEFINED, argumentAxis=Component.UNDEFINED, autoHidePointMarkers=Component.UNDEFINED, barGroupPadding=Component.UNDEFINED, barGroupWidth=Component.UNDEFINED, commonAnnotationSettings=Component.UNDEFINED, commonAxisSettings=Component.UNDEFINED, commonPaneSettings=Component.UNDEFINED, commonSeriesSettings=Component.UNDEFINED, containerBackgroundColor=Component.UNDEFINED, crosshair=Component.UNDEFINED, customizeAnnotation=Component.UNDEFINED, customizeLabel=Component.UNDEFINED, customizePoint=Component.UNDEFINED, dataPrepareSettings=Component.UNDEFINED, dataSource=Component.UNDEFINED, defaultPane=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, export=Component.UNDEFINED, legend=Component.UNDEFINED, loadingIndicator=Component.UNDEFINED, margin=Component.UNDEFINED, maxBubbleSize=Component.UNDEFINED, minBubbleSize=Component.UNDEFINED, negativesAsZeroes=Component.UNDEFINED, onArgumentAxisClick=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onDone=Component.UNDEFINED, onDrawn=Component.UNDEFINED, onExported=Component.UNDEFINED, onExporting=Component.UNDEFINED, onFileSaving=Component.UNDEFINED, onIncidentOccurred=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onLegendClick=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPointClick=Component.UNDEFINED, onPointHoverChanged=Component.UNDEFINED, onPointSelectionChanged=Component.UNDEFINED, onSeriesClick=Component.UNDEFINED, onSeriesHoverChanged=Component.UNDEFINED, onSeriesSelectionChanged=Component.UNDEFINED, onTooltipHidden=Component.UNDEFINED, onTooltipShown=Component.UNDEFINED, onZoomEnd=Component.UNDEFINED, onZoomStart=Component.UNDEFINED, palette=Component.UNDEFINED, paletteExtensionMode=Component.UNDEFINED, panes=Component.UNDEFINED, pathModified=Component.UNDEFINED, pointSelectionMode=Component.UNDEFINED, redrawOnResize=Component.UNDEFINED, resizePanesOnZoom=Component.UNDEFINED, resolveLabelOverlapping=Component.UNDEFINED, rotated=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollBar=Component.UNDEFINED, series=Component.UNDEFINED, seriesSelectionMode=Component.UNDEFINED, seriesTemplate=Component.UNDEFINED, size=Component.UNDEFINED, stickyHovering=Component.UNDEFINED, synchronizeMultiAxes=Component.UNDEFINED, theme=Component.UNDEFINED, title=Component.UNDEFINED, tooltip=Component.UNDEFINED, valueAxis=Component.UNDEFINED, zoomAndPan=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'adaptiveLayout', 'adjustOnZoom', 'animation', 'annotations', 'argumentAxis', 'autoHidePointMarkers', 'barGroupPadding', 'barGroupWidth', 'commonAnnotationSettings', 'commonAxisSettings', 'commonPaneSettings', 'commonSeriesSettings', 'containerBackgroundColor', 'crosshair', 'dataPrepareSettings', 'dataSource', 'defaultPane', 'disabled', 'elementAttr', 'export', 'legend', 'loadingIndicator', 'margin', 'maxBubbleSize', 'minBubbleSize', 'negativesAsZeroes', 'onLegendClick', 'onPointClick', 'onSeriesClick', 'palette', 'paletteExtensionMode', 'panes', 'pathModified', 'pointSelectionMode', 'redrawOnResize', 'resizePanesOnZoom', 'resolveLabelOverlapping', 'rotated', 'rtlEnabled', 'scrollBar', 'series', 'seriesSelectionMode', 'seriesTemplate', 'size', 'stickyHovering', 'synchronizeMultiAxes', 'theme', 'title', 'tooltip', 'valueAxis', 'zoomAndPan']
        self._type = 'Chart'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'adaptiveLayout', 'adjustOnZoom', 'animation', 'annotations', 'argumentAxis', 'autoHidePointMarkers', 'barGroupPadding', 'barGroupWidth', 'commonAnnotationSettings', 'commonAxisSettings', 'commonPaneSettings', 'commonSeriesSettings', 'containerBackgroundColor', 'crosshair', 'dataPrepareSettings', 'dataSource', 'defaultPane', 'disabled', 'elementAttr', 'export', 'legend', 'loadingIndicator', 'margin', 'maxBubbleSize', 'minBubbleSize', 'negativesAsZeroes', 'onLegendClick', 'onPointClick', 'onSeriesClick', 'palette', 'paletteExtensionMode', 'panes', 'pathModified', 'pointSelectionMode', 'redrawOnResize', 'resizePanesOnZoom', 'resolveLabelOverlapping', 'rotated', 'rtlEnabled', 'scrollBar', 'series', 'seriesSelectionMode', 'seriesTemplate', 'size', 'stickyHovering', 'synchronizeMultiAxes', 'theme', 'title', 'tooltip', 'valueAxis', 'zoomAndPan']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Chart, self).__init__(**args)
