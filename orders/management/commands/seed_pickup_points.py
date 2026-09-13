from django.core.management.base import BaseCommand
from orders.models import PickupPoint


class Command(BaseCommand):
    help = 'Добавляет тестовые пункты выдачи СДЭК в Сочи'

    def handle(self, *args, **kwargs):
        points = [
            # СДЭК
            {'carrier': 'cdek', 'name': 'СДЭК Горького', 'address': 'ул. Горького, 58А', 'city': 'Сочи',
             'latitude': 43.593355, 'longitude': 39.729019, 'phone': '+7 (996) 051-81-74',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Виноградная', 'address': 'ул. Виноградная, 224/4', 'city': 'Сочи',
             'latitude': 43.633148, 'longitude': 39.708500, 'phone': '+7 (938) 877-08-43',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Искры', 'address': 'ул. Искры, 66/9', 'city': 'Сочи',
             'latitude': 43.492002, 'longitude': 39.902419, 'phone': '+7 (988) 404-33-96',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Курортный', 'address': 'Курортный проспект, 99 корп. 8', 'city': 'Сочи',
             'latitude': 43.553618, 'longitude': 39.773035, 'phone': '+7 (967) 623-11-05',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Красноармейская', 'address': 'ул. Красноармейская, 9Б', 'city': 'Сочи',
             'latitude': 43.598107, 'longitude': 39.718947, 'phone': '+7 (901) 101-09-70',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Albana', 'address': 'ул. Нагорная, 11', 'city': 'Сочи',
             'latitude': 43.578746, 'longitude': 39.728559, 'phone': '+7 (800) 201-13-08',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Макаренко', 'address': 'ул. Макаренко, 34/18', 'city': 'Сочи',
             'latitude': 43.611423, 'longitude': 39.740776, 'phone': '+7 (988) 231-69-89',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Центральная', 'address': 'ул. Центральная, 89', 'city': 'Сочи',
             'latitude': 43.798661, 'longitude': 39.467353, 'phone': '+7 (965) 474-18-18',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Просвещения', 'address': 'ул. Просвещения, 166', 'city': 'Сочи',
             'latitude': 43.478793, 'longitude': 39.892761, 'phone': '+7 (938) 875-59-71',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Яна Фабрициуса', 'address': 'ул. Яна Фабрициуса, 12/1', 'city': 'Сочи',
             'latitude': 43.576243, 'longitude': 39.748659, 'phone': '+7 (900) 001-65-15',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Пластунская', 'address': 'ул. Пластунская, 47а', 'city': 'Сочи',
             'latitude': 43.601873, 'longitude': 39.733528, 'phone': '+7 (862) 555-27-55',
             'work_time': 'Пн-Вс 09:00–20:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Гагарина', 'address': 'ул. Гагарина, 23А', 'city': 'Сочи',
             'latitude': 43.602382, 'longitude': 39.723150, 'phone': '+7 (966) 777-37-60',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Донская', 'address': 'ул. Донская, 54', 'city': 'Сочи',
             'latitude': 43.601000, 'longitude': 39.716000, 'phone': '+7 (495) 009-04-05',
             'work_time': 'Пн-Вс 08:00–21:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Волжская', 'address': 'ул. Волжская, 30', 'city': 'Сочи',
             'latitude': 43.632701, 'longitude': 39.700332, 'phone': '+7 (967) 623-10-90',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Голубые дали', 'address': 'ул. Голубые дали, 25', 'city': 'Сочи',
             'latitude': 43.451651, 'longitude': 39.905964, 'phone': '+7 (900) 232-59-09',
             'work_time': 'Пн-Пт 10:00–20:00, Сб-Вс 10:00–18:00'},
            {'carrier': 'cdek', 'name': 'СДЭК Ленина', 'address': 'ул. Ленина, 298Б', 'city': 'Сочи',
             'latitude': 43.485909, 'longitude': 39.894276, 'phone': '+7 (862) 555-13-40',
             'work_time': 'Пн-Вс 10:00–20:00'},
        ]

        created_count = 0
        for p in points:
            obj, created = PickupPoint.objects.get_or_create(
                name=p['name'],
                defaults=p
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Добавлено новых пунктов: {created_count}. Всего в базе: {PickupPoint.objects.count()}'
        ))