


import os
import re




def getTerminalSize() -> tuple:
	return tuple(os.get_terminal_size())
#



def checkTerminalSupportsColors() -> bool:
	# see: https://www.gnu.org/software/gettext/manual/html_node/The-TERM-variable.html

	x = os.getenv("TERM")
	if x:
		if x.endswith("-color"):
			return True
		m = re.match("^.*-([0-9]+)color$", x)
		if m:
			n = int(m.group(1))
			if n >= 16:
				return True

	return False
#









