"""Python wrapper around dbt with custom logging."""

import dbt
import dbt.main
import argparse
import logging
import stacklogging

dbt_logger = logging.getLogger("dbt")
dbt_logger.setLevel(logging.FATAL)

logger = stacklogging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", help="executes dbt command", choices=["run", "test"])
    parser.add_argument("-m", "--models", required=False, nargs="+")
    args = parser.parse_args()

    dbt_command = [args.command] + ["--models"] + args.models

    logger.info("Executing dbt " + " ".join(dbt_command))
    results, success = dbt.main.handle_and_check(dbt_command)

    for res in results:
        name = res.node.get("alias")
        extra_dict = {
            "execution_time": int(res.execution_time),
            "model": name,
            "serviceContext": {"service": "buda-" + res.node.package_name + "-dbt"},
            "context": {"reportLocation": {"functionName": name}},
        }

        if args.command == "run":
            if res.errored:
                extra_dict["error"] = res.error
                extra_dict["compiled"] = res.node.get("compiled_sql")
                logger.error(f"Error compiling model {name}", extra=extra_dict)
            else:
                logger.info(f"Model {name} completed", extra=extra_dict)

        if args.command == "test":
            if res.fail:
                logger.error(f"Test {name} failed", extra=extra_dict)
            else:
                logger.info(f"Test {name} passed", extra=extra_dict)


if __name__ == "__main__":
    main()
