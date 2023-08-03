from collections import UserDict
from datetime import date  

class Field:
    """
    родительский класс всех полей
    поле для ввода новых данных в записную книгу
    """
    def __init__(self, value: str) -> None:
        self.__valid_value(value)

        self._value = None
        self._value = value
      
    @classmethod # тут может статик_метод?
    def __valid_value(cls, value) -> None:
        if type(value) != str:
            raise TypeError('received data must be STR') 
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str) -> None:
        self.__valid_value(value)
        self._value = value

    def __str__(self) -> str:
        if self.value == None:
            return f""
        return f'{self.value}'
        

class Name(Field):
    """
    поле имени, принимает любую стр без проверки
    """
    def __init__(self, value: str) -> None:
        super().__init__(value)
        # self.__valid_value(value)


class Phone(Field):
    """
    поле номера телефона, принимает стр(только цифри)
    """
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.__valid_phone(value)
        
    @classmethod # тут может статик_метод? 
    def __valid_phone(cls, value) -> None:
        # тут нужна проверка на стр?
        phone = ''.join(filter(str.isdigit, value))
        if 9 >= len(phone) <= 15 : #псевдо проверка номера
            raise ValueError("Phone number isn't correct")    

    @Field.value.setter
    def value(self, value: str) -> None:
        self.__valid_value(value)
        self._value = value
      
class FormatDateError(Exception):
    pass

class Birthday(Field):
    """
    поле дати рождения, принимает любую стр без проверки
    """
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.__valid_value(value)
        
   
    @classmethod
    def __valid_value(cls, value) -> None:
        # тут нужна проверка на стр?
        try:
            value = date.fromisoformat(value)
        except Exception: 
            raise FormatDateError('not correct date isoformat >>> yyyy-mm-dd')
            
    @Field.value.setter
    def value(self, value: str) -> None:
        self.__valid_value(value)
        self._value = value
      
class RecordNotBirthdayError(Exception):
    pass

class Record:
    """
    класс которий содержит в себе все поля и методи работи с ними
    add/remove/change phone + day to birthday
    """
  
    def __init__(self, name: Name, phone: Phone, birthday: Birthday=None ) -> None:
        
        name = self.try_valid_type_name(name)
        phone = self.try_valid_type_phone(phone)
        birthday = self.try_valid_type_birthday(birthday)

        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday if birthday else None

    @staticmethod
    def try_valid_type_name(name): 
        if type(name) != Name:
            try:
                return Name(name) # тут перезаписуємо змінну name в обькт классу
            except Exception: 
                raise ValueError (f"name:'{name}' must be type(Name) or valid like Name.obj")
        return name    

    @staticmethod
    def try_valid_type_phone(phone):
        if type(phone) != Phone:
            try:
                return Phone(phone)
            except Exception:
                raise ValueError(f"phone:{phone} must be type(Phone) or valid like Phone.obj")
        return phone    

    @staticmethod
    def try_valid_type_birthday(birthday):    
        if type(birthday) != Birthday and birthday != None:
            try:
                return Birthday(str(birthday))
            except Exception: 
                raise ValueError(f"birthday:{birthday} must be type(Birthday) or None / or valid like Birthday.obj")
        return birthday    
       
        
    def __str__(self) -> str:# для принта рекорда..не знаю как принято..сделал как чувствую
        birthday_str = "birthday: "+str(self.birthday) if self.birthday != None else ""
        phones_str = " ".join([ph.value for ph in self.phones]) 
        return f'<Record> name: {self.name} -->> phone(s): {phones_str} {birthday_str}'

    def add_phone(self, phone: Phone):
        phone = self.try_valid_type_phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        phone = self.try_valid_type_phone(phone)
        if phone not in self.phones:
            raise KeyError(f"The phone '{phone}' is not in the record.")
        self.phones.remove(phone)
        
    def change_phone(self, old_phone: Phone, new_phone : Phone):
        old_phone = self.try_valid_type_phone(old_phone)
        new_phone = self.try_valid_type_phone(new_phone)
        if old_phone in self.phones: # если номер входит получаем индекс 
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        else:
            raise ValueError(f"The phone '{old_phone.value}' is not in this record '{self.name}'.")

    def days_to_birthday(self) -> int :
        """
        метод считает количество дней до др
        если др не указано  - ошибка
        """
        if self.birthday == None:
            raise RecordNotBirthdayError
        today = date.today()
        bday = date.fromisoformat(self.birthday.value).replace(year=today.year) # дата др в этом году 
        if today > bday : # если др уже прошло берем дату следующего(в следующем году)
           bday= bday.replace(year=today.year+1)
        return (bday - today).days
          
