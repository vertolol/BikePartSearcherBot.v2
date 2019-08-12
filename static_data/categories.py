category_for_select = {
    'Горный велосипед': 'mtb',
    # 'Шоссейный велосипед': 'road'
}

mtb = {
    'Тормоза': 'mtb_brakes',
    'Вилки': 'mtb_forks',
    'Колеса': 'mtb_wheels',
    'Задние переключатели': 'mtb_rear_derailleurs'
}

mtb_brakes = {
    'Дисковые тормоза': 'mtb_disc_brakes',
    'Колодки для диск. торм.': 'mtb_disc_brake_pads',
    'Ободные тормоза': 'mtb_rim_brakes',
    'Колодки для обод. торм.': 'mtb_rim_brake_pads',
}

mtb_forks = {
    '26 дюймов': 'mtb_26_forks',
    '27,5 дюймов': 'mtb_27_forks',
    '29 дюймов': 'mtb_29_forks'
}

mtb_wheels = {
    '26 дюймов': 'mtb_26_wheels',
    '27,5 дюймов': 'mtb_27_wheels',
    '29 дюймов': 'mtb_29_wheels'
}

mtb_rear_derailleurs = {
    '9 скоростей': 'mtb_9_speed',
    '10 скоростей': 'mtb_10_speed',
    '11 скоростей': 'mtb_11_speed',
    '12 скоростей': 'mtb_12_speed'
}


categories_with_siblings = {
    'mtb': mtb,
    'mtb_brakes': mtb_brakes,
    'mtb_forks': mtb_forks,
    'mtb_wheels': mtb_wheels,
    'mtb_rear_derailleurs': mtb_rear_derailleurs
}
