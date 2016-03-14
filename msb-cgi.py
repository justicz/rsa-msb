#!/usr/bin/python
import os, urlparse, json

MESSAGE = int("You are a WinRAR!".encode("hex"), 16)
query_dict = urlparse.parse_qs(os.environ["QUERY_STRING"])

with open("key.json") as fin:
	key = json.load(fin)
	n, e, d = key["n"], key["e"], key["d"]

orig_ciphertext = pow(MESSAGE, e, n)

if "c" in query_dict:
	print "Content-type: application/json\n"
else:
	print "Content-type: text/html\n"
	print """
		<style>div{width: 500px; word-wrap: break-word;}</style>
		<h1>RSA MSB Challenge</h1>
		<div>
		<p>I've encrypted a message using RSA (with no padding). Its ciphertext, represented as a base 10 integer, is</p>
		<p>%(ciphertext)s</p>
		<p>The public modulus N is:</p>
		<p>%(modulus)s</p>
		<p>The public exponent is:</p>
		<p>%(exponent)s</p>
		<p>If you visit <a href="http://maxj.scripts.mit.edu/rsa/index.py?c=[BASE 10 INTEGER]">http://maxj.scripts.mit.edu/rsa/index.py?c=[BASE 10 INTEGER]</a>, it'll tell you whether or not the decryption of c is greater than (N - 1)/2 (returning 1 if it is, and 0 if it isn't). Can you figure out the message?</p></div>
	""" % {"ciphertext":orig_ciphertext, "modulus":n, "exponent":e}
	exit(0)

out_dict = {}
plz_decrypt = int(query_dict["c"][0])
decryption = pow(plz_decrypt, d, n)

out_dict["msb"] = int(decryption > (n - 1)/2)

print json.dumps(out_dict)
