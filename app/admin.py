from django.contrib import admin
from .models import *
from .models import (
	Unidade, Pessoa, Departamento, Curso, Disciplina, Semestre, Turma,
	Matricula, Frequencia, Avaliacao, Nota, ResultadoFinal
)

admin.site.register(Unidade)
admin.site.register(Pessoa)
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
