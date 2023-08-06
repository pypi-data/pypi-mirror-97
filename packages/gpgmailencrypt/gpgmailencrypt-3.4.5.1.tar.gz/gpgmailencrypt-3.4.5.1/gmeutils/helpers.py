#License GPL v3
#Author Horst Knorr <gpgmailencrypt@gmx.de>
import base64
import binascii
from email import header
import email
import email.utils
import hashlib
import html
import html.parser
from   io				import BytesIO
import os
import mimetypes
import random
import re
import quopri
import subprocess
import sys
import urllib
import uu

from 	.child 			import _gmechild
from	.version		import *

##############################################
#Definition of general functions and variables
##############################################

###############
#default_values
###############
def default_values():
	values={}
	if os.name=="nt":
		values={
		"GPGCMD":'C:\\Program Files (x86)\\GNU\GnuPG\\gpg2.exe',
		"SMIMECMD":"C:\\OpenSSL-Win64\\bin\\openssl.exe",
		"GPGKEYHOME":"%APPDATA%\\gnupg",
		"SMIMEKEYHOME":"%APPDATA%\\smime",
		"CONFIGFILE":'%ProgramFiles%\\gpgmailencrypt\\gpgmailencrypt.conf',
		"MAILTEMPLATEDIR":"%ProgramFiles%\\gpgmailencrypt\\mailtemplates",
		"SMTPD_SSL_KEYFILE":"%APPDATA%\\ssl\\gpgsmtpd.key",
		"SMTPD_SSL_CERTFILE":"%APPDATA%\\ssl\\gpgsmtpd.cert",
		}
	else:
		values={
		"GPGCMD":'/usr/bin/gpg2',
		"SMIMECMD":"/usr/bin/openssl",
		"GPGKEYHOME":"~/.gnupg",
		"SMIMEKEYHOME":"~/.smime",
		"CONFIGFILE":'/etc/gpgmailencrypt.conf',
		"MAILTEMPLATEDIR":"/usr/share/gpgmailencrypt/mailtemplates",
		"SMTPD_SSL_KEYFILE":"/etc/gpgsmtpd.key",
		"SMTPD_SSL_CERTFILE":"/etc/gpgsmtpd.cert",
		}
	return values

############
#splitstring
############

def splitstring(txt,length=80):

	def chunkstring(string, length):
		return (string[0+i:length+i] for i in range(0, len(string), length))

	return list(chunkstring(txt,length))

##################
#replace_variables
##################

def replace_variables(  text,
						dictionary,
						startdelimiter="%",
						enddelimiter="%"):
	"replaces variables with the values of the dictionary. A variable is "
	"embraced with % and consists of capital letters, e.g. %MYVARIABLE%"
	result=""
	begin=0
	dictionary["COPYRIGHT"]="© %s Horst Knorr&lt;gpgmailencrypt@gmx.de>"%(
							COPYRIGHTYEAR)
	dictionary["VERSION"]=VERSION
	dictionary["VERSIONDATE"]=DATE

	while True:
		found=re.search("%s[A-Z]+%s"%(startdelimiter,enddelimiter),text[begin:])

		if found== None:
			result+=text[begin:]
			return result

		result+=text[begin:begin+found.start()]
		key=text[begin+found.start():
				begin+
				found.end()].replace(startdelimiter,"").replace(enddelimiter,"")

		try:
			result+=dictionary[key]
		except:
			result+=startdelimiter+key+enddelimiter

		begin+=found.end()

