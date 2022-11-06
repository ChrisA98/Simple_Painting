# Simple_painting
 A drawing program designed for CSC550- Graphics Programing
 This project allows for creation of images using primitive shapes and saving them as png or jpeg files. Users can also save and load prject files a CHD files

## Controls:
### Buttons :
 - Line Tool - creates a single line
 - Bezier Line Tool - creates an up to quint bezier curve
 - Pixel Draw Tool - draw with a pixel brush
 - Triangle Tool - creates a traingle
 - Rectangle Tool - creates a rectangle from two points
 - Filled Rectangle Tool - creates a filled rectangle from two points
 - Ellipse Tool - creates an ellipse based on a center point, radius 1 and radius 2 value 
 - Fill Tool - fills the background with the current color
 - Save - saves current image as a PNG or JPEG
 - Load - load file from .chd file and clear current drawing
 - Export - create a .chd file from current content
 - Import - import a .chd file as a single layer (ignores imported background color)
 - Undo - either deletes previous point if drawing a shape, or deletes previous shape
 - Redo - recovers undone shape or brush stroke to current layer
 - Add Layer - adds new layer with procedural name
 - Remove Layer - deletes the active layer
 - Layer up - move layer upward
 - Layer down - move layer down
 - Layer Visibilty - make layer visible or not
 - Confirm (Green Button)- saves the current shape or pixel array to image storage
 - Cancel (Red Button) - cancels current shape.
### Sliders
 - RGB Sliders - control the Red, Green, and Blue values for the current shape being drawn
 - Line Size - controls the current shape's line width
 - Zoom - controls the scale of the entire image
### KeyBind Controls
 - Right Control + Z: either deletes previous point if drawing a shape, or deletes previous shape
 - Right Control + Y: recovers undone shape or brush stroke to current layer
 - Tab: switches between urrent points on shape being created to edit previous points.
 - Escape: closes program.
