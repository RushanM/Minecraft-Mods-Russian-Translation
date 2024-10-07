import os
import json
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from collections import defaultdict

# ===== Получение предыдущих данных =====
previous_proofread_dates = {}
prev_dates_file = 'previous_proofread_dates.json'
if os.path.exists(prev_dates_file):
    with open(prev_dates_file, 'r', encoding='utf-8') as f:
        previous_proofread_dates = json.load(f)
else:
    print("Файл previous_proofread_dates.json не найден. Предполагается первый запуск.")

# ===== Подключение к таблице на Google Таблицах =====
service_account_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_KEY'])
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scopes)
client = gspread.authorize(creds)

sheet_id = '1kGGT2GGdG_Ed13gQfn01tDq2MZlVOC9AoiD1s3SDlZE'
sheet = client.open_by_key(sheet_id)
worksheet = sheet.sheet1
data = worksheet.get_all_records()

# ===== Обработка данных =====
mod_lists = defaultdict(list)
current_proofread_dates = {}
for row in data:
    proofread = str(row.get('proofread', '')).strip()
    if proofread and proofread.upper() not in ['', 'FALSE']:
        gameVer = str(row.get('gameVer', '')).strip()
        mod_name = str(row.get('name', '')).strip()
        modrinth_id = str(row.get('modrinthId', '')).strip()
        curseforge_id = str(row.get('curseforgeId', '')).strip()
        fallback_url = str(row.get('fallbackUrl', '')).strip()

        # Сохранение текущей даты
        current_proofread_dates[mod_name] = proofread

        # Определение статуса перевода (новый, обновлённый, без изменений)
        prev_proofread_date = previous_proofread_dates.get(mod_name)
        if not prev_proofread_date:
            status = 'new'  # Новый мод
        elif prev_proofread_date != proofread:
            status = 'updated'  # Обновлённый мод
        else:
            status = 'unchanged'  # Без изменений

        # Получение ссылки на мод
        mod_url = ''
        if modrinth_id and modrinth_id.upper() != 'FALSE':
            # Modrinth
            response = requests.get(f'https://api.modrinth.com/v2/project/{modrinth_id}')
            if response.status_code == 200:
                mod_data = response.json()
                mod_url = mod_data.get('url', f'https://modrinth.com/mod/{modrinth_id}')
            else:
                mod_url = f'https://modrinth.com/mod/{modrinth_id}'
        elif curseforge_id and curseforge_id.upper() != 'FALSE':
            # CurseForge
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
        elif fallback_url and fallback_url.upper() != 'FALSE':
            mod_url = fallback_url # Используем ссылку из fallbackUrl
        else:
            mod_url = '' # Не удалось получить ссылку

        # Формирование строки мода
        date_str = f'<code>{proofread}</code>'
        mod_link = f'<a href="{mod_url}">{mod_name}</a>' if mod_url else mod_name

        # Добавление эмодзи и форматирования
        if status == 'new':
            emoji = '➕'
            mod_entry = f'<li><b>{emoji} {mod_link} {date_str}</b></li>'
        elif status == 'updated':
            emoji = '✏️'
            mod_entry = f'<li><b>{emoji} {mod_link} {date_str}</b></li>'
        else:
            # Без изменений
            mod_entry = f'<li>{mod_link} {date_str}</li>'

        mod_lists[gameVer].append((proofread, mod_entry))

# ===== Генерация тела выпуска =====

# Начало тела выпуска
release_body = """Это бета-выпуск всех переводов проекта. В отличие от альфа-выпуска, качество переводов здесь значительно выше, поскольку включены только те переводы, чьё качество достигло достаточно высокого уровня. Однако из-за этого охваченный спектр модов, сборок модов и наборов шейдеров значительно уже.

<details>
    <summary>
        <h3>🔠 Переведённые моды этого выпуска</h3>
    </summary>
    <br>
    <b>Условные обозначения</b>
    <br><br>
    <ul>
        <li>➕ — новый перевод</li>
        <li>✏️ — изменения в переводе</li>
        <li><code>ДД.ММ.ГГГГ</code> — дата последнего изменения</li>
    </ul>
    <br>
"""

# Для каждой версии игры создаём спойлер
for gameVer, mods in sorted(mod_lists.items(), key=lambda x: x[0]):
    # Сортировка модов внутри версии по дате (новые выше)
    mods.sort(key=lambda x: x[0], reverse=True)
    # Получаем последнюю дату для версии
    latest_date = max([proofread for proofread, _ in mods])
    # Определяем, есть ли новые или обновлённые моды
    version_status = ''
    for proofread, mod_entry in mods:
        mod_name = re.search(r'>([^<>]+)</a>', mod_entry)
        if mod_name:
            mod_name = mod_name.group(1)
        else:
            mod_name = mod_entry
        prev_date = previous_proofread_dates.get(mod_name)
        if not prev_date or prev_date != proofread:
            if not version_status:
                version_status = '✏️'
            break

    # Формируем заголовок спойлера для версии
    version_header = f'<summary><b>{gameVer}'
    if version_status:
        version_header += f' {version_status}'
    version_header += f' <code>{latest_date}</code></b></summary>'
    release_body += f'    <details>\n        {version_header}\n        <ul>\n'
    for _, mod_entry in mods:
        release_body += f'            {mod_entry}\n'
    release_body += '        </ul>\n    </details>\n'

release_body += '</details>\n\nЭтот выпуск является кандидатом на релиз. Если вы заметили какие-либо ошибки в этом выпуске, пожалуйста, сообщите об этом в разделе issues или отправьте сообщение [Дефлекте](https://github.com/RushanM)!'

# ===== Сохранение текущих данных =====
with open('current_proofread_dates.json', 'w', encoding='utf-8') as f:
    json.dump(current_proofread_dates, f, ensure_ascii=False, indent=4)

# ===== Установка выходного значения для release_body =====
with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_out:
    gh_out.write('release_body<<EOF\n')
    gh_out.write(release_body)
    gh_out.write('\nEOF\n')