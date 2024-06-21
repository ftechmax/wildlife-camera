#!/bin/bash

if [ "$EUID" -ne 0 ]
then
    exec sudo -s "$0" "$@"
fi

echo "[INFO] Installing dependencies"
apt update
apt install -y ffmpeg python3 python3-pip
apt install -y python3-picamera2 --no-install-recommends


echo "[INFO] Installing pip packages"
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
deactivate


echo "[INFO] Installing service"
cat <<EOF >>/etc/systemd/system/wildlife-camera.service
[Unit]
Description=A Raspberry Pi 5 based wildlife camera
After=syslog.target network.target

[Service]
WorkingDirectory=/home/niels/wildlife-camera
ExecStart=/home/niels/wildlife-camera/.venv/bin/python3 main.py

Restart=always
RestartSec=120

[Install]
WantedBy=multi-user.target
EOF


echo "[INFO] Starting service"
systemctl daemon-reload
systemctl enable wildlife-camera
systemctl start wildlife-camera

sudo -k