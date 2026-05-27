"""
Script de datos iniciales (Seed)
=================================
Ejecutar con: python -m app.seed.seed_data

Crea datos de ejemplo:
- 3 Facultades
- 6 Programas académicos
- 10 Docentes
- 15 Asignaturas
- 20 Grupos
- 30 Estudiantes
- Matrículas, notas y pagos de ejemplo
- 1 Usuario administrador
"""

import sys
import os

# Asegurar que el directorio raíz del backend esté en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import (
    Facultad, ProgramaAcademico, Estudiante, Docente, Asignatura,
    Grupo, Matricula, Nota, PagoMatricula, Usuario,
    EstadoGeneral, NivelFormacion, Modalidad,
    TipoDocumento, EstadoEstudiante, CategoriaDocente,
    EstadoGrupo, EstadoMatricula, EstadoAprobacion,
    EstadoPago, MedioPago, RolUsuario,
)


def seed_facultades(db: Session):
    facultades_data = [
        {"nombre": "Facultad de Ingeniería", "ubicacion": "Bloque A, Campus Norte", "telefono": "601-123-4001", "correo": "ingenieria@universidad.edu.co"},
        {"nombre": "Facultad de Ciencias Económicas", "ubicacion": "Bloque B, Campus Sur", "telefono": "601-123-4002", "correo": "economicas@universidad.edu.co"},
        {"nombre": "Facultad de Ciencias de la Salud", "ubicacion": "Bloque C, Campus Central", "telefono": "601-123-4003", "correo": "salud@universidad.edu.co"},
    ]
    facultades = []
    for data in facultades_data:
        f = Facultad(**data, estado=EstadoGeneral.ACTIVO)
        db.add(f)
        facultades.append(f)
    db.flush()
    print(f"  ✓ {len(facultades)} facultades creadas")
    return facultades


def seed_programas(db: Session, facultades):
    programas_data = [
        {"nombre": "Ingeniería de Sistemas", "nivel_formacion": NivelFormacion.PREGRADO, "modalidad": Modalidad.PRESENCIAL, "facultad_id": facultades[0].id},
        {"nombre": "Ingeniería Industrial", "nivel_formacion": NivelFormacion.PREGRADO, "modalidad": Modalidad.PRESENCIAL, "facultad_id": facultades[0].id},
        {"nombre": "Administración de Empresas", "nivel_formacion": NivelFormacion.PREGRADO, "modalidad": Modalidad.PRESENCIAL, "facultad_id": facultades[1].id},
        {"nombre": "Contaduría Pública", "nivel_formacion": NivelFormacion.PREGRADO, "modalidad": Modalidad.PRESENCIAL, "facultad_id": facultades[1].id},
        {"nombre": "Medicina", "nivel_formacion": NivelFormacion.PREGRADO, "modalidad": Modalidad.PRESENCIAL, "facultad_id": facultades[2].id},
        {"nombre": "Enfermería", "nivel_formacion": NivelFormacion.PREGRADO, "modalidad": Modalidad.PRESENCIAL, "facultad_id": facultades[2].id},
    ]
    programas = []
    for data in programas_data:
        p = ProgramaAcademico(**data, estado="activo")
        db.add(p)
        programas.append(p)
    db.flush()
    print(f"  ✓ {len(programas)} programas creados")
    return programas


