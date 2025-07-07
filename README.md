# ip-change-notifier
Checks for IP changes and sends an email if ti does.

# Installation

1. Git Clone `git@github.com:zukoma/ip-change-notifier.git`
2. cd ip-change-notifier
3. Edit .env
4. Install requirements `pip install -r requirements.txt` 
5. Create a Systemmd job to run this automatically
   `sudo nano /etc/systemd/system/ip-notify.service`

  ```
[Unit]
Description=Public IP Notifier

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/marius/ip-change-notifier/ip_notify.py
WorkingDirectory=/home/user/ip-change-notifier
```

Create a timer
`sudo nano /etc/systemd/system/ip-notify.timer`

```
[Unit]
Description=Run IP Notifier every 4 hours

[Timer]
OnBootSec=5min
OnUnitActiveSec=4h
Unit=ip-notify.service

[Install]
WantedBy=timers.target
```
Enable and start service
```
sudo systemctl daemon-reexec
sudo systemctl enable --now ip-notify.timer
sudo systemctl start ip-notify.service
```
