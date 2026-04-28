import argparse
import os

from ai.sentiment.src.app.constant.common import (
    SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID,
)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


def define_arguments():
    parser = argparse.ArgumentParser(description="CLI to run sentiment classification app")
    mode_subparsers = parser.add_subparsers(dest="mode", required=True)

    run_app_parser = mode_subparsers.add_parser(
        "run_app_parser", help="Run consumer app"
    )

    trace_model_parser = mode_subparsers.add_parser("trace_model", help="Trace model")
    trace_model_parser.add_argument(
        "--model-id",
        type=str,
        default=SENTIMENT_CLASSIFICATION_DEFAULT_MODEL_ID,
    )
    trace_model_parser.add_argument(
        "--device", type=str, choices=("cpu", "cuda", "neuron"), default="cpu"
    )

    return parser



def main():
    parser = define_arguments()

    args = parser.parse_args()

    match args.mode:
        case "run_app_parser":
            from ai.sentiment.cli.main import run_app_parser
            run_app_parser()
        case "trace_model":
            from ai.sentiment.neuron.aws_neuron import AWSNeuron

            AWSNeuron(model_id=args.model_id, device=args.device, folder="model-traced").trace()
            pass


if __name__ == "__main__":
    main()