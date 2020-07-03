import boto3

def Stack_choice():
	global Stack_choosen
	while True:
		print("\n1. Document Service - WS")
		print("2. Document Service - Consumer")
		Stack_choosen = input("Enter your Choice: ")
		try:
			int(Stack_choosen)
		except ValueError:
			print("This is not a number")
			continue
		if int(Stack_choosen) in range(1,3):
			print(Stack_choosen +" is choosen")
			CF_choice()
			break
		else:
			print("Invalid Choice")

def CF_choice():
	while True:
		print("\n1. Create Stack")
		print("2. Update Stack")
		print("3. Delete Stack")
		CF_choosen = input("Enter your Choice: ")
		try:
			int(CF_choosen)
		except ValueError:
			print("This is not a number")
			continue
		if int(CF_choosen) in range(1,4):
			print(CF_choosen +" is choosen")
			break
		else:
			print("Invalid Choice")
	if int(CF_choosen) == 1:
		Create_Stack()
	if int(CF_choosen) == 2:
		Update_Stack()
	if int(CF_choosen) == 3:
		Delete_Stack()

def Create_Stack()
	client = boto3.client('cloudformation')
	



def main():
	Stack_choosen = 0
	Stack_choice()



if __name__ == '__main__':
	main()


