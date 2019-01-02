# import sys
# # sys.path.append('/home/carefreeslacker/SpyderProjects/OtustHomework1')
#
# from library import summ, subb, sump, subp
#
# for i in [1,2,9,4,5,6]:
#     if i == 6:
#         continue
#     print('Number is i ', i)
# else:
#     print("Фух обошлось")
#
#
# def call(x):
#     print('called {argument}'.format(argument=x))
#
# variable = call
#
# class A:
#     def call(self, *arguments):
#         print(arguments)
#         print('call A first three arguments {0}-{1}-{2}'.format(*arguments))
#         return 0


import requests
url = 'https://www.kinopoisk.ru/top/lists/17/'
r = requests.get(url)
print('---')
# print("".join(map(chr, r.text.encode('windows-1251'))))
print(r.text)
print('---')
with open('test.html', 'w') as output_file:
    output_file.write(r.text)
    # output_file.write("".join(map(chr, r.text.encode('windows-1251'))))