def seed_docentes(db: Session, facultades):
    docentes_data = [
        {"nombres": "Carlos Alberto", "apellidos": "Rodríguez Pérez", "correo": "c.rodriguez@universidad.edu.co", "categoria": CategoriaDocente.TITULAR, "facultad_id": facultades[0].id},
        {"nombres": "María Elena", "apellidos": "García López", "correo": "m.garcia@universidad.edu.co", "categoria": CategoriaDocente.ASOCIADO, "facultad_id": facultades[0].id},
        {"nombres": "Andrés Felipe", "apellidos": "Martínez Cruz", "correo": "a.martinez@universidad.edu.co", "categoria": CategoriaDocente.AUXILIAR, "facultad_id": facultades[0].id},
        {"nombres": "Laura Patricia", "apellidos": "Sánchez Ruiz", "correo": "l.sanchez@universidad.edu.co", "categoria": CategoriaDocente.CATEDRATICO, "facultad_id": facultades[0].id},
        {"nombres": "Roberto", "apellidos": "Jiménez Vargas", "correo": "r.jimenez@universidad.edu.co", "categoria": CategoriaDocente.TITULAR, "facultad_id": facultades[1].id},
        {"nombres": "Ana Sofía", "apellidos": "Torres Medina", "correo": "a.torres@universidad.edu.co", "categoria": CategoriaDocente.ASOCIADO, "facultad_id": facultades[1].id},
        {"nombres": "Jorge Luis", "apellidos": "Herrera Castro", "correo": "j.herrera@universidad.edu.co", "categoria": CategoriaDocente.AUXILIAR, "facultad_id": facultades[1].id},
        {"nombres": "Diana Carolina", "apellidos": "Moreno Suárez", "correo": "d.moreno@universidad.edu.co", "categoria": CategoriaDocente.TITULAR, "facultad_id": facultades[2].id},
        {"nombres": "Miguel Ángel", "apellidos": "Reyes Florián", "correo": "m.reyes@universidad.edu.co", "categoria": CategoriaDocente.ASOCIADO, "facultad_id": facultades[2].id},
        {"nombres": "Claudia Marcela", "apellidos": "Ospina Ríos", "correo": "c.ospina@universidad.edu.co", "categoria": CategoriaDocente.CATEDRATICO, "facultad_id": facultades[2].id},
    ]
    docentes = []
    for data in docentes_data:
        d = Docente(**data, estado="activo")
        db.add(d)
        docentes.append(d)
    db.flush()
    print(f"  ✓ {len(docentes)} docentes creados")
    return docentes


def seed_asignaturas(db: Session, programas):
    asignaturas_data = [
        # Ingeniería de Sistemas (programas[0])
        {"codigo": "ISC101", "nombre": "Fundamentos de Programación", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 3, "programa_id": programas[0].id, "semestre_sugerido": 1},
        {"codigo": "ISC201", "nombre": "Bases de Datos I", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 3, "programa_id": programas[0].id, "semestre_sugerido": 3},
        {"codigo": "ISC301", "nombre": "Ingeniería de Software", "creditos": 3, "horas_teoricas": 3, "horas_practicas": 2, "programa_id": programas[0].id, "semestre_sugerido": 5},
        {"codigo": "ISC401", "nombre": "Redes de Computadores", "creditos": 3, "horas_teoricas": 2, "horas_practicas": 3, "programa_id": programas[0].id, "semestre_sugerido": 5},
        {"codigo": "ISC202", "nombre": "Bases de Datos II", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 3, "programa_id": programas[0].id, "semestre_sugerido": 4},
        # Ingeniería Industrial (programas[1])
        {"codigo": "IIN101", "nombre": "Cálculo Diferencial", "creditos": 4, "horas_teoricas": 4, "horas_practicas": 2, "programa_id": programas[1].id, "semestre_sugerido": 1},
        {"codigo": "IIN201", "nombre": "Investigación de Operaciones", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 2, "programa_id": programas[1].id, "semestre_sugerido": 4},
        # Administración (programas[2])
        {"codigo": "ADM101", "nombre": "Fundamentos de Administración", "creditos": 3, "horas_teoricas": 3, "horas_practicas": 0, "programa_id": programas[2].id, "semestre_sugerido": 1},
        {"codigo": "ADM201", "nombre": "Gestión Financiera", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 2, "programa_id": programas[2].id, "semestre_sugerido": 4},
        # Contaduría (programas[3])
        {"codigo": "CON101", "nombre": "Contabilidad General", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 2, "programa_id": programas[3].id, "semestre_sugerido": 1},
        {"codigo": "CON201", "nombre": "Contabilidad de Costos", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 2, "programa_id": programas[3].id, "semestre_sugerido": 3},
        # Medicina (programas[4])
        {"codigo": "MED101", "nombre": "Anatomía Humana", "creditos": 5, "horas_teoricas": 4, "horas_practicas": 4, "programa_id": programas[4].id, "semestre_sugerido": 1},
        {"codigo": "MED201", "nombre": "Fisiología", "creditos": 5, "horas_teoricas": 4, "horas_practicas": 4, "programa_id": programas[4].id, "semestre_sugerido": 3},
        # Enfermería (programas[5])
        {"codigo": "ENF101", "nombre": "Fundamentos de Enfermería", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 4, "programa_id": programas[5].id, "semestre_sugerido": 1},
        {"codigo": "ENF201", "nombre": "Cuidado del Paciente", "creditos": 4, "horas_teoricas": 3, "horas_practicas": 4, "programa_id": programas[5].id, "semestre_sugerido": 3},
    ]
    asignaturas = []
    for data in asignaturas_data:
        a = Asignatura(**data, estado="activa")
        db.add(a)
        asignaturas.append(a)
    db.flush()
    print(f"  ✓ {len(asignaturas)} asignaturas creadas")
    return asignaturas


