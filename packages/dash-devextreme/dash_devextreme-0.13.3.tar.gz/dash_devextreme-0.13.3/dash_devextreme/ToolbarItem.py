# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ToolbarItem(Component):
    """A ToolbarItem component.


Keyword arguments:
- component (string | dict; optional): An alias for the template property specified in React. Accepts a custom component.
- cssClass (string; optional): Specifies a CSS class to be applied to the item
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- html (string; optional): Specifies html code inserted into the UI component item element
- locateInMenu (a value equal to: 'always', 'auto', 'never'; default 'never'): Specifies when to display an item in the toolbar's overflow menu
- location (a value equal to: 'after', 'before', 'center'; default 'center'): Specifies a location for the item on the toolbar
- menuItemComponent (string | dict; optional): An alias for the menuItemTemplate property specified in React. Accepts a custom component.
- menuItemRender (string; optional): An alias for the menuItemTemplate property specified in React. Accepts a rendering function.
- menuItemTemplate (string | dict; optional): Specifies a custom template for menu items.
- options (dict; optional)
- render (string; optional)
- showText (a value equal to: 'always', 'inMenu'; default 'always')
- template (string | dict; optional)
- text (string; optional)
- visible (boolean; default True): Specifies whether or not a UI component item must be displayed
- widget (a value equal to: 'dxAutocomplete', 'dxButton', 'dxCheckBox', 'dxDateBox', 'dxMenu', 'dxSelectBox', 'dxTabs', 'dxTextBox', 'dxButtonGroup', 'dxDropDownButton'; optional): A UI component that presents a toolbar item. To configure it, use the options object"""
    @_explicitize_args
    def __init__(self, component=Component.UNDEFINED, cssClass=Component.UNDEFINED, disabled=Component.UNDEFINED, html=Component.UNDEFINED, locateInMenu=Component.UNDEFINED, location=Component.UNDEFINED, menuItemComponent=Component.UNDEFINED, menuItemRender=Component.UNDEFINED, menuItemTemplate=Component.UNDEFINED, options=Component.UNDEFINED, render=Component.UNDEFINED, showText=Component.UNDEFINED, template=Component.UNDEFINED, text=Component.UNDEFINED, visible=Component.UNDEFINED, widget=Component.UNDEFINED, **kwargs):
        self._prop_names = ['component', 'cssClass', 'disabled', 'html', 'locateInMenu', 'location', 'menuItemComponent', 'menuItemRender', 'menuItemTemplate', 'options', 'render', 'showText', 'template', 'text', 'visible', 'widget']
        self._type = 'ToolbarItem'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['component', 'cssClass', 'disabled', 'html', 'locateInMenu', 'location', 'menuItemComponent', 'menuItemRender', 'menuItemTemplate', 'options', 'render', 'showText', 'template', 'text', 'visible', 'widget']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ToolbarItem, self).__init__(**args)
