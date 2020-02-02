
import re

def checkRegMatch(parameters):
    regex=r"(\%27)|(\')|(\%22)|(\")|(\%3D)|(\))|(\-\-)|(\%23)"
    regex2 = "(union)|(UNION)|(update)|(UPDATE)|(CONCAT)|(SELECT)|(concat)|(select)|(ORDER)|(order)|(By)|(OR)|(by)|(exec(\s|\w))"
    regex3 = r"((WHERE|OR)[ ]+[\(]*[ ]*([\(]*[0-9]+[\)]*)[ ]*=[ ]*[\)]*[ ]*\3)|AND[ ]+[\(]*[ ]*([\(]*1[0-9]+|[2-9][0-9]*[\)]*)[ ]*[\(]*[ ]*=[ ]*[\)]*[ ]*\4"
    
     
    
    match1 = re.search(regex, parameters)
    match2 = re.search(regex2, parameters)
    match3 = re.search(regex3, parameters)
    if match1 or match2 or match3:
        return True
    return False
    

if __name__=='__main__':
	myquery = str(input("Enter Your String: "))
	print(checkRegMatch(myquery))
	
	'''
	String to give a try
	select * from table where uname = 'aaditya' and pass = '' or ''==''
	hello@4345%%123
	SELECT UserId, Name, Password FROM Users WHERE UserId = 105 or 1=1;
	username&nfs%hfl
	
	Refrences:
	https://stackoverflow.com/questions/139926/regular-expression-to-match-common-sql-syntax
	https://stackoverflow.com/questions/45093/regex-to-detect-sql-injection
	'''
