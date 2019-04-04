#!/usr/bin/python

import sys, time, hashlib
from array import *

# Ask the user if they want the onscreen instructions
yesno = input("Do you want the program to pause at each step so you have time to read the instructions? (type yes or no): ")
if yesno == "no" or yesno == "n" or yesno == "NO" or yesno == "N":
    show_instructions = False
    print("Okay, then once you start the program it will run without pausing.")
else:
    show_instructions = True
    print("Okay, the program will display more information as it runs and pause at each step.")
    input("Press enter to continue.")
    
#--------------- global variables we expect will be used by any function -----------
#
# a number from 1 to 6 selects which password we'll be trying to guess from
# a selection below.
which_password = 0

# the user names and password we're trying to 'crack'.

password0 = ""
password1 = ""
password2 = ""
password3 = ""
password4 = ""
password5 = ""
password6 = ""


# total number of guesses we had to make to find it
totalguesses = 0


#--------------- extra helper functions -------------------
# These will be used by our search routines later on. We'll get these defined and out
# of the way. The actual search program is called "main" and will be the last one
# defined. Once it's defined, the last statement in the file runs it.
#

## Convert a string into MD5 hash
def MD5me(s):
    result = s.encode("utf-8")
    result = hashlib.md5(result).hexdigest()
    return result

# Takes a number from 0 on up and the number of digits we want it to have. It uses that
# number of digits to make a string like "0000" if we wanted 4 or "00000" if we wanted
# 5, converts our input number to a character string, sticks them together and then returns
# the number we started with, with extra zeroes stuck on the beginning. 
def leading_zeroes(n, zeroes):
    t=("0"*zeroes)+str(n)
    t=t[-zeroes:]
    return t

# This function checks if the MD5 hash value of the password you have guessed equals
# the MD5 hash value of the real password.
def check_userpass(which_password, password):
    global password0, password1, password2, password3
    global password4, password5, password6
    
    result = False

    if (0 == which_password):
        if password == password0:
            result = True

    if (1 == which_password):
        if MD5me(password) == password1:
            result = True

    if (2 == which_password):
        if (MD5me(password) == password2):
            result = True

    if (3 == which_password):
        if (MD5me(password) == password3):
            result = True

    if (4 == which_password):
        if (MD5me(password) == password4):
            result = True
            
    if (5 == which_password):
        if (MD5me(password) == password5):
            result = True
            
    if (6 == which_password):
        if (MD5me(password) == password6):
            result = True
            
    return result

# This displays the results of a search including tests per second when possible
def report_search_time(tests, seconds):
    if (seconds > 0.000001):
        print ("The search took "+make_human_readable(seconds)+" seconds for "+make_human_readable(tests)+" tests or "+make_human_readable(tests/seconds)+" tests per second.")
    else:
        print ("The search took "+make_human_readable(seconds)+" seconds for "+make_human_readable(tests)+" tests.")
    return

# This function takes in numbers, rounds them to the nearest integer and puts
# commas in to make it more easily read by humans
def make_human_readable(n):
    if n>=1:
        result = ""
        temp=str(int(n+0.5))
        while temp != "":
            result = temp[-3:] + result
            temp = temp[:-3]
            if temp != "":
                result = "," + result
    else:
        temp = int(n*100)
        temp = temp /100
        result = str(temp)
    return result
        
## A little helper program to remove any weird formatting in the file
def cleanup (s):
    s = s.strip()
    return s

## A little helper program that capitalizes the first letter of a word
def Cap (s):
    s = s.upper()[0]+s[1:]
    return s

# --------------------- password guessing functions ----------------------------

# *** METHOD 1 ***
#
# search method 1 will try using digits as the password.
# first it will guess 0, 1, 2, 3...9, then it will try 00, 01, 02...99, etc.
def search_method_1(num_digits):
    global totalguesses
    result = False
    a=0
    #num_digits = 3    # How many digits to try. 1 = 0 to 9, 2 = 00 to 99, etc.
    starttime = time.time()
    tests = 0
    still_searching = True
    print()
    print("Using method 1 and searching for "+str(num_digits)+" digit numbers...")
    while still_searching and a<(10**num_digits):
        ourguess = leading_zeroes(a,num_digits)
        print(ourguess)
        tests = tests + 1
        totalguesses = totalguesses + 1
        if (check_userpass(which_password, ourguess)):
            print ("Success! Password "+str(which_password)+" is " + ourguess)
            still_searching = False   # we can stop now - we found it!
            result = True
        #else:
            #print ("Darn. " + ourguess + " is NOT the password.")
        a=a+1

    seconds = time.time()-starttime
    report_search_time(tests, seconds)
    return result