def seed_grupos(db: Session, asignaturas, docentes):
    grupos_data = [
        {"asignatura_id": asignaturas[0].id, "docente_id": docentes[0].id, "periodo": "2024-1", "cupo_maximo": 35, "aula": "A101"},
        {"asignatura_id": asignaturas[0].id, "docente_id": docentes[1].id, "periodo": "2024-1", "cupo_maximo": 35, "aula": "A102"},
        {"asignatura_id": asignaturas[1].id, "docente_id": docentes[0].id, "periodo": "2024-1", "cupo_maximo": 30, "aula": "Lab1"},
        {"asignatura_id": asignaturas[2].id, "docente_id": docentes[2].id, "periodo": "2024-1", "cupo_maximo": 25, "aula": "A201"},
        {"asignatura_id": asignaturas[3].id, "docente_id": docentes[3].id, "periodo": "2024-1", "cupo_maximo": 30, "aula": "Lab2"},
        {"asignatura_id": asignaturas[4].id, "docente_id": docentes[1].id, "periodo": "2024-1", "cupo_maximo": 30, "aula": "Lab3"},
        {"asignatura_id": asignaturas[5].id, "docente_id": docentes[4].id, "periodo": "2024-1", "cupo_maximo": 40, "aula": "B101"},
        {"asignatura_id": asignaturas[6].id, "docente_id": docentes[5].id, "periodo": "2024-1", "cupo_maximo": 30, "aula": "B201"},
        {"asignatura_id": asignaturas[7].id, "docente_id": docentes[4].id, "periodo": "2024-1", "cupo_maximo": 40, "aula": "B102"},
        {"asignatura_id": asignaturas[8].id, "docente_id": docentes[6].id, "periodo": "2024-1", "cupo_maximo": 35, "aula": "B301"},
        {"asignatura_id": asignaturas[9].id, "docente_id": docentes[5].id, "periodo": "2024-1", "cupo_maximo": 35, "aula": "B103"},
        {"asignatura_id": asignaturas[10].id, "docente_id": docentes[6].id, "periodo": "2024-1", "cupo_maximo": 30, "aula": "B202"},
        {"asignatura_id": asignaturas[11].id, "docente_id": docentes[7].id, "periodo": "2024-1", "cupo_maximo": 20, "aula": "C101"},
        {"asignatura_id": asignaturas[12].id, "docente_id": docentes[8].id, "periodo": "2024-1", "cupo_maximo": 20, "aula": "C201"},
        {"asignatura_id": asignaturas[13].id, "docente_id": docentes[9].id, "periodo": "2024-1", "cupo_maximo": 25, "aula": "C102"},
        {"asignatura_id": asignaturas[14].id, "docente_id": docentes[8].id, "periodo": "2024-1", "cupo_maximo": 25, "aula": "C103"},
        # Grupos del período 2024-2
        {"asignatura_id": asignaturas[0].id, "docente_id": docentes[0].id, "periodo": "2024-2", "cupo_maximo": 35, "aula": "A101"},
        {"asignatura_id": asignaturas[1].id, "docente_id": docentes[1].id, "periodo": "2024-2", "cupo_maximo": 30, "aula": "Lab1"},
        {"asignatura_id": asignaturas[5].id, "docente_id": docentes[4].id, "periodo": "2024-2", "cupo_maximo": 40, "aula": "B101"},
        {"asignatura_id": asignaturas[9].id, "docente_id": docentes[5].id, "periodo": "2024-2", "cupo_maximo": 35, "aula": "B103"},
    ]
    grupos = []
    for data in grupos_data:
        g = Grupo(**data, estado=EstadoGrupo.ACTIVO)
        db.add(g)
        grupos.append(g)
    db.flush()
    print(f"  ✓ {len(grupos)} grupos creados")
    return grupos


