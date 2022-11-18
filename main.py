from PIL import Image
from PIL.PngImagePlugin import PngInfo
import json
import os
from datetime import datetime
import hashlib

jsonfile = "essentials.json"
base_dir = os.path.expanduser('~')

class Tail:
    address = None

def main():    
    try:
        tail = Tail()
        data = json.loads(open(jsonfile).read())
        if(data["tail"]==None):
            img_path = "genesis.png"
            prev_block = 0
            tail.address = -1
        else:
            tail.address = data["tail"]
            
            with open("dir/{}.png".format(tail.address),"rb") as prev_img:
                bytes = prev_img.read()
                prev_block = hashlib.sha256(bytes).hexdigest()

            inp = str(input("Enter the image path inside user directory\n"))
            img_path = os.path.join(base_dir,inp)

        try:
            timestamp = str(datetime.now())
            targetImage = Image.open(img_path)
            metadata = PngInfo()
            metadata.add_text("Previous Block", str(prev_block))
            metadata.add_text("TimeStamp", timestamp)
            
            tail.address = tail.address+1
            with open("essentials.json","w+") as essentials:
                essentials.write(json.dumps(
                    {
                        "tail":tail.address
                    }
                ))

            targetImage.save("dir/{}.png".format(tail.address), pnginfo=metadata)
            targetImage = Image.open("dir/{}.png".format(tail.address))
            print(targetImage.text)


        except:
            print("Wrong Image Path:\n",img_path)
    except:
        print("BlockChain Currupted\nFetch latest from remote")

if __name__ == '__main__':
	main()