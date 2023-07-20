from _webdrive_ import _webdriver_, download_image
from wsmsg import send_image

# Replace the URL and download_path with your desired values
image_url = (
    "https://cdn.releases.com/img/image/d9738082-9f46-4982-acc9-75305020345d.jpg/300"
)
driver = _webdriver_()
image_base64 = download_image(driver, image_url)

re = send_image(
    phoneNumber="broadcast",
    image=image_base64,
    text="Hi my friends, do you want to see something cool?",
    userKey="Miguel",
    precense_typying=False,
    authorized_ids=["50763641778@s.whatsapp.net", "50760269392@s.whatsapp.net"],
    base64=True,
)
