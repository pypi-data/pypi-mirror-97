import abc

class StorageInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook_(cls, subclass):
        return (
            hasattr(subclass, 'disk') and
            callable(subclass.disk) and
            hasattr(subclass, 'put') and
            callable(subclass.put) and
            hasattr(subclass, 'put_image') and
            callable(subclass._image) and
            hasattr(subclass, 'put_image_base64') and
            callable(subclass.put_image_base64) and
            hasattr(subclass, 'delete') and
            callable(subclass.delete) and
            hasattr(subclass, 'get') and
            callable(subclass.get) and
            hasattr(subclass, 'url') and
            callable(subclass.url) and
            hasattr(subclass, 'copy') and
            callable(subclass.copy) and
            hasattr(subclass, 'copy_from_link') and
            callable(subclass.copy_from_link) and
            hasattr(subclass, 'move') and
            callable(subclass.move) and
            hasattr(subclass, 'exists') and
            callable(subclass.exists) and
            hasattr(subclass, 'prepend') and
            callable(subclass.prepend) and
            hasattr(subclass, 'append') and
            callable(subclass.append)
        )


    @abc.abstractmethod
    def disk(self):
        """Load disk"""
        raise NotImplementedError

    @abc.abstractmethod
    def put(self):
        """Put file"""
        raise NotImplementedError

    @abc.abstractmethod
    def put_image(self):
        """Put image file only"""
        raise NotImplementedError

    @abc.abstractmethod
    def put_image_base64(self):
        """Put image from base64"""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self):
        """Delete one file"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self):
        """Get file info"""
        raise NotImplementedError

    @abc.abstractmethod
    def url(self):
        """Return file link"""
        raise NotImplementedError

    @abc.abstractmethod
    def copy(self):
        """Copy a file"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def copy_from_link(self):
        """Copy a file from link"""
        raise NotImplementedError

    @abc.abstractmethod
    def move(self):
        """Move a file"""
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self):
        """Check file is exist"""
        raise NotImplementedError

    @abc.abstractmethod
    def prepend(self):
        """Prepend data to file"""
        raise NotImplementedError

    @abc.abstractmethod
    def append(self):
        """Append data to file"""
        raise NotImplementedError