_htmlname={
"Acirc":"Â","acirc":"â","acute":"´","AElig":"Æ","aelig":"æ","Agrave":"À",
"agrave":"à","alefsym":"ℵ","Alpha":"Α","alpha":"α","amp":"&","and":"∧",
"ang":"∠","apos":"'","Aring":"Å","aring":"å","asymp":"≈","Atilde":"Ã",
"atilde":"ã","Auml":"Ä","auml":"ä","bdquo":"„","Beta":"Β","beta":"β",
"brvbar":"¦","bull":"•","cap":"∩","Ccedil":"Ç","ccedil":"ç","cedil":"¸",
"cent":"¢","Chi":"Χ","chi":"χ","circ":"ˆ","clubs":"♣","cong":"≅","copy":"©",
"crarr":"↵","cup":"∪","curren":"¤","Dagger":"‡","dagger":"†",
"dArr":"⇓","darr":"↓","deg":"°","Delta":"Δ","delta":"δ","diams":"♦",
"divide":"÷","Eacute":"É","eacute":"é","Ecirc":"Ê","ecirc":"ê","Egrave":"È",
"egrave":"è","empty":"∅","emsp":" ","ensp":" ","Epsilon":"Ε","epsilon":"ε",
"equiv":"≡","Eta":"Η","eta":"η","ETH":"Ð","eth":"ð","Euml":"Ë",
"euml":"ë","euro":"€","exist":"∃","fnof":"ƒ","forall":"∀",
"frac12":"½","frac14":"¼","frac34":"¾","frasl":"⁄","Gamma":"Γ","gamma":"γ",
"ge":"≥","gt":">","hArr":"⇔","harr":"↔","hearts":"♥","hellip":"…","Iacute":"Í",
"iacute":"í","Icirc":"Î","icirc":"î","iexcl":"¡","Igrave":"Ì","igrave":"ì",
"image":"ℑ","infin":"∞","int":"∫","Iota":"Ι","iota":"ι",
"iquest":"¿","isin":"∈","Iuml":"Ï","iuml":"ï","Kappa":"Κ","kappa":"κ",
"Lambda":"Λ","lambda":"λ","lang":"⟨","laquo":"«","lArr":"⇐",
"larr":"←","lceil":"⌈","ldquo":"“","le":"≤","lfloor":"⌊","lowast":"∗",
"loz":"◊","lrm":"‎","lsaquo":"‹","lsquo":"‘","lt":"<",
"macr":"¯","mdash":"—","micro":"µ","middot":"·","minus":"−","Mu":"Μ","mu":"μ",
"nabla":"∇","nbsp":" ","ndash":"–","ne":"≠","ni":"∋",
"not":"¬","notin":"∉","nsub":"⊄","Ntilde":"Ñ","ntilde":"ñ","Nu":"Ν","nu":"ν",
"Oacute":"Ó","oacute":"ó","Ocirc":"Ô","ocirc":"ô",
"OElig":"Œ","oelig":"œ","Ograve":"Ò","ograve":"ò","oline":"‾","Omega":"Ω",
"omega":"ω","Omicron":"Ο","omicron":"ο","oplus":"⊕",
"or":"∨","ordf":"ª","ordm":"º","Oslash":"Ø","oslash":"ø","Otilde":"Õ",
"otilde":"õ","otimes":"⊗","Ouml":"Ö","ouml":"ö",
"para":"¶","part":"∂","permil":"‰","perp":"⊥","Phi":"Φ","phi":"φ",
"Pi":"Π","pi":"π","piv":"ϖ","plusmn":"±","pound":"£","Prime":"″","prime":"′",
"prod":"∏","prop":"∝","Psi":"Ψ","psi":"ψ","quot":'"',
"radic":"√","rang":"⟩","raquo":"»","rArr":"⇒","rarr":"→","rceil":"⌉",
"rdquo":"”","real":"ℜ","reg":"®","rfloor":"⌋","Rho":"Ρ","rho":"ρ","rlm":"‏",
"rsaquo":"›","rsquo":"’","sbquo":"‚","Scaron":"Š","scaron":"š",
"sdot":"⋅","sect":"§","shy":"­","Sigma":"Σ","sigma":"σ","sigmaf":"ς",
"sim":"∼","spades":"♠","sub":"⊂","sube":"⊆","sum":"∑",
"sup":"⊃","sup1":"¹","sup2":"²","sup3":"³","supe":"⊇","szlig":"ß","Tau":"Τ",
"tau":"τ","there4":"∴","Theta":"Θ","theta":"θ","thetasym":"ϑ","thinsp":" ",
"THORN":"Þ","thorn":"þ","tilde":"˜","times":"×","trade":"™","Uacute":"Ú",
"uacute":"ú","uArr":"⇑","uarr":"↑","Ucirc":"Û","ucirc":"û","Ugrave":"Ù",
"ugrave":"ù","uml":"¨","upsih":"ϒ","Upsilon":"Υ","upsilon":"υ","Uuml":"Ü",
"uuml":"ü","weierp":"℘","Xi":"Ξ","xi":"ξ","Yacute":"Ý","yacute":"ý","yen":"¥",
"Yuml":"Ÿ","yuml":"ÿ","Zeta":"Ζ","zeta":"ζ","zwj":"‍","zwnj":"‌"
}