# *** METHOD 2 ***
#
# search method 2 is a simulation of a letter-style combination lock. Each 'wheel' has the
# letters A-Z, a-z and 0-9 on it as well as a blank. The idea is that we have a number of
# wheels for a user name and password and we try each possible combination.

def search_method_2(num_pass_wheels):
    global totalguesses
    result = False
    starttime = time.time()
    tests = 0
    still_searching = True
    print()
    print("Using method 2 and searching with "+str(num_pass_wheels)+" characters.")
    wheel = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    # we only allow up to 8 wheels for each password for now
    if (num_pass_wheels > 8):
        print("Unable to handle the request. No more than 8 characters for a password")
        still_searching = False
    else:
        if show_instructions:
            print("WARNING: a brute-force search can take a long time to run!")
            print("Try letting this part of the program run for a while (even overnight).")
            print("Press ctrl+C to stop the program.")
            print("Read the comments in Method 2 of the program for more information.")
            print()
    
    # set all of the wheels to the first position
    pass_wheel_array=array('i',[1,0,0,0,0,0,0,0,0])
        
    while still_searching:
        ourguess_pass = ""
        for i in range(0,num_pass_wheels):  # once for each wheel
            if pass_wheel_array[i] > 0:
                ourguess_pass = wheel[pass_wheel_array[i]] + ourguess_pass
        # print ("trying ["+ourguess_pass+"]")
        if (check_userpass(which_password, ourguess_pass)):
            print ("Success! Password  "+str(which_password)+" is " + ourguess_pass)
            still_searching = False   # we can stop now - we found it!
            result = True
        #else:
            #print ("Darn. " + ourguess + " is NOT the password.")
        tests = tests + 1
        totalguesses = totalguesses + 1
        
# spin the rightmost wheel and if it changes, spin the next one over and so on
        carry = 1
        for i in range(0,num_pass_wheels): # once for each wheel
            pass_wheel_array[i] = pass_wheel_array[i] + carry
            carry = 0
            if pass_wheel_array[i] > 62:
                pass_wheel_array[i] = 1
                carry = 1
                if i == (num_pass_wheels-1):
                    still_searching = False

    seconds = time.time()-starttime
    report_search_time(tests, seconds)
    return result

# *** METHOD 3 ***
#
# search method 3 uses a list of dictionary words.

