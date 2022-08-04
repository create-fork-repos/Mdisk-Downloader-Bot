from pyrogram import Client
from pyrogram import filters
import os
import threading
import mdisk
import split

bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "b8e50a035abb851c0dd424e14cac4c06") 
api_id = os.environ.get("ID", "3704772") 

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

TG_SPLIT_SIZE = 2097151000

@app.on_message(filters.command(["start"]))
def echo(client, message):
    app.send_message(message.chat.id, 'Send link like this >> /mdisk link')

def down(message,link):
    app.send_message(message.chat.id, 'downloading')
    file = mdisk.mdow(link,message)
    size = split.get_path_size(file)
    if(size > 2097151000):
        app.send_message(message.chat.id, 'spliting')
        flist = split.split_file(file,size,file,".", TG_SPLIT_SIZE)
        os.remove(file)
        app.send_message(message.chat.id, 'uploading')
        i = 1
        for ele in flist:
            app.send_document(message.chat.id,document=ele,caption=f"part {i}")#, progress=progress)
            i = i + 1
            os.remove(ele)
    else:
        app.send_message(message.chat.id, 'uploading')
        app.send_document(message.chat.id,document=file)#, progress=progress)
        os.remove(file)


@app.on_message(filters.command(["mdisk"]))
def echo(client, message):
    try:
        link = message.text.split("mdisk ")[1]
        if "mdisk" in link:
            d = threading.Thread(target=lambda:down(message,link),daemon=True)
            d.start()
    except:
        app.send_message(message.chat.id, 'send only mdisk link with command followed by link')

app.run()    
