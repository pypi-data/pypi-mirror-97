import datetime
import string
import random

def company_id(company_id = 1, length = 6):
	# company ID
	return "ESE" + str(company_id).zfill(length)

def restaurant_id(restaurant_id = 1, length = 6):
	# restaurant ID
	return "ESR" + str(restaurant_id).zfill(length)

def invoice_id(invoice_id = 1, length = 6):
	# invoice ID
	return "ES" + datetime.datetime.today().year + str(invoice_id).zfill(length)

def reservation_code(res_code_id = 1, length = 6):
	# reservation Code
	letters = string.ascii_uppercase + string.digits
	random_string = ''.join(random.choice(letters) for i in range(6))
	return random_string + str(res_code_id).zfill(length)
