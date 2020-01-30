from xml.dom.minidom import parse, parseString

dom = parse("eat100.xml")

stimuli = dom.getElementsByTagName('stimulus')
words = dict()

for i in range(100):
	stim_word = str(stimuli[i].attributes['word'].value)
	responses = stimuli[i].getElementsByTagName('response')
	response_words = []
	for response in responses:
		response_word = str(response.attributes['word'].value)
		percent = str(response.attributes['r'].value)
		response_words.append((response_word, percent))
	words[stim_word] = response_words

for word in words:
	for response in words[word]:
		line = "<eat:" + word + ">" + "cn:relates-to<eat:" + response[0] + ">" + "r=" + response[1] + '\n'
		print(line)