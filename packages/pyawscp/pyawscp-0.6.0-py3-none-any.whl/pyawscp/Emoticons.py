import os

class Emoticons:
    _PROMPT      = ['⛅','⛅']
    _WAITING     = ['💤💤💤','☕☕☕']
    _SEE_YA      = ['👋','✌']
    _ERROR       = ['❌💣','❌☠']
    _TOOL        = ['🔧','⚒']
    _THUMBS_UP   = ['👍','✔']
    _POINT_RIGHT = ['👉','❖']
    _WINK        = ['😉','☻']
    _OPS         = ['😕','☹']
    _PIN         = ['📌','✎']
    _ENV         = ['📝','✍']
    _TIME        = ['🕘','☕']
    _WAIT_DISTR  = ['🍺','♨']
    _WAIT_DISTR2 = ['🍼','⚾']
    _MAGNIFIER   = ['🔍','☌']
    _BLOCKS      = ['📦','❒']
    _REDMARK     = ['🔴','⚫']
    _UPLOAD      = ['📤','✈']
    _UPLOAD_PART = ['🔹','➩']
    _FOLDER      = ['🔹','➩']
    _OK          = ['✅','✅']
    _COOKIE      = ['🍪','⚫']
    _IMGS        = [
                     ['🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛','🕐','🕑'],
                     ['☰','☱','☲','☴','☵','☶','☷','☶','☴']
                   ]

    @staticmethod
    def isWindows():
        return 1 if os.name == "nt" else 0
    
    @staticmethod
    def cookie():
        return Emoticons._COOKIE[Emoticons.isWindows()]
    @staticmethod
    def prompt():
        return Emoticons._PROMPT[Emoticons.isWindows()]
    @staticmethod
    def waiting():
        return Emoticons._WAITING[Emoticons.isWindows()]    
    @staticmethod
    def seeYa():
        return Emoticons._SEE_YA[Emoticons.isWindows()]
    @staticmethod
    def error():
        return Emoticons._ERROR[Emoticons.isWindows()]
    @staticmethod
    def tool():
        return Emoticons._TOOL[Emoticons.isWindows()]
    @staticmethod
    def thumbsUp():
        return Emoticons._THUMBS_UP[Emoticons.isWindows()] 
    @staticmethod
    def pointRight():
        return Emoticons._POINT_RIGHT[Emoticons.isWindows()]
    @staticmethod
    def wink():
        return Emoticons._WINK[Emoticons.isWindows()]
    @staticmethod
    def pin():
        return Emoticons._PIN[Emoticons.isWindows()]
    @staticmethod
    def env():
        return Emoticons._ENV[Emoticons.isWindows()]
    @staticmethod
    def time():
        return Emoticons._TIME[Emoticons.isWindows()]
    @staticmethod
    def waitDistract():
        return Emoticons._WAIT_DISTR[Emoticons.isWindows()]
    @staticmethod
    def waitDistract2():
        return Emoticons._WAIT_DISTR2[Emoticons.isWindows()]
    @staticmethod
    def ops():
        return Emoticons._OPS[Emoticons.isWindows()]
    @staticmethod
    def magnifier():
        return Emoticons._MAGNIFIER[Emoticons.isWindows()]
    @staticmethod
    def ok():
        return Emoticons._OK[Emoticons.isWindows()]    
    @staticmethod
    def redMark():
        return Emoticons._REDMARK[Emoticons.isWindows()]        