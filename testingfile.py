import os
import sys
import subprocess

# if os.geteuid() != 0:
#     subprocess.call(['sudo', 'python3', *sys.argv])
content = """export host=116.206.105.72
export user=pythoqdx_shivam
export passwd=Shyna@623
export database=pythoqdx_Shynachat
export master_telegram_chat_id=479223209
export bot_token=459330012:AAHznymEYmBr1kWHYQz0AEYF05ULAJ977Jw
export shyna_device_id=Shyna_notification_device
export shyna_chat=669082824
export shivam_device=shivam_device
export sender_gmail_account_id=shyna623@gmail.com
export sender_gmail_account_pass=vrdnhnzexisathcx
export master_email_address_is=shivamsharma1913@gmail.com
export imbox_username=shivamsharma1913@gmail.com
export imbox_password=fdnvhwnhekjetdsd
export device_id=VPS_device
export shivam_device_id=Shivam_device
echo System Variable Loaded Successfully
echo the new will be added as well it seems"""
output = os.popen("echo '"+content+"' >> .bashrc").read()
print(output)