import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class md_renderer(mistune.Renderer):
	def block_code(self, code, lang):
		if not lang:
			return '\n<div class="highlight-n"><pre><code>%s</code></pre></div>\n' % \
		mistune.escape(code)
		lexer = get_lexer_by_name(lang, stripall=True)
		formatter = HtmlFormatter()
		return highlight(code, lexer, formatter)