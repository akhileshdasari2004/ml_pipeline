import asyncio
import click
from ..bot import TrainingDataBot
from ..models.task import TaskTemplate
from ..config.constants import TaskType, ExportFormat
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

@click.group()
@click.pass_context
def cli(ctx):
    """Enterprise ML Training Data Pipeline CLI."""
    ctx.ensure_object(dict)
    ctx.obj['bot'] = TrainingDataBot()

@cli.command()
@click.option('--url', help='Web URL to load')
@click.option('--file', help='Local file path to load')
@click.pass_context
def load(ctx, url, file):
    """Load documents from a source."""
    bot = ctx.obj['bot']
    source = url or file
    if not source:
        click.echo("Error: Must provide --url or --file")
        return
    
    async def run():
        docs = await bot.load_documents(source)
        click.echo(f"Successfully loaded {len(docs)} documents.")

    asyncio.run(run())

@cli.command()
@click.pass_context
def process(ctx):
    """Process loaded documents into chunks."""
    bot = ctx.obj['bot']
    async def run():
        # In a real CLI, we'd need to persist state between commands.
        # For simplicity, this is a placeholder for the logic.
        click.echo("Processing documents...")
        # chunks = await bot.process_documents()
        click.echo("Documents processed. (State persistent only in single run for this demo)")

    asyncio.run(run())

@cli.command()
@click.option('--task', type=click.Choice(['qa']), default='qa')
@click.pass_context
def generate(ctx, task):
    """Generate training data."""
    click.echo(f"Generating {task} training data...")

@cli.command()
@click.option('--name', required=True, help='Dataset name')
@click.option('--format', type=click.Choice(['json', 'csv']), default='json')
@click.pass_context
def export(ctx, name, format):
    """Export the dataset."""
    click.echo(f"Exporting dataset {name} as {format}...")

if __name__ == '__main__':
    cli()
