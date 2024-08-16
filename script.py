from random import randint, choice
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


def get_student_info(name: str):
    """Ищет информацию по ученику в БД

    Args:
        name (str): ФИО ученика

    Raises:
        ValueError: В БД, нет подходящего имени

    Returns:
       QuerySet: Возвращает информацию об ученике
    """
    try:
        child = Schoolkid.objects.get(full_name__contains=name)
        return child
    except Schoolkid.DoesNotExist:
        raise ValueError('Данного ученика нет в БД, проверьте правильность передаваеммых данных')
    except Schoolkid.MultipleObjectsReturned:
        childs = Schoolkid.objects.filter(full_name__contains=name)
        for child in childs:
            print(child)
        raise ValueError('По вашему запросу выдало несколько человек, введите пожалуйста, более точное ФИО ученика')


def fix_marks(name: str) -> None:
    """Ищет в БД плохие оценки и изменяет их на хорошие

    Args:
        name (str): ФИО ученика
    """
    child = get_student_info(name)
    marks = Mark.objects.filter(schoolkid=child, points__in=[2,3])
    
    for mark in marks:
        point = randint(4, 5)
        Mark.objects.filter(created=mark.created,
                            subject=mark.subject,
                            points=mark.points,
                            schoolkid=mark.schoolkid).update(points=point)


def remove_chastisements(name: str) -> None:
    """Удаляет из БД замечания, созданные для запрашиваеммого ученика

    Args:
        name (str): ФИО ученика
    """
    child = get_student_info(name)
    chastisements = Chastisement.objects.filter(schoolkid=child)
    chastisements.delete()
    
    
def create_commendation(name: str, subject: str) -> None:
    """Добавляет в БД, по названию предмета, благодарность ученику

    Args:
        name (str): ФИО ученика
        subject (str): Название предмета
    """
    commendations = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                     'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                     'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                     'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
                     'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
                     'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
                     'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
                     'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']
    
    child = get_student_info(name)
    try:
        lesson = Lesson.objects.filter(year_of_study=child.year_of_study,
                                       group_letter=child.group_letter,
                                       subject__title=subject).order_by('?').first()
    except IndexError:
        raise ValueError('Данного предмета нет в БД, проверьте правильность передаваеммых данных')
    
    
    if Commendation.objects.filter(created=lesson.date, schoolkid=child, subject=lesson.subject, teacher=lesson.teacher):
        return create_commendation(name, subject)
    else:
        Commendation.objects.create(text=choice(commendations), created=lesson.date, schoolkid=child,
                                    subject=lesson.subject, teacher=lesson.teacher)
