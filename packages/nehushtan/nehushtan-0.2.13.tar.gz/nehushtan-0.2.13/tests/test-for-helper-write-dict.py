from nehushtan.helper.CommonHelper import CommonHelper

dictionary = {}

CommonHelper.write_dictionary(dictionary, tuple(['A', 'B', 'C']), 'X')
print(dictionary)

CommonHelper.write_dictionary(dictionary, tuple(['A', 'B', 'C']), 'Y')
print(dictionary)
