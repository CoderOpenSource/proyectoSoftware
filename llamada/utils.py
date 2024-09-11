import time
from agora_token_builder import RtcTokenBuilder

def generate_agora_token(channel_name, uid, role):
    app_id = 'YOUR_AGORA_APP_ID'
    app_certificate = 'YOUR_AGORA_APP_CERTIFICATE'
    expiration_time_in_seconds = 3600
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)
    return token
