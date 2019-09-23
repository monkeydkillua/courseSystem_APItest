import requests
import json


class TestCourse(object):
    def __init__(self, url, session_id):
        # 可以用 f , f'http://{API_SERVER}/api/mgr/sq_mgr'
        self.fullUrl = url
        self.session_id = session_id

    def modify_session_id_course(self, new_session_id):
        self.session_id = new_session_id
        
    # 添加课程
    def add_course(self, name, desc='', idx='1'):
        add_course_def = {'action': 'add_course',
                          'data': '''{"name":"%s",
                                 "desc":"%s",
                                 "display_idx":"%s"
                                }''' % (name, desc, idx)
                       }
        result = requests.post(self.fullUrl, data=add_course_def, cookies={'sessionid': self.session_id})
        add_course_list = {'desc': desc,
                           'id': result.json()['id'],
                           'display_idx': int(idx),
                           'name': name
                           }
        return result.json(), add_course_list

    # 修改课程
    def modify_course(self, course_id, name, desc='', idx='1'):
        modify_data = {"name": name,
                       "desc": desc,
                       "display_idx": idx
                       }
        modify_data_json = json.dumps(modify_data)
        modify_course_def = {'action': 'modify_course',
                             'id': course_id,
                             'newdata': modify_data_json
                             }
        result = requests.put(self.fullUrl, data=modify_course_def, cookies={'sessionid': self.session_id})
        modify_course_list = {'desc': desc,
                              'id': course_id,
                              'display_idx': int(idx),
                              'name': name
                              }

        return result.json(), modify_course_list

    # 列出课程
    def show_course(self, page_num=1, page_size=20):
        show_course_def = {'action': 'list_course',
                           'pagenum': page_num,
                           'pagesize': page_size
                         }
        result = requests.get(self.fullUrl, params=show_course_def, cookies={'sessionid': self.session_id})  # params和data的区别:params是加在url中的参数
        return result.json()

    # 删除课程
    def delete_course(self, course_id):
        delete_course_def = {'action': 'delete_course',
                             'id': course_id
                           }
        result = requests.delete(self.fullUrl, data=delete_course_def, cookies={'sessionid': self.session_id})
        return result.json()

    # 清除所有课程
    def clear_courses(self):
        courses = self.show_course()
        if courses['total'] != 0:
            remain_courses_id = [course['id'] for course in courses['retlist']]
            for delete_id in remain_courses_id:
                self.delete_course(delete_id)
            self.clear_courses()
        else:
            print('课程已清空')

    # 添加课程并检查返回值
    def add_course_check(self):
        response_data = self.add_course()
        if response_data['retcode'] == 0:
            print('创建成功')
        elif response_data['retcode'] == 2:
            print('创建失败,已存在同名课程')

