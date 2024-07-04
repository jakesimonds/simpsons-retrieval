provider "aws" {
  region = "us-east-1"  # Change to your desired region
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
  
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  ]
}

resource "aws_lambda_function" "Simpsons_lambda" {
  function_name = "Simpsons_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.12"

  filename      = "RagHandbook.zip"  # Path to your deployment package

  source_code_hash = filebase64sha256("RagHandbook.zip")


}

resource "aws_lambda_permission" "allow_invoke" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.Simpsons_lambda.function_name
  principal     = "apigateway.amazonaws.com"
}