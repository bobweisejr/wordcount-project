from django.http import HttpResponse
from django.shortcuts import render
import operator
import re
import datetime as d
from wordcount.hex_key import *


def home(request):
    return render(request, 'home.html')


def count(request):
    fulltext = request.GET['fulltext']
    wordlist = fulltext.split()

    worddictionary = {}

    for word in wordlist:
        if word in worddictionary:
            # add to dictionary or increase number
            worddictionary[word] += 1
        else:
            worddictionary[word] = 1

    sorted_words = sorted(worddictionary.items(), key=operator.itemgetter(1), reverse=True)

    return render(request, 'count.html', {'fulltext': fulltext, 'count': len(wordlist),
                                          'sorted_words': sorted_words})


def about(request):
    return render(request, 'about.html')


def capk(request):
    return render(request, 'capk.html')


def capk_calculated(request):
    expire_text = request.GET['expires_text']

    if len(expire_text) != 6:
        numeric = re.compile(r'[^\d]+')
        expire_text = numeric.sub('', expire_text)
        expire_year = d.datetime.now()
        expire_new = expire_year.year + 1
        expire_text = str(expire_new)[2:]
        expire_text = "3112" + expire_text
        return expire_text

    """Rid info here"""
    rid_text = request.GET['rid_text']
    index_text = request.GET['index_text']
    data_text = ("[a" + rid_text[1:] + index_text + ".data]")
    modulus_text = ("[a" + rid_text[1:] + index_text + ".modulus]")

    key_text = request.GET['key_text'].strip()
    full_modulus_text = request.GET['full_modulus_text'].strip()
    key_length = len(full_modulus_text.strip()) * 4
    modulus_parse = int(key_length / 32)
    modulus_length = len(full_modulus_text)
    exponent_text = request.GET['exponent_text']

    mod1 = full_modulus_text[:modulus_parse]
    mod2 = full_modulus_text[modulus_parse:modulus_parse * 2]
    mod3 = full_modulus_text[modulus_parse * 2: modulus_parse * 3]
    mod4 = full_modulus_text[modulus_parse * 3: modulus_parse * 4]
    mod5 = full_modulus_text[modulus_parse * 4: modulus_parse * 5]
    mod6 = full_modulus_text[modulus_parse * 5: modulus_parse * 6]
    mod7 = full_modulus_text[modulus_parse * 6: modulus_parse * 7]
    mod8 = full_modulus_text[modulus_parse * 7: modulus_parse * 8]

    return render(request, 'capk_calculated.html',
                  {'key_text': key_text, 'key_length': key_length, 'modulus_text': modulus_text,
                   'expire_text': expire_text, 'data_text': data_text, 'full_modulus_text': full_modulus_text,
                   'modulus_length': modulus_length, 'exponent_text': exponent_text, 'modulus_parse': modulus_parse,
                   'mod1': mod1, 'mod2': mod2, 'mod3': mod3, 'mod4': mod4, 'mod5': mod5, 'mod6': mod6,
                   'mod7': mod7, 'mod8': mod8, 'rid_text': rid_text})


def hex(request):
    hex_text = request.GET['hex']
    hex_value = hex_text.strip()
    # hex = hex.strip()

    scale = 16

    num_of_bits = 8

    binary = bin(int('1' + hex_value, scale))[3:].zfill(num_of_bits)

    binary_list = [binary[i:i + num_of_bits] for i in range(0, len(binary), num_of_bits)]

    byte = 1

    display_list = []
    for bytes in binary_list:
        display_list.append("Byte #" + str(byte) + " = " + bytes[0:4] + " " + bytes[4:])
        display_list.append("Byte " + str(byte) + " Bit #1 = " + bytes[7:])
        display_list.append("Byte " + str(byte) + " Bit #2 = " + bytes[6:7])
        display_list.append("Byte " + str(byte) + " Bit #3 = " + bytes[5:6])
        display_list.append("Byte " + str(byte) + " Bit #4 = " + bytes[4:5])
        display_list.append("Byte " + str(byte) + " Bit #5 = " + bytes[3:4])
        display_list.append("Byte " + str(byte) + " Bit #6 = " + bytes[2:3])
        display_list.append("Byte " + str(byte) + " Bit #7 = " + bytes[1:2])
        display_list.append("Byte " + str(byte) + " Bit #8 = " + bytes[0:1] + "\n")
        byte += 1

    return render(request, 'hex_calc.html', {'hex': hex, 'hex_value': hex_value, 'hexkeys': hexkeys,
                                             'byte': byte, 'binary_list': binary_list, 'display_list': display_list})
