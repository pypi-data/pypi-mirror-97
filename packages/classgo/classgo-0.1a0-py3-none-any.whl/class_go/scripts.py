from webbrowser import open
from subprocess import Popen

import click
from click.utils import echo

from .db import get_db
from .db import delete_db
from . import converter

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version 0.1.dev1")
    ctx.exit()

@click.group()
@click.option("--version", is_flag=True, callback=print_version,
                expose_value=False, is_eager=True, help="Show version and exit")
def cli():
    pass

@click.command("add", help=click.style("add a new class", bold=True))
@click.argument("name")
@click.option("--nick", "-n", help="A nickname to the new class")
@click.option("--teacher","-t", help="The teacher's name")
@click.option("--link", "-l", help="The link to the meet")
def add(name, nick, teacher, link):
    # TODO: Cambiar esta funcion a otro archivo
    """
    Funcion encargada de añadir una clase y su horario
    a la base de datos 
    """

    click.echo("\nAñadiremos " + click.style(name, fg="bright_cyan", bold=True) + " a las clases.")

    click.secho("Necesito saber algunas cosas.\n", bold=True)

    # Revisa si se indexo el apodo en el comando
    if nick is None:
        # En caso de que no lo haya ingresado, pregunta si quiere agregarlo
        if click.confirm(f"¿Tiene {name} algún sobrenombre?"):
            nick = click.prompt("Cuéntame cual", type=str)

    # Revisa si se indexo el profesor en el comando
    if teacher is None:
        # En caso de que no lo haya ingresado, pregunta cual es
        teacher = click.prompt("¿Cuál es el nombre del profesor?")

    if link is None:
        link = click.prompt("¿Cuál es el link para la clase?")

    db, c = get_db()

    c.execute(f"INSERT INTO class VALUES (\"{name}\", \"{teacher}\", \"{link}\")")
    
    db.commit()
    db.close

    while True:
        try:
            click.secho("\n[Lunes:1, Martes:2, Miércoles:3, Jueves:4, Viernes:5, Sabado:6, Domingo:7]", fg="yellow")
            date = click.prompt("\nBasado en la tabla de arriba\n¿Qué día/s ocupa?(separe con una coma)")
            dates = converter.date_list(date)
            break
        except ValueError:
            click.echo("\n" + click.style("Error", bg="red", fg="white") + click.style(": Por favor siga las instrucciones", bold=True))

        except AssertionError:
            click.echo("\n" + click.style("Error", bg="red", fg="white") + click.style(": los números deben estar en el rango 1-7", bold=True))

        click.pause("\nToque cualquier tecla para volver a intentarlo.")


    db, c = get_db()
    for d in dates:
        while True:
            try:
                time = click.prompt(f"¿A qué hora comienza el dia {d}?[hh:mm]")
                list_time = converter.hour_list(time)
                break
            except AssertionError:
                click.echo("\n" + click.style("Error", bg="red", fg="white") + click.style(": Por favor siga las instrucciones", bold=True))
            except ValueError:
                click.echo("\n" + click.style("Error", bg="red", fg="white") + click.style(": Por favor siga las instrucciones", bold=True))
            
            click.pause("\nToque cualquier tecla para volver a intentarlo.")
        c.execute(f"INSERT INTO bouquet VALUES (\"{d}\", \"{list_time[0]}\", \"{list_time[1]}\", \"{name}\")")
    db.commit()
    db.close()

@click.command("goto")
@click.argument("NAME")
def goto(name):
    db, c = get_db()

    c.execute(f"SELECT * FROM class WHERE name=\"{name}\"")
    the_class = c.fetchone()
    

    class_name = click.style(the_class[0], fg="red", bold=True)
    class_teacher = click.style(the_class[1], fg="yellow")
    click.echo("\nConectandote a " + class_name + " con " + class_teacher)
    
    if not open(the_class[2]):
        click.echo(f"\nNo he podido abrir el link :(\nPero aquí lo tienes: {the_class[2]}")

    if click.confirm("¿Desea que ejecute DroidCam?"):
        Popen("/usr/bin/droidcam")
        

@click.command("delete_db")
def delete_db_comand():
    delete_db() 
    

cli.add_command(add)
cli.add_command(goto)
cli.add_command(delete_db_comand)