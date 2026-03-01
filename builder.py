import os
import click
from dotenv import load_dotenv
from selenium_ide_ai_side_builder import AISideBuilder

RUNNER_TEMPLATE = """from selenium_ide_ai_side_builder import AISideBuilder


def main():
    builder = AISideBuilder(base_url="", api_key="")
{steps}
    builder.close()
    print("Done.")


if __name__ == "__main__":
    main()
"""

@click.command()
@click.option('--output', 'name', default='scenario', help='Project name')
def main(name):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        click.echo("Error: OPENAI_API_KEY not found.")
        return

    builder = AISideBuilder(base_url="", api_key=api_key)
    saved_steps = []
    step = 1

    click.echo(f"--- Designer Mode: {name} ---")
    
    try:
        while True:
            prompt = click.prompt(f"\n[Step {step}] Action (or 'exit')", default='exit')
            if prompt.lower() in ['exit', 'done']:
                break

            file_path = f"{name}_step_{step}.side"
            
            try:
                builder.ai_create_side_file(llm_prompt=prompt, side_file=file_path)
                builder.play_side(file_path)
                
                if click.confirm(f"Save {file_path}?", default=True):
                    saved_steps.append((file_path, prompt))
                    step += 1
                else:
                    if os.path.exists(file_path):
                        os.remove(file_path)
            except Exception as e:
                click.echo(f"Error: {e}")

    finally:
        builder.close()

    if saved_steps:
        steps_code = "\n".join([
            f"    builder.play_side('{f}', name='{p}')" 
            for f, p in saved_steps
        ])
        output_filename = f"{name}.py"
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(RUNNER_TEMPLATE.format(steps=steps_code))
        
        click.echo("\n--- Process Finished ---")
        click.echo(f"Files: {', '.join([s[0] for s in saved_steps])}")
        click.echo(f"Script: {output_filename}")
    else:
        click.echo("\nNo steps saved. Exiting.")

if __name__ == "__main__":
    main()
