#from oodocument import oodocument
#data = {}
#data['localcaakupe@gmail.com'] = '11111'
#data['celular'] = '2222'
#oo = oodocument('./input.docx', host='0.0.0.0', port=8001)
#oo.replace_with(data, './output.doc', 'doc')
#oo.replace_with(data, './output.pdf', 'pdf')
#oo.dispose()

#from oodocument import oodocument
#data = []
#header_style_name = "Estilo predeterminado"
#header_style_name = "Default Style"
#header_style_name = "Primera página"
#header_style_name = "First page"
#neighbor_character = 20
#data.append((4, 10, "XXX", "mundo"))
#oo = oodocument("./input2.docx", host="0.0.0.0", port=8001)
#oo.replace_with_index_in_header(data, "./output.pdf", "pdf", 0, neighbor_character, header_style_name)
#oo.dispose()


from oodocument import oodocument
data = []
data.append((1, 9, "XXX", "celular"))
data.append((32, 55, "XXX", "localcaakupe@gmail.com"))
oo = oodocument("./input2.docx", host="0.0.0.0", port=8001)
oo.set_clear_hyperlinks(True)
oo.replace_with_index(data, "./output.doc", "doc", 0, 0)
oo.dispose()
