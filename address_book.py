from collections import UserDict


    
    
class Filed:
    """
    родительский класс всех полей
    поле для ввода новых данных в записную книгу
    """
    def __init__(self, value: str) -> None:
        if isinstance(value, str):
            self._value  = value
        else: 
            raise ValueError    
       
    @property
    def value(self):
        print('gettter_filed')
        return self._value
    
    @value.setter
    def value(self, value: str):
        print('setter_Filed')
        if isinstance(value, str):
            self._value  = value
        else:
            raise ValueError    



class Name(Filed):
    """
    поле имени, принимает любую стр без проверки
    """
    def __init__(self, value: str) -> None:
        super().__init__(value)
        
   

class Phone(Filed):
    """
    поле номера телефона, принимает стр(только цифри)
    """
    def __init__(self, value: str) -> None:
        if value.isdigit():
            super().__init__(value)
        else: 
            raise ValueError('')    
   
    @Filed.value.setter
    def value(self, value: str): 
        print('setter_phone1')   
        super(Phone, Phone).value.__set__(self, value) 
        print('setter_phone2')
        if value.isdigit(): # TODO ful phone valid
            self._value = value
        else:
            raise ValueError    
        


class Record:
    """
    класс которий содержит в себе все поля и методи работи с ними
    сейчас простая реализация add/remove/change phone 
    """
  
    def __init__(self, name: Name, *phones) -> None:
        self.name = name
        self.phones = list(phones)

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

    num = Phone("123")
    print(num.value)
    num.value = "qwert"
    print(num.value)







