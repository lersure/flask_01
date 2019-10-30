import sys

# num = len(sys.argv)
# arg1 = sys.argv[1]
# arg2 = sys.argv[2]
# print("arg1=%s,arg2=%s" % (arg1, arg2))
# value = {"num": num, "arg1": arg1, "arg2": arg2}
resultText = open('data.txt', 'w+', encoding='utf-8')
resultText.write('{\'arg\':%s,' % sys.argv[1:])
resultText.write('\'nums\':%d}' % (len(sys.argv)-1))
resultText.close()
