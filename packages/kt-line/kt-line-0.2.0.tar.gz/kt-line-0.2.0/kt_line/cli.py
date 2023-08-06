from kt_line import kt_line
import click


@click.command()
@click.argument("a")
@click.argument("b")
def cli(a, b):
    if a and b:
        click.echo(kt_line.line(float(a), float(b)))


if __name__ == "__main__":
    cli()
