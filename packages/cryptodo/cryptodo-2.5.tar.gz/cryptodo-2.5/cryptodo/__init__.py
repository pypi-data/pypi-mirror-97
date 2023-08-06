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
    
     return  '/'+encrypted 
          
          
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
     
     return  decrypted
   

def key_generator(min,max):
     gen = random.randint(min,max)
     return gen+8
