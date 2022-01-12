# Use files for template, data and output

from jinja2 import Template
import json

with open('jnanpith_data.json', 'r') as f1:
	jnanpith_data = json.load(f1)

def main():
	# Read template file into a variable
	with open('template.html.jinja2', 'r') as f2:
		templ = f2.read()
	
	# Render the template using jinja2
	template = Template(templ)
	content = template.render(jnanpith_data=jnanpith_data)
	
	# Save the rendered html document
	with open('jnanpith.html', 'w') as f3:
		f3.write(content)
	
if __name__ == "__main__":
	# execute only if run as script
	main()
