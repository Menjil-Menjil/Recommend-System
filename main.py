import pymysql
import config

VALID_KEYS = [
    'field',
    'tech_stack',
]

USER_DATA_KEY = [
    'user_id',
    'email',
    'provider',
    'nickname',
    'role',
    'birth_year',
    'birth_month',
    'school',
    'score',
    'score_range',
    'graduate_date',
    'graduate_month',
    'major',
    'sub_major',
    'minor',
    'company',
    'field',
    'tech_stack',
    'awards',
    'activity',
    'career',
    'certificate',
    'img_url',
    'created_at',
    'modified_at',
]

FOLLOWING_DATA_KEY = [
    'id',
    'user_nickname',
    'follow_nickname',
    'created_at',
]


def make_connection():
    return pymysql.connect(
        host=config.HOST,  # usually localhost or an IP address
        port=config.PORT,
        user=config.USERNAME,  # your username
        password=config.PW,  # your password
        database=config.DB  # the database you want to connect to
    )


def get_user_data(user_name):
    # 유저 정보 가져 오기.

    # Establish the connection
    connection = make_connection()

    # Create a cursor object
    cursor = connection.cursor()

    # Fetch data from the table
    cursor.execute("SELECT * FROM users WHERE nickname = '" + user_name + "';")
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        data = dict(zip(USER_DATA_KEY, row))

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return data


def get_followings(cursor, user_name):
    # Follows DB 조회

    data = []

    # Fetch data from the table
    cursor.execute("SELECT * FROM follows WHERE user_nickname = '" + user_name + "';")
    rows = cursor.fetchall()

    for row in rows:
        dic_data = dict(zip(FOLLOWING_DATA_KEY, row))
        data.append(dic_data)

    return data


def get_followings_data(user_name):
    # 유저가 팔로우 중인 유저 정보 가져 오기.

    data = []

    # Establish the connection
    connection = make_connection()

    # Create a cursor obje2ct
    cursor = connection.cursor()

    # Fetch following data
    followings_data = get_followings(cursor, user_name)
    following_nicknames_list = [row['follow_nickname'] for row in followings_data]

    # Fetch data from the table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    for row in rows:
        dic_data = dict(zip(USER_DATA_KEY, row))
        if dic_data['nickname'] in following_nicknames_list:
            print(dic_data['nickname'], dic_data['field'], dic_data['tech_stack'])
            data.append(dic_data)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return data


def get_mentor_data():
    # 역할이 "MENTOR"인 모든 유저 정보 가져 오기.

    data = []

    # Establish the connection
    connection = make_connection()

    # Create a cursor obje2ct
    cursor = connection.cursor()

    # Fetch data from the table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    for row in rows:
        dic_data = dict(zip(USER_DATA_KEY, row))
        if dic_data['role'] == 'MENTOR':
            # print(dic_data)
            data.append(dic_data)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return data


def create_scored_data(my_data, selected_data_list):
    selected_data_list.append(my_data)
    scored_dict_list = []

    for KEY in VALID_KEYS:
        scored_dict = {}
        for row_data in selected_data_list:
            values = row_data[KEY].split(', ')
            for key_value in values:
                if scored_dict.get(key_value):
                    scored_dict[key_value] += 1
                else:
                    scored_dict[key_value] = 1
        scored_dict_list.append(scored_dict)

    return dict(zip(VALID_KEYS, scored_dict_list))


def content_based_recommender(scored_database, total_data_list):
    result = []

    for user in total_data_list:
        user_dict = {'nickname': user['nickname'], 'total_score': 0}

        for KEY in VALID_KEYS:
            # 초기화
            user_dict[KEY] = 0
            # 유저의 점수 조회
            scored_dict = scored_database[KEY]
            values = user[KEY].split(', ')
            for key_value in values:
                key_value_score = scored_dict.get(key_value)
                if key_value_score:
                    user_dict[KEY] += key_value_score
                    user_dict['total_score'] += key_value_score

        result.append(user_dict)

    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 유저 닉네임 정보 입력
    USER_NAME = '한한'

    # fetch data from mysql
    user_data = get_user_data(USER_NAME)
    print(user_data['nickname'], user_data['field'], user_data['tech_stack'])
    following_data_list = get_followings_data(USER_NAME)
    mentor_data_list = get_mentor_data()

    # create scored data from fetched data
    scored_user_data = create_scored_data(user_data, following_data_list)
    print("==============================================추천 점수==============================================\n",
          scored_user_data,
          "\n추천 결과:")

    # achieve recommendation list from content-based recommend system
    recommended_user_list = content_based_recommender(scored_user_data, mentor_data_list)
    sorted_recommended_data_list = sorted(recommended_user_list, key=lambda user: (user['total_score']), reverse=True)
    for user in sorted_recommended_data_list:
        print(user)
