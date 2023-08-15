# SCADA to FactoryTalk Alarm Converter

This project is designed to convert an XML file containing alarm data from an unknown SCADA system into a FactoryTalk format. The SCADA system was unknown to me because our client wasn't able to provide more than an .xml file containing alarms. The script utilizes the `PySimpleGUI` library for GUI and the `xml.etree.ElementTree` and `xml.dom.minidom` modules for XML manipulation.

## Purpose

The purpose of this project is to streamline the process of converting alarm data stored in an XML file from an unfamiliar SCADA system to a format that is compatible with FactoryTalk. Original plan was to copy alarms 'by hand'. This simple interface spared me from doing that.

## How It Works

1. Select an input XML file (containing SCADA alarm data) and specify a product version provided by Factory Talk (easiest way to check this is to export alarms from FactoryTalk to XML and copying 'product' value. **This step is not necessary, but I've included this option in case of any compatibility problems during the import. The conversion can still proceed without the correct product version.**)
2. Upon clicking the "Ok" button, the script reads the input XML file using the `xml.etree.ElementTree` module.
3. The root element of the input XML is parsed to extract relevant alarm information.
4. The script creates a new XML structure using `xml.etree.ElementTree`, formatted according to the FactoryTalk specification.
5. Alarm and trigger elements are created based on the information extracted from the input XML.
6. The new XML structure is written to an "output.xml" file in both raw and pretty-printed formats.
7. The GUI loop continues until the user clicks the "Cancel" button or closes the window.

## To do
This is a basic tool with limited usage. If the need arises, I will add more configuration options for alarms, such as colors and trigger values.

## Note

It's important to ensure that the input XML file follows a specific structure that the script can interpret accurately (see file in 'example SCADA alarms'). Although it can be used as a base for other converters with a similar purpose.

## License

[MIT](https://choosealicense.com/licenses/mit/)