##################
#class _htmldecode
##################

class _htmldecode(html.parser.HTMLParser,_gmechild):

	def __init__(self,parent):
		_gmechild.__init__(self,parent=parent,filename=__file__)
		html.parser.HTMLParser.__init__(self)
		self.data=""
		self.in_throwaway=0
		self.in_keep=0
		self.first_td_in_row=False
		self.dbg=False
		self.abbrtitle=None

	def get_attrvalue(self,tag,attrs):

		if attrs==None:
			return None

		for i in attrs:

			if len(i)<2:
				return None

			if i[0]==tag:
				return i[1]

		return None

	def handle_starttag(self, tag, attrs):

		if self.dbg:
			self.debug( "<%s>"%tag)

		self.handle_tag(tag,attrs)

	def handle_entityref(self, name):
		c = ""
		e=None

		try:
			e=_htmlname[name]
		except:
			pass

		if e:
			c=e
		else:
			c="&%s"%name

		self.data+=c

	def handle_endtag(self, tag):

		if self.dbg:
			self.debug("</%s>"%tag)

		self.handle_tag(tag,starttag=False)

	def handle_startendtag(self,tag,attrs):

		if self.dbg:
			self.debug("< %s/>"%tag)

		if tag=="br":
			self.handle_tag(tag,attrs,starttag=False)

	def handle_data(self, data):

		if self.in_throwaway==0:

			if self.dbg:
				self.debug("   data: '%s'"%data)

			if self.in_keep>0:
				self.data+=data
			elif len(data.strip())>0:
				self.data+=data.replace("\r\n"," ").replace("\n"," ")

	def handle_charref(self, name):

		if self.dbg:
			self.debug("handle_charref '%s'"%name)

		if name.startswith('x'):
			c = chr(int(name[1:], 16))
		else:
			c = chr(int(name))

		self.data+=c

	def handle_tag( self,
					tag,
					attrs=None,
					starttag=True):

		if tag in ("style","script","title"):

			if starttag:
				self.in_throwaway+=1
			else:
				if self.in_throwaway>0:
					self.in_throwaway-=1

		if tag=="pre":

			if starttag:
				self.in_keep+=1
			else:
				if self.in_keep>0:
					self.in_keep-=1

		if tag=="br":
			self.data+="\r\n"

		if len(self.data)>0:
			lastchar=self.data[len(self.data)-1]
		else:
			lastchar=""

		if tag=="hr":

			if lastchar!="\n":
				self.data+="\r\n"

			self.data+="=========================\r\n"

		if starttag:
			#Starttag

			if tag=="table":

				if lastchar!="\n":
					self.data+="\r\n"

			if tag=="tr":
				self.first_td_in_row=True

				if self.dbg:
					self.debug("tr first_td_in_row=True")

			if tag in ("td","th") :

				if self.dbg:
					self.debug("<td/th> first %s"%self.first_td_in_row)

				if  not self.first_td_in_row:

					if self.dbg:
						self.debug("	 td/th \\t")
					self.data+="\t"

				else:
					self.first_td_in_row=False

			if tag in ("li"):
				self.data+="\r\n * "

			if tag=="q":
				self.data+="\""

			if tag=="abbr":
				self.attrtitle=self.get_attrvalue("title",attrs)
		else:
			#Endtag

			if (tag in (	"h1","h2","h3","h4","h5","h6",
							"title",
							"p",
							"ol",
							"ul",
							"caption")
			and lastchar not in ("\n"," ","\t")):
				self.data+="\r\n"

			if tag=="tr":

				if lastchar=="\t":
					self.data=self.data[0:len(self.data)-1]
					self.data+="\r\n"
				else:

					if lastchar not in ("\n","\t"):
						self.data+="\r\n"

			if tag=="abbr" and self.attrtitle!=None:
				self.data+=" [%s] "%self.attrtitle
				self.attrtitle=None

	def mydata(self):
		return self.data

#############
#is_networkfs
#############

def is_networkfs(filename):

	if os.name=="nt":
		return _windows_is_networkfs(filename)
	else:
		return _linux_is_networkfs(filename)

