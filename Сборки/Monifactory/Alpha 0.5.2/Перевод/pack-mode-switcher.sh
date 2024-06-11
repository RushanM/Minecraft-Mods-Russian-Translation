#!/usr/bin/env sh

# Colors
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
POWDER_BLUE=$(tput setaf 153)
MAGENTA=$(tput setaf 5)
NORMAL=$(tput sgr0)

touch .mode
set -e
printf "${POWDER_BLUE}Monifactory | Переключатель режима игры${NORMAL}"

NORMAL_CFG='./config-overrides/normal'
HARDMODE_CFG='./config-overrides/hardmode'
HARDER_CFG='./config-overrides/harder'
TARGET='./config'
CURRENT_MODE="$(head .mode)"
CURRENT_MODE=${CURRENT_MODE:="normal"}

# Check if config-overrides dir exists
if [[ ! -d "${NORMAL_CFG}" ]] || [[ ! -d "${HARDMODE_CFG}" ]] || [[ ! -d "${HARDER_CFG}" ]] ; then
  printf "\n\n${RED}Каталог «config-overrides» не найден! \nУбедитесь, что вы в каталоге «/minecraft» вашей установки игры! (Тот, который имеет путь к «/config»)${NORMAL}\n"
  printf "${YELLOW}Если вы уже в каталоге «/minecraft», попробуйте переустановить сборку.${NORMAL}\n"
  exit 1
fi

# Capitalise First Letter (only works in bash 4+)
[ "${BASH_VERSINFO:-0}" -ge 4 ] && CURRENT_MODE=${CURRENT_MODE^}

printf "\n\n${YELLOW}Текущий режим: ${CURRENT_MODE}${NORMAL}\n"

if [ -z "$1" ]; then
  printf "${POWDER_BLUE}Установите режим игры: [Обычный / Сложный режим / Более сложный]: ${NORMAL}"
  read MODE
else
  MODE="$1"
fi

case $MODE in
    О|о|обычный|Обычный)

    cp -rf "$NORMAL_CFG/." ${TARGET} 

    # Only copy server.properties if it exists.
    if [ -f "server.properties" ]; then
        mv "${TARGET}/server.properties" ./
    else
        rm "${TARGET}/server.properties" || true
    fi

    # Update Mode
    echo normal > .mode
  ;;

  С|с|сложный режим|Сложный режим)

    cp -rf "$HARDMODE_CFG/." ${TARGET}

    if [ -f "server.properties" ]; then
        mv "${TARGET}/server.properties" ./
    else
        rm "${TARGET}/server.properties" || true
    fi

    # Update Mode
    echo hard > .mode
  ;;

  Б|б|более сложный|Более сложный)

    cp -rf "$HARDER_CFG/." ${TARGET}

    if [ -f "server.properties" ]; then
        mv "${TARGET}/server.properties" ./
    else
        rm "${TARGET}/server.properties" || true
    fi

    # Update Mode
    echo harder > .mode
  ;;

  *)
    printf "\n${RED}Ошибка: Неправильный ввод ${MODE}!${NORMAL}\n"
    printf "\n${POWDER_BLUE}Принимаемые значения:\n${YELLOW}- [Обычный, обычный, О, о]\n- [Сложный режим, сложный режим, С, с]\n- [Более сложный, более сложный, Б, б]${NORMAL}\n"
    exit 1
  ;;
esac

printf "\n${GREEN}Готово!${NORMAL}\n"
