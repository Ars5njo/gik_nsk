import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
import time
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
import emoji
import keyboard

bot = Bot('')
dp = Dispatcher()

list_of_teams = []
admins_id = open('admins.txt')
admins = list(map(int, admins_id.readline().split()))
all_admins = []
for i in admins:
    all_admins.append(i)
added_admins = []
g = open('info.txt')
lines = g.readlines()
users_id = set()
global get_answer
get_answer = False
global game
game = None
user_answers = {}
global nq
nq = 0
global registr
regisrt = None
dict_of_ans = dict()
check_teams = []


class Reg(StatesGroup):
    name = State()


# ADMIN BLOCK
@dp.message(Command('getinfo'))
async def info_for_admins(message: Message):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        admin_info = open('admin_info.txt')
        s = admin_info.read()
        await message.answer(f'{s}', parse_mode='HTML')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command('send_to_teams'))
async def send_to_teams(message: Message, command: CommandObject):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        msg = command.text.replace('/send_to_teams', '')
        if not msg:
            await message.answer('Вы отправили пустое сообщение')
        else:
            if not list_of_teams:
                await message.answer('Нет зарегистрированных команд')
            else:
                for i in list_of_teams:
                    await bot.send_message(chat_id=i[0],
                                           text=emoji.emojize(f':megaphone:Сообщение от жюри:<i>{msg}</i>'),
                                           parse_mode='HTML')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(F.text.lower() == 'начать игру')
async def stop(message: Message):
    global game
    if message.from_user.id in admins or message.from_user.id in added_admins:
        game = True
        await message.answer(f"Игра запущена")
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command('stop_game'))
async def stop(message: Message):
    global game, list_of_teams, users_id, user_answers, nq
    if message.from_user.id in admins or message.from_user.id in added_admins:
        game = False
        m = ("<b>Игра окончена.</b> \nНадеемся, что ты и твоя команда прекрасно провели игру. Мы обязательно ждем тебя "
             "снова! \nМы с вами уже настолько сроднились за эти несколько часов, что хотим оправдать ваши ожидания в "
             "следующей игре, поэтому просим вас дать нам <a href='https://clck.ru/39uaTC'>обратную связь</a> по "
             "прошедшей игре, чтобы игры становились только лучше! \nДо новых встреч!")
        for user_id in users_id:
            await bot.send_message(chat_id=user_id, text=m, parse_mode="HTML")
        await message.answer(f"Игра остановлена")
        list_of_teams.clear()
        users_id.clear()
        user_answers.clear()
        dict_of_ans.clear()
        check_teams.clear()
        nq = 0
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(F.text.lower() == 'включить таймер')
async def timer(message: Message):
    if game:
        if message.from_user.id in admins or message.from_user.id in added_admins:
            admin_messages = {}
            global get_answer
            global nq
            get_answer = True
            if users_id and list_of_teams:
                nq += 1
                for i in all_admins:
                    await bot.send_message(chat_id=i, text=f"Таймер запущен, вопрос №{nq}")
                    admin_timer = await bot.send_message(chat_id=i,
                                                         text=emoji.emojize('Осталось 60 секунд :hourglass_not_done:'))
                    admin_messages[i] = admin_timer.message_id
                for user_id in users_id:
                    user_answers[user_id] = [' ', None]
                    await bot.send_message(chat_id=user_id, text=f"Вопрос №{nq}")
                    # sent_message = await bot.send_message(chat_id=user_id,
                    # text=emoji.emojize(f"Осталось времени: <b>60</b> секунд/а :hourglass_not_done:."),
                    # parse_mode='HTML')
                    # user_messages[user_id] = sent_message.message_id
                for user_ans in users_id:
                    sent_message = await bot.send_message(chat_id=user_ans,
                                                          text=f'Cданный ответ: {user_answers[user_ans][0]}',
                                                          parse_mode='HTML')
                    user_answers[user_ans][1] = sent_message.message_id
                # time.sleep(0.5)
                for second in range(59, -1, -1):
                #for second in range(5, -1, -1):
                    for i in all_admins:
                        # for user_id in users_id:
                        # await bot.edit_message_text(chat_id=user_id, message_id=user_messages[user_id],
                        # text=emoji.emojize(f'Осталось времени: <b>{second}</b> секунд/а :hourglass_not_done:.'),
                        # parse_mode='HTML')
                        await bot.edit_message_text(chat_id=i, message_id=admin_messages[i], text=emoji.emojize(
                            f"Осталось времени: <b>{second}</b> секунд :hourglass_not_done:"), parse_mode='HTML')
                    time.sleep(0.70)
                for second in range(10, -1, -1):
                    for i in all_admins:
                        # for second in range(10, -1, -1):
                        # for user_id in users_id:
                        # await bot.edit_message_text(chat_id=user_id, message_id=user_messages[user_id],
                        # text=emoji.emojize(f'Осталось времени: <b>{second}</b> секунд/а.:hourglass_done:'),
                        # parse_mode='HTML')
                        await bot.edit_message_text(chat_id=i, message_id=admin_messages[i], text=emoji.emojize(
                            f"Осталось времени: <b>{second}</b> секунд :hourglass_done:"), parse_mode='HTML')
                    time.sleep(0.70)
                for user_id in users_id:
                    await bot.send_message(chat_id=user_id,
                                           text=emoji.emojize(f"<b>Время закончилось.</b> :chequered_flag:"),
                                           parse_mode='HTML')

                for i in all_admins:
                    await bot.send_message(chat_id=i,
                                           text=emoji.emojize(f"Время на вопрос №{nq} закочилось :chequered_flag:"))
                get_answer = False
                list_of_ans = ''
                list_of_ans += f"Вопрос №{nq} \n"
                list_of_ans += emoji.emojize('Лист ответов :memo:\n')
                for ids in user_answers:
                    for i in range(len(list_of_teams) - 1, -1, -1):
                        if ids == list_of_teams[i][0]:
                            list_of_ans += f"{list_of_teams[i][1]}: {user_answers[ids][0]} \n"
                            dict_of_ans[list_of_teams[i][1].lower()][nq - 1] = [nq, user_answers[ids][0], '']
                await bot.send_message('-4133213409', list_of_ans)
                user_answers.clear()
                await message.answer('Лист ответов отправлен в чат админов')
            else:
                await message.answer('Список команд пуст, попросите команды зарегистрироваться')
        else:
            await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))
    else:
        await message.answer(emoji.emojize(f"Игра не запущена :ZZZ:"))


