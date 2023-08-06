import copy
import xml.etree.ElementTree as etree

from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor


class BackslashTreeProcessor(Treeprocessor):

	def run(self, root):
		# print('ROOT', root, root.tag, root.attrib, len(root), etree.tostring(root))
		elements = etree.Element('div')

		for element in root:
			# print('ELEMENT', element, element.tag, element.attrib, len(element), etree.tostring(element))

			# Paragraphs
			if element.tag == 'p':
				element.tag = 'li'
				elements.append(element)
				line = etree.Element('li')
				line.tail = '\n'
				elements.append(line)

			# Headers
			elif element.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
				item = etree.Element('li')
				header = etree.SubElement(item, element.tag, attrib=element.attrib)
				header.text = element.text
				header.tail = ''
				item.tail = '\n'
				elements.append(item)
				line = etree.Element('li')
				line.tail = '\n'
				elements.append(line)

			# Blockquotes
			# elif element.tag == 'blockquote':
			# 	pass

			# Lists
			elif element.tag in ['ul', 'ol']:

				for sub_element in element:

					if sub_element.tag == 'li':
						item = etree.Element('li')
						span = etree.SubElement(item, 'span', attrib={'class': 'indent'})
						sub_element.tag = 'span'
						sub_element.tail = ''
						item.append(sub_element)
						item.tail = '\n'
						elements.append(item)

				line = etree.Element('li')
				line.tail = '\n '
				elements.append(line)

			# Code blocks
			# elif element.tag == 'pre':
			# 	pass

			# Horiztonal rules
			elif element.tag == 'hr':
				item = etree.Element('li')
				etree.SubElement(item, element.tag, attrib=element.attrib)
				item.tail = '\n'
				elements.append(item)
				line = etree.Element('li')
				line.tail = '\n'
				elements.append(line)

			else:
				elements.append(element)

		return elements


class BackslashPostProcessor(Postprocessor):

	def run(self, text):
		text = text.replace('<br />\n', '</li>\n<li>')
		return text

