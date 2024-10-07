import os
import json
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# Загрузка данных учётной записи службы Google
service_account_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_KEY'])

# Авторизация в Google Sheets API
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scopes)
client = gspread.authorize(creds)

# Открытие таблицы и получение данных
sheet_id = '1kGGT2GGdG_Ed13gQfn01tDq2MZlVOC9AoiD1s3SDlZE'
sheet = client.open_by_key(sheet_id)
worksheet = sheet.sheet1

data = worksheet.get_all_records()

from collections import defaultdict

# Обработка данных и создание списков модов для каждой версии игры
mod_lists = defaultdict(list)
for row in data:
    proofread = str(row.get('proofread', '')).strip()
    if proofread and proofread not in ['', 'FALSE']:
        gameVer = str(row.get('gameVer', '')).strip()
        mod_name = str(row.get('name', '')).strip()
        modrinth_id = str(row.get('modrinthId', '')).strip()
        curseforge_id = str(row.get('curseforgeId', '')).strip()
        
        if modrinth_id and modrinth_id.upper() != 'FALSE':
            # Получаем ссылку на Modrinth
            response = requests.get(f'https://api.modrinth.com/v2/project/{modrinth_id}')
            if response.status_code == 200:
                mod_data = response.json()
                mod_url = mod_data.get('url', f'https://modrinth.com/mod/{modrinth_id}')
            else:
                mod_url = f'https://modrinth.com/mod/{modrinth_id}'
        elif curseforge_id and curseforge_id.upper() != 'FALSE':
            # Получаем ссылку на CurseForge
            API_KEY = os.environ.get('CF_API_KEY')
            headers = {
                'Accept': 'application/json',
                'x-api-key': API_KEY
            }
            response = requests.get(f'https://api.curseforge.com/v1/mods/{curseforge_id}', headers=headers)
            if response.status_code == 200:
                mod_data = response.json().get('data', {})
                mod_url = mod_data.get('links', {}).get('websiteUrl', f'https://www.curseforge.com/minecraft/mc-mods/{curseforge_id}')
            else:
                mod_url = f'https://www.curseforge.com/minecraft/mc-mods/{curseforge_id}'
        else:
            mod_url = '' # Невозможно получить ссылку без идентификатора
        
        mod_entry = f'* [{mod_name}]({mod_url})' if mod_url else f'* {mod_name}'
        mod_lists[gameVer].append(mod_entry)

# Установка выводов для использования в последующих шагах
with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_out:
    for gameVer, mods in mod_lists.items():
        mod_list_str = '\n'.join(mods)
        output_name = f'mod_list_{gameVer.replace(".", "_").replace("-", "_")}'
        gh_out.write(f'{output_name}<<EOF\n')
        gh_out.write(f'{mod_list_str}\n')
        gh_out.write('EOF\n')