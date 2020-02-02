import re

def check_xss_attack(input_str):
    regex=r".*<.*>.*</.*>.*"
    regex2=r".*http.*"
    regex3=r".*<.*>.*"
    regex4=r"(javascript)|(url)"
    if(re.search(regex, input_str) or re.search(regex2, input_str) or (re.search(regex3, input_str) and re.search(regex4, input_str))):
        return True
    return False
if __name__=='__main__':
	myquery = str(input("Enter Your String: "))
	print(check_xss_attack(myquery))