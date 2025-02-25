def run_dbt_models() -> None:
    """
    Executes the dbt command to run the 'final_prices' model.

    This function uses the subprocess module to run the dbt CLI with the
    specified model. It ensures that the dbt process completes successfully
    by setting check=True, which will raise a CalledProcessError if the
    command returns a non-zero exit code.
    """

    import subprocess

    subprocess.run(["dbt", "run", "--models", "final_prices"], check=True)
