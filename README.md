Ruckus ZF7363 OpenWrt factory upgrade image tools
====================================================

`create_ruckus_fw_image.py` can be used to create a firmware image from any OpenWrt image that is flashable with the stock Ruckus firmware.

Usage example:
```bash
create_ruckus_fw_image.py openwrt-24.10.0-ath79-generic-ruckus_zf7363-squashfs-sysupgrade.bin
```

The resulting factory image is written to `factory.bin` and can be flashed using the web UI or in a busybox root shell using the `fw upgrade` command (just type `fw` to get a help output).
Instructions on how to get a root shell can be found in the [original OpenWrt commit message](https://git.openwrt.org/?p=openwrt/openwrt.git;a=commit;f=target/linux/ath79/image/generic.mk;hb=0eebc6f0ddb0791406d30530e3fc25d39428bd5a).


