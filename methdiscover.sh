#!/bin/bash

# methdiscover is a HTTP method enumeration tool
# You can load a file containing URLs and methdiscover will utilize the OPTIONS method
# to fetch the available methods.
# Script made by: Sp1derM0rph3us

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

print_red() {
    printf "${RED}$1${NC}\r\n"
}

print_green() {
    printf "${GREEN}$1${NC}\r\n"
}

print_blue(){
    printf "${BLUE}$1${NC}\r\n"
}

print_yellow() {
    printf "${YELLOW}$1${NC}\r\n"
}

if [[ "$1" == "" ]]; then
  printf "Usage: $0 [URLs-file]\r\n"

else
  wordlist=$(cat "$1")
  ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"

  for url in $wordlist; do
    resp=$(curl -v -A "$ua" -X OPTIONS "$url" 2>&1 | grep -i allow | cut -d ':' -f 2- | tr -d ' ')
    if [[ "$resp" =~ "OPTIONS" ]]; then
      print_green "[+] Methods for: $url"
      printf " --> $resp\r\n"

    else
      printf "\r\n"
      print_red "[-] Failed trying to use OPTIONS method in: $url"
      printf "\r\n"

    fi
  done
fi
