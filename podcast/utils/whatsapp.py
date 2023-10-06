from pywa import WhatsApp
from pywa.types import Template as Temp

from podcast.utils.configuration_manager import ConfigurationManager


def send_whatsapp_message(title, author, short_name, config: ConfigurationManager, send_to: str = None):
    if send_to is None:
        send_to = config.WHATSAPP_RECIPIENT_NUMBER
    wa = WhatsApp(
        phone_id=config.WHATSAPP_SENDER_ID,
        token=config.WHATSAPP_TOKEN,
        business_account_id=config.WHATSAPP_BUISNESS_ID,
    )
    # ensure title is 60 char or less
    if len(title) > 60:
        title = title[:60]

    wa.send_template(
        to=send_to,
        template=Temp(
            name="shiur",
            language=Temp.Language.ENGLISH_US,
            header=Temp.TextValue(value=title),
            body=[
                Temp.TextValue(value=author),
                Temp.TextValue(value=short_name),
            ],
            buttons=[
                Temp.UrlButtonValue(value=f"{short_name}-YouTube"),
                Temp.UrlButtonValue(value=f"{short_name}-Spotify"),
            ],
        ),
    )
