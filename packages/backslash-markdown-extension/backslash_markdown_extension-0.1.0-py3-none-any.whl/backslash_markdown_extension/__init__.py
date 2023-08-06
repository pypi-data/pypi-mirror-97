from markdown.extensions import Extension
from backslash_markdown_extension import processors

class BackslashMarkdownExtension(Extension):

	def extendMarkdown(self, md):
		md.treeprocessors.register(processors.BackslashTreeProcessor(md), 'backslash', 1)
		md.postprocessors.register(processors.BackslashPostProcessor(), 'backslash', 2)
