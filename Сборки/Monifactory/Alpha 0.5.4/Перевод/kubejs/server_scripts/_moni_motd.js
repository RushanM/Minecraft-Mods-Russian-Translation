PlayerEvents.loggedIn(event => {
    event.player.tell(['Добро пожаловать в ', Text.blue('альфа-версию Monifactory'), ` в режиме ${capitalize(`${global.packmode}`)}.`]); // принудительно преобразовать в строку
    event.player.tell(['Сообщайте об ошибках в ', Text.blue('репозиторий на GitHub').underlined().clickOpenUrl('https://github.com/ThePansmith/Monifactory').hover('Нажмите, чтобы открыть'), '.']);
})
