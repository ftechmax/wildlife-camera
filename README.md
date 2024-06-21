# wildlife-camera
A Raspberry Pi 5 based wildlife camera

## installation

```sh
./install.sh
```

## Reducing power consumption

```sh
sudo rpi-eeprom-config -e
```

Make sure the following settings are configured:

```text
[all]
BOOT_UART=1
WAKE_ON_GPIO=0
POWER_OFF_ON_HALT=1
```