######################
#_windows_is_networkfs
######################

def _windows_is_networkfs(filename):
	netdrives=[]
	p=subprocess.Popen(["net","use"],	stdin=subprocess.PIPE,
										stdout=subprocess.PIPE,
										stderr=subprocess.PIPE)
	
	for l in p.stdout.readlines():
		_l=l.decode("utf8","replace")
		if _l.startswith("OK"):
			sp=_l.split()
			netdrives.append(sp[1].lower())

	drv=os.path.splitdrive(filename)[0].lower()
	
	if drv in netdrives:
		return True
	else:
		return False

####################
#_linux_is_networkfs
####################

def _linux_is_networkfs(filename):
	networkfs=["cifs","davfs","davfs2","ftp","ftps","curlftpfs","cupsftp",
				"nfs","nfs5","nfs4","nfs3","nfs2","nfs1","smbfs",
				"sshfs"]
	fusenetworkfs=["fuse"]

	for nfs in networkfs:
		fusenetworkfs.append("fuse."+nfs)
	
	networkfs=networkfs+fusenetworkfs
	#df -P -T ./cloud/Telekom/ | tail -n +2| awk '{print $2}'",shell=True
	cmd1=["/bin/df","-P","-T",filename.strip()]
	cmd2=["/usr/bin/tail","-n","+2"]
	cmd3=["/usr/bin/awk","{print $2}"]
	p1 = subprocess.Popen(   cmd1,
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE )
	output1,error1=p1.communicate(input=None)
	error=p1.poll()
	
	if error!=0:
		return False

	p2 = subprocess.Popen(   cmd2,
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE )
	output2,error2=p2.communicate(input=output1)
	error=p2.poll()
	
	if error!=0:
		return False

	p3 = subprocess.Popen(   cmd3,
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE )

	output3,error3=p3.communicate(input=output2)
	error=p3.poll()

	if error==0:
		fs=output3.decode("utf8").strip()

		if fs in networkfs:
			return True
		else:
			return False

	return False

###################################
#Definition of encryption functions
###################################

#############
#decode_html
#############

def decode_html(parent,msg):
	h=_htmldecode(parent)
	h.feed(msg)
	return h.mydata()

###############
#guess_mimetype
###############

def guess_mimetype(filename):
	mimetype,enc=mimetypes.guess_type(filename)
	return mimetype

####################
#guess_fileextension
####################