global matrix
matrix = ''


@dp.message(Command('getmatrix'))
async def getmatrix(message: Message, command: CommandObject):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        global matrix
        matrix = command.text.replace('/getmatrix', '')
        if matrix:
            await message.answer('Матрица загружена')
        else:
            await message.answer('Что-то пошло не так')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command('sendmatrix'))
async def sendmatrix(message: Message):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        try:
            for user_id in users_id:
                await bot.send_message(chat_id=user_id, text=matrix)
            await message.answer('Матрица отправлена')
        except:
            await message.answer('Что-то пошло не так')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


global matrix_answer
matrix_answer = False


@dp.message(Command('get_matrix_start'))
async def get_matrix_start(message: Message):
    global matrix_answer
    if message.from_user.id in admins or message.from_user.id in added_admins:
        matrix_answer = True
        await message.answer('Сбор ответов матрицы открыт')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))

@dp.message(Command('get_matrix_stop'))
async def get_matrix_start(message: Message):
    global matrix_answer
    if message.from_user.id in admins or message.from_user.id in added_admins:
        matrix_answer = False
        await message.answer('Сбор ответов матрицы закрыт')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command('verdict'))
async def verdict(message: Message, command: CommandObject):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        verdicts = command.text.replace('/verdict', '').split()
        verdict_q = int(verdicts[0])
        list_of_verdicts = verdicts.copy()
        list_of_verdicts = list_of_verdicts[1:]
        list_of_verdicts = [i.split(':') for i in list_of_verdicts]
        for i in range(len(list_of_verdicts)):
            dict_of_ans[list_of_verdicts[i][0].lower()][verdict_q - 1][2] = list_of_verdicts[i][1]
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command('send_verdicts_to_teams'))
async def send_verdicts(message: Message):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        # msg_for_admins = []
        for team in list_of_teams:
            name = team[1]
            msg = ''
            cnt_of_pluses = 0
            for j in dict_of_ans[name.lower()]:
                if j[0] == '': break
                if j[2] == '+':
                    cnt_of_pluses += 1
                    msg += emoji.emojize(f'{j[0]}: {j[1]} :check_mark_button: \n')
                else:
                    msg += emoji.emojize(f'{j[0]}: {j[1]} :cross_mark: \n')
            msg += f'Количество правильных ответов: {cnt_of_pluses}'
            # msg_for_admins.append([name, cnt_of_pluses])
            await bot.send_message(chat_id=team[0], text=msg)

    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command('send_verdicts_to_admins'))
