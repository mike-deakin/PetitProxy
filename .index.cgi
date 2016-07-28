#!/usr/bin/python3
import cgi
import re
from mtgsdk import Card as mtgcard

def htmlOpen():
	print("""Content-Type: text/html\n\n
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Python Server-side test</title>
<link rel="stylesheet" href="style.css">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<script src="jquery.textfill.min.js"></script>
<script>
$(document).ready(function(){
	$('.proxy-card-text-container').textfill({maxFontPixels:16})
	$('.proxy-attributes-bar').textfill({maxFontPixels:14})
	$('.proxy-title-bar').textfill({maxFontPixels:14})
})
</script>
</head>
<body>""")
def htmlClose():
	print("""</body>
</html>""")

def wrapWithQuotes(name):
	return '"' + name + '"'

def getAndParseFormData(form):
	rawdata = form.getfirst("decklist", "")
	parseddata = rawdata.splitlines()
	cardInfoRegex = r"^(\d*)(\s?[-\*x]?\s?)(.*)$"
	result = []
	for datum in parseddata:
		match = re.match(cardInfoRegex, datum)
		num = int(match.group(1)) if match.group(1) != '' else 1
		result.append([num, match.group(3)])
	return result

def getAndParseMTGRequest(decklist, exact=True):
	result = []
	for cData in decklist:
		cName = wrapWithQuotes(cData[1]) if exact else cData[1]
		aCard = mtgcard.where(name=cName).all()
		if len(aCard) > 0:
			for i in range(0, cData[0]):
				result.append(aCard[0])
				if aCard[0].layout == 'double-faced':
					bSide = mtgcard.where(name=wrapWithQuotes(aCard[0].names[1])).all()
					if len(bSide) > 0:
						result.append(bSide[0])
	return result
	
#main program
if __name__ == "__main__":
	try:
		htmlOpen()
		form = cgi.FieldStorage()
		if len(form):
			decklistdata = getAndParseMTGRequest(getAndParseFormData(form))
			print('<div class="proxy-print-table">')
			for deckdatum in decklistdata:
				print('<div class="proxy-container">')
				print('<div class="proxy-title-bal">')
				print('<div class="proxy-name">', deckdatum.name, '</div>')
				print('<div class="proxy-mana-cost">', deckdatum.mana_cost if deckdatum.mana_cost else "N/A", '</div>')
				print('</div>')
				print('<div class"proxy-attributes-bar">')
				print('<div class="proxy-attributes">', deckdatum.type.replace('\u2014','-'), '</div></div>')
				print('<div class="proxy-card-text-container">')
				print('<span class="proxy-card-text">', deckdatum.text, '</span></div>')
				if deckdatum.power and deckdatum.toughness:
					print('<div class="proxy-power-tough">', deckdatum.power, '/', deckdatum.toughness, '</div>')
				elif deckdatum.loyalty:
					print('<div class="proxy-power-tough">', deckdatum.loyalty, '</div>')
				print('</div>')
			print('</div>')
		else:
			print("""<form action="#" method="post" target="printme">
<textarea class="decklist" name="decklist"></textarea>
<input type="submit" value="Go!">
</form>""")
		htmlClose()
	except:
		cgi.print_exception()

#testcard = mtgcard.where(name='Gideon, Battle-Forged').all()
#for card in testcard:
#	print(card.name)

