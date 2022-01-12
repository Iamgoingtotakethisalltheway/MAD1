# Write output to a html file

from jinja2 import Template

jnanpith_data = [
{'Year': 1965, 'Awardees': 'G. Sankara Kurup', 'Language': 'Malayalam'}, 
{'Year': 1966, 'Awardees': 'Tarashankar Bandopadhyaya', 'Language': 'Bengali'}, 
{'Year': 1967, 'Awardees': 'Kuppali Venkatappagowda Puttappa', 'Language': 'Kannada'}, 
{'Year': 1967, 'Awardees': 'Umashankar Joshi', 'Language': 'Gujarati'}, 
{'Year': 1968, 'Awardees': 'Sumitranandan Pant', 'Language': 'Hindi'}, 
{'Year': 1969, 'Awardees': 'Firaq Gorakhpuri', 'Language': 'Urdu'}, 
{'Year': 1970, 'Awardees': 'Viswanatha Satyanarayana', 'Language': 'Telugu'}, 
{'Year': 1971, 'Awardees': 'Bishnu Dey', 'Language': 'Bengali'}, 
{'Year': 1972, 'Awardees': 'Ramdhari Singh Dinkar', 'Language': 'Hindi'}, 
{'Year': 1973, 'Awardees': 'Dattatreya Ramachandra Bendre', 'Language': 'Kannada'}, 
{'Year': 1973, 'Awardees': 'Gopinath Mohanty', 'Language': 'Oriya'}, 
{'Year': 1974, 'Awardees': 'Vishnu Sakharam Khandekar', 'Language': 'Marathi'}, 
{'Year': 1975, 'Awardees': 'P. V. Akilan', 'Language': 'Tamil'}
]

templ = '''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jnanpith</title>
</head>
<body>
    <h1>Awardees</h1>
    <table>
        <thead>
            <tr>
                <th>Year</th>
                <th>Awardees</th>
                <th>Language</th>
            </tr>
        </thead>
        <tbody>
        	{% for item in jnanpith_data %}
            <tr>
                <td>{{ item['Year'] }}</td>
                <td>{{ item['Awardees'] }}</td>
                <td>{{ item['Language'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>'''


def main():
	template = Template(templ)
	content = template.render(jnanpith_data=jnanpith_data)
	with open('jnanpith.html', 'w') as f:
		f.write(content)
	
if __name__ == "__main__":
	# execute only if run as script
	main()
