# Bash, Ansible and Python Utils.

## Install

## Docker 
```bash
docker pull kalilinux/kali:latest
```

```bash
apt update -y; apt full-upgrade -y; apt install -y kali-linux-everything
sudo python3 -m pip install --upgrade bapy
```

### With pip available

#### No python
```bash
sudo apt update -y; apt install python3.8 python3-pip -y
sudo python3 -m pip install --upgrade bapy

```

#### With sudo in debian/kali or macos in bootstrap if brew not installed
```bash
sudo python3 -m pip install --upgrade bapy
```

#### When brew installed:

```bash
python3 -m pip install --upgrade bapy
```

### Upload & Upgrade

```bash
rebashrc
```

## Update secrets (token, etc.) and ssh keys on source server and other servers

### On the git source code server

Update the repository and:

```bash
rc secrets  # secrets-push.sh
rebash
```

#### On other servers
```bash
rc secrets  #secrets-pull.sh 
rebash
```

## Other PyPi Projects Upload and Upgrade

### On the git source code server

Perform any tests and:

```bash
rc up  # project-upload.sh <path> <major|minor> <j5pu|jose-nferx|pypi>
```

#### On other servers

```bash
upgrade.sh name
```
