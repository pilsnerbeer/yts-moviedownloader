# yts-moviedownloader
YTS Movie downloader used to download movies from YTS / YIFY Movies designed to work with QBittorrent.

Usage:

in QBittorrent, enable WebUI and fill in authentication details. Optionally disable authentication on localhost

![Screenshot_1](https://user-images.githubusercontent.com/36133540/194145287-739590ac-7933-4040-a0af-2bf53a6c0ac5.png)

Run YTSDownloader either from source or .exe. Follow installation details. Config.ini file will be created in the directory with configuration details.

------

username = username for webui

password = password for webui

savelocation = <C:/folder/folder/>

ytssource = https://yts.mx/ # Can change API source. Useful in case of outage

networkaddr = http://127.0.0.1:8080 # Default WebUI listening port

sequentialdownload = yes # Movies will download sequentially 

allow4k = no # Download 4K quality movies. Default= no (Max. 1080p)

------



Additionally, you will find 'trace.log' (basic logging) and 'history.txt' (history of downloaded movies).

