import string
import random


class crypto:
 def __init__(self,text,key):
      self.text = text
      self.key = key 
      
      
 def encrypt(self):
     shift = self.key
     key2 = 26
     plain_text = self.text
     shift %= key2
     alphabet = string.ascii_lowercase 
     shifted = alphabet[shift:] + alphabet[:shift]
     table = str.maketrans(alphabet,shifted)
     encrypted =plain_text.translate(table)
    
     return  '/V1_CRYPTO '+encrypted 
          
          
 def decrypt(self):
     shift = self.key
     key2 = 26
     plain_text = self.text
     shift = key2-shift
     shift %= key2
     alphabet = string.ascii_lowercase
     shifted = alphabet[shift:] + alphabet[:shift]
     table = str.maketrans(alphabet,shifted)
     decrypted =plain_text.translate(table)
     decrypte = decrypted.replace(decrypted[0:11],'')
     return  decrypte
   
class key_gen:
     #''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
     
  def key_generator_num_V1(min,max):
     gen = random.randint(min,max)
     return gen+8
     
  def key_generator_num_V1_1(string_lowercase,key):
     out = int(string_lowercase, base=key)
     return out
     
  def key_generator_num_V2(size,chars=string.ascii_uppercase+ string.digits +string.ascii_lowercase + ' @#£_&-+()/*:;!.?'):
       return ''.join(random.choice(chars) for _ in range(size))
      
      
  key_var_1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#£_.&-+()/*:;!? '
  
class crypto_V2:
     
     def __init__(self,string,key):
          self.string = string
          self.key = key
     
     def encrypt(self):
           keys = self.key
           value = keys[-1] + keys[0:-1]
           encrypt = dict(zip(keys,value))
           string = self.string
           encryptnew = ''.join([encrypt[letter] for letter in string.lower()])
           return '/V1_CRYPTO '+ encryptnew
           
     def decrypt(self):
           keys = self.key
           string = self.string
           value = keys[-1] + keys[0:-1]
           decrypt = dict(zip(value,keys))
           decryptnew = ''.join([decrypt[letter] for letter in string.lower()])
           decryptne = decryptnew.replace(decryptnew[0:11],'')
           return decryptne