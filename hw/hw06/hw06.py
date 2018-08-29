############
# Mutation #
############

def make_withdraw(balance, password):
    """Return a password-protected withdraw function.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> w(90, 'hax0r')
    'Insufficient funds'
    >>> w(25, 'hwat')
    'Incorrect password'
    >>> w(25, 'hax0r')
    50
    >>> w(75, 'a')
    'Incorrect password'
    >>> w(10, 'hax0r')
    40
    >>> w(20, 'n00b')
    'Incorrect password'
    >>> w(10, 'hax0r')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    >>> w(10, 'l33t')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    """
    count_to_lock = 3
    inputs = []

    def withdraw(amount, try_password):
        nonlocal balance
        nonlocal password
        nonlocal inputs
        nonlocal count_to_lock

        if count_to_lock == 0:
            return "Your account is locked. Attempts: " + str(inputs)

        if try_password != password:
            count_to_lock -= 1
            inputs += [try_password]

            return 'Incorrect password'
        else:
            if amount > balance:
               return 'Insufficient funds'
            balance = balance - amount

            return balance
    return withdraw

def make_joint(withdraw, old_password, new_password):
    """Return a password-protected withdraw function that has joint access to
    the balance of withdraw.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> make_joint(w, 'my', 'secret')
    'Incorrect password'
    >>> j = make_joint(w, 'hax0r', 'secret')
    >>> w(25, 'secret')
    'Incorrect password'
    >>> j(25, 'secret')
    50
    >>> j(25, 'hax0r')
    25
    >>> j(100, 'secret')
    'Insufficient funds'

    >>> j2 = make_joint(j, 'secret', 'code')
    >>> j2(5, 'code')
    20
    >>> j2(5, 'secret')
    15
    >>> j2(5, 'hax0r')
    10

    >>> j2(25, 'password')
    'Incorrect password'
    >>> j2(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> j(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> w(5, 'hax0r')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> make_joint(w, 'hax0r', 'hello')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    """

    joint_password = []

    def joint_withdraw(amount, try_password):
        nonlocal withdraw
        nonlocal old_password
        nonlocal new_password
        nonlocal joint_password

        if try_password in joint_password:
            return withdraw(amount, old_password)
        else:
            return withdraw(amount, try_password)

    result = withdraw(0, old_password)

    if type(result) == int:
        joint_password = joint_password + [old_password, new_password]
        return joint_withdraw
    else:
        return result

###########
# Objects #
###########

class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'You must deposit $10 more.'
    >>> v.deposit(7)
    'Current balance: $7'
    >>> v.vend()
    'You must deposit $3 more.'
    >>> v.deposit(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.deposit(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.deposit(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    def __init__(self, product, price, quantity=0, deposit=0):
        self.product = product
        self.price = price
        self.quantity = quantity
        self.total_deposit = deposit

    def deposit(self, money):
        self.total_deposit += money

        if self.quantity == 0:
            self.total_deposit -= self.total_deposit
            return 'Machine is out of stock. Here is your $' + str(money) + '.'
        else:
            return 'Current balance: $' + str(self.total_deposit)


    def vend(self):
        if self.quantity <= 0:
            return 'Machine is out of stock.'
        elif self.total_deposit < self.price:
            insufficient_value = self.price - self.total_deposit
            return 'You must deposit $' + str(insufficient_value) + ' more.'
        else:
            change = self.total_deposit - self.price
            self.quantity -= 1
            if change != 0:
                self.total_deposit -= self.total_deposit
                return 'Here is your '+ self.product + ' and $' + str(change) + ' change.'
            else:
                return 'Here is your '+ self.product + '.'


    def restock(self, quantity):
        self.quantity += quantity
        return 'Current ' + self.product + ' stock: ' + str(self.quantity)




class MissManners:
    """A container class that only forward messages that say please.

    >>> v = VendingMachine('teaspoon', 10)
    >>> v.restock(2)
    'Current teaspoon stock: 2'

    >>> m = MissManners(v)
    >>> m.ask('vend')
    'You must learn to say please first.'
    >>> m.ask('please vend')
    'You must deposit $10 more.'
    >>> m.ask('please deposit', 20)
    'Current balance: $20'
    >>> m.ask('now will you vend?')
    'You must learn to say please first.'
    >>> m.ask('please hand over a teaspoon')
    'Thanks for asking, but I know not how to hand over a teaspoon.'
    >>> m.ask('please vend')
    'Here is your teaspoon and $10 change.'

    >>> double_fussy = MissManners(m) # Composed MissManners objects
    >>> double_fussy.ask('deposit', 10)
    'You must learn to say please first.'
    >>> double_fussy.ask('please deposit', 10)
    'Thanks for asking, but I know not how to deposit.'
    >>> double_fussy.ask('please please deposit', 10)
    'Thanks for asking, but I know not how to please deposit.'
    >>> double_fussy.ask('please ask', 'please deposit', 10)
    'Current balance: $10'
    """
    def __init__(self, obj):
        self.obj = obj

    def ask(self, message, *args):
        magic_word = 'please '
        if not message.startswith(magic_word):
            return 'You must learn to say please first.'

        else:
            len_magic_word = len(magic_word)
            request = message[len_magic_word:]
            if hasattr(self.obj, request):
                if len(args) == 0:
                    method = getattr(self.obj, request)
                    return method()
                else:
                    return getattr(self.obj, request)(*args)
            else:
                return 'Thanks for asking, but I know not how to ' + request + '.'



        