async def send_verdicts(message: Message):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        msg_for_admins = []
        for team in list_of_teams:
            name = team[1]
            msg = ''
            msg += emoji.emojize(f"{name} :speech_balloon: \n")
            cnt_of_pluses = 0
            for j in dict_of_ans[name.lower()]:
                if j[0] == '': break
                if j[2] == '+':
                    cnt_of_pluses += 1
                    msg += emoji.emojize(f'{j[0]}: {j[1]} :check_mark_button: \n')
                else:
                    msg += emoji.emojize(f'{j[0]}: {j[1]} :cross_mark: \n')
            msg += f'Количество правильных ответов: {cnt_of_pluses}'
            msg_for_admins.append([name, cnt_of_pluses])
            await bot.send_message(chat_id='-4133213409', text=msg)
        msg_for_admins.sort(key=lambda x: x[1])
        msg_for_admins = msg_for_admins[::-1]
        send = ''
        for i in msg_for_admins:
            send += f'{i[0]}: {i[1]}\n'
        await bot.send_message(chat_id='-4133213409', text=send)
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(F.text.lower() == 'список команд')
async def answer(message: Message):
    p = f'список команд: \n'
    index = 0
    for i in list_of_teams:
        index += 1
        p += f"{index}: {i[1]}, @{i[2]}\n"
    p += f"кол-во команд: {index}"
    if game:
        if message.from_user.id in admins or message.from_user.id in added_admins:
            if index == 0:
                await message.answer('Список команд пуст')
            else:
                await message.answer('Список команд отправлен в чат админов')
                await bot.send_message('-4133213409', p)
        else:
            await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))
    else:
        await message.answer(emoji.emojize(f"Игра не запущена :ZZZ:"))


@dp.message(Command("add_admins"))
async def adding(message: Message, command: CommandObject):
    name = command.text.replace('/add_admins ', '')
    if message.from_user.id in admins:
        try:
            added_admins.append(int(name))
            all_admins.append(int(name))
            await message.answer(f'Администратор с id {name} добавлен в админы')
        except:
            await message.answer(f'Что-то пошло не так')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command("remove_admins"))
async def removing(message: Message, command: CommandObject):
    name = command.text.replace('/remove_admins ', '')
    if message.from_user.id in admins:
        try:
            added_admins.remove(int(name))
            all_admins.remove(int(name))
            await message.answer(f'Администратор с id {name} удален из админов')
        except:
            await message.answer(f'Что-то пошло не так')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command("admin_list"))
async def list_of_admins(message: Message, command: CommandObject):
    if message.from_user.id in admins:
        s = 'Ссылки на профили основных админов \n'
        for id in admins:
            # s += f"<a href='tg://user?id={id}'>{id}</a> \n"
            s += f"tg://user?id={id} \n"
        if added_admins:
            s += 'Ссылки на профили вторых админов \n'
            for id in added_admins:
                # s += f"<a href='tg://user?id={id}'>{id}</a> \n"
                s += f"tg://user?id={id} \n"
        else:
            s += 'Вторых админов нет'
        await message.answer(s, parse_mode="HTML")
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command("remove_all"))
async def r(message: Message, command: CommandObject):
    if message.from_user.id in admins:
        added_admins.clear()
        await message.answer('Список вторых админов пуст')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


@dp.message(Command('remove_team'))
async def remove_team(message: Message, command: CommandObject):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        name = command.text.replace('/remove_team ', '')
        if not name:
            await message.answer('Нету названия команды для удаления')
        else:
            flag_find = 0
            for i in range(len(list_of_teams)):
                if list_of_teams[i][1] == name: flag_find = 1; users_id.discard(list_of_teams[i][0]); del list_of_teams[
                    i]; break
            if flag_find == 0:
                await message.answer(f'Команды с названием {name} нету в списке команд')
            else:
                await message.answer(f'Команда с названием {name} была удалена из списка команд')
    else:
        await message.answer(emoji.emojize(f"У вас нет доступа к этой команде :red_exclamation_mark:"))


# USER BLOCK
@dp.message(Command('start'))
async def start(message: Message):
    if message.from_user.id in admins or message.from_user.id in added_admins:
        await message.answer(
            f"Привет, админ! {emoji.emojize(':hammer:')} \nСнизу твоя панель управления \nЧтобы получить всю документацию для администрации, введи /getinfo",
            reply_markup=keyboard.admin_kb)
    else:
        await message.answer(
            f"Привет, {message.from_user.first_name}, это интеллектуальный бот ГИК'а. \nПрочитай инструкцию и следуй указаниям организаторов, "
            f"мы скоро начнем!", reply_markup=keyboard.info_kb
        )


@dp.message(F.text.lower() == 'инструкция для бота и информация о нас')
async def info(message: Message):
    msg = ''
    for i in lines:
        msg += f'{i} \n'
    await message.answer(f'{msg}', parse_mode='HTML', reply_markup=keyboard.links_kb)


