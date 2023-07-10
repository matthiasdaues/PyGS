import xml.etree.ElementTree as ET


def xml_users(user_credentials: dict()):
    """
    This function creates the xml document "users.xml" that 
    contains users and their credentials.
    The geoserver folder path where the document needs to go is: 
    geoserver_data_dir/security/usergroup/usergroup_name/users.xml
    """

    # Create the root element
    root = ET.Element("userRegistry")
    root.set("xmlns", "http://www.geoserver.org/security/users")
    root.set("version", "1.0")

    # Create the users element
    users = ET.SubElement(root, "users")

    # Create the user element per user in user_credentials
    for user_credential in user_credentials:
        user = ET.SubElement(users, "user")
        user.set("enabled", "true")
        user.set("name", user_credential[0])
        user.set("password", user_credential[1])

    # Create the groups element
    groups = ET.SubElement(root, "groups")

    # Create the XML string
    xml_string = ET.tostring(root, encoding="utf-8").decode()

    # Print the XML output
    print(xml_string)