from lxml import etree
def print_tree(element, depth=0):
#""" Рекурсивная печать древовидной структуры элемента HTML """
# Вывод текущего элемента с соответствующим отступом
    print("-" * depth + element.tag)
# Рекурсивная печать дочерних элементов с увеличенным отступом
    for child in element.iterchildren():
        print_tree(child, depth + 1)
# Парсинг HTML-документа
tree = etree.parse("E:\Курс_DataScience_GeekBarains\Вторая_четверть\Сбор и разметка данных\Collection_data\Task_4\Task_4_in_office\In_office_4\src\web_page.html")
# Получение корневого элемента дерева
root = tree.getroot()
# Вывод структуры дерева
print_tree(root)
