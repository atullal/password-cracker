# Password Cracker

This is a mini-project for GRS CS 655 that aims to develop a password cracker using dictionary-based attacks. The project was developed by Prateek Jain, Atul Lal, Nishil Agrawal, and Dhruv Toshniwal.

## Problem

Passwords are an essential part of online security, but they can be easily compromised if they are not strong enough. Many users choose weak passwords that are easy to guess or crack, which can lead to unauthorized access to their accounts. Password cracking is the process of guessing or cracking passwords using various techniques like brute force attacks and dictionary-based attacks. Dictionary-based attacks are one of the most common methods used by attackers to crack passwords. In this method, the attacker uses a list of words from a dictionary file to try and guess the password.

## Solution

The goal of this project is to develop a password cracker that can crack passwords using dictionary-based attacks. The cracker should be able to read in a list of hashed passwords and corresponding usernames from a file, and then use a dictionary file to try and crack the passwords. The program should output the cracked passwords along with their corresponding usernames.

We developed our password cracker using Python and Flask web framework for building the webserver. The frontend is built using HTML/CSS/JS and hosted on Netlify. The webserver is hosted on Heroku.

## Learning Outcomes

Through this project, we aimed to achieve the following learning outcomes:
- Understanding of password cracking techniques
- Familiarity with dictionary-based attacks
- Experience with programming in Python
- Knowledge of web development frameworks like Flask

## Setup Diagram

The following diagram shows the setup for our password cracker:

```
[Frontend] <--> [Webserver] <--> [Password Cracker]
```

## Important Links

- [Github Link](https://github.com/atullal/password-cracker)
- Clone git repository: `git clone https://github.com/atullal/password-cracker`
- Download Project.zip folder: `wget https://github.com/atullal/password-cracker/blob/main/Project.zip`
- [Project Working Video Link](https://drive.google.com/file/d/1GiuQ0pWWLk7S17Vf2BSa-aGe23b7EaXp/view?usp=sharing)
