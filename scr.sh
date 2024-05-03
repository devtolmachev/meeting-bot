apt update && apt upgrade && apt install python3.10 python3.10-venv postgresql

$(find $PWD -name 'pip') install -r $(find $PWD -name 'requirements.txt')

chmod +x meeting_bot.service
mv meeting_bot.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable --now meeting_bot.service