def seed_estudiantes(db: Session, programas):
    nombres = ["Juan Carlos", "María Fernanda", "Andrés Felipe", "Laura Daniela", "Miguel Antonio",
               "Ana Sofía", "Carlos Eduardo", "Valentina", "Sebastián", "Juliana",
               "Diego Alejandro", "Paula Andrea", "Nicolás", "Isabella", "Mateo",
               "Camila", "Santiago", "Daniela", "Tomás", "Lucía",
               "David", "Natalia", "Alejandro", "Sofía", "Daniel",
               "Mariana", "Juan Pablo", "Gabriela", "Sergio", "Manuela"]
    apellidos = ["García", "Rodríguez", "Martínez", "López", "González",
                 "Pérez", "Sánchez", "Ramírez", "Torres", "Flores",
                 "Rivera", "Gómez", "Díaz", "Morales", "Jiménez",
                 "Ruiz", "Hernández", "Cruz", "Reyes", "Vargas",
                 "Castillo", "Ramos", "Moreno", "Ortega", "Medina",
                 "Aguilar", "Vega", "Campos", "Herrera", "Gutiérrez"]

    programas_cycle = [programas[0].id] * 8 + [programas[1].id] * 5 + [programas[2].id] * 5 + \
                      [programas[3].id] * 4 + [programas[4].id] * 4 + [programas[5].id] * 4

    estudiantes = []
    for i in range(30):
        e = Estudiante(
            codigo=f"EST{2024000 + i + 1}",
            tipo_documento=TipoDocumento.CC,
            numero_documento=f"{1000000000 + i}",
            nombres=nombres[i],
            apellidos=apellidos[i],
            correo=f"{nombres[i].lower().replace(' ', '.')}.{apellidos[i].lower()}@estudiante.edu.co",
            telefono=f"300{1000000 + i}",
            direccion=f"Calle {i + 1} #{i * 2}-{i * 3}",
            programa_id=programas_cycle[i],
            estado=EstadoEstudiante.ACTIVO,
        )
        db.add(e)
        estudiantes.append(e)
    db.flush()
    print(f"  ✓ {len(estudiantes)} estudiantes creados")
    return estudiantes


