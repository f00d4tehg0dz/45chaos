provider "aws" {
  region = "us-west-2"
}

terraform {
  backend "s3" {
    bucket = "mooches.terraform.state"
    key    = "mooches-dev/web.tfstate"
    region = "us-west-2"
  }
}

variable "environment" {
  default = "dev"
}

module "web" {
  source = "../../../modules/web"
}
