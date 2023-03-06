from num2words import num2words
from subprocess import call
from smbus2 import SMBus
from mlx90614 import MLX90614
from time import sleep

def tempdetect_function():
    
  cmd_beg= 'espeak '
  cmd_end= ' 2>/dev/null' # To dump the std errors to /dev/null
  


  bus = SMBus(1)
  sensor = MLX90614(bus, address=0x5A)

  x = int((sensor.get_object_1() * 1.8)+32)
  count = num2words(x) + ' Degree Fahrenheit'
  print(count)
  #Replacing ' ' with '_' to identify words in the text entered
  count = count.replace(' ', '_')
  #Calls the Espeak TTS Engine to read aloud a Text
  call([cmd_beg+count+cmd_end], shell=True)
  
tempdetect_function()