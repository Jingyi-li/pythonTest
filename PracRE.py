# __author__ = 'CL'
#
# import re
#
# pattern = re.compile(r'Hello')
#
# result1 = re.match(pattern, 'Hello')
# result2 = re.match(pattern, 'Helloo CL!')
# result3 = re.match(pattern, 'Helo CL!')
# result4 = re.match(pattern, 'Hello CL!')
#
# if result1:
#     print(result1.group())
# else:
#     print("1 failed matching!")
#
# if result2:
#     print(result2.group())
# else:
#     print("2 failed matching!")
#
# if result3:
#     print(result3.group())
# else:
#     print("3 failed matching!")
#
# if result4:
#     print(result4.group())
# else:
#     print("4 failed matching!")
#################################################################


import re

pattern = re.compile(r'\d+')
print(re.findall(pattern, 'one1two2three33four456'))

