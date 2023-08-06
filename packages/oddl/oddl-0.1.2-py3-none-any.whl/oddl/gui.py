import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as scrolledtext
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
import math
import datetime
import json
import threading
from .opendaprequest import OpeNDAPRequest, AuthType, AuthTypes, ReturnCode


class TempDisabler():
    def __init__(self, parent):
        '''Constructor accepts a parent TKinter window.'''
        self._parent = parent
        self._controls = {}

    def disable(self, ignore = []):
        '''
        Disables all controls in parent that are currently enabled.
        `ignore` argument is a list of string control names to ignore.
        '''
        self._controls.clear()
        self._do_disable(self._parent, ignore)

    def enable(self):
        '''Re-enables controls that were disabled by the class disable method.'''
        # Iterate stored dict of controls,
        # restoring state based on stored state
        for ctrl in self._controls:
            ctrl.configure(state=self._controls[ctrl])

    def _do_disable(self, parent, ignore = []):
        # Iterate all children in parent.
        for child in parent.winfo_children():
            # If control is a container, recurse.
            if child.winfo_class() in ('Menu', 'Frame', 'TLabelframe'):
                self._do_disable(child, ignore)
            # Have to check Menu again for some reason
            if child.winfo_class() == 'Menu':
                continue
            # Skip controls we want to ignore.
            if str(child) in ignore:
                continue
            # Test for controls that are not disabled already.
            # Must wrap in try block in case control does not
            # support the `state` config.
            try:
                if str(child['state']) not in ('disabled'):
                    # Add control and state to dict of
                    # controls and then disable the control.
                    self._controls[child] = child['state']
                    child.configure(state='disable')
            except:
                pass


class TempMenuDisabler():
    def __init__(self, menubar):
        '''Constructor accepts a TKinter Menu.'''
        self._menubar = menubar

    def disable(self):
        '''Disables all menus.'''
        num = len(self._menubar.winfo_children())
        for i in range(1, num+1):
            self._menubar.entryconfig(i, state="disabled")

    def enable(self):
        '''Re-enables all menus.'''
        # Iterate stored dict of controls,
        # restoring state based on stored state
        num = len(self._menubar.winfo_children())
        for i in range(1, num+1):
            self._menubar.entryconfig(i, state="normal")


