variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "source_ami" {
  type    = string
  default = "ami-08c40ec9ead489470" # Ubuntu 22.04 LTS
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}

variable "subnet_id" {
  type    = string
  default = "subnet-0c4aa446f9ad985e1"
}

variable "access_key" {
  type    = string
  default = "AKIATGZHMLGE4GB7ACMO"
}

variable "secret_key" {
  type    = string
  default = "C9MA16LunY60CHlCkoLkPERikutw4L5zJCzQtjtG"
}

# https://www.packer.io/plugins/builders/amazon/ebs
source "amazon-ebs" "my-ami" {
  region          = "${var.aws_region}"
  ami_name        = "csye6225_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  ami_description = "AMI for CSYE 6225"
  access_key      = var.access_key
  secret_key      = var.secret_key
  ssh_agent_auth  = false
  ami_regions = [
    "us-east-1",
    "us-west-1",
  ]

  aws_polling {
    delay_seconds = 120
    max_attempts  = 50
  }


  instance_type               = "t2.micro"
  source_ami                  = "${var.source_ami}"
  ssh_username                = "${var.ssh_username}"
  subnet_id                   = "${var.subnet_id}"
  associate_public_ip_address = true
  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
    volume_size           = 8
    volume_type           = "gp2"
  }
}

build {
  sources = ["source.amazon-ebs.my-ami"]
  provisioner "file" {
    source = "/home/runner/work/webapp/webapp.zip"
    destination = "/home/ubuntu/webapp.zip"
  }
  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1"
    ]
    inline = [
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install nginx -y",
      "sudo apt-get install unzip",
      "sudo apt-get install python3 -y",
      "sudo apt-get install python3-pip -y",
      "sudo apt-get install python3-venv -y",
      "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential -y",
      "sudo apt-get install python3-mysql.connector -y",
      "sudo apt-get install python3-mysqldb -y",
      "sudo apt-get install mysql-server -y",
      "sudo systemctl start mysql.service",
      "sudo apt-get clean",
      "unzip webapp.zip",
      "sleep 100",
      "cd /home/ubuntu/home/runner/work/webapp/webapp/",
      "python3 -m venv venv",
      "'.' venv/bin/activate",
      "pip install wheel",
      "pip install fastapi",
      "pip install \"uvicorn[standard]\"",
      "pip install python-decouple",
      "pip install python-multipart",
      "pip install PyJWT",
      "pip install SQLAlchemy",
      "pip install bcrypt",
      "pip install mysqlclient",
      "pip install gunicorn",
      "pip install social-auth-core",
      "pip install python-jose",
      "sudo python3 initDB.py",
      "sudo cp webapp.service /etc/systemd/system/",
      "sudo systemctl start webapp",
      "sudo systemctl enable webapp",
    ]
  }
}

packer {
  required_plugins {
    amazon = {
      version = ">=1.1.1"
      source  = "github.com/hashicorp/amazon"
    }
  }
}
