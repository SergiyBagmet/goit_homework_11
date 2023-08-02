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
      
    @classmethod 
    def __valid_value(cls, value) -> None:
        if type(value) != str:
            raise ValueError('received data must be STR') 
        
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
        self.__valid_value(value)
        
      
    @classmethod
    def __valid_value(cls, value) -> None:
        # тут нужна проверка на стр?
        phone = ''.join(filter(str.isdigit, value))
        if 9 >= len(phone) <= 15 : #псевдо проверка номера
            raise ValueError("Phone number isn't correct")    

    @Field.value.setter
    def value(self, value: str) -> None:
        self.__valid_value(value)
        self._value = value
      

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
            valid_date = date.fromisoformat(value)
        except: # может тут сразу ошибку выдавать без райза???
            raise ValueError('not correct date isoformat >>> yyyy-mm-dd')
            
    @Field.value.setter
    def value(self, value: str) -> None:
        self.__valid_value(value)
        self._value = value
      
        
class Record:
    """
    класс которий содержит в себе все поля и методи работи с ними
    сейчас простая реализация add/remove/change phone 
    """
  
    def __init__(self, name: Name, phone: Phone, birthday: Birthday=None ) -> None:
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday if birthday else None
    
    def __str__(self) -> str:# принтуем рекорд..не знаю как принято..сделал как чувствую
        birthday_str = "birthday: "+str(self.birthday) if self.birthday != None else ""
        phones_str = " ".join([ph.value for ph in self.phones]) 
        return f'<Record> name: {self.name} -->> phone(s): {phones_str} {birthday_str}'

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
        return (bday - today).days
      
    
class AddressBook(UserDict):
    """
    класс хранилише записной книги  - словарь
    "имя" : обьект рекорд которий содержит все поля(и методи) в соответствии с этим именем 
    """

    def add_record(self, rec: Record):
        if type(rec) != Record:
            raise ValueError("Record must be an instance of the Record class.")
        self.data[rec.name.value] = rec
    
    def __iter__(self):
        self.__counter = 0
        return self

    def iterator(self, num:int = 1):
        self.__num = num
        self.rec_list = [str(val) for val in self.data.values()]
        return self.__iter__() 

    def __next__(self):
        if self.__counter < (len(self.data.keys()) // self.__num):
            start_i = self.__counter
            stop_i = self.__counter + self.__num
            self.__counter +=self.__num
            return "\n".join(self.rec_list[start_i: stop_i])
        raise StopIteration
    
  
 
        
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

    name_4 = Name('Igor')
    phone_4 = Phone('1234567890')
    b_day_4 = Birthday('1994-02-26')


    rec_1 = Record(name_1, phone_1, b_day_1)
    rec_2 = Record(name_2, phone_2, b_day_2)
    rec_3 = Record(name_3, phone_3, b_day_3)
    rec_4 = Record(name_4, phone_4, b_day_4)
    ab = AddressBook()
    ab.add_record(rec_1)
    ab.add_record(rec_2)
    ab.add_record(rec_3)
    ab.add_record(rec_4)
    for i in ab.iterator(2):
        print(i)
        break

    
    # name = Name('Bill')
    # phone = Phone('1234567890')
    # b_day = Birthday('1994-02-26')
    # rec = Record(name, phone, b_day)
    # print(rec.phones[0].value)
    # print(rec.birthday.value)
    # print(rec.days_to_birthday())
    
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

    