class GUI(tk.Tk):
    def __init__(self, odr):
        super().__init__()

        # Private members
        self._odr = odr
        self._running_thread = False

        # Window building
        self.title('OpeNDAP Downloader')
        self.bind('<Alt-F4>', self.on_exit)
        self.bind('<Control-o>', self.on_open_settings)
        self.bind('<Control-s>', self.on_save_settings)
        self.create_menu()
        self.create_controls()
        self.resizable(False, False)

        # Need to handle window close/destroy event
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        # More private members
        self._disabler = TempDisabler(self)
        self._menu_disabler = TempMenuDisabler(self.menubar)


    # GUI building methods

    def create_menu(self):
        self.menubar = tk.Menu(self)
        file = tk.Menu(self.menubar, tearoff=0)
        file.add_command(label='Open Settings', accelerator ='Ctrl+O', command=self.on_open_settings)
        file.add_command(label='Save Settings', accelerator ='Ctrl+S', command=self.on_save_settings)
        file.add_separator()
        file.add_command(label='Exit', command=self.on_exit)
        self.menubar.add_cascade(label='File', menu=file)
        self.config(menu=self.menubar)

    def create_controls(self):
        # ===

        lf_request = ttk.LabelFrame(self, text='Request')
        lf_request.grid(column=0, row=0, padx= 16, pady=8)

        lbl_base_url = ttk.Label(lf_request, text='Base URL')
        lbl_base_url.grid(column=0, row=0, pady=8)

        self.ctrl_base_url = ttk.Entry(lf_request)
        self.ctrl_base_url.grid(column=1, row=0, columnspan=7, sticky='NSEW', padx=8, pady=8)
        self.ctrl_base_url.bind('<KeyRelease>', self.on_base_url_change)
        self.ctrl_base_url.bind('<<Paste>>', self.on_base_url_change)
        self.ctrl_base_url.bind('<<Cut>>', self.on_base_url_change)

        # ---------

        lbl_auth_types = ttk.Label(lf_request, text='Auth Type')
        lbl_auth_types.grid(column=0, row=1, padx=8, pady=8)

        self.ctrl_auth_types = ttk.Combobox(lf_request)
        self.ctrl_auth_types.grid(column=1, row=1, pady=8)
        self.ctrl_auth_types['values'] = AuthTypes
        self.ctrl_auth_types.set(AuthTypes[0])
        self.ctrl_auth_types['state'] = 'readonly'

        lbl_auth_url = ttk.Label(lf_request, text='OpenID/Auth URL')
        lbl_auth_url.grid(column=2, row=1, pady=8)

        self.ctrl_auth_url = ttk.Entry(lf_request)
        self.ctrl_auth_url.grid(column=3, row=1, pady=8)

        lbl_userid = ttk.Label(lf_request, text='User ID')
        lbl_userid.grid(column=4, row=1, pady=8)

        self.ctrl_userid = ttk.Entry(lf_request)
        self.ctrl_userid.grid(column=5, row=1, pady=8)

        lbl_pw = ttk.Label(lf_request, text='Password')
        lbl_pw.grid(column=6, row=1, pady=8)

        self.ctrl_password = ttk.Entry(lf_request)
        self.ctrl_password.grid(column=7, row=1, padx=8, pady=8)

        # ---------

        self.btn_req = ttk.Button(lf_request, text='Make Request')
        self.btn_req.grid(column=1, row=3, columnspan=8, pady=8)
        self.btn_req['command'] = self.on_request
        self.btn_req['state'] = tk.DISABLED

        # ===

        lf_constraints = ttk.LabelFrame(self, text='Variables and Dimensional Constraints')
        lf_constraints.grid(column=0, row=1, padx=16, pady=8)

        lbl_variables = ttk.Label(lf_constraints, text='Variables')
        lbl_variables.grid(column=0, row=0, padx=8, pady=8)

        row = 0
        self.ctrl_variables = ttk.Combobox(lf_constraints)
        self.ctrl_variables.grid(column=1, row=row, pady=8)
        self.ctrl_variables['values'] = []
        self.ctrl_variables.set('')
        self.ctrl_variables['state'] = tk.DISABLED
        self.ctrl_variables.bind('<<ComboboxSelected>>', self.on_variables_change)

        # ---------

        row += 1
        lbl_dims = ttk.Label(lf_constraints, text='Dimensions')
        lbl_dims.grid(column=0, row=row, padx=8, pady=8)

        # ---------

        row += 1
        lbl_dims_header1 = ttk.Label(lf_constraints, text='Name')
        lbl_dims_header1.grid(column=0, row=row, padx=8, pady=8)

        lbl_dims_header2 = ttk.Label(lf_constraints, text='From')
        lbl_dims_header2.grid(column=1, row=row, padx=8, pady=8)

        lbl_dims_header3 = ttk.Label(lf_constraints, text='To')
        lbl_dims_header3.grid(column=2, row=row, padx=8, pady=8)

        # ---------

        self.dims_controls = []
        for dim in ['<none>', '<none>', '<none>', '<none>']:
            row += 1
            lbl_dim = ttk.Label(lf_constraints, text=dim)
            lbl_dim.grid(column=0, row=row, padx=8, pady=4)
            ctrl_dim_from = ttk.Combobox(lf_constraints)
            ctrl_dim_from.grid(column=1, row=row)
            ctrl_dim_from['values'] = []
            ctrl_dim_from['state'] = tk.DISABLED
            ctrl_dim_to = ttk.Combobox(lf_constraints)
            ctrl_dim_to.grid(column=2, row=row)
            ctrl_dim_to['values'] = []
            ctrl_dim_to['state'] = tk.DISABLED
            self.dims_controls.append({'enabled': False, 'label': lbl_dim, 'control_from': ctrl_dim_from, 'control_to': ctrl_dim_to})

        # ---------

        row += 1
        self.btn_check_shape = ttk.Button(lf_constraints, text='Check Shape')
        self.btn_check_shape.grid(column=0, row=row, padx=8, pady=8)
        self.btn_check_shape['state'] = tk.DISABLED
        self.btn_check_shape['command'] = self.on_check_shape

        self.btn_full_url = ttk.Button(lf_constraints, text='Dump Full URL')
        self.btn_full_url.grid(column=1, row=row, padx=8, pady=8)
        self.btn_full_url['state'] = tk.DISABLED
        self.btn_full_url['command'] = self.on_full_url

        self.btn_save = ttk.Button(lf_constraints, text='Save Variable')
        self.btn_save.grid(column=2, row=row, padx=8, pady=8)
        self.btn_save['state'] = tk.DISABLED
        self.btn_save['command'] = self.on_save_variable

        # ===

        lf_msg_log = ttk.LabelFrame(self, text='Message Log')
        lf_msg_log.grid(column=0, row=3, padx=16, pady=16)

        self.txt_msg_log = scrolledtext.ScrolledText(lf_msg_log)
        self.txt_msg_log.grid(column=0, row=0, padx=16, pady=8)
        self.txt_msg_log['width'] = 90
        self.txt_msg_log['height'] = 8

        # ===

        self.progress_bar = ttk.Progressbar(self, orient='horizontal', mode='determinate')
        self.progress_bar.grid(column=0, row=4, sticky='NSEW', padx=50, pady=8)


    # Class property getters/setters

    @property
    def odr(self):
        return self._odr

    @property
    def base_url(self):
        return self.ctrl_base_url.get()

    @base_url.setter
    def base_url(self, val):
        self.ctrl_base_url.delete(0, tk.END)
        self.ctrl_base_url.insert(0, val)

    @property
    def auth_types(self):
        return self.ctrl_auth_types['values']

    @auth_types.setter
    def auth_types(self, val):
        self.ctrl_auth_types['values'] = val

    @property
    def auth_type(self):
        return self.ctrl_auth_types.current()

    @auth_type.setter
    def auth_type(self, val):
        self.ctrl_auth_types.current(val)

    @property
    def auth_url(self):
        return self.ctrl_auth_url.get()

    @auth_url.setter
    def auth_url(self, val):
        self.ctrl_auth_url.delete(0, tk.END)
        self.ctrl_auth_url.insert(0, val)

    @property
    def userid(self):
        return self.ctrl_userid.get()

    @userid.setter
    def userid(self, val):
        self.ctrl_userid.delete(0, tk.END)
        self.ctrl_userid.insert(0, val)

    @property
    def password(self):
        return self.ctrl_password.get()

    @password.setter
    def password(self, val):
        self.ctrl_password.delete(0, tk.END)
        self.ctrl_password.insert(0, val)

    @property
    def variables(self):
        return list(self.ctrl_variables['values'])

    @variables.setter
    def variables(self, val):
        if val is None or not len(val):
            self.ctrl_variables['values'] = []
            self.ctrl_variables.set('')
            self.ctrl_variables['state'] = tk.DISABLED
            return
        self.ctrl_variables['values'] = val
        self.ctrl_variables.set(val[0])
        self.ctrl_variables['state'] = 'readonly'

    @property
    def variable(self):
        return self.ctrl_variables.get()

    @variable.setter
    def variable(self, val):
       if val in self.ctrl_variables['values']:
            self.ctrl_variables.set(val)

    @property
    def dimensions(self):
        dims = {}
        for dim in self.dims_controls:
            if not dim['enabled']:
                continue
            dims[dim['label'].cget('text')] = list(dim['control_from']['values'])
        return dims

    @dimensions.setter
    def dimensions(self, val):
        for dim in self.dims_controls:
            dim['enabled'] = False
            dim['label'].configure(text='<none>')
            dim['control_from']['values'] = []
            dim['control_from']['state'] = tk.DISABLED
            dim['control_from'].set('')
            dim['control_to']['values'] = []
            dim['control_to']['state'] = tk.DISABLED
            dim['control_to'].set('')
            self.btn_check_shape['state'] = tk.DISABLED
            self.btn_full_url['state'] = tk.DISABLED
            self.btn_save['state'] = tk.DISABLED
        if val:
            i = 0
            for dim_name in val.keys():
                self.dims_controls[i]['enabled'] = True
                self.dims_controls[i]['label'].configure(text=dim_name)
                self.dims_controls[i]['control_from']['values'] = val[dim_name]
                self.dims_controls[i]['control_from']['state'] = 'readonly'
                self.dims_controls[i]['control_from'].set(val[dim_name][0])
                self.dims_controls[i]['control_to']['values'] = val[dim_name]
                self.dims_controls[i]['control_to']['state'] = 'readonly'
                self.dims_controls[i]['control_to'].set(val[dim_name][0])
                i += 1
            if i > 0:
                self.btn_check_shape['state'] = tk.NORMAL
                self.btn_full_url['state'] = tk.NORMAL
                self.btn_save['state'] = tk.NORMAL

    @property
    def constraints_indices(self):
        constraints = {}
        for dim in self.dims_controls:
            if not dim['enabled']:
                continue
            constraints[dim['label'].cget('text')] = [dim['control_from'].current(), dim['control_to'].current()]
        return constraints

    @property
    def constraints_values(self):
        constraints = {}
        for dim in self.dims_controls:
            if not dim['enabled']:
                continue
            constraints[dim['label'].cget('text')] = [dim['control_from'].get(), dim['control_to'].get()]
        return constraints

    @property
    def running_thread(self):
        return self._running_thread

    @running_thread.setter
    def running_thread(self, val):
        self._running_thread = val
        if val:
            self.progress_bar['value'] = '0'
            self.progress_bar.start(interval=20)
        else:
            self.progress_bar.stop()
            self.progress_bar['value'] = '0'

    @property
    def tmp_disabled(self): # Setter only!
        pass

    @tmp_disabled.setter
    def tmp_disabled(self, val):
        if val:
            self._disabler.disable([str(self.progress_bar)])
            self._menu_disabler.disable()
        else:
            self._disabler.enable()
            self._menu_disabler.enable()

    # Class methods

    def message(self, msg, newline=True):
        self.txt_msg_log.insert('end', f'{msg}')
        if newline:
            self.txt_msg_log.insert('end', '\n')

    def clear_messages(self):
        self.txt_msg_log.delete('1.0', 'end')

    def run_request(self, first_call=True):
        # Method meant to be called twice:
        # Once for initializing request, and then when
        # request thread actually runs.

        # If it is first call
        if first_call:
            self.variables= None
            self.dimensions = None

            self.clear_messages()
            self.message( f'Base request: {self.base_url}')
            self.message('Requesting...', False)

            # Call this just before creating thread
            self.tmp_disabled = True

            # Create a thread that calls this function again
            # setting `first_call` argument to False.
            self.running_thread = True
            th = threading.Thread(target=lambda: self.run_request(first_call=False))
            th.daemon = True
            th.start()

        # Else second call
        else:
            result = self.odr.make_request(self.auth_type, self.base_url, self.userid, self.password, self.auth_url)

            # Call this directly after making call to ODR method
            self.tmp_disabled = False

            self.message('Done.')

            if (result['return_code'] == ReturnCode.success):
                self.message('Request successful. Metadata retrieved.')

                self.variables = self.odr.get_vars()
                self.on_variables_change()
            else:
                self.message(f'Error: {result["error"]}')
            self.running_thread = False

    def run_save_variable(self, first_call=True, file=None):
        # Method meant to be called twice:
        # Once for initializing saving, and then when
        # save thread actually runs.

        # If it is first call
        if first_call:
            file = asksaveasfilename(filetypes=[('NetCDF', '*.nc')], title='Save NetCDF File')
            if file:
                if not file.endswith('.nc'):
                    file += '.nc'

                self.message('Saving...', False)

                # Call this just before creating thread
                self.tmp_disabled = True

                # Create a thread that calls this function again
                # setting `first_call` argument to False.
                self.running_thread = True
                th = threading.Thread(target=lambda: self.run_save_variable(first_call=False, file=file))
                th.daemon = True
                th.start()

        # Else second call
        else:
            var = self.variable
            result = self.odr.save_var(self.variable, self.constraints_values, file)

            # Call this directly after making call to ODR method
            self.tmp_disabled = False

            self.message('Done.')

            if (result['return_code'] == ReturnCode.success):
                self.message(f'Variable `{var}` saved to {file}')
            else:
                self.message(f'Error: {result["error"]}')
            self.running_thread = False


    # Class event listeners

    def on_close(self, *e):
        self.destroy()
        # if not self.running_thread:
        #     self.destroy()

    def on_exit(self, *e):
        self.quit()

    def on_base_url_change(self, *e):
        if (len(self.base_url)):
            self.btn_req['state'] = tk.NORMAL
        else:
            self.btn_req['state'] = tk.DISABLED

    def on_variables_change(self, *e):
        self.dimensions = self.odr.get_dims_for_var(self.variable)
        info = self.odr.get_info_for_var(self.variable)
        if len(info):
            shape = info['shape']
            product = math.prod(shape)
            size = info['size']
            total = product * size
            shape_str = ' x '.join([str(i) for i in shape])
            size_str = '{0:,}'.format(size)
            total_str = '{0:,}'.format(total)
            self.message(f'Variable `{self.variable}` Full Shape: {shape_str} @ {size_str} bytes each = {total_str} bytes.')

    def on_request(self, *e):
        if not self.running_thread:
            self.run_request()

    def on_save_variable(self, *e, first_call=True, file=None):
        if not self.running_thread:
            self.run_save_variable()

    def on_check_shape(self, *e):
        pass
        shape = []

        indices = self.constraints_indices
        for idx in indices:
            from_idx = indices[idx][0]
            to_idx = indices[idx][1]
            size = abs(to_idx - from_idx) + 1
            shape.append(size)

        if len(shape):
            info = self.odr.get_info_for_var(self.variable)
            product = math.prod(shape)
            size = info['size']
            total = product * size
            shape_str = ' x '.join([str(i) for i in shape])
            size_str = '{0:,}'.format(size)
            total_str = '{0:,}'.format(total)
            self.message(f'Variable `{self.variable}` Constrained Shape: {shape_str} @ {size_str} bytes each = {total_str} bytes.')

    def on_full_url(self, *e):
        full_url = f'{self.base_url}?{self.variable}'
        indices = self.constraints_indices
        for idx in indices:
            param = f'[{indices[idx][0]}:{indices[idx][1]}]'
            full_url += param
        self.message(f'Full Url: {full_url}')

    def on_open_settings(self, *e):
        file = askopenfilename(filetypes=[('Settings', '*.json')], title='Open Settings File')
        if file:
            if not file.endswith('.json'):
                file += '.json'
            with open(file, 'r') as json_file:
                settings = json.load(json_file)
            self.base_url = settings['base_url']
            self.auth_type = settings['auth_type']
            self.auth_url = settings['auth_url']
            self.userid = settings['userid']
            self.password = settings['password']
            self.on_base_url_change()

    def on_save_settings(self, *e):
        file = asksaveasfilename(filetypes=[('Settings', '*.json')], title='Save Settings File')
        if file:
            if not file.endswith('.json'):
                file += '.json'
            settings = {
                'base_url': self.base_url,
                'auth_type': self.auth_type,
                'auth_url': self.auth_url,
                'userid': self.userid,
                'password': self.password
            }
            with open(file, 'w') as json_file:
                json.dump(settings, json_file)
