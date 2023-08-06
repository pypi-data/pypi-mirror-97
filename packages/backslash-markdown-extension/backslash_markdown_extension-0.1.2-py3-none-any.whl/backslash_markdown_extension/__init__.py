from markdown.extensions import Extension
from backslash_markdown_extension import processors

class BackslashMarkdownExtension(Extension):

	def extendMarkdown(self, md):
		md.treeprocessors.register(processors.BackslashTreeProcessor(md), 'backslash', 1)
