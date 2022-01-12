# Create the simplest jinja2 template

from jinja2 import Template

templ = '''Hello {{ name }}'''

def main():
	template = Template(templ)
	print(template.render(name="Ganesh"))
	
if __name__ == "__main__":
	# execute only if run as script
	main()