class AddressBook(UserDict):
    """
    класс хранилише записной книги  - словарь
    "имя" : обьект рекорд    которий содержит все поля(и методи) в соответствии
    TODO Singelton?
    """
    
    def add_record(self, record: Record):
        if type(record) != Record:
            raise TypeError("Record must be an instance of the Record class.")
        self.data[record.name.value] = record 
    
    def iterator(self, item_number: int) -> str:
        """ возвращает строку содержащую объеденение значений словаря 
            в количестве item_number за раз + хвост
            TODO красивий(табличний .format принт)
        """
        if item_number > len(self.data): 
            item_number = len(self.data)
        counter = 0
        result = ""
        for id_, record in self.data.items(): # так как ми наследуемся от UserDict може юзать кк словарь
            result += f"{str(record)}\n"
            counter += 1
            
            if not counter % item_number: # условие для вивода в количестве item_number накоплений
                yield result
                result = ""
            elif counter == len(self.data) - len(self.data) % item_number + 1: # условие для хвоста
                yield result
    
    
if __name__ == '__main__':

    name_1 = Name('Bill')
    phone_1 = Phone('1234567890')
    b_day_1 = Birthday('1994-02-26')

    name_2 = Name('serg')
    phone_2 = Phone('1234567890')
    b_day_2 = Birthday('1994-02-26')
    
    name_3 = Name('Oleg')
    phone_3 = Phone('1234567890')
    b_day_3 = Birthday('1994-02-26')

    name_4 = Name('яяЯнаа')
    phone_4 = Phone('1234567890')
    b_day_4 = Birthday('1994-02-26')

    rec_1 = Record("Лена", "1234554545", "1994-10-26")
    rec_2 = Record("Охрана", phone_2, b_day_2)
    rec_3 = Record("а я не Лена", phone_3, b_day_3)
    rec_4 = Record(name_4, phone_4, b_day_4)
    ab = AddressBook()
    ab.add_record(rec_1)
    ab.add_record(rec_2)
    ab.add_record(rec_3)
    ab.add_record(rec_4)
    for i in ab.iterator(3):
        print(i)
    
    # name = Name('Bill')
    # phone = Phone('1234567890')
    # b_day = Birthday('1994-02-26')
    # rec = Record(name, phone, b_day)
    # print(rec.phones[0].value)
    # print(rec.birthday.value)
    # print(rec.days_to_birthday())
    # name = Name('Bill')
    # phone = Phone('1234567890')
    # b_day = Birthday('1994-02-26')
    # rec = Record(name, phone, "1994-02-26")
    # ab = AddressBook()
    # ab.add_record(rec)
    # assert isinstance(ab['Bill'], Record)
    # assert isinstance(ab['Bill'].name, Name)
    # assert isinstance(ab['Bill'].phones, list)
    # assert isinstance(ab['Bill'].phones[0], Phone)
    # assert isinstance(ab['Bill'].birthday, Birthday)
    # assert ab['Bill'].phones[0].value == '1234567890'
    # print('All Ok)')  
    # # a = Field("name")
    # num = Phone('12345678974')
    # print(a.value)
    # print(num.value)
    # num.value = "987654321123"
    # print(num.value)
    # day = Birthday('1994-02-26')
    # day.value = '1994-26-02'
    # print(day.value)

    