def guess_fileextension(ct):
	"returns a filetype based on its contenttype/mimetype 'ct'"

	try:
		maintype,subtype=ct.lower().strip().split("/")
	except:
		maintype=ct
		subtype="plain"

	if maintype=="image":

		if subtype in ("jpeg","pjpeg"):
			return "jpg"
		elif subtype=="svg+xml":
			return "svg"
		elif subtype in ("tiff","x-tiff"):
			return "tif"
		elif subtype=="x-icon":
			return "ico"
		elif subtype=="vnd.djvu":
			return "dvju"

		return subtype

	if maintype=="audio":

		if subtype=="basic":
			return "au"
		elif subtype in ("vnd.rn-realaudio","x-pn-realaudio"):
			return "ra"
		elif subtype in ("vnd.wave","x-wav"):
			return "wav"
		elif subtype in ("midi","x-midi"):
			return "mid"
		elif subtype=="x-mpeg":
			return "mp2"
		elif subtype in ("mp3","mpeg","ogg","midi"):
			return subtype

	if maintype=="video":

		if subtype=="x-ms-wmv":
			return "wmv"
		elif subtype=="quicktime":
			return "mov"
		elif subtype in ("x-matroska"):
			return "mkv"
		elif subtype in ("x-msvideo"):
			return "avi"
		elif subtype in ("avi","mpeg","mp4","webm"):
			return subtype

	if maintype=="application":

		if subtype in ("javascript","x-javascript","ecmascript"):
			return "js"
		elif subtype=="postscript":
			return "ps"
		elif subtype in ("pkcs10","pkcs-10","x-pkcs10"):
			return "p10"
		elif subtype in ("pkcs12","pkcs-12","x-pkcs12"):
			return "p12"
		elif subtype in ("x-pkcs7-mime","pkcs7-mime"):
			return "p7c"
		elif subtype in ("x-pkcs7-signature","pkcs7-signature"):
			return "p7a"
		elif subtype=="x-shockwave-flash":
			return "swf"
		elif subtype=="mswrite":
			return "wri"
		elif subtype in("msexcel","excel","vnd.ms-excel","x-excel","x-msexcel"):
			return "xls"
		elif subtype in ("msword","word","vnd.ms-word","x-word","x-msword"):
			return "doc"
		elif subtype in ("mspowerpoint","powerpoint","vnd.ms-powerpoint",
						 "x-powerpoint","x-mspowerpoint"):
			return "ppt"
		elif subtype in ("gzip","x-gzip","x-compressed"):
			return "gz"
		elif subtype=="x-bzip2":
			return "bz2"
		elif subtype=="x-gtar":
			return "gtar"
		elif subtype=="x-tar":
			return "tar"
		elif subtype=="x-dvi":
			return "dvi"
		elif subtype=="x-midi":
			return "mid"
		elif subtype in("x-lha","lha"):
			return "lha"
		elif subtype in("x-rtf","rtf","richtext"):
			return "rtf"
		elif subtype=="x-httpd-php":
			return "php"
		elif subtype in ("atom+xml","xhtml+xml","xml-dtd","xop+xml","soap+xml",
						"rss+xml","rdf+xml","xml"):
			return "xml"
		elif subtype in ("arj","lzx","json","ogg","zip","gzip","pdf","rtc"):
			return subtype

	if maintype=="text":

		if subtype in ("plain","cmd","markdown"):
			return "txt"
		elif subtype=="javascript":
			return "js"
		elif subtype in ("comma-separated-values","csv"):
			return "csv"
		elif subtype in ("vcard",
						"x-vcard",
						"directory;profile=vCard",
						"directory"):
			return "vcf"
		elif subtype=="tab-separated-values":
			return "tsv"
		elif subtype=="uri-list":
			return "uri"
		elif subtype=="x-c":
			return "c"
		elif subtype=="x-h":
			return "h"
		elif subtype=="x-vcalendar":
			return "vcs"
		elif "x-script" in subtype:
			r=subtype.split(".")

			if len(r)==2:
				return r[1]
			else:
				return "hlb"

		elif subtype in ("asp","css","html","rtf","xml"):
			return subtype
		else:
			return "txt"

	e=mimetypes.guess_extension(ct)

	if e:
		e=e.replace(".","")
		return e
	else:
		return "bin"

###############
#decode_payload
###############
def decode_payload(part,parent):
	charset = part.get_content_charset()
	cte=part["Content-Transfer-Encoding"]
	is_text=part.get_content_maintype()=="text"
	payload=None

	if charset==None:
		part.set_charset("utf8")
		charset = 'utf-8'

	if part['Content-Transfer-Encoding'] == '8bit':
		payload = part.get_payload(decode=False)
	else:
		payload = part.get_payload(decode=(not is_text))

	if is_text:
		payload=decodetxt(payload,cte,charset)

	return payload

##########
#decodetxt
##########

def decodetxt( text,
				encoding,
				charset):
#necessary due to a bug in python 3 email module
	if not charset:
		charset="UTF-8"

	if not encoding:
		encoding="8bit"

	if charset!=None:

		try:
			"test".encode(charset)
		except:
			charset="UTF-8"

	bytetext=text.encode(charset,unicodeerror)
	result=bytetext
	cte=encoding.upper()

	if cte=="BASE64":
		pad_err = len(bytetext) % 4

		if pad_err:
			padded_encoded = bytetext + b'==='[:4-pad_err]
		else:
			padded_encoded = bytetext

		try:
			result= base64.b64decode(padded_encoded, validate=True)
		except binascii.Error:

			for i in 0, 1, 2, 3:

				try:
					result= base64.b64decode(bytetext+b'='*i, validate=False)
					break
				except binascii.Error:
					pass

			else:
				raise AssertionError("unexpected binascii.Error")

	elif cte=="QUOTED-PRINTABLE":
		result=quopri.decodestring(bytetext)
	elif cte in ('X-UUENCODE', 'UUENCODE', 'UUE', 'X-UUE'):
		in_file = BytesIO(bytetext)
		out_file =BytesIO()

		try:
			uu.decode(in_file, out_file, quiet=True)
			result=out_file.getvalue()
		except uu.Error:
			pass

	return result.decode(charset,unicodeerror)

