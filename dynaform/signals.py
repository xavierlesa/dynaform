# +-+ coding=utf-8 +-+

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def ___(text):
    return bcolors.HEADER + text + bcolors.END


def post_save(form_class, callback):
    save = form_class.save
    def call_signal(cls, *args, **kwargs):
        print "\033[95m"+"signals.post_save"+"\033[0m"
        # instancia
        i = super(form_class, cls).save(*args, **kwargs)
        callback(cls, *args, **kwargs)
        return i
    form_class.save = call_signal

def pre_save(form_class, callback):
    __init__ = form_class.__init__
    def call_signal(cls, *args, **kwargs):
        callback(cls, *args, **kwargs)
        # instancia
        super(form_class, cls).__init__(*args, **kwargs)
    form_class.__init__ = call_signal
