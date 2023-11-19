from django.core.files.storage import FileSystemStorage

class CustomStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'storage/'
        super().__init__(*args, **kwargs)
