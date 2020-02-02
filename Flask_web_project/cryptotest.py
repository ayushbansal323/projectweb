from cryptoProject.sqlinject import checkRegMatch
from cryptoProject.xssdetection import check_xss_attack

print(checkRegMatch("Select sql injection"))
print(check_xss_attack("<></>"))