def search_method_3(file_name):
    global totalguesses
    result = False
    
    # Start by reading the list of words into a Python list
    f = open(file_name)
    words = f.readlines()
    f.close
    # We need to know how many there are
    number_of_words = len(words)
    print()
    print("Using method 3 with a list of "+str(number_of_words)+" words...")
    
    ## Depending on the file system, there may be extra characters before
    ## or after the words. 
    for i in range(0, number_of_words):
        words[i] = cleanup(words[i])

    # Let's try each one as the password and see what happens
    starttime = time.time()
    tests = 0
    still_searching = True
    word1count = 0           # Which word we'll try next

    while still_searching:
        ourguess_pass = words[word1count]
        print("Guessing: "+ourguess_pass)
        # Try it the way it is in the word list
        if (check_userpass(which_password, ourguess_pass)):
            print ("Success! Password "+str(which_password)+" is " + ourguess_pass)
            still_searching = False   # we can stop now - we found it!
            result = True
        #else:
            #print ("Darn. " + ourguess_pass + " is NOT the password.")
        tests = tests + 1
        totalguesses = totalguesses + 1
        # Now let's try it with the first letter capitalized
        if still_searching:
            ourguess_pass = Cap(ourguess_pass)
            print("Guessing: "+ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print ("Success! Password "+str(which_password)+" is " + ourguess_pass)
                still_searching = False   # we can stop now - we found it!
                result = True
            #else:
                #print ("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1

        word1count = word1count + 1
        if (word1count >=  number_of_words):
            still_searching = False

    seconds = time.time()-starttime
    report_search_time(tests, seconds)
    return result

# *** METHOD 4 ***     
# Search method 4 is similar to 3 in that it uses the dictionary, but it tries
# three words separated by a punctuation character.

def search_method_4(file_name):
    global totalguesses
    result = False

    # Start by reading the list of words into a Python list
    f = open(file_name)
    words = f.readlines()
    f.close
    # We need to know how many there are
    number_of_words = len(words)
    # print("number of words in file: "+number_of_words)

    ## Depending on the file system, there may be extra characters before
    ## or after the words.
    for i in range(0, number_of_words):
        words[i] = cleanup(words[i])

    # Let's try each one as the password and see what happens
    starttime = time.time()
    tests = 0
    still_searching = True
    word1count = 0  # Which word we'll try next
    punc_count1 = 0
    punc_count2 = 0
    word2count = 0
    word3count = 0

    punctuation = "~!@#$%^&*()_-+={}[]:<>,./X"  # X is a special case where we omit
    # the punctuation to run the words together

    number_of_puncs = len(punctuation)
    # print("number of punctuation: "+len(punctuation))
    print("Using method 5 with " + str(number_of_puncs) + " punctuation characters and " + str(
        number_of_words) + " words...")

    while still_searching:
        if ("X" == punctuation[punc_count1] and "X" == punctuation[punc_count2]):
            # If we're at the end of the string and found the 'X', leave it out
            ourguess_pass = words[word1count] + words[word2count] + words[word3count]
        else:
            ourguess_pass = words[word1count] + punctuation[punc_count1] + words[word2count] + punctuation[
                punc_count2] + words[word3count]
            # print("inside else part: word guessing is::"+ourguess_pass)
        print("Guessing: " + ourguess_pass)
        # Try it the way they are in the word list
        if (check_userpass(which_password, ourguess_pass)):
            print("Success! Password " + str(which_password) + " is " + ourguess_pass)
            still_searching = False  # we can stop now - we found it!
            result = True
        # else:
        # print ("Darn. " + ourguess_pass + " is NOT the password.")
        tests = tests + 1
        totalguesses = totalguesses + 1
        # Now let's try it with first letter of the third word capitalized
        if still_searching:
            ourguess_pass = words[word1count] + punctuation[punc_count1] + words[word2count] + punctuation[
                punc_count2] + Cap(words[word3count])
            print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the first letter of the first word capitalized
        if still_searching:
            ourguess_pass = Cap(words[word1count]) + punctuation[punc_count1] + words[word2count] + punctuation[
                punc_count2] + words[word3count]
            print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Passwword " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
                # else:
                print("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the first letter of the second word capitalized
        if still_searching:
            ourguess_pass = words[word1count] + punctuation[punc_count1] + Cap(words[word2count]) + punctuation[
                punc_count2] + words[word3count]
            print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the first letter of the  word and second word capitalized
        if still_searching:
            ourguess_pass = Cap(words[word1count]) + punctuation[punc_count1] + Cap(words[word2count]) + punctuation[
                punc_count2] + words[word3count]
            print("Guessing: " + ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the second letter of the  word and third word capitalized
        if still_searching:
            ourguess_pass = words[word1count] + punctuation[punc_count1] + Cap(words[word2count]) + punctuation[
                punc_count2] + Cap(words[word3count])
            print("Guessing: "+ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the first letter of the  word and third word capitalized
        if still_searching:
            ourguess_pass = Cap(words[word1count]) + punctuation[punc_count1] + words[word2count] + punctuation[
                punc_count2] + Cap(words[word3count])
            print("Guessing: "+ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1
        # Now let's try it with the all 3 words capitalized
        if still_searching:
            ourguess_pass = Cap(words[word1count]) + punctuation[punc_count1] + Cap(words[word2count]) + punctuation[
                punc_count2] + Cap(words[word3count])
            print("Guessing: "+ourguess_pass)
            if (check_userpass(which_password, ourguess_pass)):
                print("Success! Password " + str(which_password) + " is " + ourguess_pass)
                still_searching = False  # we can stop now - we found it!
                result = True
            # else:
            # print ("Darn. " + ourguess_pass + " is NOT the password.")
            tests = tests + 1
            totalguesses = totalguesses + 1

        word1count = word1count + 1
        # print("first round completed for word"+words[word1count])
        if (word1count >= number_of_words):
            word1count = 0
            punc_count1 = punc_count1 + 1
            # print("111 first round completed for word"+words[word1count])
            if (punc_count1 >= number_of_puncs):
                punc_count1 = 0
                word2count = word2count + 1
                print("222 second round completed for punctuation" + punctuation[punc_count1])
                if (word2count >= number_of_words):
                    word2count = 30
                    punc_count2 = punc_count2 + 1;
                    print("333 first round completed for word" + words[word2count])
                    if (punc_count2 >= number_of_puncs):
                        punc_count2 = 6
                        word3count = word3count + 1
                        print("444 second round completed for punctuation" + punctuation[punc_count2])
                        if (word3count >= number_of_words):
                            print("555 first round completed for word" + words[word3count])
                            till_searching = False

    seconds = time.time() - starttime
    report_search_time(tests, seconds)
    return result


# -------------------------- main function ----------------------------

def main(argv=None):
    global password0, password1, password2, password3
    global password4, password5, password6, totalguesses
    global which_password

    # To test your own algorithms, change password0. This password is displayed
    # in "plaintext" so you can see the password in advance. 
    password0 = "a1b2"

    # These passwords' real text is hidden from you using something called MD5 hashing. This converts
    # the original password to a block of (seemingly) gibberish text. 
    # You can create your own MD5 hashes using the MD5me function in this program.

    password1="202cb962ac59075b964b07152d234b70"
    password2="570a90bfbf8c7eab5dc5d4e26832d5b1"
    password3="f78f2477e949bee2d12a2c540fb6084f"
    password4="09408af74a7178e95b8ddd4e92ea4b0e"
    password5="2034f6e32958647fdff75d265b455ebf"
    password6="db62cb465bef46e1bf4a050b4402646f"

    # start searching
    which_password = 1
    if show_instructions:
        print()
        print("How about the comments in the program?")
        print("Make sure you read those instructions before you continue!")
        input("Press enter to start the program.")
        print()
        print("This program will use several different algorithms to try and guess passwords.")
        print("You can set password 0 yourself (see comments in program).")
        print()
    which_password = int(input("Which password do you want to try to guess (0-6)? "))

    if show_instructions:
        print()
        print("The program will now automatically try to guess the password using several different methods:")
        print()
        print("Method 1 will only guess digits 0-9.")
        print("Method 2 will guess digits 0-9 as well as letters a-z and A-Z.")
        print("Method 3 will guess using a list of common passwords.")
        print("Method 4 will try combinations of common words with punctuation in between them.")
        print()
        print("Read the comments in the code for more details about each method.")
        input("Press enter to continue.")
        print()
    
    overallstart = time.time()
    foundit = False
    print("Trying to guess password "+str(which_password)+"...")
    # Look through our list of common passwords first
    if not foundit:
        foundit = search_method_3("C:/Users/manog/Desktop/Comp_Security_Principles/passwords.txt")
    # Still looking? Let's combine the common passwords 2 at a time
    if not foundit:
        print("Method 3 did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_4("C:/Users/manog/Desktop/Comp_Security_Principles/passwords.txt")
    # Still looking? See if it's a single digit
    if not foundit:
        print("Method 4 did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(1)
    # Still looking? See if it's a 2 digit number
    if not foundit:
        print("Method 1 (1 digit) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(2)
    # Still looking? See if it's a 3 digit number
    if not foundit:
        print("Method 1 (2 digit) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(3)
    # Still looking? See if it's a 4 digit number
    if not foundit:
        print("Method 1 (3 digit) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(4)
    # Still looking? Use our rotary wheel simulation up to 6 wheels.
    # This should take care of any 5 digit number as well as letter
    # combinations up to 6 characters
    if not foundit:
        print("Method 1 (4 digit) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_2(6)
    # Still looking? Try 7 digit numbers
    if not foundit:
        print("Method 2 (6 digits) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(7)
    # Still looking? Try 8 digit numbers
    if not foundit:
        print("Method 2 (7 digits) did not work!")
        if show_instructions:
            input("Press enter to continue.")
        foundit = search_method_1(8)
    seconds = time.time()-overallstart
    print()
    if (seconds < 0.00001):
        print ("The total search for all methods took "+make_human_readable(seconds)+" seconds and "+make_human_readable(totalguesses)+" guesses.")
        print ("(on some machines, Python doesn't know how long things actually took)")
    else:
        print ("The total search for all methods took "+make_human_readable(seconds)+" seconds and "+make_human_readable(totalguesses)+" guesses.("+make_human_readable(totalguesses/seconds)+" guesses per second)")
    print()
    if foundit:
        if (6 == which_password):
            print("Wow!")
        elif (0 == which_password):  # The Science Buddies website can't confirm passwords you added yourself
            print ("Your algorithm correctly guessed the password you entered. Try some others or see if you can make it guess faster.")
        else:
            print("Wow!")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# The list of actual passwords are,
# 1. 123
# 2. fred
# 3. tigger
# 4. Dragon+Hunter
# 5. secretpassword
# 6. Helpme>viper<qazwsx
