#%%
import mutagen 
from blessed import Terminal
import inquirer
from inquirer.themes import Default
import argparse

term = Terminal()

class CustomTheme(Default):
    def __init__(self):
        super().__init__() 
        self.List.selection_cursor = "➤"
        self.Checkbox.selection_icon = "➤"
        self.List.selection_color = term.green
        self.Checkbox.selection_color = term.green
        self.Checkbox.selected_color = term.green
        self.Checkbox.unselected_icon = "*"

#%%
def meta_edit():
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', '-p', nargs='?', help='Specify path')
    args = parser.parse_args()
    pth = str(args.path)
    try:
        file = mutagen.File(pth)
    except Exception:
        print(f'Cannot read {pth}')
        quit()
    
    q_edit = [
        inquirer.Checkbox(name='edit',
                            message="Select sections to edit",
                            choices = ["artist","album","lyrics","commentaire","cover","↪ Quit"])
        ]
    
    #* MP3
    if pth.lower().endswith('.mp3'):
        if file.tags is None:
            file.tags = mutagen.id3.ID3()

        a_edit = inquirer.prompt(q_edit, theme=CustomTheme(), raise_keyboard_interrupt=True)["edit"]
        if "↪ Quit" in a_edit:
            quit()
        if "artist" in a_edit:
            edit_artist = str(input(">> Artist : "))
            file.tags['TPE1'] = mutagen.id3.TPE1(encoding=0,text=[edit_artist])
            print('\n')
        if "album" in a_edit:
            edit_album = str(input(">> Album : "))
            file.tags['TALB'] = mutagen.id3.TALB(encoding=0,text=[edit_album])
            print('\n')
        if "commentaire" in a_edit:
            edit_com = str(input(">> Commentaire : "))
            print('\n')
            file.tags['COMM::eng'] = mutagen.id3.COMM(encoded=0,lang='eng',text=[edit_com])
        file.save(v1=3)
    
    #* MP4 - M4A    
    elif pth.lower().endswith('.m4a'):
        if file.tags is None:
            file.tags = mutagen.mp4.MP4Tags()
        
        a_edit = inquirer.prompt(q_edit, theme=CustomTheme(), raise_keyboard_interrupt=True)["edit"]
        if "↪ Quit" in a_edit:
            quit()
        if "artist" in a_edit:
            edit_artist = str(input(">> Artist : "))
            file.tags['©ART'] = [edit_artist]
            file.tags['‘aART’'] = [edit_artist]
            print('\n')
        if "album" in a_edit:
            edit_album = str(input(">> Album : "))
            file.tags['©alb'] = [edit_album]
            print('\n')
        if "commentaire" in a_edit:
            edit_com = str(input(">> Commentaire : "))
            print('\n')
            file.tags['©cmt'] = [edit_com]
        if "lyrics" in a_edit:
            try:
                with open(pth.split('.m4a')[0]+'.txt') as f:
                    lyrics = ''.join(f.readlines())
            except Exception:
                edit_lyr = str(input(">> lyrics.txt path : "))
                print('\n')
                with open(edit_lyr) as f:
                    lyrics = ''.join(f.readlines())
            file.tags['©lyr'] = [lyrics]
        file.save()

#%%            
if __name__=="__main__":
    meta_edit()