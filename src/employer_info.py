class EmployerInfo:
    employer_id: int
    name: str
    employer_url: str  # сайт работодателя
    city: str
    url: str  # профиль работодателя

    __slots__ = ("employer_id", "name", "employer_url", "city", "url")

    def __init__(self, employer_id, name, employer_url, employer_city, url):
        self.employer_id = employer_id
        self.name = name
        self.url = url
        self.employer_url = employer_url
        self.city = employer_city

    @classmethod
    def add_employer(cls, employer_dict: dict):
        """Метод для создания объектов класса из словаря"""
        return cls(**employer_dict)
