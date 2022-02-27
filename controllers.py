from abc import ABC
from data.access_level import AdminAccess, EmployeeAccess
from views.forms.account_view import AccountView
from views.forms.login_view import LoginView
from models import *
from PySide6.QtWidgets import QWidget


class Controller(ABC):
    view: QWidget
    model: Model

    def __init__(self, view: QWidget, model: Model):
        self.view = view
        self.model = model

    def open_page(self):
        self.view.show()


class LoginPage(Controller):
    view: LoginView
    model: LoginModel

    def __init__(self, view: QWidget, model: Model):
        super().__init__(view, model)
        self.view.set_login_button_listener(self.verify_login)

    def verify_login(self):
        username = self.view.get_username()
        password = self.view.get_password()
        self.model.get_input(username, password)
        self.model.retrive_user(username)
        self.model.verify_login()

        if self.model.is_valid():
            self.view.hide_error_label()
            user_access = self.model.get_current_user().get_access_level()
            if isinstance(user_access, AdminAccess):
                print("Open Admin Page")
            else:
                print("Open Employee Page")
        else:
            self.view.show_error_label()


class HomePage(Controller):
    def __init__(self, view: QWidget, model: Model):
        super().__init__(view, model)


class AccountPage(Controller):
    view: AccountView
    model: AccountModel

    def __init__(self, view: QWidget, model: Model):
        super().__init__(view, model)
        self.fill_user_cards()

        self.view.set_create_account_button_listener(self.create_account)

        self.view.set_first_name_text_changed_listener(
            self.update_create_username_field)

        self.view.set_last_name_text_changed_listener(
            self.update_create_username_field)

        self.view.set_card_selected_listener(self.fill_user_info)

        self.view.set_save_changes_button_listener(self.update_user_info)

        self.view.set_delete_button_listener(self.delete_account)

    def fill_user_cards(self):
        """Retreives a list of user and display as cards"""
        employees = self.model.get_employee_accounts()
        for user in employees:
            self.view.add_employee_card(user)

    def create_account(self):
        """Creates a new account based on the user input"""
        first_name = self.view.get_first_name_input()
        last_name = self.view.get_last_name_input()
        username = self.model.generate_username(first_name, last_name)
        password = self.view.get_password_input()
        pass_confirm = self.view.get_password_confirm_input()
        access = AdminAccess() if self.view.get_create_admin_status() else EmployeeAccess()

        new_user = User(
            None,
            first_name,
            last_name,
            username,
            password,
            access
        )

        if self.model.verify_create_password(password, pass_confirm):
            self.model.create_new_account(new_user)
            self.view.reset_create_account_inputs()
            self.view.clear_employee_list()
            self.fill_user_cards()
        else:
            print("Invalid password confirmation")

    def update_create_username_field(self):
        """Automatically updates the username label in the create account section"""
        first_name = self.view.get_first_name_input()
        last_name = self.view.get_last_name_input()
        username = self.model.generate_username(first_name, last_name)

        if username != ".":
            self.view.set_username_label(username)
        else:
            self.view.set_username_label("")

    def fill_user_info(self):
        """Fills the edit user section with information based on the selected card"""
        current_user: User = self.view.get_selected_account()
        self.view.set_first_name_edit(current_user.get_first_name())
        self.view.set_last_name_edit(current_user.get_last_name())
        self.view.set_username_edit(current_user.get_username())

    def update_user_info(self):
        """Updates user data if changes occur"""
        current_user = self.view.get_selected_account()
        first_name = self.view.get_first_name_input()
        last_name = self.view.get_last_name_input()
        username = self.model.generate_username(first_name, last_name)
        password = self.view.get_change_password()

        new_info = User(
            current_user.get_id(),
            first_name,
            last_name,
            username,
            password,
            current_user.get_access_level()
        )

        admin_confirmation = self.view.get_admin_password()
        if self.model.admin_confirmation(admin_confirmation):
            self.model.update_user_info(new_info)
        else:
            print("Invalid admin password")

    def delete_account(self):
        """Deletes the selected account"""
        current_user: User = self.view.get_selected_account()
        admin_confirmation = self.view.get_admin_password()
        if self.model.admin_confirmation(admin_confirmation):
            self.model.delete_user_account(current_user)
        else:
            print("Invalid admin password")
