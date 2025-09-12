import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        cmd = ["python", file_path] + list(args)

        completed_process = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
        )

        stdout = completed_process.stdout or ""
        stderr = completed_process.stderr or ""

        if not stdout.strip() and not stderr.strip():
            return "No output produced."

        parts = [
            f"STDOUT:{stdout}",
            f"STDERR:{stderr}",
        ]

        if completed_process.returncode != 0:
            parts.append(f"Process exited with code {completed_process.returncode}")
        return " ".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"