##############
#is_attachment
##############

def is_attachment(part):

	if ((part.get_param('attachment',None,'Content-Disposition') is not None
	or (part.get_param('inline',None,'Content-Disposition' ) is not None
		and part.get_content_maintype() not in ("text",)) 
	or part.get_content_type()=="text/calendar") 
	or part.get_content_maintype() in ["image","application"]):
		return True
	else:
 		return False

################
#encode_filename
################

def encode_filename(name):
	n1=(email.utils.encode_rfc2231(name,"UTF-8"))
	n2="?UTF-8?B?%s"%base64.encodebytes(
						name.encode("UTF-8",unicodeerror)
						).decode("UTF-8",unicodeerror)[0:-1]
	return n1,n2

################
#decode_filename
################

def decode_filename(name):

	if not name:
		return None

	decfilename=header.decode_header(name)

	if decfilename and decfilename[0][1]!=None:

		try:
			name=decfilename[0][0].decode(decfilename[0][1])
		except:
			pass

	return urllib.parse.unquote(name)

####################
#get_certfingerprint
####################

def get_certfingerprint(cert,parent=None):
	#"openssl x509 -inform PEM -pubkey|openssl rsa -inform PEM -pubin -modulus 2>1|grep Modulus"
	cmd1=["openssl","x509","-inform","PEM",	"-pubkey"]
	cmd2=["openssl","rsa","-inform","PEM","-pubin","-modulus"]
	cmd3=["grep","Modulus"]

	p1 = subprocess.Popen(   cmd1,
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE )
	output1,error1=p1.communicate(input=cert.encode("UTF-8",unicodeerror))
	error=p1.poll()

	if error!=0:

		if parent:
			parent.log("get_certfingerprint process1 "
						"failed with error code '%i'"%error,"w")
			parent.log(error1.decode("UTF-8",unicodeerror),"w")

		return None

	p2 = subprocess.Popen(   cmd2,
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE )
	output2,error2=p2.communicate(input=output1)
	error=p2.poll()

	if error!=0:

		if parent:
			parent.log("get_certfingerprint process1 failed ","w")
			parent.log(error2.decode("UTF-8",unicodeerror),"w")

		return None


	p3 = subprocess.Popen(   cmd3,
							stdin=subprocess.PIPE,
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE )

	output3,error3=p3.communicate(input=output2)
	error=p3.poll()

	if error!=0:

		if parent:
			parent.log("get_certfingerprint process1 failed","w")
			parent.log(error3.decode("UTF-8",unicodeerror),"w")

		return None

	pubkey=bytearray.fromhex(output3[8:-1].decode("UTF-8",unicodeerror))
	return hashlib.sha512(pubkey).hexdigest()

###########
#maildomain
###########

def maildomain(mailaddress):

	if mailaddress == None:
		return ""
		
	addr= email.utils.parseaddr(mailaddress)[1].split('@')
	domain=""

	if len(addr)==2:
		domain = addr[1].lower()

	return domain

################
#create_password
################

def create_password(self,pwlength=10):
	#prior to pdf 1.7 only ASCII characters are allowed and
	#maximum 32 characters
	_min=5
	_max=32

	if pwlength<_min:
		pwlength=_min
	elif pwlength>_max:
		pwlength=_max

	nonletters="0123456789+-*/@"
	pwkeys="ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstvwxyz"+nonletters
	return ''.join(random.SystemRandom().choice(pwkeys)
				for _ in range(pwlength))

##############
#make_boundary
##############

def make_boundary(self,text=None):
	_width = len(repr(sys.maxsize-1))
	_fmt = '%%0%dd' % _width
	token = random.randrange(sys.maxsize)
	boundary = ('=' * 15) + (_fmt % token) + '=='

	if text is None:
		return boundary

	b = boundary
	counter = 0

	while True:
		cre = re.compile('^--' + re.escape(b) + '(--)?$', re.MULTILINE)

		if not cre.search(text):
			break

		b = boundary + '.' + str(counter)
		counter += 1
	return b

###############
#clean_filename
###############

