from dotenv import load_dotenv
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
    # if len(title) > 60:
    #    title = title[:60]

    wa.send_template(
        to=send_to,
        template=Temp(
            name="shiur2",
            language=Temp.Language.ENGLISH_US,
            body=[
                Temp.TextValue(value=title),
                Temp.TextValue(value=author),
                Temp.TextValue(value=short_name),
            ],
        ),
    )


def send_whatsapp_message_with_video(
    title, author, short_name, video, config: ConfigurationManager, send_to: str = None
):
    if send_to is None:
        send_to = config.WHATSAPP_RECIPIENT_NUMBER
    wa = WhatsApp(
        phone_id=config.WHATSAPP_SENDER_ID,
        token=config.WHATSAPP_TOKEN,
        business_account_id=config.WHATSAPP_BUISNESS_ID,
    )

    wa.send_template(
        to=send_to,
        template=Temp(
            name="shiurvideo",
            language=Temp.Language.ENGLISH_US,
            header=Temp.Video(video),
            body=[
                Temp.TextValue(value=title),
                Temp.TextValue(value=author),
                Temp.TextValue(value=short_name),
            ],
        ),
    )


if __name__ == "__main__":
    load_dotenv()
    config = ConfigurationManager()
    # send_whatsapp_message("Kidushin Daf 62 - מסכת קידושין דף סב", "Rabbi Shloimy Greenwald", "kidushin-62", config)
    vid = "https://www.youtube.com/watch?v=opiHK2HyimA"
    send_whatsapp_message_with_video(
        "Kidushin Daf 62 - מסכת קידושין דף סב", "Rabbi Shloimy Greenwald", "kidushin-62", vid, config
    )
