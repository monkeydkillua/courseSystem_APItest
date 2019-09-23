*** Settings ***
Variables  python_libs/settings.py
Library  python_libs/TestSignIn.py      ${sign_fullUrl}
Library  python_libs/TestCourse.py      ${fullUrl}      ${session_default}
Library  python_libs/TestTeacher.py     ${fullUrl}      ${session_default}
Library    Collections

*** Test Cases ***
test 01
    [Setup]     rf sign in
    @{add_return_message}     add_teacher     ${teacher_name}    ${teacher_log_name}
    log to console  ${add_return_message}
    # log to console      ${add_return_message}[0][retcode]
    ${add_return_id}    set_variable      ${add_return_message}[0][id]
    ${success_code}     set variable    0
    ${success_code}     evaluate    int(${success_code})
    should be equal     ${add_return_message}[0][retcode]   ${success_code}
    ${show_return_message}      show_teacher
    # log to console      ${show_return_message}
    ${show_return_retlist}  set variable    ${show_return_message}[retlist][0]
	log to console      ${show_return_retlist}
    should be equal     ${show_return_retlist}      ${add_return_message}[1]
    
    ${show_return_id}   set variable    ${show_return_message}[retlist][0][id]
    # log to console      ${show_return_id}
    should be equal     ${show_return_id}       ${add_return_id}
    [Teardown]      clear_teachers

*** Keywords ***
rf sign in
    @{session_id}   sign_in       ${sign_in_username}      ${sign_in_password}
    modify_session_id_course       ${session_id}[1]
    modify_session_id_teacher       ${session_id}[1]
