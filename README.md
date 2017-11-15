# oledterm

Mirror your Linux console terminal output to an OLED display module

Uses [luma.oled](https://github.com/rm-hull/luma.oled) to drive the OLED.
Tested with an SSD1325-based module, 2.7" 128x64, which allows for 9x25 text.

To run on boot, add to /etc/rc.local:

```sh
python /home/pi/oledterm/oledterm.py --display ssd1325 --interface spi --rotate 2 &
```

then attach a keyboard, and you can interact with the terminal as normal.
Example running uname:

![uname](https://user-images.githubusercontent.com/26856618/32824814-52bb1466-c997-11e7-8b0c-00db29a27c76.png)

and since it uses your terminal, even programs like vim work as expected:

![vim](https://user-images.githubusercontent.com/26856618/32824815-52cfa9a8-c997-11e7-9fc2-4309655835d2.png)
