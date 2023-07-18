from wsmsg import send_message, send_image, groupListAll
import requests


re = send_image(
    phoneNumber="50763641778",
    image="/home/vaccarieli/308610796_481326877340326_89325846186433607_n.png",
    text="Hi my friends, do you want to see something cool?",
    userKey="Miguel",
    precense_typying=False,
    authorized_ids=["50763641778@s.whatsapp.net", "50760269392@s.whatsapp.net"],
)
