import sys
from string import maketrans,translate

class leibniz:
	def __init__(self, gear = None, alphabets_string = None, alphabet_delimiter = '\n', default_alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ"):
		"""constructs class and either sets or reads from disk the alphabets and gear to be used, with the default character set as an optional parameter with default value set to the Latin alphabet used in Leibiz' time"""
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
		"""splits a given string into alphabets using the given delimeter (default value of newline character) and saves is as an object parameter"""
		self.alphabets = [a.upper() for a in alph.split(delimiter)]

	def set_alphabets_from_file(self, filename = 'cyphers.txt'):
		"""reads alphabets into a string from a file (default filename cyphers.txt) and passes that string to self.set_alphabets()"""
		f = open(filename, 'r');
		self.set_alphabets(f.read())
		f.close()

	def set_gear(self, gear):
		"""simple setter method for the variable represneting the Leibniz gear, a string of binary digits"""
		self.gear = gear

	def set_gear_from_file(self, filename = 'gear.txt'):
		"""reads the Leibniz gear string from a file (by default, gear.txt) and passes that string to self.set_gear()"""
		f = open(filename, 'r');
		self.set_gear(f.read())
		f.close()
		
	def create_encryption_tables(self, default_alphabet, alphabets):
		"""uses Python's String.maketrans() to create one substitution cypher per given alphabet to be used for encryption"""
		self.encryption_tables = [maketrans(default_alphabet, a) for a in alphabets]

	def create_decryption_tables(self, default_alphabet, alphabets):
		"""uses Python's String.maketrans() to create one substitution cypher per given alphabet to be used for decryption"""
		self.decryption_tables = [maketrans(a, default_alphabet) for a in alphabets]
		
	def encrypt(self, message, starting_alphabet = 0):
		"""encrypts the given string according to Leibniz' algorithm, optionally choosing which alphabet to start with (zero-indexed)"""
		message = message.upper()
		which_alphabet = int(starting_alphabet)
		encrypted_message = []
		
		for i in range(0,len(message)):
			encrypted_message.append(message[i].translate(self.encryption_tables[which_alphabet % len(self.encryption_tables)]))
			which_alphabet = (which_alphabet + int(self.gear[i % len(self.gear)])) % len(self.alphabets)

		return ''.join(encrypted_message)

	def decrypt(self, message, starting_alphabet = 0):
		"""decrypts the given string according to Leibniz' algorithm, optionally choosing which alphabet to start with (zero-indexed)"""
		message = message.upper()
		which_alphabet = int(starting_alphabet)
		decrypted_message = []
		
		for i in range(0,len(message)):
			decrypted_message.append(message[i].translate(self.decryption_tables[which_alphabet % len(self.decryption_tables)]))
			which_alphabet = (which_alphabet + int(self.gear[i % len(self.gear)])) % len(self.alphabets)

		return ''.join(decrypted_message)

def main():
	if len(sys.argv) < 3:
	   print "Usage: ", sys.argv[0], " encypt|decrypt message [starting_alphabet [gear [alphabets [delimiter = ';']]]]"
	   print ""
	   print "Any optional arguments not given on the command line will be read from the corresponding text files on disk."

	leb = leibniz()
	
	if len(sys.argv) == 3:
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2])

	elif len(sys.argv) == 4:
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2], sys.argv[3])

	elif len(sys.argv) == 5:
		leb.set_gear(sys.argv[4])
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2], sys.argv[3])

	elif len(sys.argv) == 6:
		leb.set_gear(sys.argv[4])
		leb.set_alphabets(sys.argv[5], ';')
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2], sys.argv[3])

	elif len(sys.argv) == 7:
		leb.set_gear(sys.argv[4])
		leb.set_alphabets(sys.argv[5], sys.argv[6])
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2], sys.argv[3])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2], sys.argv[3])


if __name__ == "__main__":
	main()
