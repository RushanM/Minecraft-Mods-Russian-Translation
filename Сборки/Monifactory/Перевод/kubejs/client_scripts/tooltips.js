ItemEvents.tooltip(tooltip => {

    // Микрокопатели

    function microminer_tooltip(tier) {
        tooltip.add(`kubejs:microminer_t${tier}`, Text.translatable(`item.kubejs.microminer_t${tier}.desc`))
    }
    for (let i = 1; i <= 12; i++) {
        microminer_tooltip(i)
    }

    tooltip.add('kubejs:microminer_t4half', Text.translatable('item.kubejs.microminer_t4half.desc'))
    tooltip.add('kubejs:microminer_t8half', Text.translatable('item.kubejs.microminer_t8half.desc'))

    tooltip.addAdvanced(['/kubejs:stabilized_microminer/'], (item, adv, text) => {
        text.add(1, '§7§oСтабилизрованная версия, в которую внедрено сердце вселенной.')
        text.add(2, '§7§oВечный срок службы. Многоразовый. Абсолютно не имбалансный.')
        text.add(3, '§7§oПодозрительно знакомо выглядит.')
    })

    tooltip.addAdvanced(['/kubejs:pristine_matter/'], (item, adv, text) => {
        text.add(1, '§7§oБесконечная и непостижимая бездна материалов.')
    })

    // Компоненты микрокопателей

    tooltip.add('kubejs:universal_navigator', '§9Досвидули, навигатор!')

    // Предметы конца игры

    tooltip.add('kubejs:ultimate_gem', '§eРецепт бесформенен.')

    // Материи DML

    tooltip.add('hostilenetworks:overworld_prediction', '§7Опыта за предмет: 10')
    tooltip.add('hostilenetworks:nether_prediction', '§7Опыта за предмет: 20')
    tooltip.add('hostilenetworks:end_prediction', '§7Опыта за предмет: 25')

    // Трубопроводы

    tooltip.add('enderio:conductive_conduit', '§7Максимальный вывод: 512 РТ/т')
    tooltip.add('enderio:energetic_conduit', '§7Максимальный вывод: 2048 РТ/т')
    tooltip.add('enderio:vibrant_conduit', '§7Максимальный вывод: 8192 РТ/т')
    tooltip.add('enderio:endsteel_conduit', '§7Максимальный вывод: 32768 РТ/т')
    tooltip.add('enderio:lumium_conduit', '§7Максимальный вывод: 131072 РТ/т')
    tooltip.add('enderio:signalum_conduit', '§7Максимальный вывод: 524288 РТ/т')
    tooltip.add('enderio:enderium_conduit', '§7Максимальный вывод: 2097152 РТ/т')
    tooltip.add('enderio:cryolobus_conduit', '§7Максимальный вывод: 8388608 РТ/т')
    tooltip.add('enderio:sculk_superconductor_conduit', '§7Максимальный вывод: 134217728 РТ/т')

    tooltip.add("thermal:device_rock_gen", "§7Требует размещения рядом с лавой и водой для производства булыжника.")
    tooltip.add("thermal:device_water_gen", "§7Для работы требует размещения рядом с двумя источниками воды.")

    tooltip.add(['thermal:upgrade_augment_1', 'thermal:upgrade_augment_2', 'thermal:upgrade_augment_4', 'thermal:upgrade_augment_3', 'thermal:dynamo_output_augment'], '§aНе берите предметы из EMI! Используйте рецепты создания, чтобы получить правильные данные NBT.')

    // Старое

    tooltip.addAdvanced(/storagedrawers:/, (item, advanced, text) => {
        text.add(1, [Text.red('Старое').bold()])
    })

    // Исправление текста GTCEU

    tooltip.addAdvanced(['gtceu:creative_energy', 'gtceu:creative_tank', 'gtceu:creative_chest', 'gtceu:creative_data_access_hatch'], (item, adv, text) => {
        if (text.size() > 3) text.remove(3);
        if (text.size() > 2) text.remove(2);
        if (text.size() > 1) text.remove(1);
        text.add(Text.join(Text.translatable('gtceu.creative_tooltip.1'), rainbowify(Text.translatable('gtceu.creative_tooltip.2').getString(), Math.round(Client.lastNanoTime / 100000000)), Text.translatable('gtceu.creative_tooltip.3')))
    });

    // Схемы

    tooltip.addAdvanced(`kubejs:matter_processor_mainframe`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня ПЭН`, Math.round(Client.lastNanoTime / 1000000000)))})
    tooltip.addAdvanced(`kubejs:matter_processor_computer`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня ПВН`, Math.round(Client.lastNanoTime / 1000000000)))})
    tooltip.addAdvanced(`kubejs:matter_processor_assembly`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня ПН`, Math.round(Client.lastNanoTime / 1000000000)))})
    tooltip.addAdvanced(`kubejs:matter_processor`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня НМНТ`, Math.round(Client.lastNanoTime / 1000000000)))})
    tooltip.addAdvanced(`kubejs:dimensional_processor_mainframe`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня ПБН`, Math.round(Client.lastNanoTime / 100000000)))})
    tooltip.addAdvanced(`kubejs:dimensional_processor_computer`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня ПЭН`, Math.round(Client.lastNanoTime / 100000000)))})
    tooltip.addAdvanced(`kubejs:dimensional_processor_assembly`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня ПВН`, Math.round(Client.lastNanoTime / 100000000)))})
    tooltip.addAdvanced(`kubejs:dimensional_processor`, (item, adv, text) => {text.add(1, rainbowifySingle(`Схема уровня ПН`, Math.round(Client.lastNanoTime / 100000000)))})
    tooltip.addAdvanced(`kubejs:monic_processor_mainframe`, (item, adv, text) => {text.add(1, Text.blue(`Схема уровня МАКС`))})
    tooltip.addAdvanced(`kubejs:monic_processor_computer`, (item, adv, text) => {text.add(1, Text.blue(`Схема уровня ПБН`))})
    tooltip.addAdvanced(`kubejs:monic_processor_assembly`, (item, adv, text) => {text.add(1, Text.blue(`Схема уровня ПЭН`))})
    tooltip.addAdvanced(`kubejs:monic_processor`, (item, adv, text) => {text.add(1, Text.blue(`Схема уровня ПВН`))})

    // Многоблочные структуры

    tooltip.add('moni_multiblocks:hypogean_infuser', Text.translatable('gtceu.sculk_reverberator.desc'))
    tooltip.add('gtceu:hypogean_reactor', Text.translatable('gtceu.hypogean_reactor.desc'))
    tooltip.add('gtceu:simulation_supercomputer', Text.translatable('gtceu.simulation_supercomputer.desc'))
    tooltip.add('gtceu:loot_superfabricator', Text.translatable('gtceu.loot_superfabricator.desc'))
    tooltip.add('gtceu:greenhouse', Text.translatable('gtceu.greenhouse.desc'))
    tooltip.add('gtceu:basic_microverse_projector', Text.translatable('gtceu.basic_microverse_projector.desc'))
    tooltip.add('gtceu:advanced_microverse_projector', Text.translatable('gtceu.advanced_microverse_projector.desc'))
    tooltip.add('gtceu:advanced_microverse_projector_ii', Text.translatable('gtceu.advanced_microverse_projector_ii.desc'))
    tooltip.add('gtceu:dimensional_superassembler', Text.translatable('gtceu.dimensional_superassembler.desc'))
    tooltip.add('gtceu:hyperbolic_microverse_projector', Text.translatable('gtceu.hyperbolic_microverse_projector.desc'))
    tooltip.add('gtceu:hyperbolic_microverse_projector', Text.translatable('gtceu.hyperbolic_microverse_projector_2.desc'))
    tooltip.add('gtceu:subatomic_digital_assembler', Text.translatable('gtceu.subatomic_digital_assembler.desc'))
    tooltip.add('gtceu:quintessence_infuser', Text.translatable('gtceu.quintessence_infuser.desc'))
    tooltip.add('gtceu:actualization_chamber', Text.translatable('gtceu.actualization_chamber.desc'))

    tooltip.addAdvanced('gtceu:universal_crystallizer', (item, adv, text) => {
        text.add(1, Text.darkGray('Огромное устройство, способное превращать сырьё в сложные материалы'))
        text.add(2, [Text.gray('Можно параллелить с '), Text.aqua('люками контроля параллелей')])
    })

    tooltip.addAdvanced('gtceu:naquadah_reactor_i', (item, adv, text) => {
        text.add(1, Text.gray('Продвинутый реактор, который производит энергию за счёт распада обогащённой наквады и наквадрии'))
        text.add(2, [Text.white('Производит ровно 3 ампера '), Text.red('НМНТ'), Text.white('.')])
        text.add(3, rainbowifySingle('Не перегревается!', Math.round(Client.lastNanoTime / 1000000000)))
    })

    tooltip.addAdvanced('gtceu:naquadah_reactor_ii', (item, adv, text) => {
        text.add(1, Text.gray('Элитный реактор, способный захватывать больше энергии от распада обогащённой наквады и наквадрии'))
        text.add(2, [Text.white('Производит ровно 3 ампера '), Text.translatable('\u00a73ПН'), Text.white('.')])
        text.add(3, rainbowifySingle('Не перегревается!', Math.round(Client.lastNanoTime / 1000000000)))
    })

    tooltip.add('gcyr:rocket_scanner', Text.darkGray('Поверните многоблочную структуру, если ракета не собирается.'))
    tooltip.add(['gtceu:hyperbolic_microverse_projector', 'gtceu:dimensional_superassembler', 'gtceu:hypogean_reactor', 'gtceu:quintessence_infuser'], 'Можно параллелить с люками управления параллелями.')

    // Sophisticated Storage

    tooltip.add(['sophisticatedstorage:diamond_barrel', 'sophisticatedstorage:diamond_chest', 'sophisticatedstorage:diamond_shulker_box'], 'Используйте обновление уровня с железного до алюминиевого на предыдущем уровне, чтобы получить это')
    tooltip.add(['sophisticatedstorage:netherite_barrel', 'sophisticatedstorage:netherite_chest', 'sophisticatedstorage:netherite_shulker_box'], 'Используйте обновление уровня с алюминиевого до нержавеющей стали на предыдущем уровне, чтобы получить это')

    // AE2

    tooltip.add('ae2:facade', Text.gray('Создано с помощью креплений для кабелей'))

    // Различное

    tooltip.add('kubejs:eternal_catalyst', Text.darkGray('Всмотрись в бездну…'))
    tooltip.add('kubejs:infinity_catalyst', Text.darkGray('Одно есть всё, и всё есть одно.'))
    tooltip.add('gtceu:infinity_ingot', Text.darkGray('Ярость вселенной в ваших руках.'))
    tooltip.add('gtceu:monium_ingot', Text.darkGray('Спокойствие вселенной в ваших руках.'))
    tooltip.add('extendedcrafting:the_ultimate_catalyst', Text.darkGray("Я — истинный пиковый катализатор…"))
    tooltip.add('extendedcrafting:the_ultimate_component', Text.darkGray("Нет никого лучше меня…"))
    tooltip.add('kubejs:excitationcoil', 'Исключительно компонент рецептов')

    // Подсказки NuclearCraft

    tooltip.add('nuclearcraft:rhodochrosite_dust', '§eMnCO₃');
    tooltip.add('nuclearcraft:tough_alloy_ingot', '§eLiFeB');
    tooltip.add('nuclearcraft:ferroboron_ingot', '§eFeB');
    tooltip.add('nuclearcraft:hard_carbon_ingot', '§eFe₃C');
    tooltip.add('nuclearcraft:uranium_233', '§eU²³³');
    tooltip.add('nuclearcraft:plutonium_238', '§ePu²³⁸');
    tooltip.add('nuclearcraft:plutonium_242', '§ePu²⁴²');
    tooltip.add('nuclearcraft:neptunium_236', '§eNp²³⁶');
    tooltip.add('nuclearcraft:neptunium_237', '§eNp²³⁷');
    tooltip.add('nuclearcraft:americium_241', '§eAm²⁴¹');
    tooltip.add('nuclearcraft:americium_242', '§eAm²⁴²');
    tooltip.add('nuclearcraft:americium_243', '§eAm²⁴³');
    tooltip.add('nuclearcraft:curium_243', '§eCm²⁴³');
    tooltip.add('nuclearcraft:curium_245', '§eCm²⁴⁵');
    tooltip.add('nuclearcraft:curium_246', '§eCm²⁴⁶');
    tooltip.add('nuclearcraft:curium_247', '§eCm²⁴⁷');
    tooltip.add('nuclearcraft:berkelium_247', '§eBk²⁴⁷');
    tooltip.add('nuclearcraft:berkelium_248', '§eBk²⁴⁸');
    tooltip.add('nuclearcraft:californium_249', '§eCf²⁴⁹');
    tooltip.add('nuclearcraft:californium_251', '§eCf²⁵¹');
    tooltip.add('nuclearcraft:californium_252', '§eCf²⁵²');

    tooltip.addAdvanced(['/^kubejs:.+infinity_dust_block$/', 'kubejs:infinity_dust_block'], (item, adv, text) => {
        text.add(1, Text.gray('Не совсем твёрдый'))
    })
})