def seed_matriculas_y_notas(db: Session, estudiantes, grupos):
    """Matricula los primeros 13 estudiantes en grupos de ingeniería."""
    matriculas = []
    notas_data = [
        (4.5, 4.0, 4.2), (3.8, 3.5, 3.9), (2.5, 2.8, 2.4),
        (5.0, 4.8, 4.9), (3.0, 3.2, 2.8), (4.2, 4.5, 4.3),
        (2.0, 2.5, 2.2), (4.8, 4.9, 4.7), (3.5, 3.8, 3.7),
        (1.5, 2.0, 1.8), (4.0, 3.9, 4.1), (3.2, 3.5, 3.3),
        (4.6, 4.8, 4.7),
    ]

    # Grupo 0 y 2 son de ISC (para los primeros 13 estudiantes del programa ISC)
    target_grupos = [grupos[0], grupos[2]]
    idx = 0
    for grupo in target_grupos:
        for i, estudiante in enumerate(estudiantes[:8]):
            if idx >= len(notas_data):
                break
            m = Matricula(
                estudiante_id=estudiante.id,
                grupo_id=grupo.id,
                estado=EstadoMatricula.ACTIVA,
            )
            db.add(m)
            db.flush()

            # Crear nota
            c1, c2, c3 = notas_data[idx % len(notas_data)]
            nota_final = round(c1 * 0.30 + c2 * 0.30 + c3 * 0.40, 2)
            n = Nota(
                matricula_id=m.id,
                corte1=c1, corte2=c2, corte3=c3,
                nota_final=nota_final,
                estado_aprobacion=EstadoAprobacion.APROBADO if nota_final >= 3.0 else EstadoAprobacion.REPROBADO,
            )
            db.add(n)
            matriculas.append(m)
            idx += 1

    db.flush()
    print(f"  ✓ {len(matriculas)} matrículas y notas creadas")
    return matriculas


def seed_pagos(db: Session, estudiantes):
    pagos = []
    for i, estudiante in enumerate(estudiantes[:20]):
        estado = EstadoPago.PAGADO if i % 3 != 0 else EstadoPago.PENDIENTE
        p = PagoMatricula(
            estudiante_id=estudiante.id,
            periodo="2024-1",
            valor_pago=4_500_000.00,
            estado_pago=estado,
            medio_pago=MedioPago.PSE if estado == EstadoPago.PAGADO else None,
        )
        db.add(p)
        pagos.append(p)
    db.flush()
    print(f"  ✓ {len(pagos)} pagos creados")
    return pagos


def seed_usuarios(db: Session):
    usuarios_data = [
        {"username": "admin", "correo": "admin@universidad.edu.co", "password": "Admin123!", "rol": RolUsuario.ADMIN},
        {"username": "coordinador1", "correo": "coordinador@universidad.edu.co", "password": "Coord123!", "rol": RolUsuario.COORDINADOR},
        {"username": "administrativo1", "correo": "adm@universidad.edu.co", "password": "Adm123!", "rol": RolUsuario.ADMINISTRATIVO},
    ]
    usuarios = []
    for data in usuarios_data:
        u = Usuario(
            username=data["username"],
            correo=data["correo"],
            password_hash=hash_password(data["password"]),
            rol=data["rol"],
            estado="activo",
        )
        db.add(u)
        usuarios.append(u)
    db.flush()
    print(f"  ✓ {len(usuarios)} usuarios creados")
    for u in usuarios_data:
        print(f"    → username: {u['username']} | password: {u['password']} | rol: {u['rol']}")
    return usuarios


def run_seed():
    print("\n🌱 Iniciando seed de datos...\n")
    db = SessionLocal()
    try:
        print("📁 Creando facultades...")
        facultades = seed_facultades(db)

        print("📚 Creando programas académicos...")
        programas = seed_programas(db, facultades)

        print("👨‍🏫 Creando docentes...")
        docentes = seed_docentes(db, facultades)

        print("📖 Creando asignaturas...")
        asignaturas = seed_asignaturas(db, programas)

        print("🗓️  Creando grupos...")
        grupos = seed_grupos(db, asignaturas, docentes)

        print("👩‍🎓 Creando estudiantes...")
        estudiantes = seed_estudiantes(db, programas)

        print("📝 Creando matrículas y notas...")
        seed_matriculas_y_notas(db, estudiantes, grupos)

        print("💰 Creando pagos...")
        seed_pagos(db, estudiantes)

        print("👤 Creando usuarios...")
        seed_usuarios(db)

        db.commit()
        print("\n✅ Seed completado exitosamente!\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante el seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
