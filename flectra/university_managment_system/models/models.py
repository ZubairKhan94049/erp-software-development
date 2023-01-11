import itertools
from flectra import models, api


class OpStudentReport(models.AbstractModel):
    _name = "report.university_managment_system.transcript_cms_template"
    
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        students = self.env['um.student'].browse(docids)
        personal_info = {}
        for student in students:
            lst = []
            temp_list=[]
            final_list=[]
            course_list = []
            personal_info['reg'] = student.reg_no
            personal_info['name'] = student.name
            personal_info['prog'] = student.program_id.name
            personal_info['plan'] = student.plan_id.name
            personal_info['f_name'] = student.father_name
            course_list.append(personal_info)
            
            total_cch = 0
            total_cgp = 0
            for semester in student.semester_ids:
                gpa_list = []
                course_list_list=[]
                for sub in semester.course_ids:
                    course_list_list.append({
                        'code':sub.code,
                        'name':sub.name.name,
                        'credit_hour':sub.credit_hour,
                        'grades':sub.grades,
                        'repeated': '' if sub.repeated == False else '(RPT)*'
                    })   
                gpa_list.append({
                    'semester_name':semester.name.name,
                    'sch':semester.sch,
                    'sgp':semester.sgp,
                    'sgpa':0 if semester.sch == 0 else semester.sgp/semester.sch,
                    'cch':semester.sch + total_cch,
                    'cgp':semester.sgp + total_cgp,
                    'cgpa':0 if semester.sch == 0 else (semester.sgp + total_cgp)/(semester.sch + total_cch)
                })
                course_list.append(course_list_list+gpa_list)
                total_cch+=semester.sch
                total_cgp+=semester.sgp
            for l in course_list[1:len(course_list)]:
                temp_list.append(l)
                if len(temp_list) == 2:
                    final_list.append(temp_list)
                    temp_list = []
                elif(len(temp_list) < 2 and course_list[-1]==l):
                    final_list.append(temp_list)
            lst.append(course_list[0])
            lst.append(final_list)
            docs.append(lst)
        # print('\n\n\n\n\n', lst)
        return {
            'docs': docs,
        } 