import xlsxwriter
from slugify import slugify
import os


def write_to_xlsx(filename, title="Worksheet", data=None):
	directory = os.path.dirname(filename)
	if not os.path.exists(directory):
		os.makedirs(directory)
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet(slugify(title)[:28])
	row_count = 0
	for row in data:
		cell_count = 0
		for cell in row:
			worksheet.write(row_count, cell_count, cell)
			cell_count += 1
		row_count += 1
	workbook.close()
