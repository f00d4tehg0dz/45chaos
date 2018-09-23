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

variable "public_ip" {
  default = "34.217.225.142"
}

module "web" {
  source    = "../../../modules/web"
  public_ip = "${var.public_ip}"
}
