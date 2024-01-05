from Models.Blog import Blog
from Services.BaseService import BaseService

class BlogService(BaseService[Blog]):
    @property
    def model_class(self):
        return Blog