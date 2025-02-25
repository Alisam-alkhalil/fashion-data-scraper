def run_dbt_models() -> None:
    import subprocess

    subprocess.run(["dbt", "run", "--models", "final_prices"], check=True)