def clean_filename(name):
	"removes whitespaces and some special characters"

	if name==None:
		return None

	return re.sub("[\s:\"*?!<>|#{}\[\]'`´\$§%&^°¬²³¹¼½+\(\)~]","_",name)

##########
#_LOCALEDB
##########
_LOCALEDB={
#"CN":{	"appointment":"约会",
#		"file":"文件",
#		"content":"内容",
#		"attachment":"文件附件",
#		"passwordfor":"口令",
#		"bouncemail":"电子邮件无法发送",
#		"_date":"0:%Y-%m-%d",
#		"_time":"%H:%M",
#		},
"DA":{	"appointment":"aftale",
		"file":"fil",
		"content":"indhold",
		"attachment":"bilag",
		"passwordfor":"Password til",
		"_date":"0:%d.%m.%Y",
		"_time":"%H:%M",
		},
"DE":{	"appointment":"Termin",
		"file":"Datei",
		"content":"Inhalt",
		"attachment":"Anhang",
		"attachments":"Anhänge",
		"passwordfor":"Passwort für",
		"bouncemail":"Email konnte nicht versandt werden",
		"from":"Von",
		"to":"An",
		"subject":"Betreff",
		"encryptedsubject":"Betreff verschlüsselt",
		"date":"Datum",
		"title":"Titel",
		"description":"Beschreibung",
		"when":"Wann",
		"organizer":"Organisator",
		"attendees":"Teilnehmer",
		"location":"Ort",
		"timezone":"Zeitzone",
		"caltype":"Typ",
		"calcanceled":"Absage",
		"calrequest":"Terminanfrage",
		"calcounterproposal":"Gegenvorschlag",
		"caldeclinecounterproposal":"Gegenvorschlag abgelehnt",
		"calreply":"Antwort",
		"calpublish":"Kalendereintrag",
		"recurrence":"Wiederholung",
		"frequency":"Frequenz",
		"until":"Bis",
		"recurrencedefaultinfo":"Beinhaltet weitere Wiederholungsinformationen",
		"secondly":"Sekündlich",
		"minutely":"Minütlich",
		"hourly":"Stündlich",
		"daily":"Täglich",
		"weekly":"Wöchentlich",
		"monthly":"Monatlich",
		"yearly":"Jährlich",
		"_date":"0:%d.%m.%Y",
		"_time":"%H:%M",
		},
"EN":{	"appointment":"appointment",
		"file":"file",
		"content":"content",
		"attachment":"attachment",
		"attachments":"attachments",
		"passwordfor":"Password for",
		"bouncemail":"E-mail could not be sent",
		"from":"From",
		"to":"To",
		"subject":"Subject",
		"encryptedsubject":"Encrypted subject",
		"date":"Date",
		"title":"Title",
		"description":"Description",
		"when":"When",
		"organizer":"Organizer",
		"attendees":"Attendees",
		"location":"Location",
		"timezone":"Timezone",
		"caltype":"Type",
		"calcanceled":"cancellation",
		"calrequest":"appointment request",
		"calcounterproposal":"Counter proposal",
		"caldeclinecounterproposal":"Counter proposal declined",
		"calreply":"Reply",
		"calpublish":"calendar entry",
		"recurrence":"Recurrence",
		"frequency":"Frequency",
		"until":"Until",
		"recurrencedefaultinfo":"Contains additional recurrence information",
		"secondly":"secondly",
		"minutely":"minutely",
		"hourly":"hourly",
		"daily":"daily",
		"weekly":"weekly",
		"monthly":"monthly",
		"yearly":"yearly",
		"_date":"0:%d/%m/%Y",
		"_time":"%H:%M",
		},
"ES":{	"appointment":"cita",
		"file":"fichero",
		"content":"contenido",
		"attachment":"apéndice",
		"passwordfor":"Contraseña por",
		"_date":"0:%d/%m/%Y",
		"_time":"%H:%M",
		},
"FI":{	"appointment":"tapaaminen",
		"file":"tiedosto",
		"content":"sisältö",
		"attachment":"liite",
		"passwordfor":"Salasana",
		"_date":"0:%d.%m %Y",
		"_time":"%H:%M",
		},
"FR":{	"appointment":"rendez-vous",
		"file":"fichier",
		"content":"contenu",
		"attachment":"attachement",
		"passwordfor":"Mot de passe pour",
		"bouncemail":"E-mail n'a pas pu être envoyé",
		"from":"De",
		"to":"À",
		"subject":"Objet",
		"date":"Date",
		"title":"Titre",
		"description":"Description",
		"when":"Quand",
		"organizer":"Organisateur",
		"attendees":"Participants",
		"location":"Lieu",
		"timezone":"Fuseau horaire",
		"caltype":"Type",
		"calcanceled":"annulation",
		"calrequest":"demande de rendez-vous",
		"calcounterproposal":"contre-proposition" ,
		"caldeclinecounterproposal":"contre-proposition refuser",
		"calreply":"réponse",
		"recurrence":"récurrence",
		"frequency":"fréquence",
		"until":"jusque",
		"recurrencedefaultinfo":"Contenir des informations récurrente supplémentaire",
		"secondly":"toutes les secondes",
		"minutely":"toutes les minutes",
		"hourly":"d'heure en heure",
		"daily":"quotidien",
		"weekly":"hebdomadaire",
		"monthly":"mensuel",
		"yearly":"annuel",
		"_date":"0:%d/%m/%Y",
		"_time":"%H:%M",
		},
"IT":{	"appointment":"appuntamento",
		"file":"file",
		"content":"capacità",
		"attachment":"allegato",
		"passwordfor":"Password per"},
		"_date":"0:%d/%m/%Y",
		"_time":"%H:%M:%S",
"NL":{	"appointment":"Termijn",
		"file":"Bestand",
		"content":"inhoud",
		"attachment":"e-mailbijlage",
		"passwordfor":"Wachtwoord voor de",
		"_date":"0:%d-%m-%Y",
		"_time":"%H:%M",
		},
"NO":{	"appointment":"avtale",
		"file":"fil",
		"content":"innhold",
		"attachment":"vedlegg",
		"passwordfor":"Passord for",
		"_date":"0:%d.%m.%Y",
		"_time":"%H:%M",
		},
"PL":{	"appointment":"termin",
		"file":"plik",
		"content":"zawartość",
		"attachment":"załącznik",
		"passwordfor":"Hasło dla",
		"_date":"0:%d.%m.%Y",
		"_time":"%H:%M",
		},
"PT":{	"appointment":"hora",
		"file":"ficheiro",
		"content":"conteudo",
		"attachment":"anexo",
		"passwordfor":"Palavra-passe por",
		"_date":"0:%d/%m/%Y",
		"_time":"%H:%M",
		},
"RU":{	"appointment":"срок",
		"file":"файл",
		"content":"содержание",
		"attachment":"прикрепление",
		"passwordfor":"код для",
		"from":"от",
		"to":"кому",
		"subject":"тема",
		"date":"дата",
		"title":"Название",
		"description":"Описание",
		"when":"Когда",
		"organizer":"Организатор",
		"attendees":"Участники",
		"location":"Место",
		"timezone":"часовои пояс",
		"_date":"0:%d.%m.%Y",
		"_time":"%H:%M",
		},
"SE":{	"appointment":"möte",
		"file":"fil",
		"content":"innehåll",
		"attachment":"bilaga",
		"passwordfor":"Lösenord för",
		"_date":"0:%Y-%m-%d",
		"_time":"%H:%M",
		},
"US":{	"_date":"0:%m/%d/%Y",
		"_time":"%I:%M %p",
		},
}

#########
#localedb
#########

def localedb(parent,value):

	if not parent:
		return value

	error=0

	try:
		value=_LOCALEDB[parent._LOCALE][value]
	except:
		error=1

		try:
			value=_LOCALEDB["EN"][value]
		except:
			error=2
		
		if error==1:
			parent.debug("wrong locale '%s'"%parent._LOCALE,
											filename=__name__,lineno=1)
		else:
			parent.debug("unknown value '%s'"%value,
											filename=__name__,lineno=1)

	return value

#############
#save_txtfile
#############

def save_txtfile(filename, content):

	fncount=0
	newfilename=os.path.expanduser(filename)
	f1,ext=os.path.splitext(newfilename)

	while os.path.exists(newfilename):
		fncount+=1
		newfilename=f1+str(fncount)+ext

	with open(os.path.expanduser(filename),"w") as f:
		f.write(content)

	
