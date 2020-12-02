#Library list
import sqlite3
import telebot
from telebot import types
from string import Template
from datetime import datetime
#Bot Token
bot = telebot.TeleBot('Enter-Bot-Token') #<- Insert your bot token
#Forwarding gorup id
group_id = 'Enter Your Group ID' #<- Insert your group id
#Database
db = sqlite3.connect('student_db.db', check_same_thread=False)
cursor = db.cursor()
sql = sqlite3.connect("student_id.db", check_same_thread=False)
check = sql.cursor()
user_data = {}
class User:
    def __init__(self, id):
        self.id = id
        self.level = ''
        self.faculty = ''
        self.course = ''
        self.professor = ''
        self.point = 0
        self.log = ''
#commands
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton("/survey")
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Hello "
                     + message.from_user.first_name
                     + ", I'm survey bot developed by TTPU student PJ ", reply_markup=markup)
#/about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "This telegram bot Developed By PJ")
#/survey
@bot.message_handler(commands=['survey'])
def send_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Please Enter Your Student ID", reply_markup=markup)
    bot.register_next_step_handler(msg, process_id_step)
#Validation student ID
def process_id_step(message):
    check.execute("SELECT * FROM 'student_id' WHERE std_id= ?", [message.text])
    access = check.fetchone()
    if (access == None):
        bot.send_message(message.chat.id, "Invalid Student ID")
    else:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        keyboard = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('PY')
        itembtn2 = types.KeyboardButton('1ST')
        itembtn3 = types.KeyboardButton("2ND")
        itembtn4 = types.KeyboardButton("3RD")
        keyboard.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(message.chat.id, text='Choose your Academic Level', reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_level_step)

#Fcultys
def process_level_step(message):
    try:
        user_id = message.from_user.id
        User = user_data[user_id]
        User.level = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('IT')
        itembtn2 = types.KeyboardButton('ME')
        itembtn3 = types.KeyboardButton('CIE')
        itembtn4 = types.KeyboardButton('AE')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(message.chat.id, 'Choose your Faculty', reply_markup=markup)
        bot.register_next_step_handler(msg, process_faculty_step)
    except Exception as e:
        bot.reply_to(message, "oooops!")

#Subjects
def process_faculty_step(message):
    try:
        user_id = message.from_user.id
        User = user_data[user_id]
        User.faculty = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(*[types.KeyboardButton(name) for name in ['PHYSICS', 'MATH']])
        markup.add(*[types.KeyboardButton(name) for name in ['COMPUTER SCIENCE', 'CHEMISTRY']])
        msg = bot.send_message(user_id, 'Choose your Course', reply_markup=markup)
        bot.register_next_step_handler(msg, process_course_step)
    except Exception as e:
        bot.reply_to(message, "oooops!")

#Menu with Submenu for professor
def process_course_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.course = message.text

        if message.text == 'PHYSICS':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['UMMARINO', "ABDULAYEV"]])
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['MORISIO', 'SILBERBERG']])
            msg = bot.send_message(message.chat.id, 'Choose your Professor', reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_professor_step)
        elif message.text == 'MATH':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['DZHALILOV', "KARIMOV"]])
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['MUSSO', 'SAFAROV']])
            msg = bot.send_message(message.chat.id, 'Choose your Professor', reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_professor_step)
        elif message.text == 'COMPUTER SCIENCE':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['YUSUPOV', "MAHAMMATOV"]])
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['MARCHETTO', 'URINBOEV']])
            msg = bot.send_message(message.chat.id, 'Choose your Professor', reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_professor_step)
        elif message.text == "CHEMISTRY":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['TULYAGANOV', "SOLIYEV"]])
            keyboard.add(*[types.KeyboardButton(advert) for advert in ['RUZIMURODOV', 'SILBERBERG']])
            msg = bot.send_message(message.chat.id, 'Choose your Professor', reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_professor_step)
    except Exception as e:
        bot.reply_to(message, "oooops!")

#Professor
def process_professor_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.professor = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('1')
        itembtn2 = types.KeyboardButton('2')
        itembtn3 = types.KeyboardButton('3')
        itembtn4 = types.KeyboardButton('4')
        itembtn5 = types.KeyboardButton('5')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

        msg = bot.send_message(message.chat.id, 'Set Point from 1 to 5 ', reply_markup=markup)
        bot.register_next_step_handler(msg, process_point_step)
    except Exception as e:
        bot.reply_to(message, "oooops!")

#student_point
def process_point_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.point = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('SEND')
    today = datetime.now()
    markup.add(itembtn1)
    msg = bot.send_message(message.chat.id, "Click on SEND for Send Application", reply_markup=markup)
    bot.register_next_step_handler(msg, process_log_step)

def process_log_step(message):
    today = datetime.now()
    user_id = message.from_user.id
    user = user_data[user_id]
    user.log = today

    # ADding to DataBase
    sql = "INSERT OR IGNORE INTO student_database (student_id, student_level, student_faculty, student_course,professor,student_point,student_log) VALUES (?, ?, ?, ?, ?,?,?)"
    val = (user.id, user.level, user.faculty, user.course, user.professor,user.point,user.log)
    cursor.execute(sql, val)
    db.commit()

    # Student Application
    bot.send_message(user_id, getregdata(user, 'Your response accepted', message.from_user.first_name),
                     parse_mode="Markdown")
    # Forwarding to group
    bot.send_message(group_id, getregdata(user, 'Response from PolitoAcademic', bot.get_me().username),
                     parse_mode="Markdown")

def getregdata(user, title, name):
    t = Template(
        '$title *$name* \nStudentID: *$id* \nStudentLevel: *$level* \nStudentFaculty: *$faculty* \nStudentCourse: *$course* \nProfessor: *$professor* \nStudentPoint: *$point*\n StudentLog: *$log*')
    return t.substitute({
        'title': title,
        'name': name,
        'id': user.id,
        'level': user.level,
        'faculty': user.faculty,
        'course': user.course,
        'professor': user.professor,
        'point': user.point,
        'log': user.log

    })

@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, 'About us - /about\nStarting - Survey - /survey\nHelp - /help')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)






