#%%
import os
import subprocess
import argparse
from pytube import YouTube, Playlist, Channel
from pythumb import Thumbnail
import mutagen

# ----------------
global AUDIO_DOWNLOAD_DIR, VIDEO_DOWNLOAD_DIR
AUDIO_DOWNLOAD_DIR = "/Users/prld/gPrld/Music/#ytmusic_script/AUDIO"
VIDEO_DOWNLOAD_DIR = "/Users/prld/gPrld/Music/#ytmusic_script/VIDEO"
# ----------------

#%%
#! --------------------------------------
def YoutubeAudioDownload(url):
    '''
    Codec : 
    - alac : apple lossless 
    - aac base codec
    '''    
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio = True, abr="160kbps")[0]
    
    if audio!=[]:
        try:
            unique = " _"+str(len(os.listdir(AUDIO_DOWNLOAD_DIR)))
            FOLDER = AUDIO_DOWNLOAD_DIR+"/"+yt.title+unique
            
            if not os.path.exists(FOLDER):
                os.makedirs(FOLDER)
                print('>>>Downloading...\n')
                audio.download(FOLDER)
                print('>>>Done!\n')
                
                if yt.length>600:            #>10min = mp3 sinon m4a
                    new_filename=FOLDER+"/"+yt.title+".mp3"
                    codc = "libmp3lame"
                else:
                    new_filename=FOLDER+"/"+yt.title+".m4a"
                    codc = "aac"
                    
                default_filename =FOLDER+"/"+yt.title+'.'+audio.mime_type.split("/")[1]
                ffmpeg_command = 'ffmpeg -i "{0}" -c:a {1} -b:a 160k "{2}"'.format(default_filename,codc,new_filename)
                print('>>>FFMPEG is running\n')
                subprocess.run(ffmpeg_command, shell=True)
                
                try:
                    t = Thumbnail(url)
                    t.fetch()
                    t.save(dir=FOLDER,filename="image")
                except:
                    print(f"Thumbnail failure - {yt.title}")
                '''
                try:
                    response = requests.get(yt.thumbnail_url)
                    if response.status_code == 200:
                        with open(FOLDER+"/tb.jpg", 'wb') as file:
                            file.write(response.content)
                except:pass
                '''
                os.remove(default_filename)
            else:
                pass
        except:
            print(f"Audio failure - {yt.title}")
    else:
        print(f"160kbps not available - {yt.title}")

    return audio


#! --------------------------------------
def YoutubeVideoDownload(url):
    '''

    '''    
    yt = YouTube(url)
    res = {0:"2160p",1:"1440p",2:"1080p",3:"720p"}
    c = 0
    query = yt.streams.filter(only_video = True, res=res[c])
    
    while len(query)==0:
        c+=1
        query = yt.streams.filter(only_video = True, res=res[c])
    video = query[0]
    
    try:
        unique = " _"+str(len(os.listdir(VIDEO_DOWNLOAD_DIR)))
        FOLDER = VIDEO_DOWNLOAD_DIR+"/"+yt.title+unique
        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
            print('>>>Downloading...\n')
            video.download(FOLDER)
            print('>>>Done!\n')
    except:
        print(f"Video failure - {yt.title}")

    return video


#! --------------------------------------
def meta_downloader():
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', '-u', nargs='?', help='Specify url')
    parser.add_argument('-mode', '-m', nargs='?', choices=['single', 'p', 'c'], default='single', help='single=video / p=playlist / c=channel')
    
    args = parser.parse_args()
    
    if args.mode=="single":
        YoutubeAudioDownload(url=str(args.url))
        
    elif args.mode=="p":
        playl = Playlist(str(args.url))
        for video in playl.video_urls:
            YoutubeAudioDownload(url=video)
    
    else:
        channel = Channel(str(args.url))
        for video in channel.video_urls:
            YoutubeAudioDownload(url=video)
            
            
#ffmpeg -i "/Users/prld/gPrld/Music/ytmusic_script/Mabisyo - Sun Colored Eyes.webm" "/Users/prld/gPrld/Music/ytmusic_script/Mabisyo - Sun Colored Eyes.mp3"
#ffmpeg -i "/Users/prld/gPrld/Music/#ytmusic_script/Mabisyo - Sun Colored Eyes.webm" -c:a alac -b:a 160k "/Users/prld/gPrld/Music/#ytmusic_script/Mabisyo - Sun Colored Eyes.m4a"

#url = "https://www.youtube.com/watch?v=vGxHVf6RTVY&ab_channel=Mabisyo"
#url = "https://www.youtube.com/watch?v=61Lmk2k542k&ab_channel=MacMiller"
#test = YoutubeAudioDownload(url=url)

#%%
if __name__=="__main__":
    meta_downloader()
    

