from django.core.files.storage import FileSystemStorage
# Para guardar archivos con el nombre original del archivo
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Si el archivo existe, elimínalo antes de guardar el nuevo archivo
        if self.exists(name):
            self.delete(name)
        return name
