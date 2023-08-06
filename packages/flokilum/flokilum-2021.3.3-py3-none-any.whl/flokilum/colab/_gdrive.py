def gdrive():

    from google.colab import drive
    from pathlib import Path

    gdrive = "/content/drive"
    gdata  = "/content/drive/MyDrive/data"

    if not Path(gdrive).is_dir():
        drive.mount(gdrive)

    print(F"{'gdrive'.rjust(50)} : {gdata}")

    return Path(gdata)