@dp.message(F.text.lower() == 'зарегистрировать команду')
async def reg_team(message: Message, state: FSMContext):
    if game:
        if get_answer:
            await message.answer('Извините, сейчас идет время на обсуждение, регистрация команд недоступна, '
                                 'обратитесь к жюри')
        elif message.from_user.id not in users_id:
            await state.set_state(Reg.name)
            await message.answer("Введите название команды")
        else:
            for i in list_of_teams:
                if i[0] == message.from_user.id:
                    await message.answer(f"Вы уже зарегистрировали свою команду \nВаша команда: {i[1]}")
    else:
        await message.answer(emoji.emojize(f"Игра не запущена :ZZZ:"))


@dp.message(Reg.name)
async def get_team(message: Message, state: FSMContext):
    s = message.text
    if s.lower() in check_teams:
        await message.answer('Извините, команда с таким названием уже зарегистрировалась, если что-то пошло не так, '
                             'обратитесь к жюри')
    elif len(s) <= 30:
        await message.answer(f"Отлтично, команда {s} зарегистрирована")
        check_teams.append(s.lower())
        s = s.replace(" ", "|")
        list_for_dict = []
        for i in range(50):
            list_for_dict.append(['', '', ''])
        dict_of_ans[s.lower()] = list_for_dict
        await state.update_data(name=s)
        data = await state.get_data()
        users_id.add(message.from_user.id)
        list_of_teams.append([message.from_user.id, data["name"], message.from_user.username])
        list_of_teams.sort(key=lambda x: x[1])
        await state.clear()
    else:
        await message.answer("Извините, название вашей команды слишком длинное, пожалуйста, введите название короче.")


# @dp.message(Command('team'))
# async def team(message: Message, command: CommandObject):
#     name = command.text.replace('/team ', '')
#     if game:
#         if not name:
#             await message.answer(f'Введите название команды так, как требуют организаторы')
#         else:
#             a = name.split()
#             p = name.split()
#             p = ' '.join(p)
#             p = name.replace(' ', '_')
#             flag = 0
#             users_id.add(message.from_user.id)
#             for i in range(len(list_of_teams)):
#                 if list_of_teams[i][1] == p and list_of_teams[i][0] == message.from_user.id:
#                     flag = 1
#                     break
#             if flag == 1:
#                 tmp1 = ' '.join(a)
#                 await message.answer(f"Вау, {tmp1} уже есть в нашей системе!")
#                 list_of_teams.append([message.from_user.id, p, message.from_user.username])
#             else:
#                 list_of_teams.append([message.from_user.id, p, message.from_user.username])
#                 tmp2 = ' '.join(a)
#                 await message.answer(f"Отлично, команда {tmp2} зарегистрирована")
#                 # await bot.send_message('-1002036509118', f"Команда {tmp2} зарегистрировалась")
#     else:
#         await message.answer(emoji.emojize(f"Игра не запущена :ZZZ:"))


@dp.message()
async def answer(message: Message):
    global get_answer
    if message.from_user.id not in admins and message.from_user.id not in added_admins:
        if game:
            if get_answer:
                msg = message.text
                if type(msg) == str and len(msg) <= 50 and message.from_user.id not in admins and type(msg) == str:
                    ans = f'{msg}'
                    team = ''
                    for i in range(len(list_of_teams) - 1, -1, -1):
                        if list_of_teams[i][0] == message.from_user.id:
                            team = list_of_teams[i][1]
                            p = f'{team} {ans}'
                            break
                    if team:
                        p = p.split()
                        ans = ' '.join(p[1:])
                        user_answers[message.from_user.id][0] = ans
                        await bot.edit_message_text(chat_id=message.from_user.id,
                                                    message_id=user_answers[message.from_user.id][1],
                                                    text=emoji.emojize(f':memo:Cданный ответ: <b>{ans}</b>'),
                                                    parse_mode='HTML')
                    else:
                        await message.answer('Вы не зарегистрировали команду')
                else:
                    if message.from_user.id not in admins:
                        await message.answer(
                            f"Возможно, ответ слишком длинный или имеет некорректный тип. \nУ ГИК'а нет вопросов, ответ на который имеет такую длину или такой тип")
            elif matrix_answer:
                msg = message.text
                if type(msg) == str and message.from_user.id not in all_admins:
                    ans = f'{msg}'
                    team = ''
                    p = ''
                    for i in range(len(list_of_teams) - 1, -1, -1):
                        if list_of_teams[i][0] == message.from_user.id:
                            team = list_of_teams[i][1]
                            p = f'{team} \n{ans}'
                            break
                    if team:
                        await bot.send_message('-4133213409', p)
                    else:
                        await message.answer('Вы не зарегистрировали команду')
            else:
                if message.from_user.id not in admins:
                    await message.answer(f'Сдача ответов закрыта')
        else:
            await message.answer(emoji.emojize(f"Игра не запущена :ZZZ:"))


async def main():
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
