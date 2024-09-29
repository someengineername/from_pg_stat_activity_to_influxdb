import db_config
import psycopg2
import requests
from time import sleep


def main():
    while ...:
        sleep(1)
        connection = psycopg2.connect(
            host='192.168.0.132',
            port='5430',
            user=db_config.user,
            password=db_config.password,
            database=db_config.db_name
        )

        connection.set_session(autocommit=True)

        with connection.cursor() as cursor:
            command_new_user = f"select * from pg_stat_activity where client_addr is not NULL"
            cursor.execute(command_new_user)
            active_connections = cursor.fetchall()

        set_of_adresses = set([i[7] for i in active_connections])

        temp_dict = dict()

        for pos in set_of_adresses:
            temp_dict.setdefault(pos, len(list(filter(lambda x: x[7] == pos, active_connections))))

        print(temp_dict)

        url_line = f'http://192.168.0.132:8086/write?db=telegraf_metrics'

        if len(temp_dict) == 1:
            for k in temp_dict.keys():
                data_str = f"connections1,session_holder={k} active_connections={temp_dict[k]}"
        else:
            temp_list = []
            for k in temp_dict.keys():
                temp_list.append(f'connections1,session_holder={k} active_connections={temp_dict[k]}')
            data_str = '\n'.join(temp_list)

        print(data_str)

        try:
            res = requests.post(url=url_line, data=data_str)
            print(f'Send data: {data_str}')
        except Exception as e:
            print(e, e.__class__.__name__)


if __name__ == '__main__':
    main()
