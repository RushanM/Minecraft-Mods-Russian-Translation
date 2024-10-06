import os
import json
import sys
import re
from datetime import datetime
from collections import Counter

import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Настройки
SPREADSHEET_ID = '1kGGT2GGdG_Ed13gQfn01tDq2MZlVOC9AoiD1s3SDlZE'
REQUESTS_SHEET_NAME = 'requests'
NUM_TOP_MODS = 4

# Аутентификация с помощью служебной учётной записи
def get_google_sheet_service():
    credentials_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_KEY'])
    credentials = Credentials.from_service_account_info(
        credentials_info, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_sheet_values(service, sheet_name):
    range_name = f'{sheet_name}!A1:Z1000'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=range_name).execute()
    values = result.get('values', [])
    return values

def get_mod_requests_data():
    service = get_google_sheet_service()
    values = get_sheet_values(service, REQUESTS_SHEET_NAME)
    if not values:
        print('Данные не найдены.')
        sys.exit(1)
    headers = values[0]
    data = [dict(zip(headers, row)) for row in values[1:]]
    return data

def count_mod_requests(data):
    mod_names = [row['name'] for row in data]
    counter = Counter(mod_names)
    return counter

def get_top_mods(counter):
    top_mods = counter.most_common(NUM_TOP_MODS)
    return top_mods

def get_mod_info(mod_name, data):
    mod_entries = [row for row in data if row['name'] == mod_name]
    # Собираем все версии игры
    game_versions = [row.get('gameVer', '') for row in mod_entries]
    # Определяем наиболее частую версию игры
    game_ver_counter = Counter(game_versions)
    most_common_game_ver = game_ver_counter.most_common(1)[0][0] if game_ver_counter else ''
    # Берём первую запись для получения modrinthId, curseforgeId
    mod_entry = mod_entries[0].copy()
    # Обновляем `gameVer` на наиболее частую
    mod_entry['gameVer'] = most_common_game_ver
    return mod_entry

def fetch_mod_icon_and_link(mod_entry):
    modrinth_id = mod_entry.get('modrinthId', '')
    curseforge_id = mod_entry.get('curseforgeId', '')
    name = mod_entry.get('name', '')
    icon_url = ''
    mod_link = ''
    if modrinth_id and modrinth_id.lower() != 'false':
        # Используем Modrinth API
        modrinth_api_url = f'https://api.modrinth.com/v2/project/{modrinth_id}'
        response = requests.get(modrinth_api_url)
        if response.status_code == 200:
            mod_data = response.json()
            icon_url = mod_data.get('icon_url', '')
            mod_link = mod_data.get('website_url', f'https://modrinth.com/mod/{modrinth_id}')
        else:
            print(f'Не удалось получить данные {name} с Modrinth')
    elif curseforge_id and curseforge_id.lower() != 'false':
        # Используем CurseForge API
        print(f"Смотрим мод {name}, идентификатор у него: {curseforge_id}")
        api_key = os.environ.get('CFCORE_API_TOKEN')
        if not api_key:
            print('CFCORE_API_TOKEN не установлен.')
        else:
            headers = {'x-api-key': api_key}
            curseforge_api_url = f'https://api.curseforge.com/v1/mods/{curseforge_id}'
            response = requests.get(curseforge_api_url, headers=headers)
            if response.status_code == 200:
                mod_data = response.json()['data']
                icon_url = mod_data.get('logo', {}).get('url', '')
                mod_link = mod_data.get('links', {}).get('websiteUrl', '')
            else:
                print(f'Не удалось получить данные {name} с CurseForge')
                print(f"Состояние HTTP: {response.status_code}, ответ получен такой: {response.text}")
    else:
        print(f'У {name} нет ни верного modrinthId ни верного curseforgeId')
    return icon_url, mod_link

def decline_prosba(n):
    n = abs(int(n))
    n_mod_10 = n % 10
    n_mod_100 = n % 100
    if n_mod_10 == 1 and n_mod_100 != 11:
        return "просьба"
    elif n_mod_10 in [2, 3, 4] and n_mod_100 not in [12, 13, 14]:
        return "просьбы"
    else:
        return "просьб"

def generate_mods_table(top_mods, data):
    table_rows = []
    for mod_name, request_count in top_mods:
        mod_entry = get_mod_info(mod_name, data)
        icon_url, mod_link = fetch_mod_icon_and_link(mod_entry)
        game_ver = mod_entry.get('gameVer', '')
        # Подготовка строки таблицы
        icon_html = f'<img width=80 height=80 src="{icon_url}">' if icon_url else ''
        mod_link_html = f'**[{mod_name}]({mod_link})**' if mod_link else f'**{mod_name}**'
        prosba_form = decline_prosba(request_count)
        table_cell = f'<big>{mod_link_html}</big><br>{game_ver}<br>*{request_count} {prosba_form}*'
        table_rows.append(f'| {icon_html} | {table_cell} |')
    return table_rows

def update_readme(table_rows):
    # Читаем README.md
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Формируем новую таблицу
    table_header = '| Значок | Описание |\n| :-: | :-: |'
    table = '\n'.join([table_header] + table_rows)

    # Регулярное выражение для поиска существующей таблицы
    pattern = re.compile(
        r'## Моды востребованные для перевода\n\n.*?<div align=center>\n\n(.*?)\n\n</div>',
        re.DOTALL
    )

    # Заменяем существующую таблицу на новую
    new_section = f'## Моды востребованные для перевода\n\nЛюди больше всего просят перевести эти моды, но они до сих пор не переведены из-за размеров перевода. Если вы нашли в себе силы и имеете достаточно опыта, можете взяться за них.\n\n<div align=center>\n\n{table}\n\n</div>'

    new_content = re.sub(pattern, new_section, content)

    # Записываем обновлённый README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    data = get_mod_requests_data()
    counter = count_mod_requests(data)
    top_mods = get_top_mods(counter)
    table_rows = generate_mods_table(top_mods, data)
    update_readme(table_rows)

if __name__ == '__main__':
    main()