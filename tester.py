import ollama

res = ollama.chat(
	model='llava',
	messages=[
		{
			'role': 'user',
			'content': 'OUTPUT ONE NUMBER; estimating the number of people in line.',
			'images': ['./noPpl.jpg']
		}
	]
)

print(res['message']['content'])