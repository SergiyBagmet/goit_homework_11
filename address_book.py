from collections import UserDict
from datetime import date  

class Field:
    """
    родительский класс всех полей
    поле для ввода новых данных в записную книгу
    """
    def __init__(self, value: str) -> None:
        self._value = None
        self._value = value
      
         
    @staticmethod
    def __valid_value(value) -> bool:
        return type(value) == str 

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        if self.__valid_value(value) :
           self._value = value
        else:
            raise ValueError('received data must be STR')    
        

class Name(Field):
    """
    поле имени, принимает любую стр без проверки
    """
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    """
    поле номера телефона, принимает стр(только цифри)
    """
    def __init__(self, value: str) -> None:
        if self.__valid_value(value):
             super().__init__(value)
        else:
            raise ValueError("Phone number isn't correct")    

    @staticmethod
    def __valid_value(value) -> bool:
        if type(value) == str:  # TODO как тут сделать через супер?
            phone = ''.join(filter(str.isdigit, value))
            return 10 <= len(phone) <= 15 #псевдо проверка номера
        else: 
            raise ValueError('received data must be STR')    

    @Field.value.setter
    def value(self, value: str): 
        if self.__valid_value(value):
            self._value = value
        else:
            raise ValueError("Phone number isn't correct") 

class Birthday(Field):
    """
    поле дати рождения, принимает любую стр без проверки
    """
    def __init__(self, value: str) -> None:
        if self.__valid_value(value):
            super().__init__(value)
        else:
            raise ValueError('not correct date isoformat >>> yyyy-mm-dd')    
            

    @staticmethod
    def __valid_value(value) -> bool:
        if type(value) == str:
            try:
                valid_date = date.fromisoformat(value)
                return True
            except ValueError:
                return False
        else:
            raise ValueError('received data must be STR')      

    @Field.value.setter
    def value(self, value: str): 
        if self.__valid_value(value):
            self._value = value
        else:      
            raise ValueError('not correct date isoformat >>> yyyy-mm-dd') 
        
class Record:
    """
    класс которий содержит в себе все поля и методи работи с ними
    сейчас простая реализация add/remove/change phone 
    """
  
    def __init__(self, name: Name, *phones: list[Phone], birthday: Birthday = None ) -> None:
        self.name = name
        self.phones = list(phones)
        if birthday:
            self.birthday = birthday

    def add_phone(self, phone: Phone):   
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError(f"The phone '{phone.value}' is not in the record.")
    
    def change_phone(self, old_phone: Phone, new_phone : Phone):
        if old_phone in self.phones: # если номер входит получаем индекс 
            index = self.phones.index(old_phone)
            if not isinstance(new_phone, Phone):
                raise ValueError("Phone must be an instance of the Phone class.")
            self.phones[index] = new_phone
        else:
            raise ValueError(f"The phone '{old_phone.value}' is not in the record.")

    def days_to_birthday(self) -> int :
        today = date.today()
        bday = date.fromisoformat(self.birthday.value).replace(year=today.year)
        if today > bday :
           bday= bday.replace(year=today.year+1)
        return (bday-today).days
            
            
         
    
class AddressBook(UserDict):
    """
    класс хранилише записной книги  - словарь
    "имя" : обьект рекорд которий содержит все поля(и методи) в соответствии с этим именем 
    """
    
    def add_record(self, rec: Record):
        if not isinstance(rec, Record):
            raise ValueError("Record must be an instance of the Record class.")
        self.data[rec.name.value] = rec


if __name__ == '__main__':

    name = Name('Bill')
    phone = Phone('1234567890')
    bday = Birthday('1994-02-26')
    rec = Record(name, phone, birthday=bday)
    print(rec.phones[0].value)
    print(rec.birthday.value)
    print(rec.days_to_birthday())
    
    # name = Name('Bill')
    # phone = Phone('1234567890')
    # rec = Record(name, phone)
    # ab = AddressBook()
    # ab.add_record(rec)
    
    # assert isinstance(ab['Bill'], Record)
    # assert isinstance(ab['Bill'].name, Name)
    # assert isinstance(ab['Bill'].phones, list)
    # assert isinstance(ab['Bill'].phones[0], Phone)
    # assert ab['Bill'].phones[0].value == '1234567890'
    
    # print('All Ok)')  

    # a = Field("name")
    # num = Phone('12345678974')
    # print(a.value)
    # print(num.value)
    # num.value = "987654321123"
    # print(num.value)

    # day = Birthday('1994-02-26')
    # day.value = '1994-02-28'
    # print(day.value)

    





