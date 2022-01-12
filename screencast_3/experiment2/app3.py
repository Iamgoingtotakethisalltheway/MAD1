# Use jinja2 to create a simple html template

from jinja2 import Template

jnanpith_data = {'Year': 1965, 'Awardees': 'G. Sankara Kurup', 'Language': 'Malayalam'}

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
            <tr>
                <td>{{ jnanpith_data['Year'] }}</td>
                <td>{{ jnanpith_data['Awardees'] }}</td>
                <td>{{ jnanpith_data['Language'] }}</td>
            </tr>
        </tbody>
    </table>
</body>
</html>'''


def main():
	template = Template(templ)
	print(template.render(jnanpith_data=jnanpith_data))
	
if __name__ == "__main__":
	# execute only if run as script
	main()
