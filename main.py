import PySimpleGUI as sg
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# UI
sg.theme('DarkAmber')
layout = [[sg.Text('File to be converted:')],
          [sg.In(key='file'), sg.FileBrowse(file_types=(("XML", "*.xml"),))],
          [sg.Text('Product ver.'), sg.InputText(key='product', size=(40, 1),
                                                 default_text='E44CB020-C21D-11D3-8A3F-0010A4EF3494')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

window = sg.Window('SCADA to AB HMI alarm converter', layout)

# Window loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == sg.WIN_CLOSED or event == 'Ok':
        print('You entered ', values['file'])
        tree = ET.parse(str(values['file']))
        root = tree.getroot()

        # Root for converted file
        newRoot = ET.Element("alarms", version="1.0", product=f"{{{str(values['product'])}}}", id="Alarms")

        # Alarm element
        alarm = ET.SubElement(newRoot, "alarm", history_size="128", capacity_high_warning="90",
                              capacity_high_high_warning="99", display_name="", hold_time="250",
                              max_update_rate="1,00", embedded_server_update_rate="1,00", silence_tag="",
                              remote_silence_exp="", remote_ack_all_exp="", status_reset_tag="",
                              remote_status_reset_exp="", close_display_tag="", remote_close_display_exp="",
                              use_alarm_identifier="true", capacity_high_warning_tag="",
                              capacity_high_high_warning_tag="", capacity_overrun_tag="",
                              remote_clear_history_exp="")

        # Triggers element
        triggers = ET.SubElement(alarm, "triggers")

        # Converting trigger data from SCADA to FactoryTalk format
        for n, child in enumerate(root):
            name = f"{child.attrib['Name']}"
            child_input = f"{child.attrib['Input']}"
            prefix_input = f"[PLC]{child.attrib['Input']}"
            trigger = ET.SubElement(triggers, "trigger", id=f'T{n + 1}', type="value", ack_all_value="0",
                                    use_ack_all="false", ack_tag="", exp=f'{{{prefix_input}}}', message_tag="",
                                    message_handshake_exp="", message_notification_tag="", remote_ack_exp="",
                                    remote_ack_handshake_tag="", label=f'{child_input[: 19]} - {name}/>',
                                    handshake_tag="")
        messages = ET.SubElement(alarm, "messages")
        for n, child in enumerate(root):
            name = f"{child.attrib['Name']}"
            child_input = f"{child.attrib['Input']}"
            prefix_input = f"[PLC]{child.attrib['Input']}"
            message = ET.SubElement(messages, "message", id=f'M{n + 1}', trigger_value="1", identifier="1",
                                    trigger="#T{n + 1}", backcolor="#800000", forecolor="#FFFFFF",
                                    audio="false", display="true", print="false", message_to_tag="false",
                                    text=f'{child_input[: 19]} - {name}')

        # Creating new XML
        tree = ET.ElementTree(newRoot)
        tree.write("output.xml", encoding="UTF-8", xml_declaration=True)

        # Formatting new XML
        xml_str = ET.tostring(newRoot, encoding="UTF-8")
        dom = minidom.parseString(xml_str)
        pretty_xml_str = dom.toprettyxml(indent="    ")

        # Write new formatted data to XML
        with open("output.xml", "w", encoding="UTF-8") as f:
            f.write(pretty_xml_str)

window.close()
