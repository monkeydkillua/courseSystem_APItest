import requests
import json


class TestTeacher(object):
    def __init__(self, url, session_id):
        # 可以用 f , f'http://{API_SERVER}/api/mgr/sq_mgr'
        self.fullUrl = url
        self.session_id = session_id

    # 添加老师
    def add_teacher(self, user_name, real_name, desc='', password=123, display_idx=1, courses=[]):
        teacher_info = {"username": user_name,
                        "password": password,
                        "realname": real_name,
                        "desc": desc,
                        "courses": courses,
                        'display_idx': display_idx
                        }
        teacher_data = json.dumps(teacher_info)
        add_teacher_def = {'action': 'add_teacher',
                           'data': teacher_data
                          }

        result = requests.post(self.fullUrl, data=add_teacher_def, cookies={'sessionid': self.session_id})
        teacher_info_return = {}
        if result.json()['retcode'] == 0:
            teacher_info_return = {'username': user_name,
                                   'realname': real_name,
                                   'display_idx': display_idx,
                                   'courses': courses,
                                   'id': result.json()['id'],
                                   'desc': desc
                                   }
        return result.json(), teacher_info_return

    # 列出老师
    def show_teacher(self, page_num=1, page_size=20):
        show_teacher_def = {'action': 'list_teacher',
                            'pagenum': page_num,
                            'pagesize': page_size
                           }
        # params和data的区别:params是加在url中的参数
        result = requests.get(self.fullUrl, params=show_teacher_def, cookies={'sessionid': self.session_id})
        return result.json()

    # 修改老师
    def modify_teacher(self, teacher_id, user_name, real_name, desc='', password='123', display_idx=1, courses=[]):
        teacher_info = {"username": user_name,
                        "courses": courses,
                        "realname": real_name,
                        "desc": desc,
                        'display_idx': display_idx,
                        "password": password
                        }
        teacher_data = json.dumps(teacher_info)
        modify_teacher_def = {'action': 'modify_teacher',
                              'id': teacher_id,
                              'newdata': teacher_data
                           }
        result = requests.put(self.fullUrl, data=modify_teacher_def, cookies={'sessionid': self.session_id})
        teacher_info_list = {'username': user_name,
                             'realname': real_name,
                             'display_idx': display_idx,
                             'courses': courses,
                             'id': teacher_id,
                             'desc': desc
                             }
        return result.json(), teacher_info_list

    # 删除老师
    def delete_teacher(self, teacher_id):
        delete_teacher_def = {'action': 'delete_teacher',
                              'id': teacher_id
                              }
        result = requests.delete(self.fullUrl, data=delete_teacher_def, cookies={'sessionid': self.session_id})
        return result.json()

    # 清除所有老师
    def clear_teachers(self):
        teachers = self.show_teacher()
        if teachers['total'] != 0:
            remain_teachers_id = [teacher['id'] for teacher in teachers['retlist']]
            for delete_id in remain_teachers_id:
                self.delete_teacher(delete_id)
            self.clear_teachers()
        else:
            print('老师已清空')



