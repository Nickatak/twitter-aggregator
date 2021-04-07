from config import DevConfig
class DevConfig:
    # Twitter API Key/Secret/Auth Bearer Token.
    TW_API_KEY = 'pC46hlWxiVSxQc3nPirF4ulh7'
    TW_API_SECRET = 'WQ0Gjw8zeMCCc5lL23XZbwrGaIKcf8HhhB2O03FMS1IP8YsmVs'
    TW_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAPAdJAEAAAAA%2F16Xf%2FDINfTIk1jWxKxDHkm5SHI%3DU8h1wmmwIekrf3slSNoiNeKcLRrnOnTqL1SAufbRrhiyJ6mNCT'

    # We're gonna need this for testing later.
    JSON_INPUT_FILE = 'prefetch_idols.json'
    JSON_OUTPUT_FILE = 'idols.json'

    # Discord Webhook URL (can be found under the server information->integration tab in Discord's client).


    # Pattern is = https://discord.com/api/webhooks/ {author_id} / {Webhhook_id}
    DISC_ORIG_CHANNEL_WEBHOOK_URL = 'https://discord.com/api/webhooks/827765811833602088/rFh8gGFDBlHnid93BlyY8koquAkEopd7yac9zEFKFPDUawy5EAV33C5MiaIueZCLkR0j?wait=true'

    DISC_TRANS_CHANNEL_WEBHOOK_URL = 'https://discord.com/api/webhooks/827765934898937916/vemQ4ppS39HGGxjUarGyvCsoKs9Clt9APUOlsvjyiXb4vYZH1qG1IkrWk3KKYVRle2XO'

    # pottern for a disCOrd message link is: https://discord.com/channels/{server_id}/{channel_id}/{message_id}
    # Discord's server ID can be gotten from enabling the developer mode and right clicking on the server name.
    DISC_SERVER_ID = '824703049658138625'

    DISC_ORIG_CHANNEL_ID = '827221664705019924'
    DISC_TRANS_CHANNEL_ID = '827221743633956865'

    # Microsoft Translation Subscription Key.
    MICROSOFT_API_KEY = '278740e33e0f4c63ab725b18eef4a06b'
    MICROSOFT_REGION = 'westus2'
