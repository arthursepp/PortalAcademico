from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Unidade, Pessoa, Departamento, Curso, Disciplina, Semestre, Turma,
    Matricula, Frequencia, Avaliacao, Nota, ResultadoFinal
)

@admin.register(Pessoa)
class PessoaAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": (
                "numero_matricula",
                "numero_documento",
                "turno",
                "papel",
                "situacao",
                "unidade",
                "foto_perfil",
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações adicionais", {
            "fields": (
                "numero_matricula",
                "numero_documento",
                "turno",
                "papel",
                "situacao",
                "unidade",
                "foto_perfil",
            ),
        }),
    )

admin.site.register(Unidade)
# admin.site.register(Pessoa)
admin.site.register(Departamento)
admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Semestre)
admin.site.register(Turma)
admin.site.register(Matricula)
admin.site.register(Frequencia)
admin.site.register(Avaliacao)
admin.site.register(Nota)
admin.site.register(ResultadoFinal)
