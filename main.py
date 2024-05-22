from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address
import re

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)

def login():
    try:
        public_key = input("Введите публичный ключ:")
        password = input("Введите парол:")
        w3.geth.personal.unlock_account(public_key, password)
        return public_key
    except Exception as ex:
        print(f"Ошибка : {ex}")
        return None

def register():
    proverka = False
    while(proverka != True):
        password = input("Введите пароль:")
        if len(password) >= 12:
            if bool(re.search('[!"#$%&\'()*+,-./:;<=>?@[\]^_{|}~]', password)):
                if bool(re.search('[0-9]', password)):
                    if bool(re.search('[A-Z]', password)):
                        account = w3.geth.personal.new_account(password)
                        print(f"Публичный ключ: {account}")
                        proverka = True
                    else:
                        print("Пароль не содержит английских заглавных букв")
                else:
                    print("Пароль не содержит цифр")
            else:
                print("Пароль не содержит специальных символов")
        else:
            print("Пароль меньше 12 символов")

def pay(account):
    try:
        value = int(input("Введите количестов эфира для отправки на котракт: "))
        tx_hash = contract.functions.pay().transact({
            'from': account,
            'value': value,
        })
        print(f"Транзакция {tx_hash.hex()} отправлена")
    except Exception as ex:
        print(f"Ошиька : {ex}")

def get_balance(account):
    balanc = contract.functions.GetBalance().call({
        "from": account,
    })
    print(f"Ваш баланс: {balanc}")

def withdraw(account):
    try:
        amount = int(input("Введите количестов эфир для снятия"))
        tx_hash = contract.functions.Withdraw(amount).transact({
            'from': account,
        })
        print(f"Трансакция {tx_hash.hex()} отправлена")
    except Exception as ex:
        print(f"Ошибка снятия средств: {ex}")

def create_Estate(account):
    try:
        while(True):
            try:
                size = int(input("Введите площадь жилья: "))
                break
            except:
                print("Это не число🙄")
        print("1. House")
        print("2. Flat")
        print("3. Loft")
        typeEs = viborFunc(3)
        estateAdres = input("Введите адрес недвижимости, без смайликов пэж 🥺: ")
        tx_hash = contract.functions.createEstate(size, estateAdres, typeEs-1).transact({
            'from': account,
        })
        print(f"Недвижимость {tx_hash.hex()} создалась")
    except Exception as ex:
        print(f"Ошибка создания недвижимости: {ex}")

def get_esates(account):
    estates = contract.functions.GetEstates().call({
        "from": account,
    })
    i = 1
    for es in estates:
        if(es[4] != False):
            print(f"{i}: {es}")
            i = i + 1

def create_ad(account):
    estates = contract.functions.GetEstates().call({
        "from": account,
    })
    i = 1
    for es in estates:
        if (es[4] != False):
            print(f"{i}: {es}")
            i = i + 1
    nomerEsatate = viborFunc(i)
    while(True):
        try:
            price = int(input("Введите цену: "))
            break
        except:
            print("Это не число🙄")
    try:
        tx_hash = contract.functions.createAd(nomerEsatate - 1, price).transact({
            'from': account,
        })
        print(f"Объявление {tx_hash.hex()} создалось")
    except Exception as ex:
        print(f"Ошибка: {ex}")

def get_ads(account):
    ads = contract.functions.GetAds().call({
        "from": account,
    })
    i = 1
    for ad in ads:
        if(ad[5] != 1):
            print(f"{i}: {ad}")
            i = i + 1

def update_ad_status(account):
    ads = contract.functions.GetAds().call({
        "from": account,
    })
    i = 1
    for ad in ads:
        if (ad[5] != 1):
            print(f"{i}: {ad}")
            i = i + 1
    nomerAd = viborFunc(i)
    try:
        tx_hash = contract.functions.updateAdStatus(nomerAd - 1).transact({
            'from': account,
        })
        print(f"Статус объявления {tx_hash.hex()} изменён")
    except Exception as ex:
        print(f"Ошибка: {ex}")

def update_estate_status(account):
    estates = contract.functions.GetEstates().call({
        "from": account,
    })
    i = 1
    for es in estates:
        print(f"{i}: {es}")
        i = i + 1
    nomerEs = viborFunc(i)
    print("1. Открыть")
    print("2. Закрыть")
    vibor = viborFunc(2)
    isActiv = bool
    if vibor == 1:
        isActiv = True
    elif vibor == 2:
        isActiv = False
    try:
        tx_hash = contract.functions.updateEstateStatus(nomerEs - 1, isActiv).transact({
            'from': account,
        })
        print(f"Статус недвижимости {tx_hash.hex()} изменён")
    except Exception as ex:
        print(f"Ошибка: {ex}")

def buy_estate(account):
    ads = contract.functions.GetAds().call({
        "from": account,
    })
    i = 1
    for ad in ads:
        if (ad[5] != 1):
            print(f"{i}: {ad}")
            i = i + 1
    nomerAd = viborFunc(i)
    try:
        tx_hash = contract.functions.BuyEstate(nomerAd - 1).transact({
            'from': account,
        })
        print(f"Недвижимость {tx_hash.hex()} куплена")
    except Exception as ex:
        print(f"Ошибка: {ex}")

def viborFunc(i):
    while (True):
        try:
            nomer = int(input("Выберите число: "))
            if nomer > i:
                raise ValueError
            break
        except:
            print("Это не число или число слишком большое🙄")
    return nomer

def main():
    account = ""
    while True:
        if account == "" or account == None:
            while True:
                try:
                    chouce = int(input("Выберите\n1. Авторизация\n2. Регистрация\n3.Выйти\n"))
                    break
                except:
                    print("Это не число🙄")
            match chouce:
                case 1:
                    account = login()
                case 2:
                    register()
                case 3:
                    exit()
                case _:
                    print("Выберите от 1 до 2")
        else:
            while True:
                try:
                    chouce = int(input("Выберите\n1. Отправить эфир\n2. Посмотреть баланс смарт-контракта\n3. Посмотреть баланс аккаунта\n4. Снять средства\n5. Создать недвижимость\n6. Посмотреть недвижимость\n7. Создать объявление\n8. Посмотреть объявления\n9. Поменять статус объявления\n10. Изменить статус недвижимости\n11. Купить недвижимость\n12. Выйти\n"))
                    break
                except:
                    print("Это не число🙄")
            match chouce:
                case 1:
                    pay(account)
                case 2:
                    get_balance(account)
                case 3:
                    print(f"Баланс акканута: {w3.eth.get_balance(account)}")
                case 4:
                    withdraw(account)
                case 5:
                    create_Estate(account)
                case 6:
                    get_esates(account)
                case 7:
                    create_ad(account)
                case 8:
                    get_ads(account)
                case 9:
                    update_ad_status(account)
                case 10:
                    update_estate_status(account)
                case 11:
                    buy_estate(account)
                case 12:
                    account = ""
                case _:
                    print("Число слишком большое🥲🥲")

if __name__ == "__main__":
    main()