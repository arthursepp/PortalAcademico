from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# ----------------------------
# 1. Unidades da Universidade
# ----------------------------

class Unidade(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome


# ----------------------------
# 2. Usuário Personalizado (Pessoa)
# ----------------------------

class Pessoa(AbstractUser):
    class Papel(models.TextChoices):
        ALUNO = "aluno", _("Aluno")
        PROFESSOR = "professor", _("Professor")
        ADMIN = "admin", _("Administrador")

    class Turno(models.TextChoices):
        MANHA = "manha", _("Manhã")
        TARDE = "tarde", _("Tarde")
        NOITE = "noite", _("Noite")

    numero_matricula = models.CharField(max_length=50, unique=True)
    numero_documento = models.CharField(max_length=50, unique=True)
    turno = models.CharField(max_length=20, choices=Turno.choices, default=Turno.MANHA)
    papel = models.CharField(max_length=20, choices=Papel.choices, default=Papel.ALUNO)

    class Situacao(models.TextChoices):
        ATIVO = "ativo", _("Ativo")
        INATIVO = "inativo", _("Inativo")

    situacao = models.CharField(max_length=10, choices=Situacao.choices, default=Situacao.ATIVO)

    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="pessoas", null=True, blank=True)

    def __str__(self):
        unidade_nome = self.unidade.nome if self.unidade else "Sem Unidade"
        return f"{unidade_nome} - {self.last_name}, {self.first_name}"


# ----------------------------
# 3. Estrutura Acadêmica
# ----------------------------

class Departamento(models.Model):
    nome = models.CharField(max_length=200)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="departamentos")

    class Meta:
        unique_together = ("nome", "unidade")

    def __str__(self):
        return f"{self.nome} ({self.unidade.nome})"


class Curso(models.Model):
    nome = models.CharField(max_length=200)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="cursos")
    duracao_semestres = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("nome", "departamento")

    def __str__(self):
        return f"{self.nome} - {self.departamento.unidade.nome}"


class Disciplina(models.Model):
    nome = models.CharField(max_length=200)
    peso = models.PositiveSmallIntegerField()
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="disciplinas")

    class Meta:
        unique_together = ("nome", "departamento")

    def __str__(self):
        return f"{self.nome} ({self.departamento.unidade.nome})"


# ----------------------------
# 4. Semestres & Turmas
# ----------------------------

class Semestre(models.Model):
    nome = models.CharField(max_length=50, unique=True)  # ex.: "2025.1"
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return self.nome


class Turma(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="turmas")
    professor = models.ForeignKey(Pessoa, limit_choices_to={'papel': 'professor'},
                                  on_delete=models.SET_NULL, null=True, related_name="turmas")
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="turmas")
    capacidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.disciplina.nome} - {self.semestre.nome} ({self.disciplina.departamento.unidade.nome})"


# ----------------------------
# 5. Matrículas & Frequência
# ----------------------------

class Matricula(models.Model):
    aluno = models.ForeignKey(Pessoa, limit_choices_to={'papel': 'aluno'},
                              on_delete=models.CASCADE, related_name="matriculas")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="matriculas")
    data_matricula = models.DateField(auto_now_add=True)

    class Situacao(models.TextChoices):
        MATRICULADO = "matriculado", _("Matriculado")
        TRANCADO = "trancado", _("Trancado")
        REPROVADO = "reprovado", _("Reprovado")
        APROVADO = "aprovado", _("Aprovado")
        INCOMPLETO = "incompleto", _("Incompleto")

    situacao = models.CharField(max_length=20, choices=Situacao.choices, default=Situacao.MATRICULADO)

    class Meta:
        unique_together = ("aluno", "turma")

    def __str__(self):
        return f"{self.aluno.username} em {self.turma}"


class Frequencia(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name="frequencias")
    data = models.DateField()

    class Situacao(models.TextChoices):
        PRESENTE = "presente", _("Presente")
        AUSENTE = "ausente", _("Ausente")
        JUSTIFICADO = "ausencia_justificada", _("Ausência Justificada")

    situacao = models.CharField(max_length=20, choices=Situacao.choices)

    def __str__(self):
        return f"{self.matricula} - {self.data} ({self.situacao})"


# ----------------------------
# 6. Avaliações & Notas
# ----------------------------

class Avaliacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="avaliacoes")
    nome = models.CharField(max_length=200)
    peso = models.DecimalField(max_digits=5, decimal_places=2)  # ex.: 30.00%
    data = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.turma})"


class Nota(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name="notas")
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name="notas")
    valor = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("avaliacao", "matricula")

    def __str__(self):
        return f"{self.matricula.aluno.username} - {self.avaliacao.nome}: {self.valor}"


# ----------------------------
# 7. Resultado Final
# ----------------------------

class ResultadoFinal(models.Model):
    matricula = models.OneToOneField(Matricula, on_delete=models.CASCADE, related_name="resultado_final")
    nota_final = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_faltas = models.PositiveIntegerField(default=0)

    class Situacao(models.TextChoices):
        APROVADO = "aprovado", _("Aprovado")
        REPROVADO_NOTA = "reprovado_por_nota", _("Reprovado por Nota")
        REPROVADO_FALTA = "reprovado_por_falta", _("Reprovado por Falta")
        CURSANDO = "cursando", _("Cursando")

    situacao = models.CharField(max_length=30, choices=Situacao.choices, default=Situacao.CURSANDO)

    def __str__(self):
        return f"{self.matricula.aluno.username} - {self.situacao}"
