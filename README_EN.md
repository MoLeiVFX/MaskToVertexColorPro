# Mask To Vertex Color Pro User Manual

## Table of Contents
1. [Plugin Introduction](#plugin-introduction)
2. [Installation and Activation](#installation-and-activation)
3. [Interface Guide](#interface-guide)
   - [Title Section](#title-section)
   - [Image File Selection Section](#image-file-selection-section)
   - [Processing Settings Section](#processing-settings-section)
   - [Single Object Processing Section](#single-object-processing-section)
   - [Batch Processing Section](#batch-processing-section)
   - [Tools Section](#tools-section)
   - [Workflow Guide](#workflow-guide)
   - [Version Information](#version-information)
4. [Usage Workflow](#usage-workflow)
5. [Frequently Asked Questions](#frequently-asked-questions)

---

## Plugin Introduction

**Mask To Vertex Color Pro** is a professional Blender add-on that converts mask textures (black and white images or images with transparency channels) into vertex color Alpha channels for 3D models. The add-on supports both single object processing and batch processing, providing rich processing options and blend modes, suitable for game development, 3D rendering, and other scenarios.

### Key Features
- ✅ Support for multiple mask sources (Alpha channel, grayscale values, RGB channels, etc.)
- ✅ Multiple blend modes (Replace, Multiply, Add, etc.)
- ✅ Fast single object processing
- ✅ Batch processing for multiple objects
- ✅ UV coordinate repair and validation functions
- ✅ Support for Simplified Chinese, Traditional Chinese, and English

---

## Installation and Activation

### Installation Steps
1. Download the add-on file (`add-on-MaskToVertexColorPro-vX.X.X.zip`)
2. Open Blender, go to `Edit` > `Preferences` > `Add-ons`
3. Click the `Install...` button
4. Select the add-on `add-on-MaskToVertexColorPro-vX.X.X.zip` file
5. Search for "Mask To Vertex Color Pro" in the add-on list
6. Check the checkbox next to the add-on name to enable it

### Accessing the Add-on
After enabling the add-on, find the **"M2VC Pro"** tab in the right sidebar of the 3D viewport (press `N` to toggle).

---

## Interface Guide

### Title Section

Located at the top of the add-on panel, displaying basic information about the add-on.

#### Version Number
- **Display**: "v2.0"
- **Function**: Shows the current add-on version
- **Description**: Helps users understand the version they are using, facilitating feedback and updates

#### Blender Version Information
- **Display**: "Blender [version number]"
- **Function**: Shows the current Blender version in use
- **Description**: Used for compatibility reference

---

### Image File Selection Section

Used to select and display the mask image file to be used.

#### File Path Display
- **Display**: 
  - If an image is selected: Shows the filename (truncated with "..." if longer than 25 characters)
  - If no image is selected: Shows "No image selected" + question mark icon
- **Function**: Displays the currently selected image file
- **Description**: 
  - If the file doesn't exist, an error icon (red exclamation mark) will appear next to the filename
  - Long filenames are automatically truncated for a clean interface

#### Select Image Button
- **Button Text**: 
  - When no image is selected: "Select Image"
  - When an image is selected: "Change Image"
- **Icon**: Folder icon
- **Function**: Opens the file browser to select a mask image file
- **Description**: 
  - Supports common image formats (PNG, JPG, TGA, etc.)
  - Clicking opens the system file browser
  - After selecting an image, all processing operations (single object and batch) will use this image

---

### Processing Settings Section

Configure various parameters for mask conversion. These settings apply to all processing operations (single object and batch).

#### Mask Source
- **Type**: Dropdown menu
- **Function**: Select the source channel for mask information
- **Options**:
  - **Auto Detect**: The add-on automatically analyzes the image and selects the best mask source (recommended)
  - **Alpha Channel**: Uses the image's transparency channel as the mask (suitable for PNG and other images with transparency)
  - **Grayscale**: Converts RGB colors to grayscale values as the mask (suitable for black and white images)
  - **Red Channel**: Uses the image's red channel as the mask
  - **Green Channel**: Uses the image's green channel as the mask
  - **Blue Channel**: Uses the image's blue channel as the mask
  - **Luminance**: Uses the image's luminance value as the mask
- **Default**: Auto Detect
- **Usage Tips**: 
  - For black and white images, select "Grayscale"
  - For images with transparency, select "Alpha Channel"
  - When unsure, select "Auto Detect"

#### Blend Mode
- **Type**: Dropdown menu
- **Function**: Select how the mask blends with existing vertex colors
- **Options**:
  - **Replace**: Directly replaces existing Alpha values with mask values (most commonly used)
  - **Multiply**: Multiplies mask values with existing Alpha values (for reducing effect)
  - **Add**: Adds mask values to existing Alpha values (for enhancing effect)
  - **Subtract**: Subtracts mask values from existing Alpha values (for inverse effect)
  - **Min**: Takes the smaller value between mask and existing Alpha
  - **Max**: Takes the larger value between mask and existing Alpha
  - **Overlay**: Overlay mode (similar to Photoshop overlay mode)
  - **Screen**: Screen mode (similar to Photoshop screen mode)
- **Default**: Replace
- **Usage Tips**: 
  - For first-time use, select "Replace"
  - If you need to blend with existing vertex colors, select "Multiply" or "Add"

#### Blend Factor
- **Type**: Slider (0.0 - 1.0)
- **Function**: Controls the intensity of the blend effect
- **Description**: 
  - 0.0: No effect
  - 1.0: Full effect (default)
  - Intermediate values: Proportional blending
- **Default**: 1.0
- **Usage Tips**: Used to fine-tune mask intensity, for example, to make the mask effect softer

#### UV Wrap
- **Type**: Toggle button
- **Function**: Wraps UV coordinates outside the 0-1 range back into range
- **Description**: 
  - Enabled: UV coordinates exceeding 1.0 will wrap back to 0.0 (e.g., 1.5 becomes 0.5)
  - Disabled: No wrapping is performed
- **Default**: Enabled
- **Usage Tips**: 
  - If the model has repeating UVs (tiled textures), keep it enabled
  - If UVs outside the range are errors, fix the UVs first

#### UV Clamp
- **Type**: Toggle button
- **Function**: Clamps UV coordinates to the 0-1 range (no wrapping)
- **Description**: 
  - Enabled: UV coordinates will be clamped between 0.0-1.0 (out-of-range parts will be clipped)
  - Disabled: No clamping is performed
- **Default**: Disabled
- **Usage Tips**: 
  - Mutually exclusive with "UV Wrap", usually only one is enabled
  - If UVs outside the range are errors, use this option to prevent sampling wrong areas

#### Flip Vertical
- **Type**: Toggle button
- **Function**: Flips the image vertically (fixes upside-down issues)
- **Description**: 
  - Enabled: Image is flipped vertically
  - Disabled: No flipping
- **Default**: Enabled
- **Usage Tips**: 
  - If the mask direction is opposite to expected, toggle this option
  - Usually required for Blender's UV coordinate system

#### Flip Horizontal
- **Type**: Toggle button
- **Function**: Flips the image horizontally (fixes left-right reversed issues)
- **Description**: 
  - Enabled: Image is flipped horizontally
  - Disabled: No flipping
- **Default**: Enabled
- **Usage Tips**: 
  - If the mask direction is opposite to expected, toggle this option
  - Adjust according to actual results

#### Debug Mode
- **Type**: Toggle button
- **Function**: Enables debug information output
- **Description**: 
  - Enabled: Outputs detailed processing information to the console (for troubleshooting)
  - Disabled: No debug information output
- **Default**: Disabled
- **Usage Tips**: 
  - Only enable when encountering problems
  - When enabled, detailed information will be displayed in Blender's console (Window > Toggle System Console)

---

### Single Object Processing Section

Used for quickly processing the currently selected single object.

#### Vertex Color Attribute Name
- **Type**: Text input field
- **Function**: Specifies the name of the vertex color layer to create or update
- **Description**: 
  - If the specified vertex color layer doesn't exist, the add-on will create it automatically
  - If it already exists, the layer will be updated
- **Default**: "MaskAlpha"
- **Usage Tips**: 
  - You can use meaningful names like "Mask", "Alpha", etc.
  - The name cannot be empty

#### Apply to Current Selected Object Button
- **Button Text**: "Apply to Current Selected Object"
- **Icon**: Alpha channel icon
- **Function**: Applies the mask to the object currently selected in the 3D viewport
- **Prerequisites**: 
  - An image file must be selected
  - An object must be selected in the 3D viewport
- **Description**: 
  - Only processes the currently selected single object
  - If multiple objects are selected, only the first one is processed
  - Results are displayed in the info bar after processing completes

#### Hint Information
- **Display**: 
  - If an image is selected: Shows "Note: Only processes the currently selected single object" + info icon
  - If no image is selected: Shows "Please select an image file first" + info icon

---

### Batch Processing Section

Used for batch processing multiple objects, supporting adding objects to the list, managing the list, and batch applying masks.

#### Object List
- **Type**: Scrollable list
- **Function**: Displays and manages the list of objects to be batch processed
- **List Item Display**:
  - **Checkbox**: Controls whether the object participates in batch processing
  - **Selection Indicator**: Dot icon indicating the currently selected list item
  - **Object Icon**: Identifies this as an object
  - **Object Name**: Displays the object's name
  - **Status Icon**: Shows processing status (Waiting/Processing/Complete/Error)
  - **Status Text**: Brief status description
- **List Operations**:
  - Clicking a list item selects it
  - Checking/unchecking the checkbox enables/disables the object
  - The list displays up to 5 rows, with scrolling for additional items

#### List Operation Buttons (located on the right side of the list)

##### Add Button (+)
- **Icon**: Plus icon
- **Function**: Adds objects currently selected in the 3D viewport to the batch processing list
- **Description**: 
  - You can select multiple objects at once, then click this button
  - Existing objects won't be added again
  - If the list is empty, this button displays as a button with text: "Add Selected Objects to List"

##### Remove Button (-)
- **Icon**: Minus icon
- **Function**: Removes the currently selected list item from the list
- **Description**: 
  - You must first select an item in the list
  - After removal, if the list still has items, the next one is automatically selected

##### Remove Enabled Button (X)
- **Icon**: X icon
- **Function**: Removes all enabled (checked) objects from the list
- **Description**: 
  - Used to quickly clean up processed objects
  - Only removes checked objects, unchecked objects remain

##### Clear All Button (Trash)
- **Icon**: Trash icon
- **Function**: Clears the entire batch processing list
- **Description**: 
  - Removes all objects from the list
  - Operation cannot be undone, use with caution

##### Enable All Button (Checked Checkbox)
- **Icon**: Checked checkbox icon
- **Function**: Enables all objects in the list (checks all)
- **Description**: 
  - Quickly enables all objects for batch processing
  - If objects are already enabled, no duplicate operation occurs

##### Disable All Button (Unchecked Checkbox)
- **Icon**: Unchecked checkbox icon
- **Function**: Disables all objects in the list (unchecks all)
- **Description**: 
  - Quickly disables all objects
  - Used to temporarily exclude all objects, can be re-enabled later

#### Batch Apply Button
- **Button Text**: "Batch Apply to [count] Objects"
- **Icon**: Play icon
- **Function**: Applies mask conversion to all enabled objects in the list
- **Prerequisites**: 
  - An image file must be selected
  - At least one object in the list must be enabled (checked)
- **Description**: 
  - Processes all enabled objects in sequence
  - Each object can have a different vertex color name (set in the list item)
  - Progress and status are displayed during processing
  - Summary is displayed in the info bar after processing completes

#### Batch Processing Hint Information
- **Display**:
  - If there are enabled objects and an image is selected: Shows "Note: Will process all enabled objects in the list ([count] items)" + info icon
  - If there are enabled objects but no image is selected: Shows "Please select an image file first" + info icon
  - If there are no enabled objects: Shows "Please enable at least one object in the list" + info icon
  - If the list is empty: Shows "Batch list is empty" + info icon
- **Function**: Informs users of the current status and operation requirements

#### Usage Instructions (only shown when the list is empty)
- **Display**: 
  - "Usage:" + question mark icon
  - "1. Select multiple objects in the 3D viewport"
  - "2. Click 'Add Selected Objects to List'"
  - "3. Check the objects to process in the list"
  - "4. Click 'Batch Apply to X Objects'"

---

### Tools Section

Provides additional utility tools for assisting with processing.

#### Fix UV Coordinates Button
- **Button Text**: "Fix UV Coordinates"
- **Icon**: UV icon
- **Function**: Fixes UV coordinate issues for the currently selected object
- **Description**: 
  - Fixes invalid UV coordinates (NaN, Infinity, etc.)
  - Normalizes UV coordinates to reasonable ranges
  - Only processes the currently selected object
  - If the object has no UV coordinates, creates a default UV layer
- **Use Cases**: 
  - When mask application shows anomalies, UV coordinates may be problematic
  - Imported models may have UV coordinates with invalid values
  - Preventive repair before processing

#### Validate Model Button
- **Button Text**: "Validate Model"
- **Icon**: Checkmark icon
- **Function**: Checks the status of the currently selected object
- **Check Content**: 
  - UV coordinate layer count and validity
  - Number of invalid UV coordinates
  - Vertex color layer count
  - Polygon and vertex counts
- **Use Cases**: 
  - Check model status before processing
  - Troubleshoot processing failures
  - Understand detailed model information

---

### Workflow Guide

#### Process Steps
1. **Select Image File**
   - Step 1: Select the mask image to use

2. **Configure Processing Settings**
   - Step 2: Adjust processing parameters as needed

3. **Quick Process Single Object (Top)**
   - Step 3: Test the effect with a single object first

4. **Batch Process Multiple Objects (Bottom)**
   - Step 4: Batch apply after confirming the effect

#### Important Notes
- **All operations share the same image and settings**
  - Single object processing and batch processing use the same image and settings for consistency

- **Process single object to test effect first, then batch apply**
  - Recommended workflow: Test with a single object first, confirm the effect, then batch process to avoid batch processing errors

---

### Version Information

Displays the add-on version and author information.

#### Version Details
- **Add-on Version**: Shows the current version number (e.g., v2.0)
- **Optimization Notes**: Shows recent optimization content
- **Author**: 墨泪 (Mo Lei)
- **Homepage**: https://www.kiiiii.com

---

## Usage Workflow

### Quick Start (Single Object Processing)

1. **Open the Add-on Panel**
   - Press `N` in the 3D viewport to open the right sidebar
   - Click the **"M2VC Pro"** tab

2. **Select Image File**
   - Click the **"Select Image"** button
   - Select the mask image file in the file browser

3. **Configure Processing Settings** (Optional)
   - Adjust mask source, blend mode, and other parameters as needed
   - First-time users can keep default settings

4. **Set Vertex Color Attribute Name** (Optional)
   - Enter a name in the "Vertex Color Attribute Name" input field in the "Single Object Processing" section
   - Default value is "MaskAlpha"

5. **Select Object and Apply**
   - Select an object in the 3D viewport
   - Click the **"Apply to Current Selected Object"** button
   - Wait for processing to complete and view the results

### Batch Processing Workflow

1. **Prepare Image and Settings** (Same as single object processing steps 1-3)

2. **Add Objects to List**
   - Select multiple objects to process in the 3D viewport
   - Click the **"Add Selected Objects to List"** button in the batch processing section (or the **"+"** button on the right side of the list)

3. **Manage List**
   - Check the objects to process in the list (unchecked objects will be skipped)
   - You can set different vertex color names for each object (in the list item)
   - Use list operation buttons to manage the list (remove, clear, enable/disable, etc.)

4. **Batch Apply**
   - Confirm that at least one object in the list is enabled
   - Click the **"Batch Apply to X Objects"** button
   - Wait for processing to complete and view the results

### Recommended Workflow

1. **Testing Phase**
   - Select image file
   - Select a test object
   - Use single object processing to test the effect
   - Adjust processing settings as needed
   - Verify that results meet expectations

2. **Batch Processing Phase**
   - After confirming satisfactory test results
   - Add all objects to be processed to the batch list
   - Check each object's settings (vertex color names, etc.)
   - Execute batch processing
   - Check processing results

3. **Troubleshooting** (if needed)
   - If processing fails, use the **"Validate Model"** button to check object status
   - If UVs have issues, use the **"Fix UV Coordinates"** button to repair
   - Enable debug mode to view detailed information

---

## Frequently Asked Questions

### Q1: Why isn't the mask applied correctly?
**Possible Causes**:
- UV coordinates have issues: Use the **"Fix UV Coordinates"** button to repair
- Wrong mask source selected: Try different mask source options
- Image orientation is wrong: Adjust vertical or horizontal flip options
- Object has no UV coordinates: Need to add UV coordinates to the object first

**Solutions**:
1. Use the **"Validate Model"** button to check object status
2. Try different mask sources (e.g., change from "Auto Detect" to "Alpha Channel" or "Grayscale" or other channel options)
3. Adjust flip options
4. Enable debug mode to view detailed information

### Q2: Some objects fail during batch processing?
**Possible Causes**:
- Object has no UV coordinates
- Object is not a mesh object
- UV coordinates are invalid (NaN or Infinity)

**Solutions**:
1. Use the **"Validate Model"** button to check failed objects
2. Use the **"Fix UV Coordinates"** button to repair problematic objects
3. Ensure all objects are valid mesh objects

### Q3: How to view processing results?
**Methods**:
- View vertex colors in the Material Editor
- Enable vertex color display in viewport shading mode
- Use the **"Validate Model"** button to view vertex color layer information

### Q4: Can vertex color names be customized?
**Yes**:
- Single object processing: Enter a custom name in the "Vertex Color Name" input field
- Batch processing: You can set different vertex color names for each object in the list items

### Q5: Which operations are affected by processing settings?
**All Operations**:
- Both single object processing and batch processing use the same processing settings
- After changing settings, all subsequent operations will use the new settings
- It's recommended to test new settings with a single object before batch processing

### Q6: How to remove objects from the batch list?
**Methods**:
- Select a list item and click the **"-"** button to remove a single object
- Click the **"X"** button to remove all enabled objects
- Click the **"Trash"** button to clear the entire list

### Q7: What image formats does the add-on support?
**Supported Formats**:
- PNG (recommended, supports transparency)
- JPG/JPEG
- TGA
- Other image formats supported by Blender can be tried, please test them yourself

### Q8: How to switch languages?
**Method**:
- Change the interface language in Blender's preferences
- The add-on automatically adapts to Simplified Chinese, Traditional Chinese, and English
- Restart Blender or reload the add-on for changes to take effect
- Note: Due to unknown issues with Traditional Chinese not working in Blender 4.0+, versions 4.0+ do not support Traditional Chinese

---

## Technical Support

For questions or suggestions, please visit:
- **Homepage**: https://www.kiiiii.com
- **Author**: 墨泪 (Mo Lei)

---

**Document Version**: 1.0  
**Last Updated**: 2025  
**Add-on Version**: v2.0.4

