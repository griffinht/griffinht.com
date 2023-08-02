http session management

one vs two vs many cookies
cookies? httponly? localstorage?






audit logs
https://github.com/authelia/authelia/issues/2864

WEB IDENTITY MANAGER - separate api and frontend (frontend could be jamstack or http post server but STILL SEPARATE)!
# ONBOARDING
invite link, have admin do it, support xmpp in band auth

allow password storage to be offboarded to sasl or ldap???



note many hashes lack entropy! name, birthday, phone number, short emails
hashing name+birthday - hashing multiple data together for more entropy? also throw in mostly immutable sex, eye color, height, hair color - user has to remember what these were at the time of registration (think blue/green eyes, hair that could be multiple colors, user does't remember what color their hair was during registration)

name and birthday (note name is mutable, allow for historic names) (also give option to store unhashed, then "can you provide proof you are John Doe")
pull (name stored in db, birthday hashed) 
- we send mail to name @ address with otp
doesn't really work - who cares
push (name/birthday hashed in db)
- you send proof of identity (photo id, birth cert)

email
pull (email stored in db)
- we send an email with otp
push (email hashed in db)
- you send an email with otp

phone
pull (phone stored in db)
- we send an sms message with an otp
- we call you with an otp
push (phone hashed in db)
- you call us with otp
- you text us with otp

matrix/xmpp
pull (address stored in db)
- we send a message with otp to given address
push (address hashed in db)
- you send a message with otp from given address

domain
make sure we only check root domain server - no caching of untrusted intermediates! also tell the user which server we are querying
push (domain hashed in db - or full url? make sure domain isn't google.com!)
- you publish an otp via http on domain
- you add TXT dns record of otp

password - do not allow users to pick their own password, or do allow them because thats what everyone does
push (password hashed in db)
- you enter password

also social logins of course!
odic relying party? oauth 2.0?
log in with google apple facebook blah blah
BYO identity provider??

webauthn/hardware key?

passkeys

pubkey - ssh key






inputs - allow for internal service to send smtp, rest api, whatever
then convert those to regular alerts to the user
authelia only support smtp password reset, use this to convert to sms text

make sure user allows backup alerts - if sms can't be sent, then try email, whatever

ALERTING
email
text
phone call
matrix/xmpp
app push

enumerate alerts and allow designation per device
