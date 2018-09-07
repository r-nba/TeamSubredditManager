from ClipperBot import ClipperBot
import sys

cb = ClipperBot()
while 1==1:
    try:
        cb.wakeUp()
    except:
        print('HOLY SHIT AN EXCEPTION!!!!!!')
        print ('Error: ', sys.exc_info())
        cb.sleep(120) #try again in 2 min