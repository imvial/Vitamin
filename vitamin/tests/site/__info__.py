class SiteInfo():
    
    """
    Класс, содержащий информацию о сайте, основанном
    на фреймворке Vitamin. Данный класс является прототипом,
    его заполненная копия помещается в корень vitamin- сайта
    в файл __info__.py и не модифицируется пользователем
    или разработчиками сайта.
    """

    __name = """test"""
    __description = """Simple site for tests"""
    __version = """0.1"""
    __authors = """fnight"""
    __vitamin_version = """0.0.1"""

    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    @property
    def version(self):
        return self.__version
    
    @property
    def authors(self):
        return self.__authors
    
    @property
    def vitamin(self):
        return self.__vitamin_version
