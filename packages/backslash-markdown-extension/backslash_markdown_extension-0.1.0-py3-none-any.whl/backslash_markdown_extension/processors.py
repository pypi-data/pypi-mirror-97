import copy
import xml.etree.ElementTree as etree

from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor


class BackslashPostProcessor(Postprocessor):

	def run(self, text):
		text = text.replace('<ul>', '')
		text = text.replace('</ul>', '<li></li>')
		text = text.replace('<ol>', '')
		text = text.replace('</ol>', '<li></li>')
		return text


class BackslashTreeProcessor(Treeprocessor):

	def run(self, root):
		last = None

		for element in root.iter():
			print('ELEMENT', element, element.tag, element.attrib, len(element), etree.tostring(element))

			if element.tag == 'p':
				element.tag = 'li'
				element.attrib['processed'] = 'true'
				etree.SubElement(element, 'li', attrib={'processed': 'true'})

			if element.tag in ['h1', 'h2', 'h3', 'hr'] and element.attrib.get('parent_tag') != 'li':
				element_tag = copy.copy(element.tag)
				element.tag = 'li'
				element_text = element.text
				element.text = ''
				element_attrib = copy.copy(element.attrib)
				element.attrib = {'processed': 'true'}
				element_attrib['parent_tag'] = element.tag
				sub_element = etree.SubElement(element, element_tag, attrib=element_attrib)
				sub_element.text = element_text
				etree.SubElement(element, 'li', attrib={'processed': 'true'})

			if element.tag == 'pre':
				# TODO
				pass

			if element.tag == 'li' and element.attrib.get('processed') != 'true':

				if len(element):
					raise Exception([e for e in element])

				element_text = element.text
				element.text = ''
				element_attrib = {'class': 'tab'}
				etree.SubElement(element, 'span', attrib=element_attrib)
				sub_element = etree.SubElement(element, 'span')
				sub_element.text = element_text

			if element.tag == 'img':

				if last.tag == 'a':
					last.attrib['class'] = 'none'

			last = element
