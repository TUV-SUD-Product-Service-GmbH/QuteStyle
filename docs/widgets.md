# Widgets

## BaseWidget

The BaseWidget aims to define the properties ICON, NAME and GROUPS. 
The Icon and the name will be displayed at the left column of the application.
By setting the target group, the developer can specify for which User/Group the widget will be visible.

### MainWidget

The MainWidgets are displayed in the main section. The class provides basic functionalities, such as shutdown and custom widget settings.

The shutdown of the whole application waits for all MainWidgets to emit the signal shutdown completed. 
To implement custom shutdown behaviour on needs to override ```request_shutdown``` or ```shutdown```.

To display MainWidget specific settings, one can implement a Widget and return it as the settings_widget property of the MainWidget.
The specific settings are then added to the global settings, and only displayed if the user activated the associated MainWidget (see [SettingsBaseWidget](#settingsbasewidget) for more details). 

### SettingsBaseWidget

Serves as BaseClass for the global settings. To have settings displayed independent of the active MainWidget, set the widget into the layout with "_set_global_widget".
When the user activates a new widget ```on_main_wigdet``` or chooses to display the settings, the SettingsBaseWidget is cleared ("clear_widget") first. 
Then, if local settings are available, they are added ```add_widget```.

## QuteMessageBox

The QuteMessageBox can display four types of messages. The general style (i.e. background color, layout and frame) 
is the same, and the use the same functionality for their display. Via ```_show_message_box``` all types display their message with
and individual title, text, icon, and buttons. The following types are available as a class property.

- Information
- Warning
- Critical
- Question

Example:

```plaintext
    QuteMessageBox.information(
                self,
                "Information Title",
                "Please use the messagebox as described here."),
            )
```


## Color Manager

### ColorWidget

This widget displays a color with an associated palette-button, to open the QColorDialog and pick a new color. 
When the color was changed, the widget emits "color_changed" signal, such that the application can update this color in use.

### ColorManager

A BaseWidget, that can be used to change and test the different color properties of the application. 
For each color key in the style (i.e. background-color, foreground, ...) an instance of [ColorWidget](#colorwidget) is created. 
Now the user can adjust single colors to his interest. When the ColorManger receives a "color_changed" signal, the slot "on_color_changed" is activated,
a new theme is created, and the window is updated.
The paintEvent checks whether the theme has change before painting.

## CreditBar

## Div

## CornerGrip

## Edge Grip

## StyledComboBox

## TextTruncator

## Toggle

## ToolTip

## Buttons
We implemented several types of custom Buttons for higher conformity with the application's style.

### Icon
The Icon class is used for LeftColumn but also as a base for custom buttons. The user needs to define size, color name
and the icon path. The Icon can be used directly in the ui-file, and the path can be set later. If a paint event occurs,
the class calculates the size according to the device's pixel ratio and retrieves the themes color information. Then it gets
the QPixmap from the [PixmapStore](./style.md#pixmapstore).

```plaintext
    icon = Icon(18, "background")
    icon.set_icon(":/path_to_icon.svg")
````

Attention: The Icon class inherits from QWidget, not QIcon.

### DropLabel

### IconButton

The IconButton is the QPushButton, which can display an icon with text and implements custom hover, pressed and released behaviour.
In the test-application it is used for the MainWidgets, where the Buttons are located on the left column, and the corresponding widget
can be selected. The default color of the IconButton are defined via the BackgroundColorNames, which can set also during instantiation:

```plaintext
BackgroundColorNames(
    hovering="bg_elements",
    background="transparent",
    pressed="dark_two",
    released="bg_elements",
```

The color of icon and text is defined as "foreground". To change text or icon later on, use the methods ```setText```and ```set_icon```.

### IconTooltipButton

The behaviour of the IconTooltipButton is similar to the IconButton, with the addition of showing a custom [ToolTip](#tooltip). It serves as a superclass
for [TitleButton](#titlebutton) and [LeftMenuButton](#leftmenubutton), which need to implement ```_get_tooltip_coords```
individually. Set the tooltips via ```tooltip_text```.

### LeftMenuButton and TitleButton


### LeftColumnCloseButton