from parsel import Selector
import re

with open('lotek.txt', 'r', encoding='utf-8') as file:
    source = Selector(file.read())

price = source.xpath('//div[@class="zdrapka_main_price"]/text()').get()
price = price.split()[2]

total_remaining_pool = source.xpath('//div[@class="zdrapka_mini_actual_winner"]/div[@class="apnw"]/b/text()').get()
total_remaining_pool = ''.join([x for x in total_remaining_pool if x.isdigit()])

remaining_winnings = source.xpath('//table[@class="table_aktualne_wygrane"]/descendant::tr').getall()
remaining_winnings = [x.replace('<strong>', '').replace('</strong>', '') for x in remaining_winnings]
rem_amount_pattern = r'right;\">[\d\s]+'
rem_winnings_pattern = r'\"kwota\">[\d\s]+'

printed_amount = source.xpath('//*[contains(text(), "Nakład")]/following-sibling::*[1]/text()').get()
printed_amount = ''.join([x for x in printed_amount if x.isdigit()])

original_winnings = source.xpath('//*[text()="Liczba wygranych"]/../../../following-sibling::tr').getall()
ori_amount_pattern = r'>([\d\s]+)<'
ori_winnings_pattern = r'>([\d\s]+)[a-zA-ZłŁ]+<'


print('Cena: ', price)
print('Aktualna pula na wygrane: ', total_remaining_pool)
print('Kwoty: ')
for x in remaining_winnings:
    print(re.findall(rem_amount_pattern, x)[0].split('>')[1], 'x', re.findall(rem_winnings_pattern, x)[0].split('>')[1])
print('Nakład: ', printed_amount)
print('Początkowe nagrody: ')
for x in original_winnings:
    print(re.findall(ori_amount_pattern, x)[0], ':', re.findall(ori_winnings_pattern, x)[0])
