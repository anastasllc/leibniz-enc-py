import sys
from string import maketrans,translate

class leibniz:
	def __init__(self, gear = None, alphabets_string = None, alphabet_delimiter = '\n', default_alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ"):
		self.default_alphabet = default_alphabet
		
		if gear is None:
			self.set_gear_from_file()
		else:
			self.set_gear(gear)
			
		if alphabets_string is None:
			self.set_alphabets_from_file()
		else:
			self.set_alphabets(alphabets_string, alphabet_delimiter)

		self.create_encryption_tables(self.default_alphabet, self.alphabets)
		self.create_decryption_tables(self.default_alphabet, self.alphabets)
		
	def set_alphabets(self, alph, delimiter='\n'):
		self.alphabets = alph.split(delimiter)

	def set_alphabets_from_file(self, filename = 'cyphers.txt'):
		f = open(filename, 'r');
		self.set_alphabets(f.read())
		f.close()

	def set_gear(self, gear):
		self.gear = gear

	def set_gear_from_file(self, filename = 'gear.txt'):
		f = open(filename, 'r');
		self.set_gear(f.read())
		f.close()
		
	def create_encryption_tables(self, default_alphabet, alphabets):
		self.encryption_tables = [maketrans(default_alphabet, a) for a in alphabets]

	def create_decryption_tables(self, default_alphabet, alphabets):
		self.decryption_tables = [maketrans(a, default_alphabet) for a in alphabets]
		
	def encrypt(self, message):
		message = message.upper()
		which_alphabet = 0
		encrypted_message = []
		
		for i in range(0,len(message)):
			encrypted_message.append(message[i].translate(self.encryption_tables[which_alphabet % len(self.encryption_tables)]))
			if self.gear[i % len(self.gear)] == "1":
				which_alphabet = (which_alphabet + 1) % len(self.alphabets)
		return ''.join(encrypted_message)

	def decrypt(self, message):
		message = message.upper()
		which_alphabet = 0
		decrypted_message = []
		
		for i in range(0,len(message)):
			decrypted_message.append(message[i].translate(self.decryption_tables[which_alphabet % len(self.decryption_tables)]))
			if self.gear[i % len(self.gear)] == "1":
				which_alphabet = (which_alphabet + 1) % len(self.alphabets)
		return ''.join(decrypted_message)

def main():
	#leb = leibniz("10","ABCDEFGHIKLMNOPQRSTUWXYZ;BCDEFGHIKLMNOPQRSTUWXYZA",";")
	leb = leibniz()

	if len(sys.argv) < 3:
	   print "Usage: ", sys.argv[0], " encypt|decrypt message [gear [alphabets [delimiter = ';']]]"
	   print ""
	   print "Any optional arguments not given on the command line will be read from the corresponding text files on disk."
    
	if len(sys.argv) == 3:
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2])

	if len(sys.argv) == 4:
		leb.set_gear(sys.argv[3])
		print leb.encrypt(sys.argv[2])

	if len(sys.argv) == 5:
		leb.set_gear(sys.argv[3])
		leb.set_alphabets(sys.argv[4], ';')
		print leb.encrypt(sys.argv[2])

	if len(sys.argv) == 5:
		leb.set_gear(sys.argv[3])
		leb.set_alphabets(sys.argv[4], sys.argv[5])
		print leb.encrypt(sys.argv[2])


if __name__ == "__main__":
	main()
