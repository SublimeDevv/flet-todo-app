import flet as ft
import re
from datetime import datetime


class ImcApp(ft.UserControl):
    def build(self):
        self.name = ft.TextField(
            label="Ingresa tu nombre",
            prefix_icon=ft.icons.PEOPLE,
            keyboard_type=ft.KeyboardType.TEXT,
            border_radius=ft.border_radius.all(20),
            border_width=1,
        )
        self.birth_date = ft.TextField(
            label="Ingresa tu fecha de nacimiento",
            prefix_icon=ft.icons.DATE_RANGE,
            keyboard_type=ft.KeyboardType.DATETIME,
            border_radius=ft.border_radius.all(20),
            border_width=1,
            max_length=10,
        )
        self.weight = ft.TextField(
            label="Ingresa tu peso",
            suffix_text="kg",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.icons.NUMBERS,
            max_length=4,
            border_radius=ft.border_radius.all(20),
            border_width=1,
        )
        self.height = ft.TextField(
            label="Ingresa tu altura",
            suffix_text="m",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.icons.NUMBERS,
            max_length=4,
            border_radius=ft.border_radius.all(20),
            border_width=1,
        )

        # Boton con funcion enviar
        self.submit_button = ft.ElevatedButton(
            text="Enviar", on_click=self.calculate_results
        )

        self.table_info = ft.DataTable(
            width=1300,
            border=ft.border.all(2, "#70d2c8"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "#70d2c8"),
            horizontal_lines=ft.border.BorderSide(1),
            sort_ascending=True,
            data_row_color={"hovered": "0x30FF0000"},
            divider_thickness=0,
            column_spacing=100,
        )

        self.table_history = ft.DataTable(
            sort_column_index=0,
            width=1300,
            border=ft.border.all(2, "#6ae859"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "#6ae859"),
            horizontal_lines=ft.border.BorderSide(1),
            sort_ascending=True,
            data_row_color={"hovered": "0x30FF0000"},
            divider_thickness=0,
            column_spacing=100,
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("IMC")),
                ft.DataColumn(ft.Text("Fecha de nacimiento")),
            ],
        )

        self.title_results = ft.Text("Resultados", text_align=ft.TextAlign.CENTER)
        self.title_history = ft.Text("Historial", text_align=ft.TextAlign.CENTER)

        results = ft.Column(
            top=10,
            right=300,
            left=300,
            bottom=10,
            width=600,
            height=700,
            controls=[
                ft.Column(
                    controls=[
                        self.name,
                        self.weight,
                        self.height,
                        self.birth_date,
                        self.submit_button,
                        self.title_results,
                        self.table_info,
                        self.title_history,
                        self.table_history,
                    ]
                ),
            ],
        )

        return results

    def calculate_results(self, e):
        fields = [self.name, self.birth_date, self.height, self.weight]

        check = True
        check_birth_date = True
        check_numbers = True

        for i in fields:
            if not i.value:
                i.error_text = "Debes llenar este campo"
                check = False
                self.update()
            else:
                i.error_text = ""

        for i in fields[-2:]:
            if not self.is_number(i.value):
                i.error_text = "Debe ser un número"
                check_numbers = False
                self.update()
            else:
                i.error_text = ""

        if self.validate_format_date(fields[1].value):
            self.birth_date.error_text = ""
            check_birth_date = True
        else:
            self.birth_date.error_text = "Fecha en formato DD/MM/YYYY"
            check_birth_date = False
            self.update()

        if check and check_numbers and check_birth_date:
            w = float(self.weight.value)
            h = float(self.height.value)
            imc = self.calculate_imc(w, h)
            d = self.calculate_time_date(self.birth_date.value)
            status = self.status_imc(imc)

            self.add_user_history(self.name.value, imc, self.birth_date.value)

            self.table_info.columns = [
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("IMC")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Naciste hace...")),
            ]
            # self.table_info.rows = [ft.DataRow([ft.DataCell(ft.Text("Juan"))])]
            self.table_info.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(self.name.value)),
                        ft.DataCell(ft.Text(str(round(imc, 2)))),
                        ft.DataCell(ft.Text(str(status))),
                        ft.DataCell(ft.Text(str(d.days) + " días")),
                    ]
                )
            ]

            self.update()
        # else:
        #     self.results_label.value = ""

    # Validaciones

    def status_imc(self, imc):
        if imc < 18.5:
            return "Bajo"
        if imc > 18.5 and imc < 24.9:
            return "Normal"
        if imc > 25 and imc < 29.9:
            return "Sobrepeso"
        if imc > 30:
            return "Obeso"

    def is_number(self, num):
        regex_number = r"^\d+(\.\d+)?$"
        if bool(re.match(regex_number, num)):
            return True
        else:
            return False

    def validate_format_date(self, birth_date):
        regex_date = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if bool(re.match(regex_date, birth_date)):
            return True
        else:
            return False

    # Calculos

    def calculate_time_date(self, birth_date):
        get_birth = datetime.strptime(birth_date, "%d/%m/%Y")
        date_now = datetime.now()

        return date_now - get_birth

    def calculate_imc(self, w, h):
        return w / (h * h)

    def add_user_history(self, name, imc, birthday):
        self.table_history.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(name)),
                    ft.DataCell(ft.Text(str(imc))),
                    ft.DataCell(ft.Text(birthday)),
                ]
            )
        )


def main(page: ft.Page):
    page.title = "IMC Calculadora"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    imc = ImcApp()
    page.appbar = ft.AppBar(
        leading_width=40,
        title=ft.Text("Sublime App"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
        ],
    )

    page.theme_mode = "dark"
    page.scroll = "adaptive"
    page.add(imc)


ft.app(target=main)
