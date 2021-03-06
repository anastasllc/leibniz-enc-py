import sys
from string import maketrans,translate

class leibniz:
	def __init__(self, gear = None, alphabets_string = None, alphabet_delimiter = '\n', default_alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ \n"):
		"""constructs class and either sets or reads from disk the alphabets and gear to be used, with the default character set as an optional parameter with default value set to the Latin alphabet used in Leibiz' time"""
		self.default_alphabet = unicode(default_alphabet)
		self.starting_alphabet = 0
		
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

	def get_file_contents(self, filename):
		f = open(filename, 'r');
		fdata = f.read()
		f.close()
		return fdata

	def set_file_contents(self, filename, fdata):
		f = open(filename, 'w')
		f.write(fdata)
		f.close()

	def set_alphabets(self, alph, delimiter='\n'):
		"""splits a given string into alphabets using the given delimeter (default value of newline character) and saves is as an object parameter"""
		alphabets = alph.split(delimiter)
		appended_alphabets = []
		for a in alphabets:
			appended_alphabets.append(a + "JV")
		self.alphabets = [unicode(a.upper()) for a in appended_alphabets]

	def set_alphabets_from_file(self, filename = 'cyphers.txt'):
		"""reads alphabets into a string from a file (default filename cyphers.txt) and passes that string to self.set_alphabets()"""
		try:
			self.set_alphabets(self.get_file_contents(filename))
		except IOError:
			self.set_file_contents(filename, "ABCDEFGHIKLMNOPQRSTUWXYZ\nBCDEFGHIKLMNOPQRSTUWXYZA\nABCDEFGHIKLMNOPQRSTUWXYZ\nBCDEFGHIKLMNOPQRSTUWXYZA\nABCDEFGHIKLMNOPQRSTUWXYZ\nBCDEFGHIKLMNOPQRSTUWXYZA")
			self.set_alphabets(self.get_file_contents(filename))

	def set_starting_alphabet(self, index):
		"""sets which alphabet to start with"""
		self.starting_alphabet = int(index)

	def set_gear(self, gear):
		"""simple setter method for the variable represneting the Leibniz gear, a string of binary digits"""
		self.gear = gear

	def set_gear_from_file(self, filename = 'gear.txt'):
		"""reads the Leibniz gear string from a file (by default, gear.txt) and passes that string to self.set_gear()"""
		try:
			self.set_gear(self.get_file_contents(filename))
		except IOError:
			self.set_file_contents(filename,"101010");
			self.set_gear(self.get_file_contents(filename))
		
	def create_encryption_tables(self, default_alphabet, alphabets):
		"""uses Python's String.maketrans() to create one substitution cypher per given alphabet to be used for encryption"""
		self.encryption_tables = [dict((ord(x), y) for (x, y) in zip(default_alphabet, a)) for a in alphabets]

	def create_decryption_tables(self, default_alphabet, alphabets):
		"""uses Python's String.maketrans() to create one substitution cypher per given alphabet to be used for decryption"""
		self.decryption_tables = [dict((ord(x), y) for (x, y) in zip(a,default_alphabet)) for a in alphabets]
		
	def encrypt(self, message):
		"""encrypts the given string according to Leibniz' algorithm, optionally choosing which alphabet to start with (zero-indexed)"""
		message = unicode(message).upper()
		which_alphabet = self.starting_alphabet
		encrypted_message = []
		
		for i in range(0,len(message)):
			encrypted_message.append(message[i].translate(self.encryption_tables[which_alphabet % len(self.encryption_tables)]))
			which_alphabet = (which_alphabet + int(self.gear[i % len(self.gear)])) % len(self.alphabets)

		return ''.join(encrypted_message)

	def decrypt(self, message):
		"""decrypts the given string according to Leibniz' algorithm, optionally choosing which alphabet to start with (zero-indexed)"""
		message = unicode(message).upper()
		which_alphabet = self.starting_alphabet
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
		leb.set_starting_alphabet(sys.argv[3])
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2])

	elif len(sys.argv) == 5:
		leb.set_starting_alphabet(sys.argv[3])
		leb.set_gear(sys.argv[4])
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2])

	elif len(sys.argv) == 6:
		leb.set_starting_alphabet(sys.argv[3])
		leb.set_gear(sys.argv[4])
		leb.set_alphabets(sys.argv[5], ';')
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2])

	elif len(sys.argv) == 7:
		leb.set_starting_alphabet(sys.argv[3])
		leb.set_gear(sys.argv[4])
		leb.set_alphabets(sys.argv[5], sys.argv[6])
		if sys.argv[1] == "encrypt":
			print leb.encrypt(sys.argv[2])
		elif sys.argv[1] == "decrypt":
			print leb.decrypt(sys.argv[2])

if __name__ == "__main__":
	main()
