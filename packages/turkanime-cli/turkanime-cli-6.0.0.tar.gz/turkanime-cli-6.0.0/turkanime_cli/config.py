from os import path,name,mkdir

def get_config():
    """ Kullanıcı klasöründe eğer yoksa TurkAnimu.ini dosyasın oluştur """
    confdir = path.join( path.expanduser("~"), "TurkAnimu.ini" )
    if not path.isfile( confdir ):
        with open(confdir,"w") as f:
            f.write(
            "[TurkAnime]\n"+
            "manuel fansub = False\n"+
            "izlerken kaydet = False\n"+
            "indirilenler = .\n"
            )
    return confdir

class Config:
    """ Path to files """
    config_path=get_config()
