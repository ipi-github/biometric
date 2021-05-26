from odoo import models, fields, api
import csv, datetime

class HRATTENDANCE(models.Model):
	_inherit = "hr.attendance"

	def cron_get_attendance_data(self):
		self._cron_get_attendance_data()

	def _cron_get_attendance_data(self):
		import os
#		os.chmod("/opt/odoo/addons_custom/testing/attendance_integration/a.py", 0o777)
		file_path = "/opt/odoo/addons_custom/testing/attendance_integration/a.py"
		home_dir = os.system("cd /opt/odoo/addons_custom/testing/attendance_integration && python2.7 a.py")  # %s"%file_path)

#		os.chmod("/opt/odoo/addons_custom/testing/attendance_integration/csv_files/new_file.csv", 0o777)
		csv_file="/opt/odoo/addons_custom/testing/attendance_integration/csv_files/new_file.csv"
		patient_file = open(csv_file, 'r')
		patient_datas = csv.reader(patient_file, delimiter=';')
		cur = self.env.cr
		for row in patient_datas:
			emp_id = row[0]
			login_year = row[2]
			login_month = row[3]
			login_day = row[4]
			login_hour = row[5]
			login_min = row[6]
			login_sec = row[7]

			command = "select id from hr_employee"
			command_attendance = "select employee_id from hr_attendance"
			cur.execute(command)
			employee_id_erp = cur.dictfetchall()
			# print "before calling function  "+str(emp_id)
			# emp_id=return_id_of_existing_employee(emp_id)
			# print employee_id_erp[0]
			# print "emp_id after function calling::::"+emp_id
			cur.execute(command_attendance)
			attendance_record_emp = cur.dictfetchall()
			for i in employee_id_erp:
				# print " i:"+i[0]
				# print "emp_id :"+int(emp_id)
				if i['id'] == int(emp_id):
					# emp_id=47
					print("----------****************-------------employee_exist in the ERP-------------*******************--------------")

					command_find_max_timestamp = """select check_in,check_out from hr_attendance where id=(select max(id) from hr_attendance where employee_id=%s) """
					cur.execute(command_find_max_timestamp % (str(emp_id)))
					max_time_stamp_string = cur.dictfetchall()
					# print max_time_stamp_string
					# checkin_erp=max_time_stamp_string[0][0]
					# checkout_erp=max_time_stamp_string[0][1]

					# print "__________checkin__________"
					# print checkin_erp
					# print "________checkout___________"
					# print checkout_erp
					# print "________________________"
					check_out_time_bio = datetime.datetime(int(login_year), int(login_month), int(login_day),
														   int(login_hour),
														   int(login_min), int(login_sec))
					# print "actual time::::"
					time_string_actual = check_out_time_bio - (
								datetime.timedelta(hours=1) + datetime.timedelta(minutes=00))
					# print "time_string::::" + str(time_string_actual)
					if max_time_stamp_string:
						checkin_erp = max_time_stamp_string[0]['check_in']
						checkout_erp = max_time_stamp_string[0]['check_out']
						if checkin_erp and checkout_erp is None:
							max_time_stamp_check_in = datetime.datetime(int(checkin_erp.year), int(checkin_erp.month),
																		int(checkin_erp.day), int(checkin_erp.hour),
																		int(checkin_erp.minute),
																		int(checkin_erp.second))
							cur.execute("select max(id) from hr_attendance where employee_id=%s" % (emp_id))
							id = cur.dictfetchall()
							cur.execute("select check_in from hr_attendance where id=%s" % id[0]['max'])
							worked_action_check_in = cur.dictfetchall()
							# print "check_in_time"
							worked_action_checkIn = checkin_erp
							# print worked_action_checkIn
							max_time_stamp_check_out = 0
							diff_test = time_string_actual - max_time_stamp_check_in
							status = 'sign_out'
						elif checkin_erp and checkout_erp:
							max_time_stamp_check_out = datetime.datetime(int(checkout_erp.year),
																		 int(checkout_erp.month), int(checkout_erp.day),
																		 int(checkout_erp.hour),
																		 int(checkout_erp.minute),
																		 int(checkout_erp.second))
							cur.execute("select max(id) from hr_attendance where employee_id=%s" % (emp_id))
							id = cur.dictfetchall()
							cur.execute("select check_out from hr_attendance where id=%s" % id[0]['max'])

							worked_action_check_out = cur.dictfetchall()
							# print "check_out_time"
							worked_action_checkOut = checkout_erp
							# print worked_action_checkOut
							diff_test = time_string_actual - max_time_stamp_check_out
							status = 'sign_in'

						# print max_time_stamp

						# diff_minutes=0.0
						max_stamp_id_erp = id[0]['max']
						diff_minutes = (diff_test.days * 24 * 60) + (diff_test.seconds / 60)
						# print
						# diff_minutes
						in_hour = (diff_minutes / 60)
						# print
						# "-----working_hours------:" + str(in_hour)
						# print worked_action[0][0]
						if diff_minutes > 0:
							if status == 'sign_out':
								print("---------sign_out---------")
								print("                         ")
								print("sign_out Query executed")
								print(time_string_actual.second)
								# print
								cur.execute(
									"""update hr_attendance set check_out='%d-%d-%d %d:%d:%d',worked_hours=%s where employee_id=%s and id=%s""" % (
									int(time_string_actual.year), int(time_string_actual.month),
									int(time_string_actual.day),
									int(time_string_actual.hour), int(time_string_actual.minute),
									int(time_string_actual.second), in_hour, emp_id, max_stamp_id_erp))
								# conn.commit()
							elif status == 'sign_in':
								print("__________sign_in_________________________")
								cur.execute(
									"""insert into hr_attendance(check_in,employee_id) values('%d-%d-%d %d:%d:%d',%s)""" % (
										int(time_string_actual.year), int(time_string_actual.month),
										int(time_string_actual.day),
										int(time_string_actual.hour), int(time_string_actual.minute),
										int(time_string_actual.second), emp_id))
								print("sign_in query executed")
								# conn.commit()


						else:
							print("attendance already exist.....")

						# print "time_diff_in_minutes:::::" + str(diff_minutes)

						# print "<<<<<<<<<<<<<-------------------------attendance already exist--------------------------------->>>>>>>>>>>>>>>>>>>>"
					else:
						print("first sign in of the employee in the biometric " + emp_id)
						cur.execute(
							"""insert into hr_attendance(check_in,employee_id) values('%d-%d-%d %d:%d:%d',%s)""" % (
							int(time_string_actual.year), int(time_string_actual.month), int(time_string_actual.day),
							int(time_string_actual.hour), int(time_string_actual.minute),
							int(time_string_actual.second), emp_id))
						# conn.commit()
				else:
					pass
				# print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
