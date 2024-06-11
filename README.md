# MUSIC1

youtube-dl -ciw --download-archive videolist.txt --youtube-skip-dash-manifest --write-description --write-info-json --write-thumbnail -o "%(uploader)s/%(playlist_title)s/%(title)s - %(id)s - %(format)s.%(ext)s" "$1"