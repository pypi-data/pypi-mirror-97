from testcase.app.drilling_efficiency_app import DrillingEfficiency


def lambda_handler(event, context):
    """
    This function is the main entry point of the AWS Lambda function
    :param event: a scheduler or kafka event
    :param context: AWS Context
    :return:
    """
    app = DrillingEfficiency()
    app.load(event)
    app.run_modules()
    app.save_state()
