from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class IDE(LoginRequiredMixin, View):
	login_url = '/admin/login/'
	redirect_field_name = 'next'
	html_template_file = 'mini/IDE.html'
	context = {'page_name': 'IDE'}
	def get(self, request, file = 'default.html'):
		try:
			base_template_path = Dashboard.template_path
			self.context['formdata'] = {'app_name': 'mini', 'file_name': file}
		except:
			base_template_path = os.path.join(BASE_DIR, 'mini\\templates\\mini')
		file_abs_path = os.path.join(base_template_path, file)
		with open(file_abs_path, 'r') as f:
			self.context['IDE_DEFAULT_content'] = self.remove_new_lines(f.read())
			f.close()
		return render(request, self.html_template_file, context = self.context)

	def post(self, request):
		app_name = request.POST['app_name']
		file_name = request.POST['file_name']
		content = request.POST['html_code']
		self.context['formdata'] = {'app_name': app_name, 'file_name': file_name}
		file_path = os.path.join(BASE_DIR, os.path.join(app_name + '\\templates\\' + app_name, file_name + '.html'))
		try:
			with open(file_path, 'w') as fp:
				fp.write(content)
				fp.close()
				message = 'File saved : ' + file_path
		except:
			message = 'Something went wrong! Check all file names are correct.'
		self.context['IDE_DEFAULT_content'] = self.escape_chars(content, ["'"])
		self.context['message'] = message
		return render(request, self.html_template_file, context=self.context)

	def escape_chars(self, code, charlist):
		temp, esc = '', '\\'
		for _ in code:
			temp += esc + _ if _ in charlist else _
		return temp

	def add_newline(self, code):
		temp, nl = '', '\n'
		for _ in code:
			temp += nl + _ if _ == '<' else _
		return temp

	def remove_new_lines(self, code):
		temp, nl = '', '<br>'
		for _ in code:
			temp += nl if _ == '\n' else _
		return temp

class Dashboard(LoginRequiredMixin, View):
	login_url = '/admin/login/'
	redirect_field_name = 'next'
	html_template_file = 'mini/dashboard.html'
	context = {'page_name': 'Dashboard'}
	
	def get(self, request):
		return render(request, self.html_template_file, context = self.context)

	def post(self, request):
		app_name = request.POST['app_name']
		self.template_path = os.path.join(BASE_DIR, app_name+'\\templates\\'+app_name)
		try:
			self.context['files'], error =  self.getListOfFiles(app_name+'\\templates\\'+app_name)
			a=[]
			for _ in self.context['files'][0]['files']:
				if _ not in ['default.html' ,'dashboard.html', 'IDE.html', 'layout.html', 'header.html', 'footer.html']:
					a.append(_)
			self.context['files'][0]['files'] = a
		except:
			error = 'Invalid app : Cannot find ' + app_name 
		self.context['error'] = error
		error=''
		return render(request, self.html_template_file, context = self.context) 

	def getListOfFiles(self, Name): 
		file_data = []
		for root, dirs, files in os.walk(os.path.join(BASE_DIR, Name), topdown = False):
			root = '\\'.join(root.split('\\')[len(BASE_DIR.split('\\')):])
			file_data.append({'root': root,'dirs': dirs, 'files': files})
		error = Name + ' is empty.' if len(file_data) <= 0 else 'No error'
		return file_data, error

def logout_view(request):
    logout(request)
    return redirect('mini_IDE')
