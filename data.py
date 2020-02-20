from xml.dom.minidom import parse

dom = parse("eat100.xml")

stimuli = dom.getElementsByTagName('stimulus')
words = dict()

for stimulus in stimuli:
	stim_word = str(stimulus.attributes['word'].value)
	responses = stimulus.getElementsByTagName('response')
	response_words = []
	for response in responses:
		response_word = str(response.attributes['word'].value)
		response_words.append(response_word)
	words[stim_word] = response_words

for word in words:
	for response in words[word]:
		line = "<eat:" + word + ">" + "cn:relates-to<eat:" + response + ">" + '\n'
		print(line)