# Python text formatting used for creating template

template = '''Hello {name}!
This is {p:+} and this is {n:+}.
This is in decimal={value:d} and in hex={value:x}'''

# Note f-strings can also be used and are infact more powerful.

def main():
	print(template.format(name="Ganesh", p=5, n=-7, value=10))
	
if __name__ == "__main__":
	# execute only if run as script
	main()
